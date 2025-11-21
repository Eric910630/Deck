"""
颜色配置器
为PPT内容配置符合Ant Design规范的颜色方案
"""

from typing import Dict, Any, List, Optional
from loguru import logger
from llm_service import LLMService, create_llm_service


class ColorConfigurator:
    """
    颜色配置器
    为润色后的内容和布局规划配置颜色方案
    """
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        初始化颜色配置器
        
        Args:
            llm_service: LLM服务实例
        """
        self.llm_service = llm_service or create_llm_service()
        logger.info("--- [ColorConfigurator]: 初始化颜色配置器")
    
    async def configure_colors(
        self,
        polished_slides: List[Dict[str, Any]],
        presentation_plans: List[Dict[str, Any]],
        layout_plans: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        为幻灯片配置颜色方案
        
        Args:
            polished_slides: 润色后的幻灯片列表
            presentation_plans: 展示策划结果列表
            layout_plans: 布局规划结果列表（可选）
            
        Returns:
            颜色配置结果列表，每个元素包含：
            - slide_index: 幻灯片索引
            - color_config: 颜色配置详情
                - overall_scheme: 整体配色方案描述
                - element_colors: 每个元素的颜色配置
                    - element_id: 元素ID
                    - text_color: 文本颜色（hex或rgba）
                    - background_color: 背景颜色（hex或rgba）
                    - border_color: 边框颜色（hex或rgba）
                    - accent_color: 强调色（hex或rgba，如有）
        """
        if not self.llm_service:
            logger.warning("   ⚠️ LLM服务不可用，使用默认颜色配置")
            return self._default_color_config(polished_slides)
        
        logger.info(f"--- [ColorConfigurator]: 开始颜色配置，共{len(polished_slides)}张幻灯片")
        
        # 读取设计规范中的颜色系统
        color_specs = self._load_color_specifications()
        
        color_configs = []
        
        for idx, (polished_slide, plan) in enumerate(zip(polished_slides, presentation_plans)):
            logger.info(f"--- [ColorConfigurator]: 配置幻灯片{idx + 1}的颜色...")
            
            try:
                color_config = await self._configure_single_slide(
                    polished_slide=polished_slide,
                    presentation_plan=plan,
                    layout_plan=layout_plans[idx] if layout_plans and idx < len(layout_plans) else None,
                    color_specs=color_specs
                )
                color_configs.append(color_config)
                logger.info(f"   ✅ 幻灯片{idx + 1}颜色配置完成")
            except Exception as e:
                logger.error(f"   ❌ 幻灯片{idx + 1}颜色配置失败: {e}", exc_info=True)
                # 使用默认配置
                default_config = self._default_single_slide_color(polished_slide, plan)
                color_configs.append(default_config)
        
        logger.info(f"--- [ColorConfigurator]: ✅ 颜色配置完成，共配置{len(color_configs)}张幻灯片")
        return color_configs
    
    async def _configure_single_slide(
        self,
        polished_slide: Dict[str, Any],
        presentation_plan: Dict[str, Any],
        layout_plan: Optional[Dict[str, Any]],
        color_specs: str
    ) -> Dict[str, Any]:
        """
        配置单张幻灯片的颜色
        
        Args:
            polished_slide: 润色后的幻灯片
            presentation_plan: 展示策划结果
            layout_plan: 布局规划结果（可选）
            color_specs: 颜色规范说明
            
        Returns:
            颜色配置结果
        """
        system_prompt = f"""你是一个专业的UI/UX设计师，精通Ant Design颜色系统。

你的任务是为PPT幻灯片配置符合Ant Design规范的颜色方案。

【Ant Design颜色系统】：
{color_specs}

【颜色配置要求】：
1. **遵循Ant Design颜色系统**：使用Ant Design定义的颜色值，不要使用自定义颜色
2. **建立视觉层次**：通过颜色建立清晰的视觉层次（标题、内容、数据等）
3. **保持一致性**：同一类型的元素使用相同的颜色方案
4. **避免红色**：根据用户要求，避免使用大红色（#F5222D），除非是错误提示
5. **高管汇报风格**：配色要专业、简洁、优雅，适合副总裁级别的汇报

【输出格式（JSON）】：
{{
  "slide_index": 幻灯片索引,
  "color_config": {{
    "overall_scheme": "整体配色方案描述（如：蓝色主色调，白色背景，深灰色文本）",
    "element_colors": [
      {{
        "element_id": "元素ID（如title_text_0）",
        "element_type": "元素类型（如title_text）",
        "text_color": "文本颜色（hex格式，如#1677FF或rgba格式）",
        "background_color": "背景颜色（hex格式，如#FFFFFF，如果是透明则用null）",
        "border_color": "边框颜色（hex格式，如#D9D9D9，如果没有边框则用null）",
        "accent_color": "强调色（hex格式，用于数据、图标等，可选）",
        "color_rationale": "颜色选择理由（简要说明为什么选择这些颜色）"
      }}
    ]
  }}
}}"""
        
        # 构建用户提示词
        slide_title = polished_slide.get('title', '')
        slide_content = polished_slide.get('content', '')
        slide_content_type = polished_slide.get('content_type', '')
        visual_elements = polished_slide.get('visual_elements_detail', [])
        layout_type = presentation_plan.get('layout_type', '')
        existing_color_scheme = presentation_plan.get('visual_guidance', {}).get('color_scheme', '')
        
        elements_info = []
        for elem in visual_elements:
            elem_id = elem.get('element_id', '')
            elem_type = elem.get('element_type', '')
            elem_title = elem.get('title', '')
            elem_data = elem.get('data', '')
            elements_info.append(f"- {elem_id} ({elem_type}): {elem_title}, 数据: {elem_data}")
        
        user_prompt = f"""请为以下幻灯片配置颜色方案。

幻灯片信息：
- 标题: {slide_title}
- 内容: {slide_content}
- 内容类型: {slide_content_type}
- 布局类型: {layout_type}
- 现有配色描述: {existing_color_scheme if existing_color_scheme else '无'}

视觉元素（共{len(visual_elements)}个）：
{chr(10).join(elements_info)}

请为每个视觉元素配置颜色，要求：
1. 标题元素：使用Ant Design主色（#1677FF）或深灰色（#262626），背景白色或透明
2. 内容文本：使用Ant Design主文本色（rgba(0,0,0,0.85)或#262626）
3. 卡片元素：背景白色（#FFFFFF），边框浅灰（#D9D9D9），文本深灰（#262626）
4. 数据元素：使用Ant Design主色（#1677FF）或成功色（#52C41A）突出显示
5. 图表元素：使用Ant Design分类色（colors10）
6. 避免使用大红色（#F5222D），除非是错误提示

请输出JSON格式的颜色配置。"""
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # 解析JSON响应
            import json
            import re
            
            if isinstance(response, str):
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    color_config = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用默认颜色配置")
                    return self._default_single_slide_color(polished_slide, presentation_plan)
            else:
                color_config = response
            
            # 确保包含slide_index
            color_config['slide_index'] = polished_slide.get('slide_index', 0)
            
            return color_config
            
        except Exception as e:
            logger.error(f"   颜色配置失败: {e}", exc_info=True)
            return self._default_single_slide_color(polished_slide, presentation_plan)
    
    def _default_single_slide_color(
        self,
        polished_slide: Dict[str, Any],
        presentation_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """默认单张幻灯片颜色配置"""
        visual_elements = polished_slide.get('visual_elements_detail', [])
        
        element_colors = []
        for elem in visual_elements:
            elem_id = elem.get('element_id', '')
            elem_type = elem.get('element_type', '')
            
            # 根据元素类型设置默认颜色
            if 'title' in elem_type:
                text_color = "#1677FF"  # Ant Design主色
                background_color = None  # 透明
                border_color = None
            elif 'content' in elem_type or 'subtitle' in elem_type:
                text_color = "rgba(0,0,0,0.85)"  # Ant Design主文本色
                background_color = None
                border_color = None
            elif 'card' in elem_type:
                text_color = "#262626"  # Ant Design主文本色
                background_color = "#FFFFFF"  # 白色
                border_color = "#D9D9D9"  # Ant Design边框色
            elif 'data' in elem_type or 'value' in elem_type:
                text_color = "#1677FF"  # Ant Design主色
                background_color = "#FFFFFF"
                border_color = "#D9D9D9"
            else:
                text_color = "rgba(0,0,0,0.85)"
                background_color = None
                border_color = None
            
            element_colors.append({
                "element_id": elem_id,
                "element_type": elem_type,
                "text_color": text_color,
                "background_color": background_color,
                "border_color": border_color,
                "accent_color": None,
                "color_rationale": "默认Ant Design配色"
            })
        
        return {
            "slide_index": polished_slide.get('slide_index', 0),
            "color_config": {
                "overall_scheme": "Ant Design标准配色：蓝色主色，白色背景，深灰色文本",
                "element_colors": element_colors
            }
        }
    
    def _default_color_config(
        self,
        polished_slides: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """默认颜色配置（回退方案）"""
        return [
            self._default_single_slide_color(slide, {})
            for slide in polished_slides
        ]
    
    def _load_color_specifications(self) -> str:
        """加载颜色规范说明"""
        try:
            from pathlib import Path
            design_file = Path(__file__).parent / "DESIGN_SYSTEM.md"
            if design_file.exists():
                content = design_file.read_text(encoding='utf-8')
                # 提取颜色系统部分（前200行左右）
                lines = content.split('\n')
                color_section = []
                in_color_section = False
                for i, line in enumerate(lines):
                    if '颜色系统' in line or 'Color' in line:
                        in_color_section = True
                    if in_color_section:
                        color_section.append(line)
                        if len(color_section) > 150:  # 提取前150行
                            break
                return '\n'.join(color_section)
        except Exception as e:
            logger.warning(f"   无法加载颜色规范文档: {e}")
        
        # 返回基础颜色规范
        return """【Ant Design颜色系统】：
- 主色调（Primary）：#1677FF（蓝色）
- 成功色（Success）：#52C41A（绿色）
- 警告色（Warning）：#FA8C16（橙色）
- 错误色（Error）：#F5222D（红色，避免使用）
- 文本主色：rgba(0,0,0,0.85) 或 #262626
- 文本次色：rgba(0,0,0,0.65) 或 #595959
- 背景色：#FFFFFF（白色），#F0F2F5（浅灰）
- 边框色：#D9D9D9（基础），#F0F0F0（次要）
- 分类色（用于图表）：['#1677FF', '#52C41A', '#FA8C16', '#F5222D', '#722ED1', '#13C2C2', '#EB2F96', '#FA541C', '#A0D911', '#2F54EB']"""

