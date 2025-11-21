"""
人类中心化分析器
按照人类理解文档的真实流程进行分析：
1. 通读理解 - 理解整体思想和含义
2. 板块拆分 - 识别各个板块及其核心思想
3. 论证逻辑 - 识别支撑核心思想的论据
4. 支撑材料 - 数据、图表等佐证材料
5. 表达风格 - 语言风格、文化特征
6. 呈现形式 - 格式、布局、视觉呈现
"""

from typing import List, Dict, Any, Optional
from loguru import logger
import re
import json
from collections import defaultdict
from ..core.llm_service import LLMService


class HumanCenteredAnalyzer:
    """
    人类中心化分析器
    按照人类理解文档的真实流程进行分析
    """
    
    def __init__(self, structure_data: Dict[str, Any], raw_text: str = "", llm_service: Optional[LLMService] = None):
        """
        初始化分析器
        
        Args:
            structure_data: 增强的结构数据（包含格式信息）
            raw_text: 原始文本内容（用于整体理解）
            llm_service: LLM服务实例（用于理解文档内容）
        """
        self.structure = structure_data
        self.raw_text = raw_text
        self.llm_service = llm_service or LLMService()
        logger.info("--- [HumanCenteredAnalyzer]: 初始化人类中心化分析器（使用LLM理解）")
    
    async def analyze_all(self) -> Dict[str, Any]:
        """
        执行完整的人类中心化分析
        
        Returns:
            包含6个理解层次的完整分析结果
        """
        logger.info("="*80)
        logger.info("--- [HumanCenteredAnalyzer]: 开始人类中心化分析（使用LLM）")
        logger.info("="*80)
        
        # 第1层：通读理解 - 理解整体思想和含义
        logger.info("--- [第1层] 通读理解：理解整体思想和含义...")
        overall_understanding = await self._understand_overall()
        
        # 第2层：板块拆分 - 识别各个板块及其核心思想
        logger.info("--- [第2层] 板块拆分：识别各个板块及其核心思想...")
        sections = await self._identify_sections()
        
        # 第3层：论证逻辑 - 识别支撑核心思想的论据
        logger.info("--- [第3层] 论证逻辑：识别支撑核心思想的论据...")
        arguments = await self._identify_arguments(sections)
        
        # 第4层：支撑材料 - 数据、图表等佐证材料
        logger.info("--- [第4层] 支撑材料：识别数据、图表等佐证材料...")
        supporting_materials = self._identify_supporting_materials()
        
        # 第5层：表达风格 - 语言风格、文化特征
        logger.info("--- [第5层] 表达风格：分析语言风格和文化特征...")
        expression_style = self._analyze_expression_style()
        
        # 第6层：呈现形式 - 格式、布局、视觉呈现
        logger.info("--- [第6层] 呈现形式：分析格式、布局、视觉呈现...")
        presentation_form = self._analyze_presentation_form()
        
        result = {
            "layer_1_overall_understanding": {
                "name": "通读理解层",
                "description": "理解文档的整体思想、主题、目的和核心价值主张",
                "data": overall_understanding
            },
            "layer_2_sections": {
                "name": "板块结构层",
                "description": "识别各个板块及其传递的核心思想",
                "data": sections
            },
            "layer_3_arguments": {
                "name": "论证逻辑层",
                "description": "识别每个板块的论据和论证方式",
                "data": arguments
            },
            "layer_4_supporting_materials": {
                "name": "支撑材料层",
                "description": "数据、图表、案例等佐证材料",
                "data": supporting_materials
            },
            "layer_5_expression_style": {
                "name": "表达风格层",
                "description": "语言风格、表达方式、文化特征",
                "data": expression_style
            },
            "layer_6_presentation_form": {
                "name": "呈现形式层",
                "description": "格式、布局、视觉呈现方式",
                "data": presentation_form
            }
        }
        
        logger.info("="*80)
        logger.info("--- [HumanCenteredAnalyzer]: 人类中心化分析完成")
        logger.info(f"   识别板块数: {len(sections.get('sections', []))}")
        logger.info(f"   核心思想: {overall_understanding.get('core_idea', '')[:50]}...")
        logger.info("="*80)
        
        return result
    
    async def _understand_overall(self) -> Dict[str, Any]:
        """
        第1层：通读理解
        使用LLM理解文档的整体思想、主题、目的和核心价值主张
        """
        logger.info("--- [HumanCenteredAnalyzer]: 【详细探针】第1层：通读理解（使用LLM）")
        
        # 收集所有文本内容
        all_texts = []
        if self.raw_text:
            # 优先使用raw_text（来自docx）
            full_text = self.raw_text
            logger.info(f"   使用raw_text，长度: {len(full_text)}字符")
        else:
            # 从structure中收集文本
            logger.info(f"   收集文本内容（从{len(self.structure.get('slides', []))}张幻灯片）...")
            for slide_idx, slide in enumerate(self.structure.get("slides", [])):
                slide_texts = []
                for shape in slide.get("shapes", []):
                    text = shape.get("text", "").strip()
                    if text:
                        slide_texts.append(text)
                        all_texts.append(text)
                logger.info(f"     幻灯片{slide_idx}: 收集到{len(slide_texts)}个文本块")
                if slide_texts:
                    logger.info(f"       文本预览: {slide_texts[0][:100]}...")
            
            full_text = "\n".join(all_texts)
            logger.info(f"   总文本长度: {len(full_text)}字符")
        
        logger.info(f"   文本预览: {full_text[:300]}...")
        
        # 使用LLM理解文档整体内容
        logger.info("   使用LLM理解文档整体内容...")
        
        system_prompt = """你是中国职场的述职汇报专家，专门为副总裁级别的职场高管筹备述职内容，最擅长将高管整理的文稿大纲转换成适合呈现在ppt上的语言内容。"""
        
        user_prompt = f"""请通读以下文档内容，理解其核心思想、主题、目的和核心价值主张。

文档内容：
{full_text}

请按照以下方向进行分析：
1. 先对文档进行整体的通读了解，确保知道文档表述的核心思想
2. 识别文档的核心主题、目的、目标受众
3. 识别文档的核心价值主张和关键信息

请以JSON格式输出分析结果：
{{
  "core_theme": "核心主题",
  "core_idea": "核心思想",
  "purpose": "文档目的",
  "target_audience": "目标受众",
  "value_propositions": ["价值主张1", "价值主张2", ...],
  "key_phrases": ["关键短语1", "关键短语2", ...]
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
                # 尝试提取JSON
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用默认值")
                    result = {}
            else:
                result = response
            
            logger.info(f"   LLM理解结果: 核心主题={result.get('core_theme', '未识别')}")
            logger.info(f"   价值主张数量: {len(result.get('value_propositions', []))}")
            
            return {
                "core_theme": result.get("core_theme", "未明确标识"),
                "core_idea": result.get("core_idea", ""),
                "value_propositions": result.get("value_propositions", []),
                "purpose": result.get("purpose", "通用文档"),
                "target_audience": result.get("target_audience", "通用受众"),
                "total_slides": self.structure.get("slide_count", 0),
                "text_length": len(full_text),
                "key_phrases": result.get("key_phrases", [])
            }
        except Exception as e:
            logger.error(f"   LLM理解失败: {e}，使用规则分析作为回退")
            # 回退到规则分析
            return self._understand_overall_fallback(full_text)
    
    def _understand_overall_fallback(self, full_text: str) -> Dict[str, Any]:
        """回退方法：使用规则分析"""
        core_theme = self._extract_core_theme(full_text)
        value_propositions = self._extract_value_propositions(full_text)
        purpose = self._identify_purpose(full_text)
        target_audience = self._identify_target_audience(full_text)
        
        return {
            "core_theme": core_theme,
            "core_idea": "",
            "value_propositions": value_propositions,
            "purpose": purpose,
            "target_audience": target_audience,
            "total_slides": self.structure.get("slide_count", 0),
            "text_length": len(full_text),
            "key_phrases": self._extract_key_phrases(full_text)
        }
    
    def _extract_core_theme(self, text: str) -> str:
        """提取核心主题"""
        # 查找标题、副标题等
        title_patterns = [
            r'^([^。，\n]{5,30})$',  # 短标题
            r'核心[主题|思想|观点]：(.+)',
            r'主题：(.+)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                return match.group(1) if len(match.groups()) > 0 else match.group(0)
        
        # 如果没有明确标题，取第一段作为主题
        first_line = text.split('\n')[0] if text else ""
        if len(first_line) < 50:
            return first_line
        
        return "未明确标识"
    
    def _extract_value_propositions(self, text: str) -> List[str]:
        """提取核心价值主张"""
        value_props = []
        
        # 查找价值主张模式
        patterns = [
            r'核心价值[：:](.+)',
            r'价值主张[：:](.+)',
            r'(.+?)\s*[|｜]\s*(.+?)\s*[|｜]\s*(.+)',  # 用|分隔的价值主张
            r'降低(.+?)\s*[%％]',  # 降低成本
            r'提升(.+?)\s*[%％]',  # 提升效率
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    value_props.extend([m for m in match if m.strip()])
                else:
                    value_props.append(match.strip())
        
        # 去重
        return list(set(value_props))[:5]  # 最多返回5个
    
    def _identify_purpose(self, text: str) -> str:
        """识别文档目的"""
        purpose_keywords = {
            "汇报": ["汇报", "报告", "总结", "回顾"],
            "提案": ["提案", "建议", "方案", "计划"],
            "介绍": ["介绍", "概述", "说明", "展示"],
            "分析": ["分析", "研究", "评估", "调研"]
        }
        
        for purpose, keywords in purpose_keywords.items():
            if any(kw in text for kw in keywords):
                return purpose
        
        return "通用文档"
    
    def _identify_target_audience(self, text: str) -> str:
        """识别目标受众"""
        audience_keywords = {
            "管理层": ["管理层", "领导", "决策", "战略"],
            "技术团队": ["技术", "开发", "工程师", "系统"],
            "业务团队": ["业务", "销售", "市场", "客户"],
            "投资者": ["投资", "融资", "股东", "回报"]
        }
        
        for audience, keywords in audience_keywords.items():
            if any(kw in text for kw in keywords):
                return audience
        
        return "通用受众"
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """提取关键短语"""
        # 简单的关键词提取（可以后续用更高级的方法）
        key_phrases = []
        
        # 查找加粗、大字体等强调的内容
        for slide in self.structure["slides"]:
            for shape in slide["shapes"]:
                format_info = shape.get("format", {})
                if format_info.get("is_bold") or (format_info.get("font_size_pt") or 0) >= 20:
                    text = shape.get("text", "").strip()
                    if text and len(text) < 50:
                        key_phrases.append(text)
        
        return list(set(key_phrases))[:10]
    
    async def _identify_sections(self) -> Dict[str, Any]:
        """
        第2层：板块拆分
        使用LLM识别各个板块及其传递的核心思想
        """
        logger.info("--- [HumanCenteredAnalyzer]: 【详细探针】第2层：板块拆分（使用LLM）")
        
        # 收集所有文本内容
        if self.raw_text:
            full_text = self.raw_text
        else:
            all_texts = []
            for slide in self.structure.get("slides", []):
                for shape in slide.get("shapes", []):
                    text = shape.get("text", "").strip()
                    if text:
                        all_texts.append(text)
            full_text = "\n".join(all_texts)
        
        logger.info(f"   文档总长度: {len(full_text)}字符")
        
        # 使用LLM进行板块拆分
        system_prompt = """你是中国职场的述职汇报专家，专门为副总裁级别的职场高管筹备述职内容，最擅长将高管整理的文稿大纲转换成适合呈现在ppt上的语言内容。"""
        
        user_prompt = f"""请仔细重读以下文档内容，根据文档的具体内容进行细分板块的拆解，以确保让整个文档叙事具备高逻辑性、高叙事性。

