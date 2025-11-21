# 阶段3分析：逐板块内容生成

## 📊 问题1：当前系统在这个板块做了什么，是怎么做的？

### 当前实现方式

#### 1.1 代码位置
- **文件**: `ppt_filler.py`
- **方法**: `_generate_content_for_framework()`
- **调用链**: `fill_from_prompt()` → `_generate_content_for_framework()` → LLM生成

#### 1.2 当前流程

```python
async def _generate_content_for_framework(
    self,
    prompt: str,
    structure: Dict[str, Any],
    text_summary: str,
    placeholder_mapping: Dict[int, List[Dict[str, Any]]]
) -> Dict[str, str]:
    """为框架生成内容"""
    
    # 1. 构建系统提示词（固定模板）
    system_prompt = """你是一个专业的PPT内容创作助手...
    要求：
    1. 理解PPT框架的结构和现有内容
    2. 根据用户需求生成专业、相关的内容
    3. 为每个占位符生成合适的内容
    ...
    """
    
    # 2. 构建用户提示词（简单拼接）
    user_prompt = f"""PPT框架信息：
    {text_summary}
    
    用户需求：{prompt}
    
    请为每张幻灯片的占位符生成合适的内容..."""
    
    # 3. 一次性调用LLM生成所有内容
    response = await self.llm_service.generate_content(
        system_prompt=system_prompt,
        user_prompt=user_prompt
    )
    
    # 4. 解析JSON响应
    content_map = self._parse_content_map(response)
    
    return content_map
```

#### 1.3 当前特点

**优点**：
- ✅ 简单直接，一次调用生成所有内容
- ✅ 代码简洁，易于维护
- ✅ 快速（单次LLM调用）

**问题**：
- ❌ **没有使用人类中心化分析结果**
  - 不知道核心主题、价值主张
  - 不知道板块结构
  - 不知道论证逻辑
  
- ❌ **没有使用内容生成策略**
  - 不知道每个板块应该强调什么
  - 不知道证据优先级
  - 不知道生成长度要求
  
- ❌ **提示词过于简单**
  - 只是简单拼接框架信息和用户需求
  - 没有考虑表达风格
  - 没有考虑文化特征
  
- ❌ **一次性生成所有内容**
  - 无法针对不同板块采用不同策略
  - 无法根据板块特点调整生成方式
  - 无法处理板块之间的逻辑关系

#### 1.4 当前输出示例

```json
{
  "slide_0_placeholder_0": "人工智能技术概述",
  "slide_0_placeholder_1": "人工智能（AI）是计算机科学的重要分支...",
  "slide_1_placeholder_0": "人工智能核心技术介绍",
  "slide_1_placeholder_1": "• 机器学习：通过算法让计算机从数据中学习规律..."
}
```

**特点**：
- 简单的标题+正文结构
- 没有考虑板块之间的逻辑关系
- 没有突出价值主张
- 没有根据论证类型调整内容

---

## 🎯 问题2：如果是你来做，会做成什么样子？

### 改进方案设计

#### 2.1 整体思路

**核心转变**：
- 从"一次性生成所有内容" → "逐板块策略化生成"
- 从"简单提示词" → "基于分析的智能提示词"
- 从"无策略" → "基于策略的内容生成"

#### 2.2 改进后的流程

```python
async def generate_content_by_sections(
    self,
    human_analysis: Dict[str, Any],
    content_strategy: Dict[str, Any],
    user_prompt: str
) -> Dict[str, str]:
    """逐板块生成内容"""
    
    content_map = {}
    section_strategies = content_strategy["section_strategies"]
    
    # 为每个板块生成内容
    for section_strategy in section_strategies:
        # 1. 构建板块特定的生成提示词
        section_prompt = self._build_section_prompt(
            section_strategy=section_strategy,
            overall_strategy=content_strategy["overall_strategy"],
            expression_strategy=content_strategy["expression_strategy"],
            user_prompt=user_prompt,
            human_analysis=human_analysis
        )
        
        # 2. 调用LLM生成板块内容
        section_content = await self._generate_section_content(section_prompt)
        
        # 3. 结构化板块内容
        structured_content = self._structure_section_content(
            section_content,
            section_strategy
        )
        
        # 4. 映射到PPT占位符
        section_content_map = self._map_to_placeholders(
            structured_content,
            section_strategy["slides"],
            human_analysis
        )
        
        # 5. 合并到总内容映射
        content_map.update(section_content_map)
    
    return content_map
```

