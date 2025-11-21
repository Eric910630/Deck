# 完整工作流程指南

## 🎯 整体流程概览

```
1. 框架内容分析（已完成）
   ↓
2. 内容生成策略制定
   ↓
3. 逐板块内容生成
   ↓
4. 格式和样式应用
   ↓
5. 支撑材料整合
   ↓
6. 最终PPT生成
```

---

## 📋 详细流程说明

### 阶段1：框架内容分析 ✅（已完成）

**目标**：理解文档的整体思想、板块结构、论证逻辑等

**输出**：
- 核心主题
- 价值主张
- 板块结构（每个板块的主题和核心思想）
- 论证逻辑（论证类型、证据点）
- 支撑材料（数据、图表、案例）
- 表达风格（正式程度、语调、文化特征）
- 呈现形式（布局、字体、视觉层次）

**已完成**：
- ✅ `human_centered_analyzer.py` - 人类中心化分析器
- ✅ 6层分析流程

---

### 阶段2：内容生成策略制定

**目标**：根据分析结果，制定内容生成策略

**策略要素**：

#### 2.1 内容生成策略

```python
{
  "overall_strategy": {
    "core_theme": "技术产品商业化",
    "value_propositions": ["降低40-60%成本", "提升20-35%效率"],
    "target_audience": "管理层",
    "tone": "积极",
    "formality_level": "中性"
  },
  "section_strategies": [
    {
      "section_index": 0,
      "theme": "技术产品商业化-文档",
      "core_idea": "全链路AI赋能解决方案",
      "argument_types": ["数据论证", "案例论证"],
      "content_generation_approach": {
        "emphasis": "价值主张",
        "evidence_priority": ["数据", "案例"],
        "length": "medium"
      }
    }
  ]
}
```

#### 2.2 表达风格策略

```python
{
  "language_style": {
    "formality": "中性",  # 根据分析结果
    "tone": "积极",      # 根据分析结果
    "cultural_features": ["强调价值导向", "数据驱动表达"]
  },
  "visual_style": {
    "layout": "16:9",
    "typography": {
      "title_font_size": 38,  # 根据Ant Design规范
      "body_font_size": 14
    },
    "color_scheme": "Ant Design主题色"
  }
}
```

**实现方式**：
- 创建 `content_strategy_generator.py`
- 根据人类中心化分析结果生成策略

---

### 阶段3：逐板块内容生成

**目标**：根据策略，为每个板块生成具体内容

**流程**：

#### 3.1 为每个板块生成内容

```python
for section in sections:
    # 1. 构建生成提示词
    prompt = build_generation_prompt(
        section_theme=section["theme"],
        core_idea=section["core_idea"],
        argument_types=section["argument_types"],
        evidence_points=section["evidence_points"],
        strategy=section["content_generation_approach"]
    )
    
    # 2. 调用LLM生成内容
    generated_content = await llm_service.generate_content(prompt)
    
    # 3. 结构化内容
    structured_content = structure_content(generated_content)
    
    # 4. 映射到PPT占位符
    placeholder_mapping = map_to_placeholders(structured_content, section["slides"])
```

#### 3.2 内容生成提示词模板

```python
def build_generation_prompt(section, strategy):
    return f"""
根据以下信息，生成符合中国商业汇报习惯的PPT内容：

【板块主题】
{section["theme"]}

【核心思想】
{section["core_idea"]}

【论证方式】
{", ".join(section["argument_types"])}

【证据点】
{format_evidence_points(section["evidence_points"])}

【生成要求】
1. 语言风格：{strategy["language_style"]["formality"]}，语调：{strategy["language_style"]["tone"]}
2. 强调：{strategy["content_generation_approach"]["emphasis"]}
3. 优先使用：{", ".join(strategy["content_generation_approach"]["evidence_priority"])}
4. 长度：{strategy["content_generation_approach"]["length"]}
5. 符合中国商业文化：{", ".join(strategy["language_style"]["cultural_features"])}

请生成：
- 标题（简洁有力，体现核心思想）
- 正文内容（包含论据和证据点）
- 数据支撑（如果有）
- 案例说明（如果有）
"""
```

