"""
支撑材料分析器
使用LLM智能识别和理解支撑材料（数据点、案例等）
"""

from typing import List, Dict, Any, Optional
from loguru import logger
import json
import re

from llm_service import LLMService, create_llm_service


class SupportingMaterialsAnalyzer:
    """
    支撑材料分析器
    使用LLM智能识别和理解支撑材料
    """
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        初始化支撑材料分析器
        
        Args:
            llm_service: LLM服务实例
        """
        self.llm_service = llm_service or create_llm_service()
        logger.info("--- [SupportingMaterialsAnalyzer]: 初始化支撑材料分析器")
    
    async def intelligently_identify_data_points(
        self,
        materials: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        智能识别数据点，理解其语义和上下文
        
        Args:
            materials: 从human_centered_analyzer提取的原始材料列表
            
        Returns:
            智能识别后的数据点列表
        """
        if not materials:
            return []
        
        logger.info(f"--- [SupportingMaterialsAnalyzer]: 开始智能识别{len(materials)}个数据点")
        
        # 收集所有数据点的文本和上下文
        data_texts = []
        for material in materials:
            data_texts.append({
                "data": material.get("data", ""),
                "context": material.get("context", ""),
                "slide_index": material.get("slide_index", 0)
            })
        
        # 构建LLM提示词
        prompt = f"""
你是一个专业的数据分析专家。请从以下数据点中提取和理解每个数据的完整信息。

数据点列表：
{json.dumps(data_texts, ensure_ascii=False, indent=2)}

要求：
1. 识别每个数据的类型（percentage百分比、number数值、ratio比率、range范围等）
2. 提取数据的单位（%、万、亿、元等）
3. 从上下文中提取数据的标签（如"成本降低"、"效率提升"等）
4. 判断数据的重要性（high/medium/low）
5. 识别数据之间的关系（如果有对比数据或趋势数据）
6. 提取数据的完整上下文

返回JSON格式：
{{
    "data_points": [
        {{
            "value": "40-60%",
            "type": "percentage_range",
            "unit": "%",
            "label": "成本降低",
            "context": "降低运营成本40-60%",
            "significance": "high",
            "comparison": null,
            "trend": null,
            "slide_index": 0
        }}
    ]
}}

只返回JSON，不要其他内容。
"""
        
        try:
            messages = [
                {"role": "system", "content": "你是一个专业的数据分析专家，擅长理解和提取数据的语义信息。"},
                {"role": "user", "content": prompt}
            ]
            response = await self.llm_service.chat_completion_async(messages=messages)
            
            # 解析JSON响应
            result = self._parse_json_response(response)
            data_points = result.get("data_points", [])
            
            logger.info(f"--- [SupportingMaterialsAnalyzer]: 成功识别{len(data_points)}个数据点")
            return data_points
            
        except Exception as e:
            logger.warning(f"--- [SupportingMaterialsAnalyzer]: LLM识别失败，使用基础识别: {e}")
            # Fallback到基础识别
            return self._basic_identify_data_points(materials)
    
    async def intelligently_identify_cases(
        self,
        materials: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        智能识别案例，理解其结构和价值
        
        Args:
            materials: 从human_centered_analyzer提取的原始材料列表
            
        Returns:
            智能识别后的案例列表
        """
        if not materials:
            return []
        
        logger.info(f"--- [SupportingMaterialsAnalyzer]: 开始智能识别{len(materials)}个案例")
        
        # 收集所有案例的文本和上下文
        case_texts = []
        for material in materials:
            case_texts.append({
                "content": material.get("content", ""),
                "slide_index": material.get("slide_index", 0)
            })
        
        # 构建LLM提示词
        prompt = f"""
你是一个专业的案例分析专家。请从以下案例文本中提取结构化信息。

案例列表：
{json.dumps(case_texts, ensure_ascii=False, indent=2)}

要求：
1. 识别案例类型（customer_case客户案例、project_case项目案例、success_story成功故事等）
2. 提取案例的关键信息：
   - 公司/组织名称（如果有）
   - 行业（如果有）
   - 挑战/问题（如果有）
   - 解决方案（如果有）
   - 结果/效果（如果有）
3. 提取案例的关键要点（3-5个）
4. 判断案例的重要性（high/medium/low）

返回JSON格式：
{{
    "cases": [
        {{
            "type": "customer_case",
            "company": "某直播公司",
            "industry": "直播",
            "challenge": "运营成本高",
            "solution": "使用AI解决方案",
            "result": "成本降低50%",
            "key_points": ["要点1", "要点2", "要点3"],
            "significance": "high",
            "slide_index": 0
        }}
    ]
}}

只返回JSON，不要其他内容。
"""
        
        try:
            messages = [
                {"role": "system", "content": "你是一个专业的案例分析专家，擅长提取和结构化案例信息。"},
                {"role": "user", "content": prompt}
            ]
            response = await self.llm_service.chat_completion_async(messages=messages)
            
            # 解析JSON响应
            result = self._parse_json_response(response)
            cases = result.get("cases", [])
            
            logger.info(f"--- [SupportingMaterialsAnalyzer]: 成功识别{len(cases)}个案例")
            return cases
            
        except Exception as e:
            logger.warning(f"--- [SupportingMaterialsAnalyzer]: LLM识别失败，使用基础识别: {e}")
            # Fallback到基础识别
            return self._basic_identify_cases(materials)
    
    async def identify_chartable_data(
        self,
        data_points: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        识别可以可视化的数据
        
        Args:
            data_points: 智能识别后的数据点列表
            
        Returns:
            可可视化的数据列表
        """
        if not data_points:
            return []
        
        logger.info(f"--- [SupportingMaterialsAnalyzer]: 开始识别可可视化数据")
        
        # 构建LLM提示词
        prompt = f"""
你是一个专业的数据可视化专家。请分析以下数据点，判断哪些适合生成图表。

数据点列表：
{json.dumps(data_points, ensure_ascii=False, indent=2)}

要求：
1. 识别适合可视化的数据（有对比、有趋势、有分类、有分布等）
2. 推荐图表类型（bar柱状图、line折线图、pie饼图、area面积图等）
3. 准备图表数据（结构化数据）
4. 推荐图表位置（slide_index和位置信息）

判断标准：
- 有多个数据点可以对比 → 柱状图
- 有时间序列数据 → 折线图
- 有比例关系 → 饼图
- 有分布数据 → 面积图

返回JSON格式：
{{
    "chartable_data": [
        {{
            "chart_type": "bar",
            "data": [
                {{"label": "成本降低", "value": 50}},
                {{"label": "效率提升", "value": 30}}
            ],
            "title": "成本降低和效率提升对比",
            "x_axis": "指标",
            "y_axis": "百分比(%)",
            "slide_index": 2,
            "recommended_position": {{
                "x": 10,
                "y": 5,
                "width": 15,
                "height": 8
            }}
        }}
    ]
}}

只返回JSON，不要其他内容。如果没有适合可视化的数据，返回空的chartable_data数组。
"""
        
        try:
            messages = [
                {"role": "system", "content": "你是一个专业的数据可视化专家，擅长判断数据是否适合可视化并推荐图表类型。"},
                {"role": "user", "content": prompt}
            ]
            response = await self.llm_service.chat_completion_async(messages=messages)
            
            # 解析JSON响应
            result = self._parse_json_response(response)
            chartable_data = result.get("chartable_data", [])
            
            logger.info(f"--- [SupportingMaterialsAnalyzer]: 识别出{len(chartable_data)}个可可视化数据")
            return chartable_data
            
        except Exception as e:
            logger.warning(f"--- [SupportingMaterialsAnalyzer]: LLM识别失败: {e}")
            return []
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        解析LLM的JSON响应
        
        Args:
            response: LLM响应文本
            
        Returns:
            解析后的JSON字典
        """
        try:
            # 尝试直接解析JSON
            return json.loads(response)
        except json.JSONDecodeError:
            # 尝试提取JSON部分
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                logger.error(f"--- [SupportingMaterialsAnalyzer]: 无法解析JSON响应: {response[:200]}")
                return {}
    
    def _basic_identify_data_points(
        self,
        materials: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        基础识别数据点（Fallback方法）
        
        Args:
            materials: 原始材料列表
            
        Returns:
            基础识别的数据点列表
        """
        data_points = []
        for material in materials:
            data = material.get("data", "")
            # 简单判断类型
            if "%" in data or "％" in data:
                data_type = "percentage"
                unit = "%"
            elif "万" in data:
                data_type = "number"
                unit = "万"
            elif "亿" in data:
                data_type = "number"
                unit = "亿"
            else:
                data_type = "number"
                unit = ""
            
            data_points.append({
                "value": data,
                "type": data_type,
                "unit": unit,
                "label": "",
                "context": material.get("context", ""),
                "significance": "medium",
                "comparison": None,
                "trend": None,
                "slide_index": material.get("slide_index", 0)
            })
        
        return data_points
    
    def _basic_identify_cases(
        self,
        materials: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        基础识别案例（Fallback方法）
        
        Args:
            materials: 原始材料列表
            
        Returns:
            基础识别的案例列表
        """
        cases = []
        for material in materials:
            cases.append({
                "type": "case",
                "company": "",
                "industry": "",
                "challenge": "",
                "solution": "",
                "result": "",
                "key_points": [],
                "significance": "medium",
                "slide_index": material.get("slide_index", 0),
                "content": material.get("content", "")
            })
        
        return cases

