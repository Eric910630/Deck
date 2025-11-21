# PPT展示Schema使用指南

## 📋 概述

本文档描述了PPT展示系统的Schema设计，采用**折中方案**：核心字段固定 + 灵活扩展机制。

## 🎯 设计原则

1. **核心字段固定**：确保系统稳定性和可预测性
2. **灵活扩展**：允许LLM动态添加自定义字段
3. **自描述协议**：LLM输出包含Schema描述，便于后续处理
4. **版本管理**：Schema版本化，支持未来演进

## 📦 Schema结构

### 1. 润色后的幻灯片 (PolishedSlideSchema)

**核心字段（必须）**：
- `slide_index`: 幻灯片索引（在板块内的索引，从0开始）
- `title`: 幻灯片标题（简洁有力，不超过15字）
- `content`: 幻灯片核心内容（1-2句话）
- `content_type`: 内容类型（固定值：`title_page`, `content_page`, `data_page`, `effect_page`, `summary_page`）
- `visual_elements`: 视觉元素需求（字典，可包含`needs_table`, `needs_chart`, `needs_cards`等）

**扩展字段（可选）**：
- `metadata`: 元数据（用于存储扩展信息，如`priority`, `estimated_duration`等）

**示例**：
```json
{
  "slide_index": 0,
  "title": "技术产品概述",
  "content": "展示三大技术产品体系的核心价值",
  "content_type": "title_page",
  "visual_elements": {
    "needs_table": false,
    "needs_chart": false,
    "needs_cards": false,
    "custom_visual_requirement": "需要品牌logo"
  },
  "metadata": {
    "priority": "high",
    "estimated_duration": "30秒"
  }
}
```

### 2. 展示策划 (PresentationPlanSchema)

**核心字段（必须）**：
- `slide_index`: 幻灯片索引（与polished_slide对应）
- `layout_type`: 布局类型（常用值：`blank_center`, `cards_with_data`, `split_content`等，也可自定义）
- `layout_description`: 详细的布局描述（文字说明）
- `visual_guidance`: 视觉指导（必须包含`font_size`, `font_weight`, `alignment`）

**visual_guidance核心字段**：
- `font_size`: 字体大小（建议值：`large`(76pt+), `medium`(32-60pt), `small`(28pt以下)，也可用文字描述）
- `font_weight`: 字体粗细（`bold`, `normal`）
- `alignment`: 对齐方式（`center`, `left`, `right`）

**visual_guidance扩展字段（可选）**：
- `spacing`: 间距描述
- `color_scheme`: 配色方案描述
- `other_notes`: 其他视觉指导说明
- `custom_fields`: 自定义字段（字典形式，用于扩展）

**扩展字段（可选）**：
- `data_bindings`: 数据绑定（用于指定需要填充的数据、图表等）
- `metadata`: 元数据（用于存储扩展信息）

**示例**：
```json
{
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
```

## 🔧 使用方式

### 在LLM Prompt中使用

Schema描述会自动包含在LLM的system prompt中，LLM需要：

1. **理解Schema结构**：通过`PresentationProtocol.get_schema_description()`获取完整描述
2. **遵循核心字段**：必须输出所有核心字段
3. **灵活扩展**：可以在`metadata`、`custom_fields`等位置添加自定义字段
4. **使用snake_case命名**：扩展字段建议使用snake_case命名规范

### 在代码中使用

```python
from presentation_schema import (
    PresentationProtocol,
    PolishedSlideSchema,
    PresentationPlanSchema,
    VisualGuidanceSchema
)

# 验证LLM输出
if PresentationProtocol.validate_polished_slide(slide_data):
    # 处理有效数据
    pass

# 规范化LLM输出（处理字段名变体）
normalized = PresentationProtocol.normalize_llm_output(llm_output)

# 使用Schema类
polished_slide = PolishedSlideSchema.from_dict(slide_data)
presentation_plan = PresentationPlanSchema.from_dict(plan_data)
```

## 📝 扩展机制

### 允许扩展的位置

1. **polished_slide.metadata**: 存储润色相关的扩展信息
2. **polished_slide.visual_elements**: 添加自定义视觉元素需求
3. **presentation_plan.metadata**: 存储策划相关的扩展信息
4. **presentation_plan.visual_guidance.custom_fields**: 添加自定义视觉指导字段
5. **presentation_plan.data_bindings**: 添加数据绑定信息

### 命名规范

- 使用`snake_case`命名（如`custom_field_name`）
- 避免与核心字段冲突
- 保持语义清晰

## 🔄 版本管理

当前Schema版本：**1.0.0**

版本更新时，需要：
1. 更新`PresentationProtocol.SCHEMA_VERSION`
2. 更新`get_schema_description()`方法
3. 保持向后兼容（核心字段不变）

## ✅ 验证规则

### PolishedSlideSchema验证
- 必须包含：`slide_index`, `title`, `content`, `content_type`

### PresentationPlanSchema验证
- 必须包含：`slide_index`, `layout_type`, `layout_description`, `visual_guidance`
- `visual_guidance`必须包含：`font_size`, `font_weight`, `alignment`

## 🚀 最佳实践

1. **优先使用核心字段**：尽量使用预定义的枚举值
2. **合理扩展**：只在必要时添加自定义字段
3. **文档化扩展**：在metadata中添加说明，便于后续理解
4. **版本兼容**：扩展时考虑向后兼容性

## 📚 相关文件

- `presentation_schema.py`: Schema定义和协议
- `content_polisher.py`: 使用Schema进行内容润色
- `presentation_planner.py`: 使用Schema进行展示策划