#### 2.3 智能提示词构建

```python
def _build_section_prompt(
    self,
    section_strategy: Dict,
    overall_strategy: Dict,
    expression_strategy: Dict,
    user_prompt: str,
    human_analysis: Dict
) -> str:
    """构建板块特定的生成提示词"""
    
    # 获取板块相关信息
    section_analysis = self._get_section_analysis(
        section_strategy["section_index"],
        human_analysis
    )
    
    prompt = f"""
【整体背景】
核心主题：{overall_strategy["core_theme"]}
价值主张：{", ".join(overall_strategy["value_propositions"])}
目标受众：{overall_strategy["target_audience"]}
文档目的：{overall_strategy["purpose"]}

【当前板块】
板块主题：{section_strategy["theme"]}
核心思想：{section_strategy["core_idea"]}
板块位置：第{section_strategy["section_index"] + 1}个板块（共{len(section_strategies)}个）

【论证逻辑】
论证方式：{", ".join(section_strategy["argument_types"])}
证据点：
{self._format_evidence_points(section_strategy["evidence_points"])}

【生成策略】
强调重点：{section_strategy["content_generation_approach"]["emphasis"]}
证据优先级：{", ".join(section_strategy["content_generation_approach"]["evidence_priority"])}
内容长度：{section_strategy["content_generation_approach"]["length"]}

【表达风格】
正式程度：{expression_strategy["language_style"]["formality"]}
语调：{expression_strategy["language_style"]["tone"]}
文化特征：{", ".join(expression_strategy["language_style"]["cultural_features"])}

【板块上下文】
前一个板块：{self._get_previous_section_theme(section_strategy)}
后一个板块：{self._get_next_section_theme(section_strategy)}

【用户需求】
{user_prompt}

【生成要求】
1. 标题：简洁有力，体现核心思想，不超过20字
2. 正文：根据"强调重点"和"证据优先级"组织内容
3. 数据：如果有数据论证，突出显示数据（如"降低40-60%成本"）
4. 案例：如果有案例论证，简洁说明案例
5. 逻辑：与前一个板块有逻辑衔接，为后一个板块做铺垫
6. 风格：符合{expression_strategy["language_style"]["formality"]}风格，语调{expression_strategy["language_style"]["tone"]}
7. 文化：体现{", ".join(expression_strategy["language_style"]["cultural_features"])}

请生成该板块的内容（JSON格式）：
{{
  "title": "标题",
  "content": "正文内容",
  "key_points": ["要点1", "要点2", ...],
  "data_highlights": ["数据1", "数据2", ...],
  "case_studies": ["案例1", "案例2", ...]
}}
"""
    return prompt
```

#### 2.4 结构化内容处理

```python
def _structure_section_content(
    self,
    section_content: Dict,
    section_strategy: Dict
) -> Dict[str, Any]:
    """结构化板块内容"""
    
    structured = {
        "title": section_content.get("title", ""),
        "main_content": section_content.get("content", ""),
        "key_points": section_content.get("key_points", []),
        "data_highlights": section_content.get("data_highlights", []),
        "case_studies": section_content.get("case_studies", []),
        "section_index": section_strategy["section_index"],
        "slides": section_strategy["slides"]
    }
    
    # 根据论证类型调整结构
    if "数据论证" in section_strategy["argument_types"]:
        # 突出数据
        structured["emphasis"] = "data"
        structured["data_formatted"] = self._format_data_highlights(
            structured["data_highlights"]
        )
    
    if "案例论证" in section_strategy["argument_types"]:
        # 突出案例
        structured["emphasis"] = "case"
        structured["cases_formatted"] = self._format_case_studies(
            structured["case_studies"]
        )
    
    return structured
```

#### 2.5 智能占位符映射

