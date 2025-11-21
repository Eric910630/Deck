# 阶段5分析：支撑材料整合

## 📊 问题1：当前系统在这个板块做了什么，是怎么做的？

### 当前实现方式

#### 1.1 代码位置
- **文件**: `human_centered_analyzer.py`, `ppt_filler.py`
- **方法**: 
  - `_identify_supporting_materials()` - 识别支撑材料
  - `_generate_content_by_sections()` - 生成内容时包含数据点和案例
  - `_format_data_highlights()`, `_format_case_studies()` - 格式化数据点和案例

#### 1.2 当前流程

**步骤1：识别支撑材料**
```python
# human_centered_analyzer.py
def _identify_supporting_materials(self):
    materials = {
        "data_points": [],
        "charts": [],
        "tables": [],
        "cases": [],
        "quotes": []
    }
    
    # 简单正则提取数据
    data_matches = re.findall(r'\d+[%％]|\d+\.\d+%|\d+万|\d+亿', text)
    for data in data_matches:
        materials["data_points"].append({
            "slide_index": slide_idx,
            "data": data,
            "context": text[:50]
        })
    
    # 简单关键词匹配案例
    if any(kw in text for kw in ["案例", "例子", "客户", "项目"]):
        materials["cases"].append({
            "slide_index": slide_idx,
            "content": text[:100]
        })
```

**步骤2：在内容生成时包含支撑材料**
```python
# ppt_filler.py
def _generate_content_by_sections():
    # LLM生成内容时，会包含data_highlights和case_studies字段
    structured_content = {
        "title": "...",
        "main_content": "...",
        "key_points": [...],
        "data_highlights": ["数据1", "数据2"],  # 从LLM生成
        "case_studies": ["案例1", "案例2"]      # 从LLM生成
    }
    
    # 格式化数据点和案例
    if structured_content.get("data_highlights"):
        structured["data_formatted"] = self._format_data_highlights(
            structured_content["data_highlights"]
        )
    
    if structured_content.get("case_studies"):
        structured["cases_formatted"] = self._format_case_studies(
            structured_content["case_studies"]
        )
```

**步骤3：格式化支撑材料**
```python
def _format_data_highlights(self, data_highlights: List[str]) -> str:
    """格式化数据高亮"""
    formatted = []
    for data in data_highlights:
        formatted.append(f"• {data}")
    return "\n".join(formatted)

def _format_case_studies(self, case_studies: List[str]) -> str:
    """格式化案例研究"""
    formatted = []
    for case in case_studies:
        formatted.append(f"• {case}")
    return "\n".join(formatted)
```

#### 1.3 当前问题

**问题1：识别方式过于简单**
- ❌ 只使用正则表达式提取数据（`\d+[%％]`等）
- ❌ 只使用关键词匹配案例（"案例"、"例子"等）
- ❌ 没有理解数据的语义和上下文
- ❌ 没有识别数据之间的关系

**问题2：整合方式被动**
- ❌ 支撑材料只是被识别，但没有主动整合
- ❌ 数据点和案例依赖LLM生成，而不是从分析结果中提取
- ❌ 没有将识别的支撑材料传递给LLM，让LLM在生成内容时使用

**问题3：图表生成缺失**
- ❌ 虽然识别了数据点，但没有生成图表
- ❌ 没有判断哪些数据适合可视化
- ❌ 没有将图表插入到PPT中

**问题4：位置映射不准确**
- ❌ 支撑材料只记录了`slide_index`，但没有记录具体位置
- ❌ 没有将支撑材料映射到具体的占位符
- ❌ 没有考虑支撑材料在内容中的最佳位置

---

## 🎯 问题2：如果是你来做，阶段5你会怎么进行？

### 我的实现方案

#### 2.1 智能识别支撑材料

