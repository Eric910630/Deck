"""
语义分析器
识别内容语义、主题分类、逻辑关系
"""

from typing import List, Dict, Any
from loguru import logger
import re


class SemanticAnalyzer:
    """语义分析器 - 识别内容语义和逻辑关系"""
    
    def __init__(self, structure_data: Dict[str, Any]):
        """
        初始化语义分析器
        
        Args:
            structure_data: 增强的结构数据（包含格式信息）
        """
        self.structure = structure_data
        logger.info("--- [SemanticAnalyzer]: Initialized")
    
    def identify_semantic_blocks(self) -> List[Dict[str, Any]]:
        """
        识别语义块（标题-内容结构）
        
        Returns:
            语义块列表
        """
        blocks = []
        current_block = None
        
        for slide in self.structure["slides"]:
            for shape in slide["shapes"]:
                if shape.get("text") and shape.get("text").strip():
                    # 判断是否为标题
                    is_heading = self._is_heading(shape)
                    
                    if is_heading:
                        # 保存之前的块
                        if current_block:
                            blocks.append(current_block)
                        
                        # 开始新块
                        current_block = {
                            "heading": shape.get("text", ""),
                            "heading_level": self._get_heading_level(shape),
                            "heading_format": shape.get("format", {}),
                            "slide_index": slide["slide_index"],
                            "content": []
                        }
                    else:
                        # 添加到当前块的内容
                        if current_block:
                            current_block["content"].append({
                                "text": shape.get("text", ""),
                                "format": shape.get("format", {}),
                                "slide_index": slide["slide_index"]
                            })
                        else:
                            # 如果没有标题，创建一个匿名块
                            current_block = {
                                "heading": None,
                                "heading_level": 0,
                                "heading_format": {},
                                "slide_index": slide["slide_index"],
                                "content": [{
                                    "text": shape.get("text", ""),
                                    "format": shape.get("format", {}),
                                    "slide_index": slide["slide_index"]
                                }]
                            }
        
        # 保存最后一个块
        if current_block:
            blocks.append(current_block)
        
        logger.info(f"--- [SemanticAnalyzer]: Identified {len(blocks)} semantic blocks")
        return blocks
    
    def _is_heading(self, shape: Dict[str, Any]) -> bool:
        """
        判断是否为标题
        
        判断规则（多维度）:
        1. 字体大小 >= 20pt 且加粗
        2. 占位符类型包含 TITLE/HEADING
        3. 文本长度 < 50 且全加粗
        4. 包含编号模式（1. 2. 3.）
        """
        format_info = shape.get("format", {})
        text = shape.get("text", "")
        placeholder_type = shape.get("placeholder_type", "")
        
        # 检查1: 字体大小和加粗
        font_size = format_info.get("font_size_pt") or 0
        is_bold = format_info.get("is_bold", False)
        if font_size and font_size >= 20 and is_bold:
            return True
        
        # 检查2: 占位符类型
        is_title_type = any(keyword in placeholder_type for keyword in ["TITLE", "HEADING", "CENTER_TITLE"])
        if is_title_type:
            return True
        
        # 检查3: 文本长度和格式
        is_short = len(text) < 50
        if is_short and is_bold:
            return True
        
        # 检查4: 编号模式
        has_numbering = bool(re.match(r'^[\d一二三四五六七八九十]+[\.、]', text))
        if has_numbering:
            return True
        
        return False
    
    def _get_heading_level(self, shape: Dict[str, Any]) -> int:
        """
        获取标题级别
        
        Returns:
            标题级别（1-3）
        """
        format_info = shape.get("format", {})
        font_size = format_info.get("font_size_pt", 0)
        placeholder_type = shape.get("placeholder_type", "")
        
        # 根据字体大小判断
        if font_size >= 24:
            return 1
        elif font_size >= 18:
            return 2
        elif "CENTER_TITLE" in placeholder_type:
            return 1
        elif "TITLE" in placeholder_type:
            return 2
        else:
            return 3
    
    def identify_topics(self, blocks: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """
        识别主题
        
        Args:
            blocks: 语义块列表
            
        Returns:
            主题字典，键是主题名，值是相关块列表
        """
        topics = {}
        keywords_patterns = {
            "业务相关": ["业务", "销售", "客户", "市场", "产品", "商业化", "运营", "转化"],
            "技术相关": ["技术", "系统", "平台", "开发", "实现", "AI", "智能", "算法"],
            "数据相关": ["数据", "分析", "统计", "报表", "指标", "数据中心", "数据平台"]
        }
        
        for block in blocks:
            # 构建块文本（标题+内容预览）
            block_text = block["heading"] or ""
            if block["content"]:
                content_preview = " ".join([c["text"][:50] for c in block["content"][:3]])
                block_text += " " + content_preview
            
            # 匹配关键词
            for topic, keywords in keywords_patterns.items():
                if any(keyword in block_text for keyword in keywords):
                    if topic not in topics:
                        topics[topic] = []
                    topics[topic].append({
                        "heading": block["heading"],
                        "heading_level": block["heading_level"],
                        "content_preview": [c["text"][:50] for c in block["content"][:2]]
                    })
                    break
        
        logger.info(f"--- [SemanticAnalyzer]: Identified {len(topics)} topics")
        return topics
    
    def identify_logical_relations(self, blocks: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """
        识别逻辑关系
        
        Args:
            blocks: 语义块列表
            
        Returns:
            逻辑关系字典
        """
        relations = {
            "sequential": [],
            "hierarchical": [],
            "comparative": []
        }
        
        # 顺序关系：连续的块
        for i in range(len(blocks) - 1):
            relations["sequential"].append({
                "from": blocks[i]["heading"] or f"块{i+1}",
                "to": blocks[i+1]["heading"] or f"块{i+2}",
                "from_index": i,
                "to_index": i + 1
            })
        
        # 层级关系：基于标题级别
        for i, block in enumerate(blocks):
            if block["heading_level"] > 0:
                relations["hierarchical"].append({
                    "heading": block["heading"],
                    "level": block["heading_level"],
                    "sub_items": len(block["content"]),
                    "block_index": i
                })
        
        logger.info(f"--- [SemanticAnalyzer]: Identified {len(relations['sequential'])} sequential, {len(relations['hierarchical'])} hierarchical relations")
        return relations

