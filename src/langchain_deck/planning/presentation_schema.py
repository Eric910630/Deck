"""
PPT展示Schema定义
采用折中方案：核心字段固定 + 灵活扩展机制
"""

from typing import Dict, Any, List, Optional
from enum import Enum
import json
from loguru import logger


class ContentType(str, Enum):
    """内容类型枚举"""
    TITLE_PAGE = "title_page"
    CONTENT_PAGE = "content_page"
    DATA_PAGE = "data_page"
    EFFECT_PAGE = "effect_page"
    SUMMARY_PAGE = "summary_page"


class LayoutType(str, Enum):
    """布局类型枚举（常用布局）"""
    BLANK_CENTER = "blank_center"
    CARDS_WITH_DATA = "cards_with_data"
    SPLIT_CONTENT = "split_content"
    TIMELINE_HORIZONTAL = "timeline_horizontal"
    TABLE_WITH_SUMMARY = "table_with_summary"
    CARDS_GRID = "cards_grid"
    CHART_WITH_INSIGHT = "chart_with_insight"
    KEY_MESSAGE = "key_message"
    DUAL_WHEEL_CHART = "dual_wheel_chart"
    CHART_WITH_ANNOTATION = "chart_with_annotation"
    # 允许LLM动态扩展其他布局类型


class FontSize(str, Enum):
    """字体大小枚举"""
    LARGE = "large"  # 76pt+
    MEDIUM = "medium"  # 32-60pt
    SMALL = "small"  # 28pt以下


class FontWeight(str, Enum):
    """字体粗细枚举"""
    BOLD = "bold"
    NORMAL = "normal"


class Alignment(str, Enum):
    """对齐方式枚举"""
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"


