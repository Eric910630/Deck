"""
文本提取器
提取文本元素的内容和样式信息
"""

from typing import Dict, Any, List, Optional
from loguru import logger
import re


class TextExtractor:
    """
    文本提取器
    提取文本内容、字体、大小、颜色等样式信息
    """
    
    def __init__(self):
        """初始化文本提取器"""
        logger.info("--- [TextExtractor]: Initialized")
    
    async def extract_text(self, text_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        提取文本信息
        
        Args:
            text_info: 文本信息（来自ElementAnalyzer）
            
        Returns:
            提取的文本信息，包含内容和样式
        """
        try:
            style = text_info.get('style', {})
            
            # 解析字体大小（从px转换为pt）
            font_size_pt = self._parse_font_size(style.get('fontSize', '14px'))
            
            # 解析颜色（从rgb/rgba转换为hex）
            color_hex = self._parse_color(style.get('color', '#000000'))
            
            # 解析字重
            font_weight = style.get('fontWeight', '400')
            is_bold = font_weight in ['bold', '600', '700', '800', '900']
            
            # 解析对齐方式
            text_align = style.get('textAlign', 'left')
            
            return {
                'text': text_info.get('text', ''),
                'position': text_info.get('position', {}),
                'size': text_info.get('size', {}),
                'style': {
                    'font_family': style.get('fontFamily', 'Arial'),
                    'font_size_pt': font_size_pt,
                    'color_hex': color_hex,
                    'is_bold': is_bold,
                    'text_align': text_align,
                    'line_height': style.get('lineHeight', '1.5'),
                }
            }
        except Exception as e:
            logger.warning(f"--- [TextExtractor]: Failed to extract text: {e}")
            return None
    
    async def extract_all_texts(self, texts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        提取所有文本
        
        Args:
            texts: 文本信息列表
            
        Returns:
            提取结果列表
        """
        logger.info(f"--- [TextExtractor]: Extracting {len(texts)} text elements...")
        
        extracted = []
        for text_info in texts:
            result = await self.extract_text(text_info)
            if result:
                extracted.append(result)
        
        logger.info(f"--- [TextExtractor]: Extracted {len(extracted)} text elements")
        return extracted
    
    def _parse_font_size(self, font_size_str: str) -> int:
        """
        解析字体大小（px转pt）
        
        Args:
            font_size_str: 字体大小字符串，如 "14px", "1.2em"
            
        Returns:
            字体大小（pt）
        """
        try:
            # 提取数字
            match = re.search(r'([\d.]+)', font_size_str)
            if match:
                size_value = float(match.group(1))
                
                # 如果是px，直接转换为pt（1px ≈ 0.75pt，但PPT中通常直接使用px值）
                if 'px' in font_size_str:
                    return int(size_value)
                # 如果是em，假设基础字体是14px
                elif 'em' in font_size_str:
                    return int(size_value * 14)
                else:
                    return int(size_value)
        except:
            pass
        
        return 14  # 默认值
    
    def _parse_color(self, color_str: str) -> str:
        """
        解析颜色（rgb/rgba转hex）
        
        Args:
            color_str: 颜色字符串，如 "rgb(24, 144, 255)", "rgba(0,0,0,0.85)", "#1890ff"
            
        Returns:
            hex颜色字符串，如 "#1890ff"
        """
        try:
            # 如果是hex格式，直接返回
            if color_str.startswith('#'):
                return color_str
            
            # 解析rgb/rgba
            rgb_match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', color_str)
            if rgb_match:
                r = int(rgb_match.group(1))
                g = int(rgb_match.group(2))
                b = int(rgb_match.group(3))
                return f"#{r:02x}{g:02x}{b:02x}"
        except:
            pass
        
        return "#000000"  # 默认黑色