**步骤1：深度理解数据点**
```python
def _intelligently_identify_data_points(self, text: str, context: Dict) -> List[Dict]:
    """
    智能识别数据点，理解其语义和上下文
    
    返回格式：
    [
        {
            "value": "40-60%",
            "type": "percentage",  # percentage, number, ratio等
            "unit": "%",
            "label": "成本降低",
            "context": "降低运营成本40-60%",
            "significance": "high",  # high, medium, low
            "comparison": None,  # 如果有对比数据
            "trend": None  # 如果有趋势数据
        }
    ]
    """
    # 1. 使用LLM理解数据的语义
    # 2. 识别数据类型和单位
    # 3. 提取数据标签（如"成本降低"）
    # 4. 判断数据的重要性
    # 5. 识别数据之间的关系（对比、趋势等）
```

**步骤2：智能识别案例**
```python
def _intelligently_identify_cases(self, text: str, context: Dict) -> List[Dict]:
    """
    智能识别案例，理解其结构和价值
    
    返回格式：
    [
        {
            "type": "customer_case",  # customer_case, project_case, success_story等
            "company": "某直播公司",
            "industry": "直播",
            "challenge": "运营成本高",
            "solution": "使用AI解决方案",
            "result": "成本降低50%",
            "key_points": ["要点1", "要点2"],
            "significance": "high"
        }
    ]
    """
    # 1. 使用LLM识别案例类型
    # 2. 提取案例的关键信息（公司、行业、挑战、解决方案、结果）
    # 3. 提取案例的关键要点
    # 4. 判断案例的重要性
```

**步骤3：识别可可视化数据**
```python
def _identify_chartable_data(self, data_points: List[Dict]) -> List[Dict]:
    """
    识别可以可视化的数据
    
    返回格式：
    [
        {
            "chart_type": "bar",  # bar, line, pie, etc.
            "data": [...],
            "title": "成本降低对比",
            "x_axis": "时间/类别",
            "y_axis": "百分比",
            "recommended_position": "slide_2_bottom"
        }
    ]
    """
    # 1. 分析数据点之间的关系
    # 2. 判断适合的图表类型
    # 3. 准备图表数据
    # 4. 推荐图表位置
```

#### 2.2 主动整合支撑材料

**步骤1：将支撑材料传递给LLM**
```python
def _build_content_generation_prompt(
    self,
    section: Dict,
    strategy: Dict,
    supporting_materials: Dict  # 新增：支撑材料
) -> str:
    """
    构建内容生成提示词，包含支撑材料信息
    """
    prompt = f"""
    根据以下信息生成PPT内容：
    
    【板块主题】
    {section["theme"]}
    
    【核心思想】
    {section["core_idea"]}
    
    【可用数据点】
    {format_data_points(supporting_materials["data_points"])}
    
    【可用案例】
    {format_cases(supporting_materials["cases"])}
    
    【生成要求】
    1. 优先使用上述数据点和案例
    2. 如果数据点适合，在内容中突出显示
    3. 如果案例适合，在内容中引用
    4. 确保数据点和案例与核心思想相关
    """
    return prompt
```

**步骤2：智能插入支撑材料**
```python
def _intelligently_integrate_materials(
    self,
    content: str,
    supporting_materials: Dict,
    section: Dict
) -> str:
    """
    智能整合支撑材料到内容中
    
    策略：
    1. 数据点：优先插入到关键位置，突出显示
    2. 案例：插入到相关段落，作为佐证
    3. 图表：在合适位置插入图表引用
    """
    # 1. 分析内容结构
    # 2. 找到最适合插入数据点的位置
    # 3. 找到最适合插入案例的位置
    # 4. 格式化插入的支撑材料
    # 5. 确保逻辑连贯
```

#### 2.3 生成和插入图表

