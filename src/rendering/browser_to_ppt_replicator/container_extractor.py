"""
容器提取器
截图容器元素并保存为PNG
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from playwright.async_api import ElementHandle
from loguru import logger


class ContainerExtractor:
    """
    容器提取器
    截图容器元素并保存为PNG文件
    """
    
    def __init__(self, output_dir: Path):
        """
        初始化容器提取器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.container_count = 0
        logger.info(f"--- [ContainerExtractor]: Initialized, output_dir: {self.output_dir}")
    
    async def extract_container(
        self,
        container_info: Dict[str, Any],
        container_index: int,
        hide_text: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        提取容器（截图）
        
        【新架构原则】：混合渲染法
        - 如果 hide_text=True：隐藏文字后截图（用于混合渲染，文字单独插入）
        - 如果 hide_text=False：直接截图（文字包含在图片中）
        
        Args:
            container_info: 容器信息（来自ElementAnalyzer）
            container_index: 容器索引
            hide_text: 是否隐藏文字后截图（默认True，用于混合渲染）
            
        Returns:
            容器提取结果，包含图片路径和位置信息
        """
        try:
            element: ElementHandle = container_info['element']
            page = element.page if hasattr(element, 'page') else None
            
            # 生成文件名
            filename = f"container_{container_index:03d}.png"
            output_path = self.output_dir / filename
            
            # 【混合渲染法】：隐藏文字后截图
            if hide_text and page:
                try:
                    # 获取元素选择器
                    element_id = await element.get_attribute('id')
                    selector = f"#{element_id}" if element_id else None
                    
                    if selector:
                        # 临时隐藏文字
                        await page.evaluate(f"""
                            (selector) => {{
                                const el = document.querySelector(selector);
                                if (el) {{
                                    el.setAttribute('data-original-color', el.style.color || '');
                                    el.style.color = 'transparent';
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
                        
                        # 截图（包含阴影，透明背景）
                        await element.screenshot(
                            path=str(output_path),
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
                        
                        logger.debug(f"--- [ContainerExtractor]: 【混合渲染】容器截图完成（文字已隐藏）: {filename}")
                    else:
                        # 如果没有选择器，直接截图
                        await element.screenshot(path=str(output_path))
                        logger.debug(f"--- [ContainerExtractor]: 容器截图完成（无选择器，直接截图）: {filename}")
                except Exception as e:
                    logger.warning(f"--- [ContainerExtractor]: 隐藏文字失败，使用直接截图: {e}")
                    await element.screenshot(path=str(output_path))
            else:
                # 直接截图（文字包含在图片中）
                await element.screenshot(path=str(output_path))
                logger.debug(f"--- [ContainerExtractor]: 容器截图完成（文字包含）: {filename}")
            
            return {
                'image_path': str(output_path),
                'position': container_info['position'],
                'size': container_info['size'],
                'style': container_info.get('style', {}),
                'z_index': container_info.get('z_index', 0),
                'hide_text': hide_text  # 记录是否隐藏了文字
            }
        except Exception as e:
            logger.warning(f"--- [ContainerExtractor]: Failed to extract container {container_index}: {e}")
            return None
    
    async def extract_all_containers(
        self,
        containers: list[Dict[str, Any]],
        hide_text: bool = True
    ) -> List[Dict[str, Any]]:
        """
        提取所有容器
        
        【新架构原则】：支持混合渲染法
        - hide_text=True：隐藏文字后截图（容器用图片，文字单独插入）
        - hide_text=False：直接截图（文字包含在图片中）
        
        Args:
            containers: 容器信息列表
            hide_text: 是否隐藏文字后截图（默认True）
            
        Returns:
            提取结果列表
        """
        logger.info(f"--- [ContainerExtractor]: Extracting {len(containers)} containers (hide_text={hide_text})...")
        
        # 按z-index排序（从后往前，先处理底层）
        sorted_containers = sorted(containers, key=lambda c: c.get('z_index', 0))
        
        extracted = []
        for idx, container in enumerate(sorted_containers):
            result = await self.extract_container(container, idx, hide_text=hide_text)
            if result:
                extracted.append(result)
        
        logger.info(f"--- [ContainerExtractor]: Extracted {len(extracted)} containers")
        return extracted

