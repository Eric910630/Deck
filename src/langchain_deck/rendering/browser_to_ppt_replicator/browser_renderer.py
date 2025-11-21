"""
浏览器渲染器
使用Playwright渲染HTML内容（Ant Design组件）
"""

from typing import Optional
from pathlib import Path
from loguru import logger

try:
    from playwright.async_api import async_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not installed. Install with: pip install playwright && playwright install chromium")


class BrowserRenderer:
    """
    浏览器渲染器
    使用Playwright渲染HTML内容，支持Ant Design/AntV组件
    """
    
    # 16:9画布尺寸
    CANVAS_WIDTH = 1920
    CANVAS_HEIGHT = 1080
    
    def __init__(self):
        """初始化浏览器渲染器"""
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright is required. "
                "Install with: pip install playwright && playwright install chromium"
            )
        self.browser: Optional[Browser] = None
        logger.info("--- [BrowserRenderer]: Initialized")
    
    async def render_html(self, html_content: str) -> Page:
        """
        渲染HTML内容
        
        Args:
            html_content: HTML内容字符串
            
        Returns:
            Playwright Page对象
        """
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        
        page = await self.browser.new_page(
            viewport={
                'width': self.CANVAS_WIDTH,
                'height': self.CANVAS_HEIGHT
            }
        )
        
        # 加载HTML内容
        await page.set_content(html_content, wait_until='networkidle')
        
        # 等待页面完全渲染（Ant Design组件可能需要时间）
        await page.wait_for_timeout(1000)
        
        logger.info(f"--- [BrowserRenderer]: HTML rendered (viewport: {self.CANVAS_WIDTH}x{self.CANVAS_HEIGHT})")
        return page
    
    async def render_html_file(self, html_file_path: Path) -> Page:
        """
        从文件渲染HTML
        
        Args:
            html_file_path: HTML文件路径
            
        Returns:
            Playwright Page对象
        """
        html_content = html_file_path.read_text(encoding='utf-8')
        return await self.render_html(html_content)
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            self.browser = None
            logger.info("--- [BrowserRenderer]: Browser closed")
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()

