"""
布局规划器
基于视觉元素查询Ant Design和AntV设计规范，输出详细的文字布局规划说明
"""

from typing import List, Dict, Any, Optional
from loguru import logger
from ..core.llm_service import LLMService, create_llm_service


class LayoutPlanner:
    """
    布局规划器
    基于润色结果和展示策划，查询设计规范，输出详细的文字布局规划说明
    """
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        初始化布局规划器
        
        Args:
            llm_service: LLM服务实例
        """
        self.llm_service = llm_service or create_llm_service()
        if not self.llm_service:
            logger.warning("   ⚠️ LLM服务不可用，布局规划功能将受限")
    
    async def plan_layout(
        self,
        polished_slides: List[Dict[str, Any]],
        presentation_plan: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        规划布局
        
        Args:
            polished_slides: 润色后的幻灯片列表
            presentation_plan: 展示策划结果
            
        Returns:
            布局规划结果列表，每个元素包含详细的文字布局说明
        """
        if not self.llm_service:
            logger.warning("   ⚠️ LLM服务不可用，使用默认布局规划")
            return self._default_layout_plan(polished_slides, presentation_plan)
        
        logger.info(f"--- [LayoutPlanner]: 开始布局规划，共{len(polished_slides)}张幻灯片")
        
        layout_plans = []
        
        for idx, (polished_slide, plan) in enumerate(zip(polished_slides, presentation_plan)):
            logger.info(f"--- [LayoutPlanner]: 规划幻灯片{idx + 1}...")
            
            try:
                layout_plan = await self._plan_single_slide(
                    polished_slide=polished_slide,
                    presentation_plan=plan
                )
                layout_plans.append(layout_plan)
                logger.info(f"   ✅ 幻灯片{idx + 1}布局规划完成")
            except Exception as e:
                logger.error(f"   ❌ 幻灯片{idx + 1}布局规划失败: {e}", exc_info=True)
                # 使用默认规划
                default_plan = self._default_single_slide_plan(polished_slide, plan)
                layout_plans.append(default_plan)
        
        logger.info(f"--- [LayoutPlanner]: ✅ 布局规划完成，共规划{len(layout_plans)}张幻灯片")
        return layout_plans
    
    async def _plan_single_slide(
        self,
        polished_slide: Dict[str, Any],
        presentation_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        规划单张幻灯片的布局
        
        Args:
            polished_slide: 润色后的幻灯片
            presentation_plan: 展示策划结果
            
        Returns:
            布局规划结果
        """
        # 提取视觉元素信息
        visual_elements = polished_slide.get('visual_elements_detail', [])
        layout_type = presentation_plan.get('layout_type', '')
        layout_description = presentation_plan.get('layout_description', '')
        visual_guidance = presentation_plan.get('visual_guidance', {})
        
        # 读取设计规范文档
        design_specs = self._load_design_specifications()
        
        # 构建系统提示词（按照新架构原则：LLM生成CSS，浏览器计算坐标）
        system_prompt = """你是一个专业的UI/UX设计师，精通Ant Design和AntV设计规范。

【核心原则】：用CSS描述布局意图，让浏览器负责计算坐标。不要输出坐标，输出HTML/CSS代码。

你的任务是：
1. 基于视觉元素的数量和类型，生成完整的HTML/CSS代码
2. 使用Flex/Grid布局，让浏览器自动计算位置
3. 应用Design Tokens（CSS变量）统一管理样式
4. 为每个元素添加 data-ppt-element 属性，便于后续提取坐标

【Ant Design设计规范】：
""" + design_specs + """

【布局组件使用指南】：
- **Flex布局**：用于垂直或水平排列
  - `display: flex; flex-direction: column;` - 垂直排列
  - `display: flex; flex-direction: row;` - 水平排列
  - `justify-content: center;` - 主轴居中
  - `align-items: center;` - 交叉轴居中
  - `gap: 24px;` - 元素间距（使用Design Tokens：16px/24px/32px）

- **Grid布局**：用于网格排列
  - `display: grid; grid-template-columns: repeat(3, 1fr);` - 三列等分
  - `gap: 24px;` - 网格间距

- **卡片布局**：
  - 使用 `.ant-card` 类名
  - 白色背景，顶部装饰条（border-top: 4px solid）
  - 内边距：24px（padding-lg）
  - 圆角：8px（border-radius-base）
  - 阴影：使用Design Token（--ant-box-shadow）

【颜色使用规范（重要）】：
- **大标题 (H1)**：使用 `color: var(--ant-text-color-heading);` (深黑色 #262626)，不要使用主色
- **卡片标题 (H3)**：使用 `color: var(--ant-text-color-heading);` (深黑色)，保持专业稳重
- **正文 (P)**：使用 `color: var(--ant-text-color-body);` (深灰 #595959)
- **Footer/副标题**：使用 `color: var(--ant-text-color-secondary);` (浅灰 #8C8C8C)
- **装饰元素**：使用 `var(--ant-color-primary)` (品牌色 #1677FF)，如左侧装饰条、卡片顶部横条
- **原则**：品牌色用于装饰和强调，文本色用于内容，确保可读性和专业性

【查询设计规范的方法】：
当遇到特定数量的视觉元素时，使用对应的布局模式：
- 1个元素：Flex居中，`justify-content: center; align-items: center;`
- 2个元素：Flex水平排列，`flex-direction: row; gap: 24px;`
- 3个元素：Flex水平排列，`flex-direction: row; justify-content: space-between; gap: 24px;`
- 4个元素：Grid 2x2布局，`grid-template-columns: repeat(2, 1fr); gap: 24px;`
- 多个卡片：Flex水平排列，每个卡片 `flex: 1;`，间距使用 `gap: 24px;`

【输出要求】：
直接生成完整的HTML/CSS代码，包括：
1. 完整的HTML结构（使用Flex/Grid布局）
2. 内联CSS样式（或<style>标签）
3. 每个元素必须有 data-ppt-element 属性
4. 使用CSS变量（Design Tokens）统一管理样式

【布局策略】：
根据场景选择合适的布局：
- 述职汇报：左对齐标题 + 三列数据卡片 + 底部总结
- 产品发布：居中标题 + 大图 + 底部CTA
- 数据展示：顶部标题 + 图表网格 + 底部说明

【CSS布局示例】：
```html
<div class="slide-container" style="display: flex; flex-direction: column; height: 100vh; padding: 40px; background: var(--ant-bg-color-layout);">
  <header style="margin-bottom: 60px; border-left: 12px solid var(--ant-color-primary); padding-left: 24px;">
    <h1 data-ppt-element="true" data-ppt-element-id="title_text_0" data-ppt-element-type="title" 
        style="font-size: 48px; font-weight: 600; color: var(--ant-color-primary); text-align: left; margin: 0;">
      核心价值主张
    </h1>
  </header>
  <main style="flex: 1; display: flex; gap: 24px; align-items: stretch;">
    <div class="ant-card" data-ppt-element="true" data-ppt-element-id="value_card_0" data-ppt-element-type="card"
         style="flex: 1; background: var(--ant-bg-color-container); padding: 40px 32px; border-radius: var(--ant-border-radius-base); box-shadow: var(--ant-box-shadow); border-top: 6px solid #1677FF;">
      <h3 style="margin: 0 0 24px 0; font-size: 32px; font-weight: 700; color: #1677FF; text-align: center;">成本降低</h3>
      <p style="margin: 0; font-size: 18px; color: var(--ant-text-color-secondary); line-height: 1.8; text-align: center;">降低运营成本40-60%</p>
    </div>
    <!-- 更多卡片... -->
  </main>
  <footer style="margin-top: 40px; text-align: center; padding: 8px; background: rgba(0,0,0,0.02); border-radius: 4px;">
    <p data-ppt-element="true" data-ppt-element-id="subtitle_text_0" data-ppt-element-type="text"
       style="margin: 0; font-size: 24px; color: var(--ant-text-color-secondary);">
      全链路AI赋能解决方案
    </p>
  </footer>
</div>
```

输出格式（JSON）：
{
  "slide_index": 幻灯片索引,
  "layout_plan": {
    "html_code": "完整的HTML代码（包含<style>标签和<body>内容）",
    "layout_strategy": "布局策略说明（如：述职汇报风格，左对齐标题+三列卡片+底部总结）",
    "design_tokens_used": ["--ant-color-primary", "--ant-bg-color-container", ...]
  }
}"""
        
        # 构建用户提示词
        visual_elements_info = []
        for elem in visual_elements:
            elem_id = elem.get('element_id', '')
            elem_type = elem.get('element_type', '')
            elem_title = elem.get('title', '')
            elem_content = elem.get('content', '')[:100]
            elem_data = elem.get('data', '')
            elem_desc = elem.get('description', '')
            elem_info = f"""
- 元素ID: {elem_id}
- 元素类型: {elem_type}
- 标题: {elem_title}
- 内容: {elem_content}...
- 数据: {elem_data}
- 说明: {elem_desc}"""
            visual_elements_info.append(elem_info)
        
        # 避免f-string嵌套，使用字符串拼接
        slide_title = polished_slide.get('title', '')
        slide_content = polished_slide.get('content', '')
        slide_content_type = polished_slide.get('content_type', '')
        font_size = visual_guidance.get('font_size', '')
        font_weight = visual_guidance.get('font_weight', '')
        alignment = visual_guidance.get('alignment', '')
        spacing = visual_guidance.get('spacing', '')
        color_scheme = visual_guidance.get('color_scheme', '')
        elements_count = len(visual_elements)
        elements_info_str = ''.join(visual_elements_info)
        
        user_prompt = f"""请为以下幻灯片进行布局规划。

幻灯片信息：
- 标题: {slide_title}
- 内容: {slide_content}
- 内容类型: {slide_content_type}
- 布局类型: {layout_type}
- 布局描述: {layout_description}

视觉指导：
- 字体大小: {font_size}
- 字体粗细: {font_weight}
- 对齐方式: {alignment}
- 间距: {spacing}
- 配色: {color_scheme}

视觉元素（共{elements_count}个）：
{elements_info_str}

请基于这些视觉元素的数量和类型，查询Ant Design和AntV的设计规范，输出详细的文字布局规划说明。

要求：
1. 明确说明整体布局结构（如：三个价值卡片并排排列）
2. 详细描述每个元素的位置、尺寸、对齐方式
3. 说明元素间距（使用px单位）
4. 说明视觉层次
5. 引用具体的设计规范（如：遵循Ant Design卡片设计规范，圆角6px，内边距16px）"""
        
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
                    layout_plan = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用默认规划")
                    return self._default_single_slide_plan(polished_slide, presentation_plan)
            else:
                layout_plan = response
            
            # 验证和规范化
            if 'layout_plan' not in layout_plan:
                logger.warning("   LLM响应缺少layout_plan字段，使用默认规划")
                return self._default_single_slide_plan(polished_slide, presentation_plan)
            
            # 确保包含slide_index
            layout_plan['slide_index'] = polished_slide.get('slide_index', 0)
            
            return layout_plan
            
        except Exception as e:
            logger.error(f"   布局规划失败: {e}", exc_info=True)
            return self._default_single_slide_plan(polished_slide, presentation_plan)
    
    def _default_single_slide_plan(
        self,
        polished_slide: Dict[str, Any],
        presentation_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """默认单张幻灯片布局规划"""
        visual_elements = polished_slide.get('visual_elements_detail', [])
        layout_type = presentation_plan.get('layout_type', 'standard')
        
        # 根据布局类型生成默认规划
        if layout_type == 'blank_center':
            overall_structure = "页面居中布局，标题和副标题垂直居中排列"
        elif layout_type == 'cards_grid':
            num_cards = len([e for e in visual_elements if 'card' in e.get('element_type', '')])
            overall_structure = f"{num_cards}个卡片横向等分排列，居中分布"
        else:
            overall_structure = "标准布局，元素按顺序排列"
        
        return {
            "slide_index": polished_slide.get('slide_index', 0),
            "layout_plan": {
                "overall_structure": overall_structure,
                "element_positions": [],
                "element_spacing": {
                    "between_elements": "默认间距24px",
                    "internal_padding": "默认内边距16px"
                },
                "visual_hierarchy": "默认视觉层次",
                "design_specifications": "遵循Ant Design基础设计规范"
            }
        }
    
    def _default_layout_plan(
        self,
        polished_slides: List[Dict[str, Any]],
        presentation_plan: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """默认布局规划"""
        return [
            self._default_single_slide_plan(slide, plan)
            for slide, plan in zip(polished_slides, presentation_plan)
        ]
    
    def _load_design_specifications(self) -> str:
        """加载设计规范文档"""
        try:
            from pathlib import Path
            design_file = Path(__file__).parent / "DESIGN_SYSTEM.md"
            if design_file.exists():
                return design_file.read_text(encoding='utf-8')
        except Exception as e:
            logger.warning(f"   无法加载设计规范文档: {e}")
        
        # 返回基础设计规范
        return """【Ant Design设计规范要点】：
- 间距系统：基于8px基础单位（8px, 16px, 24px, 32px, 48px等）
- 布局系统：24栅格系统，支持响应式布局
- 卡片设计：圆角6px，内边距16px或24px，阴影0 2px 8px rgba(0,0,0,0.15)
- 文字层级：标题38pt/30pt/24pt，正文14pt/16pt
- 对齐原则：左对齐为主，居中用于标题和强调
- 颜色系统：主色#1890ff，成功#52c41a，警告#faad14，错误#f5222d
- 文本色：主文本rgba(0,0,0,0.85)，次文本rgba(0,0,0,0.65)
- 背景色：#ffffff（白色），#f0f2f5（浅灰）
- 边框色：#d9d9d9（基础），#f0f0f0（次要）

【AntV设计规范要点】：
- 图表容器：保持适当的内边距（16px或24px），确保图表元素不贴边
- 数据可视化：遵循数据-图形映射原则
- 颜色使用：使用Ant Design颜色系统（category10分类色）
- 图表背景：白色（#ffffff）
- 网格线：浅灰（#f0f0f0）
- 坐标轴：灰色（#d9d9d9）"""