**步骤1：生成图表**
```python
def _generate_charts_for_section(
    self,
    section: Dict,
    supporting_materials: Dict
) -> List[Dict]:
    """
    为板块生成图表
    
    返回格式：
    [
        {
            "chart_type": "bar",
            "chart_path": "path/to/chart.png",
            "slide_index": 2,
            "position": {"x": 10, "y": 5, "width": 15, "height": 8},
            "title": "成本降低对比"
        }
    ]
    """
    # 1. 识别可可视化数据
    chartable_data = self._identify_chartable_data(
        supporting_materials["data_points"]
    )
    
    # 2. 为每个可可视化数据生成图表
    charts = []
    for chart_data in chartable_data:
        chart = self.chart_generator.generate_chart(
            chart_type=chart_data["chart_type"],
            data=chart_data["data"],
            title=chart_data["title"]
        )
        charts.append({
            "chart_path": chart,
            "slide_index": chart_data["slide_index"],
            "position": chart_data["recommended_position"]
        })
    
    return charts
```

**步骤2：插入图表到PPT**
```python
def _insert_charts_to_ppt(
    self,
    prs: Presentation,
    charts: List[Dict]
):
    """
    将图表插入到PPT中
    """
    for chart in charts:
        slide = prs.slides[chart["slide_index"]]
        
        # 插入图表图片
        slide.shapes.add_picture(
            chart["chart_path"],
            Cm(chart["position"]["x"]),
            Cm(chart["position"]["y"]),
            Cm(chart["position"]["width"]),
            Cm(chart["position"]["height"])
        )
```

#### 2.4 完整流程

```python
def integrate_supporting_materials(
    self,
    ppt: Presentation,
    human_analysis: Dict,
    content_map: Dict
) -> Presentation:
    """
    完整整合支撑材料
    
    流程：
    1. 从分析结果中提取支撑材料
    2. 智能识别和理解支撑材料
    3. 将支撑材料传递给内容生成
    4. 智能插入支撑材料到内容中
    5. 生成和插入图表
    6. 优化支撑材料的展示方式
    """
    # 1. 提取支撑材料
    supporting_materials = human_analysis["layer_4_supporting_materials"]["data"]
    
    # 2. 智能识别
    data_points = self._intelligently_identify_data_points(
        supporting_materials["materials"]["data_points"]
    )
    cases = self._intelligently_identify_cases(
        supporting_materials["materials"]["cases"]
    )
    
    # 3. 识别可可视化数据
    chartable_data = self._identify_chartable_data(data_points)
    
    # 4. 生成图表
    charts = []
    for chart_data in chartable_data:
        chart = self._generate_chart(chart_data)
        charts.append(chart)
    
    # 5. 插入图表到PPT
    self._insert_charts_to_ppt(ppt, charts)
    
    # 6. 优化数据点和案例的展示
    self._optimize_materials_display(ppt, data_points, cases)
    
    return ppt
```

---

## 🔍 问题3：你们俩的方案有什么区别？怎么改正？

### 对比分析

| 维度 | 当前系统 | 我的方案 | 改进方向 |
|------|---------|---------|---------|
| **识别方式** | 简单正则/关键词匹配 | LLM语义理解 | ✅ 使用LLM理解数据语义 |
| **数据理解** | 只提取数值 | 理解类型、单位、标签、重要性 | ✅ 深度理解数据 |
| **案例理解** | 只识别关键词 | 提取结构信息（公司、行业、挑战、解决方案、结果） | ✅ 结构化提取案例 |
| **整合方式** | 被动（依赖LLM生成） | 主动（从分析结果提取并传递给LLM） | ✅ 主动整合 |
| **图表生成** | ❌ 缺失 | ✅ 完整实现 | ✅ 实现图表生成和插入 |
| **位置映射** | 只记录slide_index | 记录具体位置和推荐位置 | ✅ 精确位置映射 |
| **展示优化** | 简单格式化 | 智能展示（突出重要数据、格式化案例） | ✅ 优化展示方式 |

### 改进方案

#### 改进1：增强支撑材料识别

