"""
内容润色模块
将文档内容润色成适合PPT展示的文案
"""

from typing import Dict, Any, List
from loguru import logger
from ..core.llm_service import LLMService
from .presentation_schema import (
    PresentationProtocol,
    PolishedSlideSchema,
    ContentType
)
import json
import re


class ContentPolisher:
    """
    内容润色器
    将文档内容润色成适合PPT展示的文案
    """
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        logger.info("--- [ContentPolisher]: 初始化内容润色器")
    
    async def polish_section(
        self,
        section_analysis: Dict[str, Any],
        section_index: int
    ) -> List[Dict[str, Any]]:
        """
        润色板块内容，生成适合PPT展示的文案
        
        Args:
            section_analysis: 板块分析结果（包含主题、核心思想、内容摘要等）
            section_index: 板块索引
            
        Returns:
            润色后的幻灯片列表，每个元素包含：
            - slide_index: 幻灯片索引（在该板块内的索引）
            - title: 幻灯片标题
            - content: 幻灯片内容
            - content_type: 内容类型（title_page, content_page, data_page等）
            - notes: 备注（如需要表格、图表等）
        """
        logger.info(f"--- [ContentPolisher]: 润色板块{section_index}: {section_analysis.get('theme', '')}")
        
        # 获取Schema描述
        schema_desc = PresentationProtocol.get_schema_description()
        schema_json = json.dumps(schema_desc, ensure_ascii=False, indent=2)
        
        system_prompt = f"""你是中国职场的述职汇报专家，专门为副总裁级别的职场高管筹备述职内容，最擅长将高管整理的文稿大纲转换成适合呈现在ppt上的语言内容。

你具备强大的内容润色能力，能够将文档内容润色成适合PPT展示的文案。

【重要】PPT不是文字堆砌的展示平台，润色要求：
1. **简洁有力**：每张幻灯片只表达一个核心观点
2. **标题化**：将内容提炼成简洁的标题和副标题
3. **视觉化**：考虑如何用视觉元素（表格、图表、卡片等）展示内容
4. **层次化**：将复杂内容拆分成多张幻灯片，每张聚焦一个要点
5. **数据化**：识别需要数据支持的内容，标注需要表格/图表的位置
6. **详细展开**：当有多个视觉元素（如多个卡片、多个图表）时，必须详细展开每个元素的具体内容，不能只说"需要3个卡片"，而要说明每个卡片的具体标题、内容、数据等

【输出Schema规范】：
请严格按照以下Schema规范输出JSON格式的结果。核心字段必须包含，扩展字段可放在metadata中。

{schema_json}

【关键说明】：
- 必须使用JSON格式输出，包含"polished_slides"数组
- 每个slide必须包含：slide_index, title, content, content_type
- content_type必须是以下之一：{', '.join([e.value for e in ContentType])}
- visual_elements可以包含needs_table, needs_chart, needs_cards等标准字段，也可以添加自定义字段
- 如果需要扩展信息，请放在metadata字段中，使用snake_case命名"""
        
        user_prompt = f"""请对以下板块内容进行PPT展示层面的润色，生成适合PPT展示的文案。

板块信息：
- 板块主题：{section_analysis.get('theme', '')}
- 核心思想：{section_analysis.get('core_idea', '')}
- 内容摘要：{section_analysis.get('content_summary', '')}

请按照以下要求进行润色：
1. 将板块内容拆分成多张幻灯片（根据内容复杂度，通常2-4张）
2. 为每张幻灯片生成：
   - 简洁有力的标题（不超过15字）
   - 核心内容描述（1-2句话）
   - 内容类型（title_page标题页、content_page内容页、data_page数据页等）
   - 视觉元素需求（如需要表格、图表、卡片等，用占位符标注）

【润色示例】：
板块：技术产品概览与价值主张
内容摘要：介绍全链路AI赋能解决方案，核心价值主张包括降低运营成本40-60%、提升转化效率20-35%、加速业务智能化转型。包含25年技术回顾，涵盖朋友云、AI平台和数据中心的成果展示

润色结果：
幻灯片1：
- 标题：技术产品概述与价值主张
- 内容类型：title_page（标题页，空白模板，页面正中间加粗、放大显示）
- 视觉元素：无

幻灯片2：
- 标题：产品核心价值 —— 全链路AI赋能解决方案
- 内容类型：content_page（内容页，页面正中间加粗、放大显示）
- 视觉元素：无

幻灯片3：
- 标题：技术成果展示
- 内容：25年技术回顾，涵盖朋友云、AI平台和数据中心的成果展示
- 内容类型：data_page（数据页，需要表格/图表展示）
- 视觉元素：需要表格数据，但检索当前文档无相关数据，使用占位符保留位置

幻灯片4：
- 标题：技术产品落地效果
- 内容：降低运营成本40-60%、提升转化效率20-35%、加速业务智能化转型
- 内容类型：content_page（内容页，用圆角矩形卡片展示）
- 视觉元素：三个圆角矩形分别包裹三个系统内容，下方用居中的数字/文字展示提升数据
- 视觉元素详细展开（必须包含所有元素，包括标题和内容）：
  * 元素0 (ID: title_text_0, 类型: title_text)：技术产品落地效果
    - 内容: 幻灯片标题
    - 说明: 标题文本，用于标识幻灯片主题
  * 元素1 (ID: content_text_0, 类型: content_text)：降低运营成本40-60%、提升转化效率20-35%、加速业务智能化转型
    - 内容: 幻灯片内容描述
    - 说明: 内容文本，概述幻灯片核心信息
  * 元素2 (ID: value_card_0, 类型: value_card)：降本
    - 内容: 运营成本降低40-60%
    - 数据: 40-60%
    - 说明: 通过自动化流程和智能优化实现运营成本大幅降低
  * 元素3 (ID: value_card_1, 类型: value_card)：增效
    - 内容: 转化效率提升20-35%
    - 数据: 20-35%
    - 说明: 通过AI技术提升转化效率
  * 元素4 (ID: value_card_2, 类型: value_card)：转型
    - 内容: 加速业务智能化转型
    - 数据: 智能化
    - 说明: 推动业务向智能化方向转型

请以JSON格式输出润色结果：
{{
  "polished_slides": [
    {{
      "slide_index": 在该板块内的索引（从0开始）,
      "title": "幻灯片标题",
      "content": "幻灯片核心内容（1-2句话）",
      "content_type": "title_page|content_page|data_page|effect_page",
      "visual_elements": {{
        "needs_table": true/false,
        "needs_chart": true/false,
        "needs_cards": true/false,
        "needs_placeholder": true/false,
        "notes": "视觉元素说明（如：需要三个圆角矩形卡片）"
      }},
      "visual_elements_detail": [
        {{
          "element_index": 元素索引（从0开始）,
          "element_id": "元素唯一标识（格式：element_type_element_index，如value_card_0、product_card_1等，用于唯一标识每个元素，避免传参混淆）",
          "element_type": "元素类型（必须根据元素的具体用途命名，不能都用'card'，应该用：value_card|product_card|advantage_card|data_card|feature_card|trend_card|strategy_card|chart|table|text|icon等）",
          "title": "元素标题（如卡片标题）",
          "content": "元素内容描述",
          "data": "元素数据（如有）",
          "description": "元素详细说明"
        }},
        ...
      ]
    }},
    ...
  ]
}}

【关键要求】：
- **重要**：每张幻灯片的所有内容元素都必须展开，包括：
  * 标题文本（title_text）：幻灯片的标题，必须作为独立元素
  * 内容文本（content_text）：幻灯片的内容描述，必须作为独立元素
  * 视觉元素（cards、charts等）：所有视觉元素都必须展开
- visual_elements_detail必须包含幻灯片上的所有元素，不能遗漏：
  * 元素0通常是title_text（标题文本）
  * 元素1通常是content_text（内容文本）
  * 元素2+是各种视觉元素（cards、charts等）
- 每个元素都要有element_index、element_id、element_type、title、content
- element_id格式：element_type_element_index（如title_text_0、content_text_0、value_card_0、product_card_1），用于唯一标识，避免传参混淆
- element_type必须根据元素的具体用途命名：
    - title_text：标题文本（幻灯片的标题）
    - content_text：内容文本（幻灯片的内容描述）
    - subtitle_text：副标题文本（如有）
    - value_card：价值卡片（展示价值主张、效益等）
    - product_card：产品卡片（展示产品、系统等）
    - advantage_card：优势卡片（展示竞争优势、特点等）
    - data_card：数据卡片（展示数据指标、统计等）
    - feature_card：功能卡片（展示功能特性等）
    - trend_card：趋势卡片（展示趋势、方向等）
    - strategy_card：策略卡片（展示策略、方案等）
    - chart：图表
    - table：表格
    - icon：图标
- 如果有数据，必须包含data字段
- 每个元素都要有清晰的description说明其具体作用
- 示例：一张包含标题、内容和3个卡片的幻灯片，visual_elements_detail应该包含5个元素：
  * 元素0 (title_text_0)：标题文本
  * 元素1 (content_text_0)：内容文本
  * 元素2 (value_card_0)：第一个卡片
  * 元素3 (value_card_1)：第二个卡片
  * 元素4 (value_card_2)：第三个卡片"""
        
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
                    logger.warning("   无法从LLM响应中提取JSON，使用默认润色")
                    return self._default_polish(section_analysis)
            else:
                raw_result = response
            
            # 规范化LLM输出
            normalized_result = PresentationProtocol.normalize_llm_output(raw_result)
            polished_slides = normalized_result.get("polished_slides", [])
            
            # 验证每个slide
            validated_slides = []
            for slide in polished_slides:
                if PresentationProtocol.validate_polished_slide(slide):
                    validated_slides.append(slide)
                else:
                    logger.warning(f"   幻灯片数据不符合Schema，跳过: {slide}")
            
            if not validated_slides:
                logger.warning("   没有有效的润色结果，使用默认润色")
                return self._default_polish(section_analysis)
            
            logger.info(f"   ✅ 润色完成，生成{len(validated_slides)}张幻灯片")
            for slide in validated_slides:
                logger.info(f"      幻灯片{slide.get('slide_index', 0)}: {slide.get('title', '')} ({slide.get('content_type', '')})")
            
            return validated_slides
        except Exception as e:
            logger.error(f"   ❌ 润色失败: {e}，使用默认润色", exc_info=True)
            return self._default_polish(section_analysis)
    
    def _default_polish(self, section_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """默认润色（回退方案）"""
        return [{
            "slide_index": 0,
            "title": section_analysis.get("theme", "未命名板块"),
            "content": section_analysis.get("content_summary", ""),
            "content_type": "content_page",
            "visual_elements": {
                "needs_table": False,
                "needs_chart": False,
                "needs_cards": False,
                "needs_placeholder": False,
                "notes": ""
            }
        }]