**实现方式**：
- 修改 `ppt_filler.py`
- 使用人类中心化分析结果
- 调用LLM生成内容

---

### 阶段4：格式和样式应用

**目标**：应用Ant Design规范和表达风格

**流程**：

#### 4.1 应用格式规范

```python
def apply_format_and_style(ppt, analysis_result):
    # 1. 强制16:9布局
    ppt.slide_width = Cm(33.867)
    ppt.slide_height = Cm(19.05)
    
    # 2. 应用Ant Design字体
    for slide in ppt.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text_frame"):
                for para in shape.text_frame.paragraphs:
                    apply_ant_design_style(para, analysis_result)
    
    # 3. 应用表达风格
    apply_expression_style(ppt, analysis_result["layer_5_expression_style"])
```

#### 4.2 根据表达风格调整

```python
def apply_expression_style(ppt, style_data):
    formality = style_data["formality_level"]
    tone = style_data["tone"]
    cultural_features = style_data["cultural_features"]
    
    # 根据正式程度调整字体大小
    if formality == "正式":
        title_font_size = 40  # 更大
        body_font_size = 15
    elif formality == "非正式":
        title_font_size = 36  # 稍小
        body_font_size = 14
    else:
        title_font_size = 38  # 标准
        body_font_size = 14
    
    # 根据语调调整颜色
    if tone == "积极":
        primary_color = AntDesignColors.primary  # 蓝色
    elif tone == "谨慎":
        primary_color = AntDesignColors.warning  # 橙色
    else:
        primary_color = AntDesignColors.text_primary  # 黑色
    
    # 应用文化特征
    if "强调价值导向" in cultural_features:
        # 突出价值主张部分
        emphasize_value_propositions(ppt)
    
    if "数据驱动表达" in cultural_features:
        # 突出数据部分
        emphasize_data_points(ppt)
```

**实现方式**：
- 增强 `ppt_filler.py` 中的格式应用逻辑
- 根据表达风格动态调整

---

### 阶段5：支撑材料整合

**目标**：整合数据、图表、案例等支撑材料

**流程**：

#### 5.1 数据点整合

```python
def integrate_supporting_materials(ppt, analysis_result):
    materials = analysis_result["layer_4_supporting_materials"]["data"]["materials"]
    
    # 1. 数据点整合
    for data_point in materials["data_points"]:
        slide_idx = data_point["slide_index"]
        # 在对应幻灯片中突出显示数据
        highlight_data_point(ppt.slides[slide_idx], data_point)
    
    # 2. 案例整合
    for case in materials["cases"]:
        slide_idx = case["slide_index"]
        # 在对应幻灯片中添加案例说明
        add_case_study(ppt.slides[slide_idx], case)
    
    # 3. 图表生成（如果需要）
    if need_charts(analysis_result):
        generate_charts(ppt, analysis_result)
```

#### 5.2 图表生成策略

```python
def generate_charts(ppt, analysis_result):
    # 根据数据点生成图表
    data_points = analysis_result["layer_4_supporting_materials"]["data"]["materials"]["data_points"]
    
    # 识别可以可视化的数据
    chartable_data = identify_chartable_data(data_points)
    
    for chart_data in chartable_data:
        # 生成图表
        chart = generate_chart(chart_data)
        
        # 插入到对应幻灯片
        insert_chart(ppt, chart, chart_data["slide_index"])
```

**实现方式**：
- 增强 `ppt_filler.py`
- 使用 `chart_generator.py` 生成图表

---

### 阶段6：最终PPT生成

**目标**：生成最终的PPT文件

**流程**：

#### 6.1 最终检查和优化

