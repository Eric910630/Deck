"""
展示策划模块
为副总裁级别的汇报设计简洁明了的展示方式
"""

from typing import Dict, Any, List
from loguru import logger
from ..core.llm_service import LLMService
from .presentation_schema import (
    PresentationProtocol,
    PresentationPlanSchema,
    VisualGuidanceSchema,
    LayoutType
)
import json
import re


class PresentationPlanner:
    """
    展示策划器
    为副总裁级别的汇报设计简洁明了的展示方式
    """
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        logger.info("--- [PresentationPlanner]: 初始化展示策划器")
    
    async def plan_presentation(
        self,
        polished_slides: List[Dict[str, Any]],
        section_theme: str
    ) -> List[Dict[str, Any]]:
        """
        为润色后的幻灯片设计展示方式
        
        Args:
            polished_slides: 润色后的幻灯片列表
            section_theme: 板块主题
            
        Returns:
            展示策划结果，每个元素包含：
            - slide_index: 幻灯片索引
            - layout_type: 布局类型（blank_center, table_with_summary, cards_with_data等）
            - layout_description: 布局描述
            - visual_guidance: 视觉指导（如何展示）
        """
        logger.info(f"--- [PresentationPlanner]: 策划板块展示方式: {section_theme}")
        
        # 获取Schema描述
        schema_desc = PresentationProtocol.get_schema_description()
        schema_json = json.dumps(schema_desc, ensure_ascii=False, indent=2)
        
        system_prompt = f"""你是中国职场的述职汇报专家，专门为副总裁级别的职场高管筹备述职内容，最擅长将高管整理的文稿大纲转换成适合呈现在ppt上的语言内容。

你具备强大的展示策划能力，能够为副总裁级别的汇报设计简洁明了（注意不是简单）的展示方式。

【重要】展示策划要求：
1. **简洁明了**：快速用分格、分点、分板块的方式展示核心观点
2. **视觉层次**：通过布局、字体大小、颜色等建立清晰的视觉层次
3. **信息密度**：每张幻灯片信息密度适中，不堆砌文字
4. **视觉元素**：合理使用空白、表格、图表、卡片等视觉元素
5. **高管汇报**：听取汇报的是更高层级的管理者，需要快速抓住核心观点

【输出Schema规范】：
请严格按照以下Schema规范输出JSON格式的结果。核心字段必须包含，扩展字段可放在metadata或custom_fields中。

{schema_json}

【关键说明】：
- 必须使用JSON格式输出，包含"presentation_plan"数组
- 每个plan必须包含：slide_index, layout_type, layout_description, visual_guidance
- layout_type可以是常用值（{', '.join([e.value for e in LayoutType])}），也可以自定义
- visual_guidance必须包含：font_size, font_weight, alignment
- 如果需要扩展信息，请放在metadata字段或visual_guidance.custom_fields中，使用snake_case命名"""
        
        # 构建幻灯片信息
        slides_info = []
        for slide in polished_slides:
            slide_info = f"""
幻灯片{slide.get('slide_index', 0)}：
- 标题：{slide.get('title', '')}
- 内容：{slide.get('content', '')}
- 内容类型：{slide.get('content_type', '')}
- 视觉元素需求：{json.dumps(slide.get('visual_elements', {}), ensure_ascii=False)}"""
            slides_info.append(slide_info)
        
        user_prompt = f"""请为以下润色后的幻灯片设计展示方式。

板块主题：{section_theme}

润色后的幻灯片：
{chr(10).join(slides_info)}

请按照以下要求进行展示策划：
1. 为每张幻灯片设计具体的展示方式
2. 考虑副总裁级别汇报的特点：简洁明了、快速抓住核心观点
3. 根据内容类型和视觉元素需求，设计合适的布局

【展示策划示例】：

幻灯片1（标题页）：
- 布局类型：blank_center（空白模板，页面正中间）
- 布局描述：页面正中间加粗、放大显示标题，其他区域留白
- 视觉指导：使用大号字体（76pt+），加粗，居中显示

幻灯片2（内容页，延续标题）：
- 布局类型：blank_center（空白模板，页面正中间）
- 布局描述：页面正中间加粗、放大显示内容，或者考虑与幻灯片1结合
- 视觉指导：使用大号字体（60pt+），加粗，居中显示

幻灯片3（数据页，需要表格/图表）：
- 布局类型：table_with_summary（表格+总结）
- 布局描述：将页面拆解成三页，每一页放置一个表格或图表，在图表下方或右侧放置1-3句总结性话术
- 视觉指导：表格/图表占页面60-70%，总结文字占30-40%，使用中等字体（28-32pt）

幻灯片4（效果页，需要卡片展示）：
- 布局类型：cards_with_data（卡片+数据）
- 布局描述：用三个圆角矩形分别包裹三个系统内容，在下方用居中的数字/文字展示提升数据
- 视觉指导：三个圆角矩形卡片横向排列，每个卡片内包含系统名称和描述，卡片下方居中显示数据（大号字体，加粗）

请以JSON格式输出展示策划结果：
{{
  "presentation_plan": [
    {{
      "slide_index": 幻灯片索引,
      "layout_type": "blank_center|table_with_summary|cards_with_data|split_content|...",
      "layout_description": "详细的布局描述",
      "visual_guidance": {{
        "font_size": "大号(76pt+)|中号(32-60pt)|小号(28pt以下)",
        "font_weight": "bold|normal",
        "alignment": "center|left|right",
        "spacing": "描述间距要求",
        "color_scheme": "描述配色方案",
        "other_notes": "其他视觉指导说明"
      }}
    }},
    ...
  ]
}}"""
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # 解析JSON响应
            if isinstance(response, str):
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    raw_result = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用默认策划")
                    return self._default_plan(polished_slides)
            else:
                raw_result = response
            
            # 规范化LLM输出
            normalized_result = PresentationProtocol.normalize_llm_output(raw_result)
            presentation_plan = normalized_result.get("presentation_plan", [])
            
            # 验证每个plan
            validated_plans = []
            for plan in presentation_plan:
                if PresentationProtocol.validate_presentation_plan(plan):
                    validated_plans.append(plan)
                else:
                    logger.warning(f"   展示策划数据不符合Schema，跳过: {plan}")
            
            if not validated_plans:
                logger.warning("   没有有效的展示策划结果，使用默认策划")
                return self._default_plan(polished_slides)
            
            logger.info(f"   ✅ 展示策划完成，策划了{len(validated_plans)}张幻灯片")
            for plan in validated_plans:
                logger.info(f"      幻灯片{plan.get('slide_index', 0)}: {plan.get('layout_type', '')} - {plan.get('layout_description', '')[:50]}...")
            
            return validated_plans
        except Exception as e:
            logger.error(f"   ❌ 展示策划失败: {e}，使用默认策划", exc_info=True)
            return self._default_plan(polished_slides)
    
    def _default_plan(self, polished_slides: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """默认策划（回退方案）"""
        plans = []
        for slide in polished_slides:
            content_type = slide.get("content_type", "content_page")
            if content_type == "title_page":
                layout_type = "blank_center"
            elif content_type == "data_page":
                layout_type = "table_with_summary"
            elif content_type == "effect_page":
                layout_type = "cards_with_data"
            else:
                layout_type = "content_page"
            
            plans.append({
                "slide_index": slide.get("slide_index", 0),
                "layout_type": layout_type,
                "layout_description": f"默认{layout_type}布局",
                "visual_guidance": {
                    "font_size": "中号(32-60pt)",
                    "font_weight": "normal",
                    "alignment": "center",
                    "spacing": "默认间距",
                    "color_scheme": "默认配色",
                    "other_notes": ""
                }
            })
        return plans

