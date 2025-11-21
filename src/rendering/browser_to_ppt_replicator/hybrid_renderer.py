"""
混合渲染器（Hybrid Renderer）
实现"容器用图片，内容用原生文本"的混合渲染方案

核心原则：
1. LLM 负责"定性"（审美和结构）- 生成流式布局 HTML
2. 浏览器负责"定量"（精确计算和渲染）- 计算坐标并截图
3. PPT 负责"组装"（图片背景 + 可编辑文本）
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from loguru import logger

try:
    from playwright.async_api import Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class HybridRenderer:
    """
    混合渲染器
    
    工作流程：
    1. 加载流式布局 HTML（Flex/Grid）
    2. 等待浏览器渲染完成
    3. 提取所有元素的坐标和样式
    4. 为卡片元素截图（隐藏文字，保留样式）
    5. 返回元素信息和截图路径
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        初始化混合渲染器
        
        Args:
            output_dir: 截图输出目录
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright is required. "
                "Install with: pip install playwright && playwright install chromium"
            )
        
        self.output_dir = output_dir or Path("replicated_outputs/containers")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"--- [HybridRenderer]: Initialized (output_dir: {self.output_dir})")
    
    async def extract_layout_data(self, page: Page) -> Dict[str, Any]:
        """
        从浏览器页面提取布局数据
        
        核心逻辑：
        - 识别所有带有 data-ppt-element 属性的元素
        - 提取坐标、样式、内容
        - 为卡片元素准备截图
        
        Args:
            page: Playwright Page 对象
            
        Returns:
            {
                'elements': [
                    {
                        'id': 'element_id',
                        'type': 'card|title|text',
                        'content': '文本内容',
                        'position': {'x': 100, 'y': 200},
                        'size': {'width': 300, 'height': 200},
                        'style': {
                            'color': '#000',
                            'fontSize': '16px',
                            'backgroundColor': '#fff'
                        },
                        'screenshot_path': 'path/to/screenshot.png'  # 仅卡片有
                    }
                ]
            }
        """
        logger.info("--- [HybridRenderer]: 开始提取布局数据...")
        
        # 等待页面完全渲染
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(500)  # 额外等待 CSS 动画和布局稳定
        
        # 提取所有标记的元素
        elements_data = await page.evaluate("""
            () => {
                const results = [];
                
                // 查找所有带有 data-ppt-element 属性的元素
                // 如果没有，则查找 .ppt-element 类名的元素
                const elements = document.querySelectorAll('[data-ppt-element], .ppt-element');
                
                elements.forEach(el => {
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    
                    // 提取基本信息
                    const elementData = {
                        id: el.id || el.getAttribute('data-ppt-element-id') || '',
                        type: el.getAttribute('data-ppt-element-type') || 
                              el.className.match(/element-(card|title|text)/)?.[1] || 'text',
                        content: el.innerText || el.textContent || '',
                        position: {
                            x: rect.left + window.scrollX,
                            y: rect.top + window.scrollY
                        },
                        size: {
                            width: rect.width,
                            height: rect.height
                        },
                        style: {
                            color: style.color,
                            fontSize: style.fontSize,
                            fontWeight: style.fontWeight,
                            fontFamily: style.fontFamily,
                            backgroundColor: style.backgroundColor,
                            textAlign: style.textAlign,
                            lineHeight: style.lineHeight
                        },
                        // 用于截图的选择器
                        selector: el.id ? `#${el.id}` : 
                                 el.className ? `.${el.className.split(' ')[0]}` : null
                    };
                    
                    results.push(elementData);
                });
                
                return results;
            }
        """)
        
        logger.info(f"--- [HybridRenderer]: 找到 {len(elements_data)} 个元素")
        
        # 为卡片元素截图（隐藏文字，保留样式）
        for elem in elements_data:
            if elem['type'] == 'card' and elem.get('selector'):
                screenshot_path = await self._screenshot_card_without_text(
                    page, elem, len(elements_data)
                )
                if screenshot_path:
                    elem['screenshot_path'] = str(screenshot_path)
        
        return {
            'elements': elements_data
        }
    
    async def _screenshot_card_without_text(
        self, 
        page: Page, 
        element_data: Dict[str, Any],
        total_elements: int
    ) -> Optional[Path]:
        """
        为卡片元素截图（隐藏文字，保留样式）
        
        策略：
        1. 临时隐藏文字（color: transparent）
        2. 截图（包含阴影和圆角）
        3. 恢复文字
        
        Args:
            page: Playwright Page 对象
            element_data: 元素数据
            total_elements: 总元素数量（用于生成唯一文件名）
            
        Returns:
            截图文件路径
        """
        element_id = element_data.get('id', '')
        selector = element_data.get('selector')
        
        if not selector:
            logger.warning(f"--- [HybridRenderer]: 元素 {element_id} 没有选择器，跳过截图")
            return None
        
        try:
            # 生成唯一文件名
            screenshot_filename = f"card_{element_id}_{total_elements}.png"
            screenshot_path = self.output_dir / screenshot_filename
            
            # 临时隐藏文字，保留样式
            await page.evaluate(f"""
                (selector) => {{
                    const el = document.querySelector(selector);
                    if (el) {{
                        // 保存原始颜色
                        el.setAttribute('data-original-color', el.style.color || '');
                        // 隐藏文字
                        el.style.color = 'transparent';
                        // 确保子元素文字也隐藏
                        const children = el.querySelectorAll('*');
                        children.forEach(child => {{
                            child.setAttribute('data-original-color', child.style.color || '');
                            child.style.color = 'transparent';
                        }});
                    }}
                }}
            """, selector)
            
            # 等待样式应用
            await page.wait_for_timeout(100)
            
            # 截图（包含阴影，需要稍微扩大截图区域）
            # 计算包含阴影的区域（通常阴影向外扩展 8-12px）
            shadow_padding = 12
            x = max(0, element_data['position']['x'] - shadow_padding)
            y = max(0, element_data['position']['y'] - shadow_padding)
            width = element_data['size']['width'] + shadow_padding * 2
            height = element_data['size']['height'] + shadow_padding * 2
            
            await page.locator(selector).screenshot(
                path=str(screenshot_path),
                omit_background=True  # 透明背景，保留圆角
            )
            
            # 恢复文字
            await page.evaluate(f"""
                (selector) => {{
                    const el = document.querySelector(selector);
                    if (el) {{
                        const originalColor = el.getAttribute('data-original-color');
                        if (originalColor) {{
                            el.style.color = originalColor;
                        }}
                        const children = el.querySelectorAll('*');
                        children.forEach(child => {{
                            const childOriginalColor = child.getAttribute('data-original-color');
                            if (childOriginalColor) {{
                                child.style.color = childOriginalColor;
                            }}
                        }});
                    }}
                }}
            """, selector)
            
            logger.info(f"--- [HybridRenderer]: ✅ 卡片截图完成: {screenshot_path}")
            return screenshot_path
            
        except Exception as e:
            logger.error(f"--- [HybridRenderer]: ❌ 卡片截图失败 {element_id}: {e}", exc_info=True)
            return None