**创建文件**: `supporting_materials_analyzer.py`

```python
class SupportingMaterialsAnalyzer:
    """
    支撑材料分析器
    使用LLM智能识别和理解支撑材料
    """
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    async def intelligently_identify_data_points(
        self,
        text: str,
        context: Dict
    ) -> List[Dict]:
        """
        智能识别数据点
        """
        prompt = f"""
        从以下文本中识别所有数据点，并理解其语义：
        
        文本：{text}
        上下文：{context}
        
        要求：
        1. 识别所有数据（百分比、数值、比率等）
        2. 理解数据的类型和单位
        3. 提取数据的标签（如"成本降低"）
        4. 判断数据的重要性（high/medium/low）
        5. 识别数据之间的关系（对比、趋势等）
        
        返回JSON格式：
        {{
            "data_points": [
                {{
                    "value": "40-60%",
                    "type": "percentage",
                    "unit": "%",
                    "label": "成本降低",
                    "context": "降低运营成本40-60%",
                    "significance": "high",
                    "comparison": null,
                    "trend": null
                }}
            ]
        }}
        """
        response = await self.llm_service.generate_content(prompt)
        return self._parse_data_points(response)
    
    async def intelligently_identify_cases(
        self,
        text: str,
        context: Dict
    ) -> List[Dict]:
        """
        智能识别案例
        """
        # 类似实现
        pass
```

#### 改进2：主动整合支撑材料

**修改文件**: `ppt_filler.py`

```python
async def _generate_content_by_sections(
    self,
    human_analysis: Dict,
    content_strategy: Dict,
    prompt: str
) -> Dict[str, str]:
    """
    逐板块生成内容，主动整合支撑材料
    """
    # 1. 提取支撑材料
    supporting_materials = human_analysis["layer_4_supporting_materials"]["data"]
    
    # 2. 智能识别支撑材料
    materials_analyzer = SupportingMaterialsAnalyzer(self.llm_service)
    data_points = await materials_analyzer.intelligently_identify_data_points(
        supporting_materials["materials"]["data_points"]
    )
    cases = await materials_analyzer.intelligently_identify_cases(
        supporting_materials["materials"]["cases"]
    )
    
    # 3. 为每个板块生成内容（包含支撑材料信息）
    content_map = {}
    sections = human_analysis["layer_2_sections"]["data"]["sections"]
    
    for section in sections:
        # 获取该板块相关的支撑材料
        section_data_points = [
            dp for dp in data_points 
            if dp["slide_index"] in section["slides"]
        ]
        section_cases = [
            c for c in cases 
            if c["slide_index"] in section["slides"]
        ]
        
        # 构建生成提示词（包含支撑材料）
        generation_prompt = self._build_content_generation_prompt(
            section=section,
            strategy=content_strategy,
            data_points=section_data_points,  # 新增
            cases=section_cases  # 新增
        )
        
        # 生成内容
        content = await self.llm_service.generate_content(generation_prompt)
        
        # 智能整合支撑材料
        integrated_content = self._intelligently_integrate_materials(
            content=content,
            data_points=section_data_points,
            cases=section_cases
        )
        
        content_map.update(integrated_content)
    
    return content_map
```

#### 改进3：实现图表生成和插入

**创建文件**: `chart_integrator.py`

