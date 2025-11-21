"""
深度解析器
整合所有分析模块，提供统一的深度解析接口
"""

from pathlib import Path
from typing import Dict, Any
from loguru import logger

from enhanced_ppt_parser import EnhancedPPTParser
from semantic_analyzer import SemanticAnalyzer


class DeepParser:
    """
    深度解析器
    整合格式分析、语义分析、主题识别、逻辑关系等所有能力
    """
    
    def __init__(self, ppt_path: str):
        """
        初始化深度解析器
        
        Args:
            ppt_path: PPT文件路径
        """
        self.ppt_path = Path(ppt_path)
        self.parser = EnhancedPPTParser(ppt_path)
        logger.info("--- [DeepParser]: Initialized")
    
    def parse_all(self) -> Dict[str, Any]:
        """
        执行完整的深度解析
        
        Returns:
            包含7个层次的完整分析结果
        """
        logger.info("="*80)
        logger.info("--- [DeepParser]: 开始深度解析")
        logger.info("="*80)
        
        # 1. 增强结构提取（包含格式信息）
        logger.info("--- [DeepParser]: 阶段1 - 提取增强结构...")
        enhanced_structure = self.parser.extract_structure_enhanced()
        
        # 2. 段落级别分析
        logger.info("--- [DeepParser]: 阶段2 - 提取段落结构...")
        paragraph_structure = self.parser.extract_paragraph_structure()
        
        # 3. 列表识别
        logger.info("--- [DeepParser]: 阶段3 - 识别列表结构...")
        list_structure = self.parser.extract_list_structure()
        
        # 4. 表格识别
        logger.info("--- [DeepParser]: 阶段4 - 识别表格结构...")
        table_structure = self.parser.extract_table_structure()
        
        # 5. 语义分析
        logger.info("--- [DeepParser]: 阶段5 - 语义分析...")
        semantic_analyzer = SemanticAnalyzer(enhanced_structure)
        semantic_blocks = semantic_analyzer.identify_semantic_blocks()
        
        # 6. 主题识别
        logger.info("--- [DeepParser]: 阶段6 - 主题识别...")
        topics = semantic_analyzer.identify_topics(semantic_blocks)
        
        # 7. 逻辑关系
        logger.info("--- [DeepParser]: 阶段7 - 逻辑关系识别...")
        logical_relations = semantic_analyzer.identify_logical_relations(semantic_blocks)
        
        # 8. 格式特征分析
        logger.info("--- [DeepParser]: 阶段8 - 格式特征分析...")
        format_features = self._analyze_format_features(enhanced_structure)
        
        # 构建7层结构
        result = {
            "file_info": {
                "path": str(self.ppt_path),
                "size_bytes": self.ppt_path.stat().st_size
            },
            "layers": {
                "layer_1_physical": {
                    "name": "物理结构层",
                    "description": "文档的物理结构：段落、表格、章节等",
                    "data": {
                        "slide_count": enhanced_structure["slide_count"],
                        "total_shapes": sum(len(s["shapes"]) for s in enhanced_structure["slides"]),
                        "total_placeholders": sum(len(s["placeholders"]) for s in enhanced_structure["slides"]),
                        "total_paragraphs": len(paragraph_structure),
                        "total_tables": len(table_structure),
                        "dimensions": {
                            "width_cm": enhanced_structure["slide_width"],
                            "height_cm": enhanced_structure["slide_height"],
                            "ratio": enhanced_structure["slide_width"] / enhanced_structure["slide_height"]
                        }
                    }
                },
                "layer_2_format": {
                    "name": "格式特征层",
                    "description": "文本格式特征：字体、字号、加粗、颜色、缩进等",
                    "data": format_features
                },
                "layer_3_semantic": {
                    "name": "内容语义层",
                    "description": "基于内容语义和格式特征识别的标题-内容块结构",
                    "data": {
                        "total_blocks": len(semantic_blocks),
                        "blocks": semantic_blocks
                    }
                },
                "layer_4_lists": {
                    "name": "列表结构层",
                    "description": "文档中的列表结构：编号列表、项目符号、缩进列表",
                    "data": list_structure
                },
                "layer_5_tables": {
                    "name": "表格数据层",
                    "description": "文档中的表格结构和数据",
                    "data": table_structure
                },
                "layer_6_topics": {
                    "name": "主题/话题层",
                    "description": "基于关键词识别的内容主题分类",
                    "data": topics
                },
                "layer_7_logic": {
                    "name": "逻辑关系层",
                    "description": "内容之间的逻辑关系：顺序、层级、对比等",
                    "data": logical_relations
                }
            }
        }
        
        logger.info("="*80)
        logger.info("--- [DeepParser]: 深度解析完成")
        logger.info(f"   识别层次: 7个")
        logger.info(f"   内容块数: {len(semantic_blocks)}")
        logger.info(f"   主题数: {len(topics)}")
        logger.info("="*80)
        
        return result
    
    def _analyze_format_features(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """分析格式特征"""
        features = {
            "font_sizes": set(),
            "font_names": set(),
            "font_colors": set(),
            "bold_count": 0,
            "italic_count": 0,
            "colored_count": 0,
            "format_statistics": {}
        }
        
        for slide in structure["slides"]:
            for shape in slide["shapes"]:
                format_info = shape.get("format", {})
                
                if format_info.get("font_size_pt"):
                    features["font_sizes"].add(format_info["font_size_pt"])
                if format_info.get("font_name"):
                    features["font_names"].add(format_info["font_name"])
                if format_info.get("font_color"):
                    features["font_colors"].add(format_info["font_color"])
                
                if format_info.get("is_bold"):
                    features["bold_count"] += 1
                if format_info.get("is_italic"):
                    features["italic_count"] += 1
                if format_info.get("font_color"):
                    features["colored_count"] += 1
        
        # 转换set为list
        features["font_sizes"] = sorted(list(features["font_sizes"]))
        features["font_names"] = list(features["font_names"])
        features["font_colors"] = list(features["font_colors"])
        
        # 统计信息
        total_shapes = sum(len(s["shapes"]) for s in structure["slides"])
        features["format_statistics"] = {
            "total_shapes": total_shapes,
            "bold_percentage": (features["bold_count"] / total_shapes * 100) if total_shapes > 0 else 0,
            "unique_font_sizes": len(features["font_sizes"]),
            "unique_font_names": len(features["font_names"])
        }
        
        return features