class PolishedSlideSchema:
    """
    润色后的幻灯片Schema（核心字段固定）
    """
    
    def __init__(
        self,
        slide_index: int,
        title: str,
        content: str,
        content_type: str,
        visual_elements: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        初始化润色后的幻灯片Schema
        
        Args:
            slide_index: 幻灯片索引（在板块内的索引）
            title: 幻灯片标题
            content: 幻灯片核心内容
            content_type: 内容类型（使用ContentType枚举或字符串）
            visual_elements: 视觉元素需求（可选，灵活扩展）
            metadata: 元数据（可选，用于存储LLM动态生成的其他信息）
        """
        self.slide_index = slide_index
        self.title = title
        self.content = content
        self.content_type = content_type
        self.visual_elements = visual_elements or {}
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "slide_index": self.slide_index,
            "title": self.title,
            "content": self.content,
            "content_type": self.content_type,
            "visual_elements": self.visual_elements,
            "metadata": self.metadata
        }
        if self.visual_elements_detail:
            result["visual_elements_detail"] = self.visual_elements_detail
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PolishedSlideSchema":
        """从字典创建"""
        return cls(
            slide_index=data.get("slide_index", 0),
            title=data.get("title", ""),
            content=data.get("content", ""),
            content_type=data.get("content_type", ContentType.CONTENT_PAGE.value),
            visual_elements=data.get("visual_elements", {}),
            visual_elements_detail=data.get("visual_elements_detail", []),
            metadata=data.get("metadata", {})
        )


class VisualGuidanceSchema:
    """
    视觉指导Schema（核心字段固定）
    """
    
    def __init__(
        self,
        font_size: str,
        font_weight: str,
        alignment: str,
        spacing: Optional[str] = None,
        color_scheme: Optional[str] = None,
        other_notes: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ):
        """
        初始化视觉指导Schema
        
        Args:
            font_size: 字体大小（使用FontSize枚举或字符串，如"大号(76pt+)"）
            font_weight: 字体粗细（使用FontWeight枚举或字符串）
            alignment: 对齐方式（使用Alignment枚举或字符串）
            spacing: 间距描述（可选）
            color_scheme: 配色方案描述（可选）
            other_notes: 其他说明（可选）
            custom_fields: 自定义字段（可选，用于LLM动态扩展）
        """
        self.font_size = font_size
        self.font_weight = font_weight
        self.alignment = alignment
        self.spacing = spacing
        self.color_scheme = color_scheme
        self.other_notes = other_notes
        self.custom_fields = custom_fields or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "font_size": self.font_size,
            "font_weight": self.font_weight,
            "alignment": self.alignment
        }
        if self.spacing:
            result["spacing"] = self.spacing
        if self.color_scheme:
            result["color_scheme"] = self.color_scheme
        if self.other_notes:
            result["other_notes"] = self.other_notes
        if self.custom_fields:
            result["custom_fields"] = self.custom_fields
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VisualGuidanceSchema":
        """从字典创建"""
        # 提取自定义字段（不在核心字段中的）
        core_fields = {"font_size", "font_weight", "alignment", "spacing", "color_scheme", "other_notes"}
        custom_fields = {k: v for k, v in data.items() if k not in core_fields}
        
        return cls(
            font_size=data.get("font_size", FontSize.MEDIUM.value),
            font_weight=data.get("font_weight", FontWeight.NORMAL.value),
            alignment=data.get("alignment", Alignment.LEFT.value),
            spacing=data.get("spacing"),
            color_scheme=data.get("color_scheme"),
            other_notes=data.get("other_notes"),
            custom_fields=custom_fields if custom_fields else None
        )


class PresentationPlanSchema:
    """
    展示策划Schema（核心字段固定）
    """
    
    def __init__(
        self,
        slide_index: int,
        layout_type: str,
        layout_description: str,
        visual_guidance: VisualGuidanceSchema,
        data_bindings: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        初始化展示策划Schema
        
        Args:
            slide_index: 幻灯片索引
            layout_type: 布局类型（使用LayoutType枚举或字符串，允许LLM动态扩展）
            layout_description: 布局描述
            visual_guidance: 视觉指导
            data_bindings: 数据绑定（可选，用于指定需要填充的数据、图表等）
            metadata: 元数据（可选，用于存储LLM动态生成的其他信息）
        """
        self.slide_index = slide_index
        self.layout_type = layout_type
        self.layout_description = layout_description
        self.visual_guidance = visual_guidance
        self.data_bindings = data_bindings or {}
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "slide_index": self.slide_index,
            "layout_type": self.layout_type,
            "layout_description": self.layout_description,
            "visual_guidance": self.visual_guidance.to_dict(),
            "data_bindings": self.data_bindings,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PresentationPlanSchema":
        """从字典创建"""
        return cls(
            slide_index=data.get("slide_index", 0),
            layout_type=data.get("layout_type", LayoutType.BLANK_CENTER.value),
            layout_description=data.get("layout_description", ""),
            visual_guidance=VisualGuidanceSchema.from_dict(data.get("visual_guidance", {})),
            data_bindings=data.get("data_bindings", {}),
            metadata=data.get("metadata", {})
        )


class PresentationProtocol:
    """
    PPT展示协议（用于LLM之间的通信）
    包含Schema版本和自描述信息
    """
    
    SCHEMA_VERSION = "1.0.0"
    
    @staticmethod
    def get_schema_description() -> Dict[str, Any]:
        """
        获取Schema描述（用于LLM理解）
        返回一个包含核心字段说明和扩展机制的描述
        """
        return {
            "schema_version": PresentationProtocol.SCHEMA_VERSION,
            "core_fields": {
                "polished_slide": {
                    "slide_index": "幻灯片索引（在板块内的索引，从0开始）",
                    "title": "幻灯片标题（简洁有力，不超过15字）",
                    "content": "幻灯片核心内容（1-2句话）",
                    "content_type": f"内容类型（固定值：{', '.join([e.value for e in ContentType])}）",
                    "visual_elements": "视觉元素需求（字典，可包含needs_table, needs_chart, needs_cards等）",
                    "visual_elements_detail": "视觉元素详细展开（数组，当有多个元素时，必须详细展开每个元素的具体内容，每个元素包含：element_index, element_id, element_type, title, content, data等。element_id格式：element_type_element_index，用于唯一标识，避免传参混淆）",
                    "metadata": "元数据（可选，用于存储扩展信息）"
                },
                "presentation_plan": {
                    "slide_index": "幻灯片索引（与polished_slide对应）",
                    "layout_type": f"布局类型（常用值：{', '.join([e.value for e in LayoutType])}，也可自定义）",
                    "layout_description": "详细的布局描述（文字说明）",
                    "visual_guidance": {
                        "font_size": f"字体大小（建议值：{', '.join([e.value for e in FontSize])}，也可用文字描述如'大号(76pt+)'）",
                        "font_weight": f"字体粗细（{', '.join([e.value for e in FontWeight])}）",
                        "alignment": f"对齐方式（{', '.join([e.value for e in Alignment])}）",
                        "spacing": "间距描述（可选，文字说明）",
                        "color_scheme": "配色方案描述（可选，文字说明）",
                        "other_notes": "其他视觉指导说明（可选）",
                        "custom_fields": "自定义字段（可选，字典形式，用于扩展）"
                    },
                    "data_bindings": "数据绑定（可选，用于指定需要填充的数据、图表等）",
                    "metadata": "元数据（可选，用于存储扩展信息）"
                }
            },
            "extension_mechanism": {
                "description": "LLM可以在以下位置添加自定义字段：",
                "locations": [
                    "polished_slide.metadata: 存储润色相关的扩展信息",
                    "polished_slide.visual_elements: 添加自定义视觉元素需求",
                    "presentation_plan.metadata: 存储策划相关的扩展信息",
                    "presentation_plan.visual_guidance.custom_fields: 添加自定义视觉指导字段",
                    "presentation_plan.data_bindings: 添加数据绑定信息"
                ],
                "naming_convention": "建议使用snake_case命名，如custom_field_name"
            },
            "example": {
                "polished_slide": {
                    "slide_index": 0,
                    "title": "技术产品概述",
                    "content": "展示三大技术产品体系的核心价值",
                    "content_type": "title_page",
                    "visual_elements": {
                        "needs_table": False,
                        "needs_chart": False,
                        "needs_cards": True,
                        "custom_visual_requirement": "需要品牌logo"
                    },
                    "visual_elements_detail": [
                        {
                            "element_index": 0,
                            "element_id": "value_card_0",
                            "element_type": "value_card",
                            "title": "降本",
                            "content": "运营成本降低40-60%",
                            "data": "40-60%",
                            "description": "通过自动化流程和智能优化，显著降低运营成本"
                        },
                        {
                            "element_index": 1,
                            "element_id": "value_card_1",
                            "element_type": "value_card",
                            "title": "增效",
                            "content": "转化效率提升20-35%",
                            "data": "20-35%",
                            "description": "通过AI技术提升转化效率"
                        },
                        {
                            "element_index": 2,
                            "element_id": "value_card_2",
                            "element_type": "value_card",
                            "title": "转型",
                            "content": "加速业务智能化转型",
                            "data": "智能化",
                            "description": "推动业务向智能化方向转型"
                        }
                    ],
                    "metadata": {
                        "priority": "high",
                        "estimated_duration": "30秒"
                    }
                },
                "presentation_plan": {
                    "slide_index": 0,
                    "layout_type": "blank_center",
                    "layout_description": "页面正中间加粗放大显示标题，其他区域留白",
                    "visual_guidance": {
                        "font_size": "large",
                        "font_weight": "bold",
                        "alignment": "center",
                        "spacing": "标题与副标题间距1.5倍行高",
                        "color_scheme": "深色标题+浅灰色副标题",
                        "custom_fields": {
                            "background_color": "#FFFFFF",
                            "title_color": "#1A1A1A"
                        }
                    },
                    "data_bindings": {},
                    "metadata": {
                        "layout_complexity": "simple",
                        "render_time_estimate": "2秒"
                    }
                }
            }
        }
    
    @staticmethod
    def validate_polished_slide(data: Dict[str, Any]) -> bool:
        """验证润色后的幻灯片数据是否符合Schema"""
        required_fields = ["slide_index", "title", "content", "content_type"]
        return all(field in data for field in required_fields)
    
    @staticmethod
    def validate_presentation_plan(data: Dict[str, Any]) -> bool:
        """验证展示策划数据是否符合Schema"""
        required_fields = ["slide_index", "layout_type", "layout_description", "visual_guidance"]
        if not all(field in data for field in required_fields):
            return False
        # 验证visual_guidance
        vg = data.get("visual_guidance", {})
        required_vg_fields = ["font_size", "font_weight", "alignment"]
        return all(field in vg for field in required_vg_fields)
    
    @staticmethod
    def _normalize_visual_elements_detail(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        规范化视觉元素详细展开，确保每个元素都有element_id
        如果LLM没有提供element_id，自动生成：element_type_element_index
        这样可以避免多个相同类型元素在传参时混淆
        """
        normalized_elements = []
        for elem in elements:
            element_index = elem.get("element_index", 0)
            element_type = elem.get("element_type", "unknown")
            element_id = elem.get("element_id")
            
            # 如果没有element_id，自动生成（格式：element_type_element_index）
            if not element_id:
                element_id = f"{element_type}_{element_index}"
            
            normalized_elem = {
                "element_index": element_index,
                "element_id": element_id,  # 唯一标识，避免传参混淆
                "element_type": element_type,
                "title": elem.get("title", ""),
                "content": elem.get("content", ""),
                "data": elem.get("data"),
                "description": elem.get("description", "")
            }
            normalized_elements.append(normalized_elem)
        return normalized_elements
    
    @staticmethod
    def normalize_llm_output(llm_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        规范化LLM输出，确保符合Schema
        如果LLM使用了不同的字段名，尝试映射到标准字段
        """
        normalized = {}
        
        # 处理polished_slides
        if "polished_slides" in llm_output:
            polished_slides = []
            for slide in llm_output["polished_slides"]:
                # 字段名映射（处理LLM可能的变体）
                normalized_slide = {
                    "slide_index": slide.get("slide_index") or slide.get("index") or slide.get("slide_id", 0),
                    "title": slide.get("title") or slide.get("slide_title") or "",
                    "content": slide.get("content") or slide.get("content_text") or "",
                    "content_type": slide.get("content_type") or slide.get("type") or ContentType.CONTENT_PAGE.value,
                    "visual_elements": slide.get("visual_elements") or slide.get("visual") or {},
                    "visual_elements_detail": PresentationProtocol._normalize_visual_elements_detail(
                        slide.get("visual_elements_detail") or slide.get("visual_detail") or slide.get("elements_detail") or []
                    ),
                    "metadata": slide.get("metadata") or {}
                }
                polished_slides.append(normalized_slide)
            normalized["polished_slides"] = polished_slides
        
        # 处理presentation_plan
        if "presentation_plan" in llm_output:
            presentation_plan = []
            for plan in llm_output["presentation_plan"]:
                # 字段名映射
                vg = plan.get("visual_guidance") or plan.get("visual") or {}
                normalized_plan = {
                    "slide_index": plan.get("slide_index") or plan.get("index") or plan.get("slide_id", 0),
                    "layout_type": plan.get("layout_type") or plan.get("layout") or LayoutType.BLANK_CENTER.value,
                    "layout_description": plan.get("layout_description") or plan.get("description") or "",
                    "visual_guidance": {
                        "font_size": vg.get("font_size") or FontSize.MEDIUM.value,
                        "font_weight": vg.get("font_weight") or FontWeight.NORMAL.value,
                        "alignment": vg.get("alignment") or Alignment.LEFT.value,
                        "spacing": vg.get("spacing"),
                        "color_scheme": vg.get("color_scheme"),
                        "other_notes": vg.get("other_notes"),
                        "custom_fields": vg.get("custom_fields") or {}
                    },
                    "data_bindings": plan.get("data_bindings") or {},
                    "metadata": plan.get("metadata") or {}
                }
                presentation_plan.append(normalized_plan)
            normalized["presentation_plan"] = presentation_plan
        
        return normalized