```python
class ChartIntegrator:
    """
    图表整合器
    识别可可视化数据，生成图表，并插入到PPT
    """
    
    def __init__(self, chart_generator: ChartGenerator):
        self.chart_generator = chart_generator
    
    async def identify_chartable_data(
        self,
        data_points: List[Dict]
    ) -> List[Dict]:
        """
        识别可以可视化的数据
        """
        # 使用LLM判断哪些数据适合可视化
        prompt = f"""
        分析以下数据点，判断哪些适合生成图表：
        
        数据点：{json.dumps(data_points, ensure_ascii=False)}
        
        要求：
        1. 识别适合可视化的数据（有对比、有趋势、有分类等）
        2. 推荐图表类型（bar, line, pie等）
        3. 准备图表数据
        4. 推荐图表位置
        
        返回JSON格式：
        {{
            "chartable_data": [
                {{
                    "chart_type": "bar",
                    "data": [...],
                    "title": "成本降低对比",
                    "slide_index": 2,
                    "recommended_position": {{"x": 10, "y": 5, "width": 15, "height": 8}}
                }}
            ]
        }}
        """
        # 调用LLM
        pass
    
    def generate_and_insert_charts(
        self,
        ppt: Presentation,
        chartable_data: List[Dict]
    ):
        """
        生成图表并插入到PPT
        """
        for chart_data in chartable_data:
            # 生成图表
            chart_path = self.chart_generator.generate_chart(
                chart_type=chart_data["chart_type"],
                data=chart_data["data"],
                title=chart_data["title"]
            )
            
            # 插入到PPT
            slide = ppt.slides[chart_data["slide_index"]]
            slide.shapes.add_picture(
                chart_path,
                Cm(chart_data["recommended_position"]["x"]),
                Cm(chart_data["recommended_position"]["y"]),
                Cm(chart_data["recommended_position"]["width"]),
                Cm(chart_data["recommended_position"]["height"])
            )
```

#### 改进4：优化支撑材料展示

**修改文件**: `html_generator.py`

```python
def _format_data_highlight(self, data_point: Dict) -> str:
    """
    格式化数据高亮（根据重要性）
    """
    if data_point["significance"] == "high":
        # 重要数据：大字号、加粗、突出颜色
        return f"""
        <div class="data-highlight-important">
            <span class="data-value">{data_point["value"]}</span>
            <span class="data-label">{data_point["label"]}</span>
        </div>
        """
    else:
        # 普通数据：标准格式
        return f"""
        <div class="data-highlight">
            <span class="data-value">{data_point["value"]}</span>
            <span class="data-label">{data_point["label"]}</span>
        </div>
        """

def _format_case_study(self, case: Dict) -> str:
    """
    格式化案例研究（结构化展示）
    """
    return f"""
    <div class="case-study">
        <div class="case-header">
            <span class="case-company">{case["company"]}</span>
            <span class="case-industry">{case["industry"]}</span>
        </div>
        <div class="case-content">
            <p><strong>挑战：</strong>{case["challenge"]}</p>
            <p><strong>解决方案：</strong>{case["solution"]}</p>
            <p><strong>结果：</strong>{case["result"]}</p>
        </div>
        <ul class="case-key-points">
            {''.join([f'<li>{point}</li>' for point in case["key_points"]])}
        </ul>
    </div>
    """
```

---

## 📋 实施计划

### 阶段1：增强支撑材料识别
1. 创建 `supporting_materials_analyzer.py`
2. 实现智能识别数据点和案例
3. 集成到 `human_centered_analyzer.py`

### 阶段2：主动整合支撑材料
1. 修改 `ppt_filler.py` 的 `_generate_content_by_sections`
2. 将支撑材料传递给LLM
3. 实现智能整合逻辑

### 阶段3：实现图表生成和插入
1. 创建 `chart_integrator.py`
2. 实现图表识别和生成
3. 实现图表插入到PPT

### 阶段4：优化展示方式
1. 修改 `html_generator.py` 的格式化方法
2. 根据重要性优化数据展示
3. 结构化展示案例

---

## ✅ 总结

**当前系统的问题**：
- ❌ 识别方式过于简单
- ❌ 整合方式被动
- ❌ 图表生成缺失
- ❌ 位置映射不准确

**改进方向**：
- ✅ 使用LLM智能识别和理解支撑材料
- ✅ 主动整合支撑材料到内容生成流程
- ✅ 实现图表生成和插入
- ✅ 优化支撑材料的展示方式