```python
def finalize_ppt(ppt, analysis_result):
    # 1. 检查16:9比例
    verify_aspect_ratio(ppt)
    
    # 2. 检查格式一致性
    verify_format_consistency(ppt, analysis_result)
    
    # 3. 检查内容完整性
    verify_content_completeness(ppt, analysis_result)
    
    # 4. 优化视觉层次
    optimize_visual_hierarchy(ppt, analysis_result)
    
    # 5. 保存PPT
    ppt.save(output_path)
```

#### 6.2 质量检查清单

```python
quality_checklist = {
    "layout": {
        "aspect_ratio": "16:9",
        "slide_width": 33.867,  # cm
        "slide_height": 19.05   # cm
    },
    "format": {
        "title_font": "Segoe UI / 微软雅黑",
        "title_size": 38,  # pt
        "body_font": "Segoe UI / 微软雅黑",
        "body_size": 14,   # pt
        "colors": "Ant Design主题色"
    },
    "content": {
        "all_sections_filled": True,
        "value_propositions_highlighted": True,
        "data_points_visible": True,
        "logical_flow": True
    },
    "style": {
        "expression_style_applied": True,
        "cultural_features_reflected": True,
        "visual_hierarchy_clear": True
    }
}
```

---

## 🔄 完整流程图

```
┌─────────────────────────────────────┐
│  1. 框架内容分析（人类中心化）        │
│  - 通读理解                          │
│  - 板块拆分                          │
│  - 论证逻辑                          │
│  - 支撑材料                          │
│  - 表达风格                          │
│  - 呈现形式                          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  2. 内容生成策略制定                  │
│  - 整体策略（主题、受众、语调）       │
│  - 板块策略（论证方式、证据优先级）   │
│  - 表达风格策略                      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  3. 逐板块内容生成                    │
│  - 构建生成提示词                    │
│  - 调用LLM生成内容                   │
│  - 结构化内容                        │
│  - 映射到PPT占位符                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  4. 格式和样式应用                    │
│  - 强制16:9布局                      │
│  - 应用Ant Design规范                │
│  - 根据表达风格调整                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  5. 支撑材料整合                      │
│  - 数据点整合                        │
│  - 案例整合                          │
│  - 图表生成（如果需要）              │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  6. 最终PPT生成                       │
│  - 质量检查                          │
│  - 格式验证                          │
│  - 内容完整性检查                    │
│  - 保存PPT                           │
└─────────────────────────────────────┘
```

---

## 📝 实现计划

### 阶段1：内容生成策略制定（下一步）

**任务**：
1. 创建 `content_strategy_generator.py`
2. 根据人类中心化分析结果生成策略
3. 集成到 `ppt_filler.py`

### 阶段2：增强内容生成（后续）

**任务**：
1. 修改 `ppt_filler.py` 使用人类中心化分析结果
2. 实现逐板块内容生成
3. 优化LLM提示词模板

### 阶段3：格式和样式增强（后续）

**任务**：
1. 根据表达风格动态调整格式
2. 应用文化特征
3. 优化视觉层次

### 阶段4：支撑材料整合（后续）

**任务**：
1. 整合数据点
2. 整合案例
3. 生成图表（如果需要）

### 阶段5：质量检查和优化（后续）

**任务**：
1. 实现质量检查清单
2. 自动格式验证
3. 内容完整性检查

---

## 🎯 关键要点

### 1. 策略驱动

不是简单地填充占位符，而是：
- 根据分析结果制定策略
- 根据策略生成内容
- 根据表达风格调整格式

### 2. 人类友好

生成的内容要：
- 符合人类思维习惯
- 符合中国商业文化
- 有逻辑性和说服力

### 3. 风格一致

整个PPT要：
- 格式统一（Ant Design规范）
- 表达风格一致
- 视觉层次清晰

---

## 📊 当前状态

✅ **已完成**：
- 阶段1：框架内容分析（人类中心化）

⏳ **下一步**：
- 阶段2：内容生成策略制定

🔜 **后续**：
- 阶段3-6：内容生成、格式应用、材料整合、最终生成