```python
def _map_to_placeholders(
    self,
    structured_content: Dict,
    slide_indices: List[int],
    human_analysis: Dict
) -> Dict[str, str]:
    """智能映射到PPT占位符"""
    
    content_map = {}
    
    for slide_idx in slide_indices:
        # 获取该幻灯片的占位符信息
        slide_placeholders = self._get_slide_placeholders(slide_idx, human_analysis)
        
        # 根据占位符类型分配内容
        for placeholder in slide_placeholders:
            placeholder_key = f"slide_{slide_idx}_placeholder_{placeholder['id']}"
            placeholder_type = placeholder.get("type", "")
            
            if "TITLE" in placeholder_type or "CENTER_TITLE" in placeholder_type:
                # 标题占位符
                content_map[placeholder_key] = structured_content["title"]
            elif "OBJECT" in placeholder_type or "BODY" in placeholder_type:
                # 正文占位符
                content = self._build_body_content(
                    structured_content,
                    placeholder_type
                )
                content_map[placeholder_key] = content
            else:
                # 其他占位符
                content_map[placeholder_key] = structured_content["main_content"]
    
    return content_map

def _build_body_content(
    self,
    structured_content: Dict,
    placeholder_type: str
) -> str:
    """构建正文内容"""
    
    parts = []
    
    # 1. 主要内容
    if structured_content["main_content"]:
        parts.append(structured_content["main_content"])
    
    # 2. 关键要点（如果是列表占位符）
    if "OBJECT" in placeholder_type and structured_content["key_points"]:
        parts.append("\n\n关键要点：")
        for point in structured_content["key_points"]:
            parts.append(f"• {point}")
    
    # 3. 数据高亮（如果有）
    if structured_content.get("data_formatted"):
        parts.append("\n\n数据支撑：")
        parts.append(structured_content["data_formatted"])
    
    # 4. 案例说明（如果有）
    if structured_content.get("cases_formatted"):
        parts.append("\n\n案例说明：")
        parts.append(structured_content["cases_formatted"])
    
    return "\n".join(parts)
```

#### 2.6 改进后的输出示例

```json
{
  "slide_0_placeholder_0": "技术产品商业化-文档",
  "slide_0_placeholder_1": "全链路AI赋能解决方案\n\n核心价值主张：\n• 降低运营成本40-60%\n• 提升转化效率20-35%\n• 加速业务智能化转型",
  "slide_1_placeholder_0": "25年技术简单回顾",
  "slide_1_placeholder_1": "回顾技术发展历程，展示技术积累和成果\n\n关键要点：\n• 朋友云做了多少需求、工时、系统\n• AI做了哪些（包括智能体）？业务反馈价值\n• 数据中心\n\n数据支撑：\n• 累计完成需求：XXX个\n• 累计工时：XXX小时"
}
```

**特点**：
- ✅ 考虑了板块之间的逻辑关系
- ✅ 突出了价值主张
- ✅ 根据论证类型调整内容结构
- ✅ 包含了数据支撑和案例说明

---

## 🔍 问题3：对比两个方案的产出物，差距在哪里？如何提升？

### 3.1 对比分析

| 维度 | 当前系统 | 改进方案 | 差距 |
|------|---------|---------|------|
| **分析结果使用** | ❌ 未使用 | ✅ 使用人类中心化分析 | **巨大差距** |
| **策略驱动** | ❌ 无策略 | ✅ 基于内容生成策略 | **巨大差距** |
| **提示词质量** | ⚠️ 简单拼接 | ✅ 智能构建，包含上下文 | **显著差距** |
| **生成方式** | ⚠️ 一次性生成 | ✅ 逐板块生成 | **显著差距** |
| **内容结构** | ⚠️ 简单标题+正文 | ✅ 结构化（要点、数据、案例） | **显著差距** |
| **逻辑关系** | ❌ 无考虑 | ✅ 考虑板块间逻辑 | **巨大差距** |
| **表达风格** | ❌ 无考虑 | ✅ 根据风格调整 | **巨大差距** |
| **文化特征** | ❌ 无考虑 | ✅ 体现文化特征 | **巨大差距** |

### 3.2 具体差距

#### 差距1：分析结果使用

