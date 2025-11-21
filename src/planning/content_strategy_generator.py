"""
内容生成策略制定器
根据人类中心化分析结果，制定内容生成策略
"""

from typing import Dict, Any, List
from loguru import logger


class ContentStrategyGenerator:
    """
    内容生成策略制定器
    根据人类中心化分析结果，制定整体策略和板块策略
    """
    
    def __init__(self, human_analysis: Dict[str, Any]):
        """
        初始化策略生成器
        
        Args:
            human_analysis: 人类中心化分析结果
        """
        self.analysis = human_analysis
        logger.info("--- [ContentStrategyGenerator]: 初始化内容生成策略制定器")
    
    def generate_strategy(self) -> Dict[str, Any]:
        """
        生成完整的内容生成策略
        
        Returns:
            包含整体策略和板块策略的字典
        """
        logger.info("--- [ContentStrategyGenerator]: 开始生成内容生成策略")
        
        # 1. 生成整体策略
        overall_strategy = self._generate_overall_strategy()
        
        # 2. 生成板块策略
        section_strategies = self._generate_section_strategies()
        
        # 3. 生成表达风格策略
        expression_strategy = self._generate_expression_strategy()
        
        strategy = {
            "overall_strategy": overall_strategy,
            "section_strategies": section_strategies,
            "expression_strategy": expression_strategy
        }
        
        logger.info(f"--- [ContentStrategyGenerator]: 策略生成完成")
        logger.info(f"   整体策略: {overall_strategy.get('core_theme', '')}")
        logger.info(f"   板块策略数: {len(section_strategies)}")
        
        return strategy
    
    def _generate_overall_strategy(self) -> Dict[str, Any]:
        """生成整体策略"""
        layer_1 = self.analysis.get("layer_1_overall_understanding", {}).get("data", {})
        layer_5 = self.analysis.get("layer_5_expression_style", {}).get("data", {})
        
        return {
            "core_theme": layer_1.get("core_theme", ""),
            "value_propositions": layer_1.get("value_propositions", []),
            "purpose": layer_1.get("purpose", "通用文档"),
            "target_audience": layer_1.get("target_audience", "通用受众"),
            "tone": layer_5.get("tone", "中性"),
            "formality_level": layer_5.get("formality_level", "中性"),
            "key_phrases": layer_1.get("key_phrases", [])
        }
    
    def _generate_section_strategies(self) -> List[Dict[str, Any]]:
        """生成板块策略（详细探针）"""
        logger.info("--- [ContentStrategyGenerator]: 【详细探针】生成板块策略")
        
        sections = self.analysis.get("layer_2_sections", {}).get("data", {}).get("sections", [])
        arguments = self.analysis.get("layer_3_arguments", {}).get("data", {}).get("arguments", [])
        
        logger.info(f"   识别到{len(sections)}个板块")
        logger.info(f"   识别到{len(arguments)}个论证逻辑")
        
        section_strategies = []
        
        for section in sections:
            section_idx = section.get("section_index", 0)
            logger.info(f"\n   处理板块{section_idx}:")
            logger.info(f"     主题: {section.get('theme', '')}")
            logger.info(f"     核心思想: {section.get('core_idea', '')[:100]}...")
            logger.info(f"     分配的幻灯片: {section.get('slides', [])}")
            
            # 找到对应的论证逻辑
            section_args = next(
                (arg for arg in arguments if arg.get("section_index") == section_idx),
                {}
            )
            
            if section_args:
                logger.info(f"     论证类型: {section_args.get('argument_types', [])}")
                logger.info(f"     证据点数量: {len(section_args.get('evidence_points', []))}")
            else:
                logger.warning(f"     ⚠️ 未找到对应的论证逻辑")
            
            # 生成板块策略
            strategy = {
                "section_index": section_idx,
                "theme": section.get("theme", ""),
                "core_idea": section.get("core_idea", ""),
                "slides": section.get("slides", []),
                "argument_types": section_args.get("argument_types", []),
                "evidence_points": section_args.get("evidence_points", []),
                "content_generation_approach": self._determine_content_approach(
                    section, section_args
                )
            }
            
            logger.info(f"     内容生成方式: {strategy['content_generation_approach']}")
            
            section_strategies.append(strategy)
        
        logger.info(f"\n   生成完成，共{len(section_strategies)}个板块策略")
        
        return section_strategies
    
    def _determine_content_approach(self, section: Dict, arguments: Dict) -> Dict[str, Any]:
        """确定内容生成方法"""
        argument_types = arguments.get("argument_types", [])
        evidence_points = arguments.get("evidence_points", [])
        
        # 根据论证类型确定重点
        if "数据论证" in argument_types:
            emphasis = "数据支撑"
            evidence_priority = ["数据", "图表"]
        elif "案例论证" in argument_types:
            emphasis = "案例说明"
            evidence_priority = ["案例", "客户反馈"]
        elif "对比论证" in argument_types:
            emphasis = "对比分析"
            evidence_priority = ["对比数据", "优势说明"]
        else:
            emphasis = "核心观点"
            evidence_priority = ["论据", "说明"]
        
        # 根据内容长度确定生成长度
        content_summary = section.get("content_summary", "")
        if len(content_summary) > 200:
            length = "long"
        elif len(content_summary) > 100:
            length = "medium"
        else:
            length = "short"
        
        return {
            "emphasis": emphasis,
            "evidence_priority": evidence_priority,
            "length": length
        }
    
    def _generate_expression_strategy(self) -> Dict[str, Any]:
        """生成表达风格策略"""
        layer_5 = self.analysis.get("layer_5_expression_style", {}).get("data", {})
        layer_6 = self.analysis.get("layer_6_presentation_form", {}).get("data", {})
        
        formality = layer_5.get("formality_level", "中性")
        tone = layer_5.get("tone", "中性")
        cultural_features = layer_5.get("cultural_features", [])
        
        # 根据正式程度确定字体大小
        if formality == "正式":
            title_font_size = 40
            body_font_size = 15
        elif formality == "非正式":
            title_font_size = 36
            body_font_size = 14
        else:
            title_font_size = 38
            body_font_size = 14
        
        # 根据语调确定颜色
        if tone == "积极":
            primary_color = "primary"  # Ant Design蓝色
            accent_color = "success"   # 绿色
        elif tone == "谨慎":
            primary_color = "warning"  # 橙色
            accent_color = "error"     # 红色
        else:
            primary_color = "text_primary"  # 黑色
            accent_color = "primary"        # 蓝色
        
        return {
            "language_style": {
                "formality": formality,
                "tone": tone,
                "cultural_features": cultural_features
            },
            "visual_style": {
                "layout": layer_6.get("layout_style", {}).get("aspect_ratio", "16:9"),
                "typography": {
                    "title_font_size": title_font_size,
                    "body_font_size": body_font_size,
                    "font_family": "Segoe UI, 微软雅黑, Arial"
                },
                "color_scheme": {
                    "primary": primary_color,
                    "accent": accent_color
                }
            }
        }
    
    def build_generation_prompt(self, section_strategy: Dict[str, Any], strategy: Dict[str, Any]) -> str:
        """
        构建内容生成提示词
        
        Args:
            section_strategy: 板块策略
            
        Returns:
            生成提示词字符串
        """
        overall = strategy.get("overall_strategy", {})
        expression = strategy.get("expression_strategy", {})
        approach = section_strategy.get("content_generation_approach", {})
        
        prompt = f"""
根据以下信息，生成符合中国商业汇报习惯的PPT内容：

【整体背景】
核心主题：{overall.get("core_theme", "")}
目标受众：{overall.get("target_audience", "")}
文档目的：{overall.get("purpose", "")}

【板块信息】
板块主题：{section_strategy.get("theme", "")}
核心思想：{section_strategy.get("core_idea", "")}

【论证方式】
{", ".join(section_strategy.get("argument_types", []))}

【证据点】
{self._format_evidence_points(section_strategy.get("evidence_points", []))}

【生成要求】
1. 语言风格：{expression.get("language_style", {}).get("formality", "中性")}，语调：{expression.get("language_style", {}).get("tone", "中性")}
2. 强调重点：{approach.get("emphasis", "")}
3. 优先使用：{", ".join(approach.get("evidence_priority", []))}
4. 内容长度：{approach.get("length", "medium")}
5. 符合中国商业文化：{", ".join(expression.get("language_style", {}).get("cultural_features", []))}

【价值主张】
{", ".join(overall.get("value_propositions", []))}

请生成：
- 标题（简洁有力，体现核心思想，不超过20字）
- 正文内容（包含论据和证据点，{approach.get("length", "medium")}长度）
- 数据支撑（如果有，突出显示）
- 案例说明（如果有，简洁明了）

要求：
- 语言符合中国商业汇报习惯
- 逻辑清晰，有说服力
- 突出价值主张
- 使用数据支撑观点
"""
        return prompt
    
    def _format_evidence_points(self, evidence_points: List[str]) -> str:
        """格式化证据点"""
        if not evidence_points:
            return "无"
        
        formatted = []
        for i, point in enumerate(evidence_points[:5], 1):  # 最多5个
            formatted.append(f"{i}. {point}")
        
        return "\n".join(formatted)

