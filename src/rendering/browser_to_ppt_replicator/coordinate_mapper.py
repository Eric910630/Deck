"""
坐标映射器 - 24栅格系统
将浏览器坐标映射到PPT坐标
"""

from typing import Tuple, Dict
from pptx.util import Cm
from loguru import logger


class CoordinateMapper:
    """
    坐标映射器 - 24栅格系统
    
    浏览器端：1920px × 1080px (16:9)
    PPT端：33.867cm × 19.05cm (16:9)
    栅格系统：24列 × 13.5行（保持16:9比例）
    
    注意：HTML中有24px的padding，需要从坐标中减去
    """
    
    # 浏览器端尺寸
    BROWSER_WIDTH = 1920
    BROWSER_HEIGHT = 1080
    GRID_COLUMNS = 24
    GRID_ROWS = 13.5  # 1080 / 80 = 13.5 (保持16:9比例)
    
    # HTML Padding（与HTML生成器保持一致）
    HTML_PADDING = 24  # px
    
    # PPT端尺寸（16:9）
    PPT_WIDTH_CM = 33.867
    PPT_HEIGHT_CM = 19.05
    
    # 实际内容区域（减去padding）
    CONTENT_WIDTH = BROWSER_WIDTH - 2 * HTML_PADDING  # 1872px
    CONTENT_HEIGHT = BROWSER_HEIGHT - 2 * HTML_PADDING  # 1032px
    
    # PPT内容区域（等比例）
    PPT_CONTENT_WIDTH_CM = PPT_WIDTH_CM - 2 * (HTML_PADDING * PPT_WIDTH_CM / BROWSER_WIDTH)  # ≈ 33.02cm
    PPT_CONTENT_HEIGHT_CM = PPT_HEIGHT_CM - 2 * (HTML_PADDING * PPT_HEIGHT_CM / BROWSER_HEIGHT)  # ≈ 18.20cm
    
    # 栅格单元尺寸（基于内容区域）
    BROWSER_CELL_WIDTH = CONTENT_WIDTH / GRID_COLUMNS  # ≈ 78px
    BROWSER_CELL_HEIGHT = CONTENT_HEIGHT / GRID_ROWS   # ≈ 76.4px
    
    PPT_CELL_WIDTH_CM = PPT_CONTENT_WIDTH_CM / GRID_COLUMNS  # ≈ 1.38cm
    PPT_CELL_HEIGHT_CM = PPT_CONTENT_HEIGHT_CM / GRID_ROWS   # ≈ 1.35cm
    
    def browser_to_ppt(self, browser_x: float, browser_y: float) -> Tuple[float, float]:
        """
        浏览器坐标转PPT坐标（cm）
        
        Args:
            browser_x: 浏览器X坐标（px，相对于body）
            browser_y: 浏览器Y坐标（px，相对于body）
            
        Returns:
            (ppt_x, ppt_y) 单位：cm
        """
        # 【重要】减去HTML padding，得到相对于内容区域的坐标
        # 如果坐标在padding内，设为0（元素可能从padding边缘开始）
        content_x = max(0, browser_x - self.HTML_PADDING)
        content_y = max(0, browser_y - self.HTML_PADDING)
        
        # 映射到PPT内容区域
        ppt_x = (content_x / self.CONTENT_WIDTH) * self.PPT_CONTENT_WIDTH_CM
        ppt_y = (content_y / self.CONTENT_HEIGHT) * self.PPT_CONTENT_HEIGHT_CM
        
        logger.info(f"--- [CoordinateMapper]: 坐标映射")
        logger.info(f"    浏览器坐标: ({browser_x:.1f}px, {browser_y:.1f}px)")
        logger.info(f"    减去padding: ({browser_x - self.HTML_PADDING:.1f}px, {browser_y - self.HTML_PADDING:.1f}px)")
        logger.info(f"    内容区域坐标: ({content_x:.1f}px, {content_y:.1f}px)")
        logger.info(f"    内容区域尺寸: {self.CONTENT_WIDTH}px × {self.CONTENT_HEIGHT}px")
        logger.info(f"    PPT内容区域尺寸: {self.PPT_CONTENT_WIDTH_CM:.2f}cm × {self.PPT_CONTENT_HEIGHT_CM:.2f}cm")
        logger.info(f"    PPT坐标: ({ppt_x:.2f}cm, {ppt_y:.2f}cm)")
        logger.info(f"    比例: x={content_x/self.CONTENT_WIDTH:.4f}, y={content_y/self.CONTENT_HEIGHT:.4f}")
        
        return ppt_x, ppt_y
    
    def browser_size_to_ppt(self, browser_width: float, browser_height: float) -> Tuple[float, float]:
        """
        浏览器尺寸转PPT尺寸（cm）
        
        Args:
            browser_width: 浏览器宽度（px）
            browser_height: 浏览器高度（px）
            
        Returns:
            (ppt_width, ppt_height) 单位：cm
        """
        # 尺寸直接按比例映射（不需要减去padding）
        ppt_width = (browser_width / self.CONTENT_WIDTH) * self.PPT_CONTENT_WIDTH_CM
        ppt_height = (browser_height / self.CONTENT_HEIGHT) * self.PPT_CONTENT_HEIGHT_CM
        
        logger.info(f"--- [CoordinateMapper]: 尺寸映射")
        logger.info(f"    浏览器尺寸: {browser_width:.1f}px × {browser_height:.1f}px")
        logger.info(f"    内容区域尺寸: {self.CONTENT_WIDTH}px × {self.CONTENT_HEIGHT}px")
        logger.info(f"    PPT内容区域尺寸: {self.PPT_CONTENT_WIDTH_CM:.2f}cm × {self.PPT_CONTENT_HEIGHT_CM:.2f}cm")
        logger.info(f"    PPT尺寸: {ppt_width:.2f}cm × {ppt_height:.2f}cm")
        logger.info(f"    比例: w={browser_width/self.CONTENT_WIDTH:.4f}, h={browser_height/self.CONTENT_HEIGHT:.4f}")
        
        return ppt_width, ppt_height
    
    def browser_to_grid(self, browser_x: float, browser_y: float) -> Tuple[int, int]:
        """
        浏览器坐标转栅格坐标
        
        Args:
            browser_x: 浏览器X坐标（px）
            browser_y: 浏览器Y坐标（px）
            
        Returns:
            (grid_x, grid_y) 栅格坐标（0-23列，0-12行）
        """
        grid_x = int(browser_x / self.BROWSER_CELL_WIDTH)
        grid_y = int(browser_y / self.BROWSER_CELL_HEIGHT)
        
        # 限制在有效范围内
        grid_x = max(0, min(grid_x, self.GRID_COLUMNS - 1))
        grid_y = max(0, min(grid_y, int(self.GRID_ROWS) - 1))
        
        return grid_x, grid_y
    
    def grid_to_ppt(self, grid_x: int, grid_y: int, span_x: int = 1, span_y: int = 1) -> Dict[str, float]:
        """
        栅格坐标转PPT位置和尺寸
        
        Args:
            grid_x: 栅格X坐标（0-23）
            grid_y: 栅格Y坐标（0-12）
            span_x: 横向跨度（占几个栅格）
            span_y: 纵向跨度（占几个栅格）
            
        Returns:
            {'left': cm, 'top': cm, 'width': cm, 'height': cm}
        """
        return {
            'left': grid_x * self.PPT_CELL_WIDTH_CM,
            'top': grid_y * self.PPT_CELL_HEIGHT_CM,
            'width': span_x * self.PPT_CELL_WIDTH_CM,
            'height': span_y * self.PPT_CELL_HEIGHT_CM
        }
    
    def calculate_grid_span(self, browser_width: float, browser_height: float) -> Tuple[int, int]:
        """
        计算浏览器尺寸对应的栅格跨度
        
        Args:
            browser_width: 浏览器宽度（px）
            browser_height: 浏览器高度（px）
            
        Returns:
            (span_x, span_y) 栅格跨度
        """
        span_x = max(1, int(browser_width / self.BROWSER_CELL_WIDTH))
        span_y = max(1, int(browser_height / self.BROWSER_CELL_HEIGHT))
        return span_x, span_y