**当前系统**：
```python
# 只使用简单的文本摘要
text_summary = self.parser.extract_text_summary()
user_prompt = f"PPT框架信息：{text_summary}\n用户需求：{prompt}"
```

**改进方案**：
```python
# 使用完整的6层分析结果
human_analysis = analyzer.analyze_all()
content_strategy = strategy_gen.generate_strategy()

# 在提示词中使用分析结果
prompt = f"""
核心主题：{overall_strategy["core_theme"]}
价值主张：{", ".join(overall_strategy["value_propositions"])}
论证方式：{", ".join(section_strategy["argument_types"])}
...
"""
```

**差距**：当前系统**完全忽略**了人类中心化分析结果，改进方案**充分利用**了所有分析信息。

#### 差距2：策略驱动

**当前系统**：
```python
# 无策略，所有板块使用相同方式生成
system_prompt = "你是一个专业的PPT内容创作助手..."
# 所有占位符使用相同的生成逻辑
```

**改进方案**：
```python
# 每个板块有独立的生成策略
for section_strategy in section_strategies:
    # 根据板块特点调整生成方式
    emphasis = section_strategy["content_generation_approach"]["emphasis"]
    evidence_priority = section_strategy["content_generation_approach"]["evidence_priority"]
    length = section_strategy["content_generation_approach"]["length"]
    
    # 根据策略生成内容
    prompt = build_section_prompt(section_strategy, ...)
```

**差距**：当前系统**无差异化**，改进方案**策略化、个性化**。

#### 差距3：提示词质量

**当前系统提示词**：
```
PPT框架信息：
PPT框架文档包含 3 张幻灯片。

幻灯片 1:
  内容: 人工智能技术概述 | 探索AI技术的核心原理...
  占位符数量: 2

用户需求：制作一个关于人工智能技术的演示文稿

请为每张幻灯片的占位符生成合适的内容。
```

**改进方案提示词**：
```
【整体背景】
核心主题：技术产品商业化
价值主张：降低运营成本40-60%, 提升转化效率20-35%
目标受众：管理层
文档目的：汇报

【当前板块】
板块主题：技术产品商业化-文档
核心思想：全链路AI赋能解决方案
板块位置：第1个板块（共4个）

【论证逻辑】
论证方式：数据论证, 案例论证
证据点：
1. 数据: 40-60%
2. 数据: 20-35%
3. 要点: 降低运营成本

【生成策略】
强调重点：数据支撑
证据优先级：数据, 图表
内容长度：medium

【表达风格】
正式程度：中性
语调：积极
文化特征：强调价值导向, 数据驱动表达

【板块上下文】
前一个板块：无
后一个板块：25年技术简单回顾

【生成要求】
1. 标题：简洁有力，体现核心思想，不超过20字
2. 正文：根据"强调重点"和"证据优先级"组织内容
3. 数据：如果有数据论证，突出显示数据
4. 逻辑：与前一个板块有逻辑衔接，为后一个板块做铺垫
5. 风格：符合中性风格，语调积极
6. 文化：体现强调价值导向, 数据驱动表达
```

**差距**：
- 当前：**信息量少**（只有框架信息和用户需求）
- 改进：**信息丰富**（包含主题、价值主张、论证逻辑、策略、风格、上下文等）

#### 差距4：内容结构

**当前系统输出**：
```json
{
  "slide_0_placeholder_0": "人工智能技术概述",
  "slide_0_placeholder_1": "人工智能（AI）是计算机科学的重要分支..."
}
```
- 简单的标题+正文
- 没有结构化
- 没有突出重点

**改进方案输出**：
```json
{
  "title": "技术产品商业化-文档",
  "content": "全链路AI赋能解决方案",
  "key_points": ["降低运营成本40-60%", "提升转化效率20-35%"],
  "data_highlights": ["40-60%", "20-35%"],
  "case_studies": ["客户案例1", "客户案例2"]
}
```
- 结构化内容（标题、正文、要点、数据、案例）
- 根据论证类型突出不同内容
- 便于后续格式化和展示

**差距**：当前系统**扁平化**，改进方案**结构化、层次化**。

### 3.3 提升方案

#### 提升1：集成人类中心化分析

