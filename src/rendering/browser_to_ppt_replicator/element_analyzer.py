"""
元素分析器
识别和分析浏览器页面中的容器和文本元素
"""

from typing import List, Dict, Any, Optional
from playwright.async_api import Page, ElementHandle
from loguru import logger


class ElementAnalyzer:
    """
    元素分析器
    识别容器元素（Card、div等）和文本元素（Typography等）
    """
    
    # 容器元素选择器（按优先级）
    CONTAINER_SELECTORS = [
        '.card',               # 通用card类
        '[class*="card"]',     # 包含card的类名
        'div.card',            # div.card
        'section',             # HTML5 section
        'div[style*="background"]',  # 有背景色的div
        'div[style*="border"]',      # 有边框的div
    ]
    
    # 文本元素选择器
    TEXT_SELECTORS = [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',  # 标题
        'p',                                   # 段落
        '.ant-typography',                     # Ant Design Typography
        '[class*="typography"]',               # 包含typography的类名
        'span',                                # 行内文本
        'li',                                  # 列表项
    ]
    
    def __init__(self):
        """初始化元素分析器"""
        logger.info("--- [ElementAnalyzer]: Initialized")
    
    async def analyze_elements(self, page: Page) -> Dict[str, List[Dict[str, Any]]]:
        """
        分析页面元素
        
        Args:
            page: Playwright Page对象
            
        Returns:
            {
                'containers': [容器信息列表],
                'texts': [文本信息列表]
            }
        """
        logger.info("--- [ElementAnalyzer]: Analyzing page elements...")
        
        # 识别容器元素
        containers = await self._identify_containers(page)
        logger.info(f"--- [ElementAnalyzer]: Found {len(containers)} container elements")
        
        # 识别文本元素
        texts = await self._identify_texts(page)
        logger.info(f"--- [ElementAnalyzer]: Found {len(texts)} text elements")
        
        return {
            'containers': containers,
            'texts': texts
        }
    
    async def _identify_containers(self, page: Page) -> List[Dict[str, Any]]:
        """识别容器元素"""
        containers = []
        
        # 尝试所有容器选择器
        for selector in self.CONTAINER_SELECTORS:
            try:
                elements = await page.query_selector_all(selector)
                for elem in elements:
                    # 检查是否已经有父容器包含此元素
                    if not await self._is_nested_in_containers(elem, containers, page):
                        container_info = await self._extract_container_info(elem)
                        if container_info:
                            containers.append(container_info)
            except Exception as e:
                logger.debug(f"--- [ElementAnalyzer]: Selector '{selector}' failed: {e}")
        
        # 去重（基于位置和尺寸）
        containers = self._deduplicate_containers(containers)
        
        return containers
    
    async def _identify_texts(self, page: Page) -> List[Dict[str, Any]]:
        """识别文本元素"""
        texts = []
        
        # 尝试所有文本选择器
        for selector in self.TEXT_SELECTORS:
            try:
                elements = await page.query_selector_all(selector)
                for elem in elements:
                    text_info = await self._extract_text_info(elem)
                    if text_info and text_info.get('text', '').strip():
                        texts.append(text_info)
            except Exception as e:
                logger.debug(f"--- [ElementAnalyzer]: Selector '{selector}' failed: {e}")
        
        # 去重（基于位置）
        texts = self._deduplicate_texts(texts)
        
        return texts
    
    async def _extract_container_info(self, element: ElementHandle) -> Optional[Dict[str, Any]]:
        """提取容器元素信息"""
        try:
            # 获取位置和尺寸
            # 【重要】bounding_box()返回的坐标是相对于viewport的
            # 由于我们的HTML结构是 body > .canvas (padding: 24px) > .container > elements
            # 而viewport = body（没有滚动），所以坐标已经是相对于body的
            # 但是，元素的实际位置需要考虑canvas的padding
            box = await element.bounding_box()
            if not box:
                return None
            
            # 【修复】获取元素相对于body的实际位置
            # 使用getBoundingClientRect() + scrollX/Y获取相对于body的准确坐标
            # 这对于CSS Grid布局更准确
            try:
                rect_info = await element.evaluate("""
                    el => {
                        const rect = el.getBoundingClientRect();
                        // 获取body的位置（相对于viewport）
                        const bodyRect = document.body.getBoundingClientRect();
                        // 计算元素相对于body的位置
                        // 需要考虑scrollX/Y（虽然我们的页面没有滚动，但为了准确性还是加上）
                        return {
                            x: rect.left - bodyRect.left + window.scrollX,
                            y: rect.top - bodyRect.top + window.scrollY,
                            width: rect.width,
                            height: rect.height
                        };
                    }
                """)
                # 使用getBoundingClientRect计算的位置（相对于body）
                box['x'] = rect_info['x']
                box['y'] = rect_info['y']
                box['width'] = rect_info['width']
                box['height'] = rect_info['height']
                logger.debug(f"--- [ElementAnalyzer]: 使用getBoundingClientRect获取位置: ({box['x']:.1f}, {box['y']:.1f})")
            except Exception as e:
                logger.warning(f"--- [ElementAnalyzer]: Failed to get getBoundingClientRect position, using bounding_box: {e}")
                # 如果获取失败，使用bounding_box（相对于viewport）
                # 由于我们的页面没有滚动，viewport = body，所以可以直接使用
                pass
            
            # 获取样式
            style = await element.evaluate("""
                el => ({
                    backgroundColor: window.getComputedStyle(el).backgroundColor,
                    borderRadius: window.getComputedStyle(el).borderRadius,
                    border: window.getComputedStyle(el).border,
                    borderWidth: window.getComputedStyle(el).borderWidth,
                    borderColor: window.getComputedStyle(el).borderColor,
                    boxShadow: window.getComputedStyle(el).boxShadow,
                    padding: window.getComputedStyle(el).padding,
                    margin: window.getComputedStyle(el).margin,
                    zIndex: window.getComputedStyle(el).zIndex,
                })
            """)
            
            # 检查是否有可见的背景或边框（才认为是容器）
            has_background = (
                style['backgroundColor'] and 
                style['backgroundColor'] not in ['rgba(0, 0, 0, 0)', 'transparent']
            )
            has_border = (
                style['border'] and 
                style['border'] != '0px none rgb(0, 0, 0)'
            )
            
            if not (has_background or has_border):
                return None
            
            # 解析z-index
            z_index_str = style.get('zIndex', '0') or '0'
            try:
                z_index = int(z_index_str) if z_index_str != 'auto' else 0
            except:
                z_index = 0
            
            return {
                'element': element,
                'type': 'container',
                'position': {'x': box['x'], 'y': box['y']},
                'size': {'width': box['width'], 'height': box['height']},
                'style': style,
                'z_index': z_index
            }
        except Exception as e:
            logger.debug(f"--- [ElementAnalyzer]: Failed to extract container info: {e}")
            return None
    
    async def _extract_text_info(self, element: ElementHandle) -> Optional[Dict[str, Any]]:
        """提取文本元素信息"""
        try:
            # 获取文本内容
            text = await element.inner_text()
            if not text or not text.strip():
                return None
            
            # 获取位置和尺寸
            # 【重要】bounding_box()返回的坐标是相对于viewport的
            # 使用getBoundingClientRect() + scrollX/Y获取相对于body的准确坐标
            # 这对于CSS Grid布局更准确
            box = await element.bounding_box()
            if not box:
                return None
            
            # 【修复】获取元素相对于body的实际位置
            try:
                rect_info = await element.evaluate("""
                    el => {
                        const rect = el.getBoundingClientRect();
                        // 获取body的位置（相对于viewport）
                        const bodyRect = document.body.getBoundingClientRect();
                        // 计算元素相对于body的位置
                        // 需要考虑scrollX/Y（虽然我们的页面没有滚动，但为了准确性还是加上）
                        return {
                            x: rect.left - bodyRect.left + window.scrollX,
                            y: rect.top - bodyRect.top + window.scrollY,
                            width: rect.width,
                            height: rect.height
                        };
                    }
                """)
                # 使用getBoundingClientRect计算的位置（相对于body）
                box['x'] = rect_info['x']
                box['y'] = rect_info['y']
                box['width'] = rect_info['width']
                box['height'] = rect_info['height']
                logger.debug(f"--- [ElementAnalyzer]: 使用getBoundingClientRect获取文本位置: ({box['x']:.1f}, {box['y']:.1f})")
            except Exception as e:
                logger.warning(f"--- [ElementAnalyzer]: Failed to get getBoundingClientRect position, using bounding_box: {e}")
                # 如果获取失败，使用bounding_box（相对于viewport）
                # 由于我们的页面没有滚动，viewport = body，所以可以直接使用
                pass
            
            # 获取样式
            style = await element.evaluate("""
                el => ({
                    fontSize: window.getComputedStyle(el).fontSize,
                    fontFamily: window.getComputedStyle(el).fontFamily,
                    fontWeight: window.getComputedStyle(el).fontWeight,
                    color: window.getComputedStyle(el).color,
                    textAlign: window.getComputedStyle(el).textAlign,
                    lineHeight: window.getComputedStyle(el).lineHeight,
                    letterSpacing: window.getComputedStyle(el).letterSpacing,
                })
            """)
            
            return {
                'element': element,
                'type': 'text',
                'text': text.strip(),
                'position': {'x': box['x'], 'y': box['y']},
                'size': {'width': box['width'], 'height': box['height']},
                'style': style
            }
        except Exception as e:
            logger.debug(f"--- [ElementAnalyzer]: Failed to extract text info: {e}")
            return None
    
    async def _is_nested_in_containers(self, element: ElementHandle, containers: List[Dict], page: Page) -> bool:
        """检查元素是否嵌套在已有容器中"""
        try:
            elem_box = await element.bounding_box()
            if not elem_box:
                return False
            
            for container in containers:
                container_pos = container['position']
                container_size = container['size']
                
                # 检查元素是否在容器内
                if (elem_box['x'] >= container_pos['x'] and
                    elem_box['y'] >= container_pos['y'] and
                    elem_box['x'] + elem_box['width'] <= container_pos['x'] + container_size['width'] and
                    elem_box['y'] + elem_box['height'] <= container_pos['y'] + container_size['height']):
                    return True
            
            return False
        except:
            return False
    
    def _deduplicate_containers(self, containers: List[Dict]) -> List[Dict]:
        """去重容器（基于位置和尺寸）"""
        seen = set()
        unique = []
        
        for container in containers:
            pos = container['position']
            size = container['size']
            key = (int(pos['x']), int(pos['y']), int(size['width']), int(size['height']))
            
            if key not in seen:
                seen.add(key)
                unique.append(container)
        
        return unique
    
    def _deduplicate_texts(self, texts: List[Dict]) -> List[Dict]:
        """去重文本（基于位置和内容）"""
        seen = set()
        unique = []
        
        for text in texts:
            pos = text['position']
            content = text['text']
            key = (int(pos['x']), int(pos['y']), content[:50])  # 只取前50字符
            
            if key not in seen:
                seen.add(key)
                unique.append(text)
        
        return unique