文档内容：
{full_text}

请按照以下方向进行分析：
1. 仔细重读文档，识别文档中的各个板块
2. 为每个板块识别其主题、核心思想
3. 确保板块之间的逻辑连贯性和叙事性

请以JSON格式输出分析结果：
{{
  "total_sections": 板块总数,
  "sections": [
    {{
      "section_index": 板块索引（从0开始）,
      "theme": "板块主题",
      "core_idea": "板块核心思想",
      "content_summary": "板块内容摘要",
      "slides": [该板块涉及的幻灯片索引列表]
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
                    result = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用规则分析作为回退")
                    return self._identify_sections_fallback()
            else:
                result = response
            
            logger.info(f"   LLM识别板块数: {result.get('total_sections', 0)}")
            for section in result.get("sections", [])[:5]:  # 显示前5个
                logger.info(f"     板块{section.get('section_index', 0)}: {section.get('theme', '')}")
            
            return result
        except Exception as e:
            logger.error(f"   LLM板块拆分失败: {e}，使用规则分析作为回退")
            return self._identify_sections_fallback()
    
    def _identify_sections_fallback(self) -> Dict[str, Any]:
        """回退方法：使用规则分析"""
        sections = []
        current_section = None
        
        for slide_idx, slide in enumerate(self.structure.get("slides", [])):
            slide_theme = self._extract_slide_theme(slide)
            
            if slide_theme:
                if current_section:
                    sections.append(current_section)
                
                current_section = {
                    "section_index": len(sections),
                    "theme": slide_theme,
                    "core_idea": self._extract_core_idea(slide),
                    "slides": [slide_idx],
                    "content_summary": self._summarize_slide_content(slide)
                }
            else:
                if current_section:
                    current_section["slides"].append(slide_idx)
                    current_section["content_summary"] += " " + self._summarize_slide_content(slide)
                else:
                    current_section = {
                        "section_index": len(sections),
                        "theme": f"板块{len(sections) + 1}",
                        "core_idea": self._extract_core_idea(slide),
                        "slides": [slide_idx],
                        "content_summary": self._summarize_slide_content(slide)
                    }
        
        if current_section:
            sections.append(current_section)
        
        return {
            "total_sections": len(sections),
            "sections": sections
        }
    
    def _extract_slide_theme(self, slide: Dict[str, Any]) -> Optional[str]:
        """提取幻灯片主题"""
        # 查找标题占位符
        for shape in slide["shapes"]:
            if shape.get("is_placeholder"):
                placeholder_type = shape.get("placeholder_type", "")
                if "TITLE" in placeholder_type or "CENTER_TITLE" in placeholder_type:
                    text = shape.get("text", "").strip()
                    if text:
                        return text
        
        # 查找大字体、加粗的文本（可能是标题）
        # 【改进】优先查找第一个shape（通常是标题）
        for shape_idx, shape in enumerate(slide["shapes"]):
            format_info = shape.get("format", {})
            text = shape.get("text", "").strip()
            
            # 如果是第一个shape且是短文本，很可能是标题
            if shape_idx == 0 and text and len(text) < 50:
                # 检查是否包含标题特征（emoji、数字编号、关键词等）
                has_emoji = any(ord(c) > 127 and c not in '，。、；：！？""''（）【】《》' for c in text[:10])
                has_numbering = re.match(r'^[0-9一二三四五六七八九十]+[、.]', text) if text else False
                has_keywords = any(kw in text for kw in ['分析', '战略', '路线图', '回顾', '市场', '商业化', '技术', '产品', '文档', '启示', '规划', '能力', '路径'])
                
                if has_emoji or has_numbering or has_keywords or format_info.get("is_bold"):
                    return text
            
            # 或者检查大字体、加粗的文本
            if (format_info.get("font_size_pt") or 0) >= 20 and format_info.get("is_bold"):
                if text and len(text) < 50:
                    return text
        
        return None
    
    def _extract_core_idea(self, slide: Dict[str, Any]) -> str:
        """提取板块核心思想"""
        # 收集所有文本
        texts = []
        for shape in slide["shapes"]:
            text = shape.get("text", "").strip()
            if text:
                texts.append(text)
        
        # 取第一段作为核心思想
        if texts:
            return texts[0][:100]  # 限制长度
        
        return ""
    
    def _summarize_slide_content(self, slide: Dict[str, Any]) -> str:
        """总结幻灯片内容"""
        texts = []
        for shape in slide["shapes"]:
            text = shape.get("text", "").strip()
            if text:
                texts.append(text)
        
        return " | ".join(texts[:3])  # 最多3段
    
    async def _identify_arguments(self, sections: Dict[str, Any]) -> Dict[str, Any]:
        """
        第3层：论证逻辑
        使用LLM深入探寻每个板块的核心内容、核心思想、具体论点、核心论据以及必要的数据呈现
        """
        logger.info("--- [HumanCenteredAnalyzer]: 【详细探针】第3层：论证逻辑（使用LLM）")
        
        # 收集所有文本内容
        if self.raw_text:
            full_text = self.raw_text
        else:
            all_texts = []
            for slide in self.structure.get("slides", []):
                for shape in slide.get("shapes", []):
                    text = shape.get("text", "").strip()
                    if text:
                        all_texts.append(text)
            full_text = "\n".join(all_texts)
        
        # 为每个板块准备内容
        sections_text = []
        for section in sections.get("sections", []):
            section_text = f"板块{section.get('section_index', 0)}: {section.get('theme', '')}\n"
            section_text += f"核心思想: {section.get('core_idea', '')}\n"
            section_text += f"内容摘要: {section.get('content_summary', '')}\n"
            sections_text.append(section_text)
        
        system_prompt = """你是中国职场的述职汇报专家，专门为副总裁级别的职场高管筹备述职内容，最擅长将高管整理的文稿大纲转换成适合呈现在ppt上的语言内容。"""
        
        user_prompt = f"""请对以下文档的每个板块进行深入探寻，深度理解每个板块的核心内容、核心思想、具体论点、核心论据以及必要的数据呈现。

文档内容：
{full_text}

已识别的板块：
{chr(10).join(sections_text)}

请按照以下方向进行分析：
1. 对每个板块进行深入探寻
2. 识别每个板块的核心内容、核心思想
3. 识别每个板块的具体论点
4. 识别每个板块的核心论据
5. 识别必要的数据呈现

请以JSON格式输出分析结果：
{{
  "total_sections_with_arguments": 有论证的板块总数,
  "arguments": [
    {{
      "section_index": 板块索引,
      "section_theme": "板块主题",
      "core_content": "核心内容",
      "core_idea": "核心思想",
      "specific_arguments": ["具体论点1", "具体论点2", ...],
      "core_evidence": ["核心论据1", "核心论据2", ...],
      "data_points": ["数据点1", "数据点2", ...],
      "argument_types": ["论证类型1", "论证类型2", ...]
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
                    result = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用规则分析作为回退")
                    return self._identify_arguments_fallback(sections)
            else:
                result = response
            
            logger.info(f"   LLM识别论证板块数: {result.get('total_sections_with_arguments', 0)}")
            
            return result
        except Exception as e:
            logger.error(f"   LLM论证逻辑分析失败: {e}，使用规则分析作为回退")
            return self._identify_arguments_fallback(sections)
    
    def _identify_arguments_fallback(self, sections: Dict[str, Any]) -> Dict[str, Any]:
        """回退方法：使用规则分析"""
        arguments = []
        
        for section in sections.get("sections", []):
            section_args = {
                "section_index": section["section_index"],
                "section_theme": section["theme"],
                "core_content": section.get("content_summary", ""),
                "core_idea": section.get("core_idea", ""),
                "specific_arguments": [],
                "core_evidence": [],
                "data_points": [],
                "argument_types": []
            }
            
            # 分析每个幻灯片中的论据
            for slide_idx in section.get("slides", []):
                if slide_idx < len(self.structure.get("slides", [])):
                    slide = self.structure["slides"][slide_idx]
                    
                    # 识别论据类型
                    arg_types = self._identify_argument_types(slide)
                    section_args["argument_types"].extend(arg_types)
                    
                    # 识别证据点
                    evidence = self._extract_evidence_points(slide)
                    section_args["core_evidence"].extend(evidence)
            
            # 去重
            section_args["argument_types"] = list(set(section_args["argument_types"]))
            arguments.append(section_args)
        
        return {
            "total_sections_with_arguments": len(arguments),
            "arguments": arguments
        }
    
    def _identify_argument_types(self, slide: Dict[str, Any]) -> List[str]:
        """识别论证类型"""
        arg_types = []
        text = " ".join([s.get("text", "") for s in slide["shapes"]])
        
        # 数据论证
        if re.search(r'\d+[%％]|\d+\.\d+', text):
            arg_types.append("数据论证")
        
        # 案例论证
        if any(kw in text for kw in ["案例", "例子", "实例", "客户", "项目"]):
            arg_types.append("案例论证")
        
        # 对比论证
        if any(kw in text for kw in ["对比", "比较", "vs", "相比", "优于"]):
            arg_types.append("对比论证")
        
        # 因果论证
        if any(kw in text for kw in ["因为", "所以", "导致", "因此", "由于"]):
            arg_types.append("因果论证")
        
        return arg_types
    
    def _extract_evidence_points(self, slide: Dict[str, Any]) -> List[str]:
        """提取证据点"""
        evidence = []
        
        for shape in slide["shapes"]:
            text = shape.get("text", "").strip()
            if not text:
                continue
            
            # 查找数据点
            data_matches = re.findall(r'\d+[%％]|\d+\.\d+%', text)
            evidence.extend([f"数据: {m}" for m in data_matches])
            
            # 查找列表项（可能是证据点）
            if re.match(r'^[•·▪▫○●■□\d]', text):
                evidence.append(f"要点: {text[:50]}")
        
        return evidence[:5]  # 最多5个证据点
    
    def _identify_supporting_materials(self) -> Dict[str, Any]:
        """
        第4层：支撑材料
        识别数据、图表、案例等佐证材料
        """
        materials = {
            "data_points": [],
            "charts": [],
            "tables": [],
            "cases": [],
            "quotes": []
        }
        
        for slide_idx, slide in enumerate(self.structure["slides"]):
            # 查找数据点
            for shape in slide["shapes"]:
                text = shape.get("text", "").strip()
                if not text:
                    continue
                
                # 提取数据
                data_matches = re.findall(r'\d+[%％]|\d+\.\d+%|\d+万|\d+亿', text)
                for data in data_matches:
                    materials["data_points"].append({
                        "slide_index": slide_idx,
                        "data": data,
                        "context": text[:50]
                    })
                
                # 查找案例
                if any(kw in text for kw in ["案例", "例子", "客户", "项目"]):
                    materials["cases"].append({
                        "slide_index": slide_idx,
                        "content": text[:100]
                    })
        
        return {
            "total_data_points": len(materials["data_points"]),
            "total_cases": len(materials["cases"]),
            "materials": materials
        }
    
    def _analyze_expression_style(self) -> Dict[str, Any]:
        """
        第5层：表达风格
        分析语言风格、表达方式、文化特征
        """
        # 收集所有文本
        all_texts = []
        for slide in self.structure["slides"]:
            for shape in slide["shapes"]:
                text = shape.get("text", "").strip()
                if text:
                    all_texts.append(text)
        
        full_text = " ".join(all_texts)
        
        # 分析语言风格
        style_features = {
            "formality_level": self._assess_formality(full_text),
            "tone": self._assess_tone(full_text),
            "cultural_features": self._identify_cultural_features(full_text),
            "use_of_numbers": self._count_numbers(full_text),
            "use_of_emojis": self._count_emojis(full_text)
        }
        
        return style_features
    
    def _assess_formality(self, text: str) -> str:
        """评估正式程度"""
        formal_keywords = ["汇报", "报告", "总结", "分析", "评估"]
        informal_keywords = ["我们", "大家", "一起", "💎", "🚀"]
        
        formal_count = sum(1 for kw in formal_keywords if kw in text)
        informal_count = sum(1 for kw in informal_keywords if kw in text)
        
        if formal_count > informal_count:
            return "正式"
        elif informal_count > formal_count:
            return "非正式"
        else:
            return "中性"
    
    def _assess_tone(self, text: str) -> str:
        """评估语调"""
        if any(kw in text for kw in ["优秀", "卓越", "领先", "突破"]):
            return "积极"
        elif any(kw in text for kw in ["问题", "挑战", "困难", "风险"]):
            return "谨慎"
        else:
            return "中性"
    
    def _identify_cultural_features(self, text: str) -> List[str]:
        """识别文化特征"""
        features = []
        
        if any(kw in text for kw in ["朋友", "交个朋友", "我们"]):
            features.append("强调团队协作")
        
        if any(kw in text for kw in ["价值", "价值主张", "核心价值"]):
            features.append("强调价值导向")
        
        if re.search(r'\d+[%％]', text):
            features.append("数据驱动表达")
        
        return features
    
    def _count_numbers(self, text: str) -> int:
        """统计数字使用"""
        return len(re.findall(r'\d+', text))
    
    def _count_emojis(self, text: str) -> int:
        """统计表情符号使用"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "]+"
        )
        return len(emoji_pattern.findall(text))
    
    def _analyze_presentation_form(self) -> Dict[str, Any]:
        """
        第6层：呈现形式
        分析格式、布局、视觉呈现方式
        """
        form_features = {
            "layout_style": self._analyze_layout_style(),
            "typography": self._analyze_typography(),
            "visual_hierarchy": self._analyze_visual_hierarchy(),
            "color_usage": self._analyze_color_usage()
        }
        
        return form_features
    
    def _analyze_layout_style(self) -> Dict[str, Any]:
        """分析布局风格"""
        # 分析幻灯片尺寸比例
        width = self.structure.get("slide_width", 0)
        height = self.structure.get("slide_height", 0)
        ratio = width / height if height > 0 else 0
        
        if 1.7 <= ratio <= 1.8:
            aspect_ratio = "16:9"
        elif 1.3 <= ratio <= 1.35:
            aspect_ratio = "4:3"
        else:
            aspect_ratio = "其他"
        
        return {
            "aspect_ratio": aspect_ratio,
            "width_cm": width,
            "height_cm": height
        }
    
    def _analyze_typography(self) -> Dict[str, Any]:
        """分析字体排版"""
        font_sizes = set()
        font_names = set()
        bold_count = 0
        
        for slide in self.structure["slides"]:
            for shape in slide["shapes"]:
                format_info = shape.get("format", {})
                if format_info.get("font_size_pt"):
                    font_sizes.add(format_info["font_size_pt"])
                if format_info.get("font_name"):
                    font_names.add(format_info["font_name"])
                if format_info.get("is_bold"):
                    bold_count += 1
        
        return {
            "font_sizes": sorted(list(font_sizes)),
            "font_names": list(font_names),
            "bold_usage_count": bold_count
        }
    
    def _analyze_visual_hierarchy(self) -> Dict[str, Any]:
        """分析视觉层次"""
        hierarchy = {
            "title_levels": 0,
            "body_levels": 0,
            "emphasis_count": 0
        }
        
        for slide in self.structure["slides"]:
            for shape in slide["shapes"]:
                format_info = shape.get("format", {})
                font_size = format_info.get("font_size_pt") or 0
                
                if font_size >= 20:
                    hierarchy["title_levels"] += 1
                elif font_size >= 14:
                    hierarchy["body_levels"] += 1
                
                if format_info.get("is_bold"):
                    hierarchy["emphasis_count"] += 1
        
        return hierarchy
    
    def _analyze_color_usage(self) -> Dict[str, Any]:
        """分析颜色使用"""
        colors = set()
        
        for slide in self.structure["slides"]:
            for shape in slide["shapes"]:
                format_info = shape.get("format", {})
                if format_info.get("font_color"):
                    colors.add(format_info["font_color"])
        
        return {
            "unique_colors": len(colors),
            "colors": list(colors)
        }