**实施步骤**：
1. 修改 `ppt_filler.py` 的 `__init__` 方法，接受人类中心化分析结果
2. 在 `fill_from_prompt` 中先进行人类中心化分析
3. 将分析结果传递给内容生成方法

**代码示例**：
```python
async def fill_from_prompt(
    self,
    prompt: str,
    output_path: Optional[str] = None,
    preserve_structure: bool = True
) -> str:
    # 1. 提取增强结构
    enhanced_parser = EnhancedPPTParser(self.framework_path)
    structure = enhanced_parser.extract_structure_enhanced()
    
    # 2. 人类中心化分析
    analyzer = HumanCenteredAnalyzer(structure)
    human_analysis = analyzer.analyze_all()
    
    # 3. 生成内容策略
    strategy_gen = ContentStrategyGenerator(human_analysis)
    content_strategy = strategy_gen.generate_strategy()
    
    # 4. 使用分析结果和策略生成内容
    content_map = await self._generate_content_by_sections(
        human_analysis=human_analysis,
        content_strategy=content_strategy,
        user_prompt=prompt
    )
    
    # 5. 填充PPT
    self._fill_ppt(content_map, output_path, preserve_structure)
```

#### 提升2：实现逐板块生成

**实施步骤**：
1. 创建 `_generate_content_by_sections` 方法
2. 实现 `_build_section_prompt` 方法
3. 实现 `_structure_section_content` 方法
4. 实现 `_map_to_placeholders` 方法

**关键代码**：
```python
async def _generate_content_by_sections(
    self,
    human_analysis: Dict[str, Any],
    content_strategy: Dict[str, Any],
    user_prompt: str
) -> Dict[str, str]:
    """逐板块生成内容"""
    content_map = {}
    section_strategies = content_strategy["section_strategies"]
    
    for section_strategy in section_strategies:
        # 构建板块提示词
        section_prompt = self._build_section_prompt(
            section_strategy, content_strategy, user_prompt, human_analysis
        )
        
        # 生成板块内容
        section_content = await self._generate_section_content(section_prompt)
        
        # 结构化并映射
        structured = self._structure_section_content(section_content, section_strategy)
        section_map = self._map_to_placeholders(
            structured, section_strategy["slides"], human_analysis
        )
        
        content_map.update(section_map)
    
    return content_map
```

#### 提升3：优化提示词构建

**实施步骤**：
1. 实现 `_build_section_prompt` 方法
2. 包含所有分析结果和策略信息
3. 添加板块上下文信息
4. 明确生成要求

**关键改进**：
- 使用 `ContentStrategyGenerator.build_generation_prompt()` 方法
- 添加板块上下文（前一个、后一个板块）
- 明确表达风格要求
- 明确文化特征要求

#### 提升4：结构化内容处理

**实施步骤**：
1. 实现 `_structure_section_content` 方法
2. 根据论证类型调整结构
3. 格式化数据高亮
4. 格式化案例说明

**关键改进**：
- 区分标题、正文、要点、数据、案例
- 根据论证类型突出不同内容
- 格式化数据（如"40-60%" → "降低运营成本40-60%"）
- 格式化案例（如"客户案例1" → "案例：某客户通过...实现..."）

---

## 📊 总结

### 核心差距

1. **分析结果使用**：当前系统**完全忽略**，改进方案**充分利用**
2. **策略驱动**：当前系统**无策略**，改进方案**策略化**
3. **提示词质量**：当前系统**简单**，改进方案**智能、丰富**
4. **生成方式**：当前系统**一次性**，改进方案**逐板块**
5. **内容结构**：当前系统**扁平**，改进方案**结构化**

### 提升优先级

1. **高优先级**：集成人类中心化分析（必须）
2. **高优先级**：实现逐板块生成（必须）
3. **中优先级**：优化提示词构建（重要）
4. **中优先级**：结构化内容处理（重要）

### 预期效果

实施改进后：
- ✅ 内容质量提升（更符合人类思维）
- ✅ 逻辑性增强（板块间有逻辑关系）
- ✅ 个性化提升（每个板块有针对性）
- ✅ 文化适应性提升（符合中国商业文化）

