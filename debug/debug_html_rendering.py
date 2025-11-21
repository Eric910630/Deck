"""
调试HTML渲染效果
使用Playwright打开生成的HTML文件并截图，查看实际布局效果
"""

import asyncio
from pathlib import Path
from loguru import logger
from playwright.async_api import async_playwright

async def debug_html_rendering(html_dir: Path, output_dir: Path):
    """
    调试HTML渲染效果
    
    Args:
        html_dir: HTML文件目录
        output_dir: 截图输出目录
    """
    html_files = sorted(html_dir.glob("*.html"))
    
    if not html_files:
        logger.error(f"未找到HTML文件: {html_dir}")
        return
    
    logger.info(f"找到{len(html_files)}个HTML文件")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 非无头模式，可以看到浏览器
        page = await browser.new_page(
            viewport={'width': 1920, 'height': 1080}
        )
        
        for html_file in html_files:
            logger.info(f"处理: {html_file.name}")
            
            # 读取HTML内容
            html_content = html_file.read_text(encoding='utf-8')
            
            # 加载HTML
            await page.set_content(html_content, wait_until='networkidle')
            await page.wait_for_timeout(2000)  # 等待渲染完成
            
            # 截图
            screenshot_path = output_dir / f"{html_file.stem}.png"
            await page.screenshot(path=str(screenshot_path), full_page=True)
            logger.info(f"  → 截图保存: {screenshot_path}")
            
            # 获取页面元素信息（用于调试）
            elements_info = await page.evaluate("""
                () => {
                    const cards = Array.from(document.querySelectorAll('.card'));
                    return cards.map(card => ({
                        text: card.textContent.substring(0, 100),
                        className: card.className,
                        boundingBox: card.getBoundingClientRect(),
                        computedStyle: {
                            display: window.getComputedStyle(card).display,
                            gridColumn: window.getComputedStyle(card).gridColumn,
                            gridRow: window.getComputedStyle(card).gridRow,
                            padding: window.getComputedStyle(card).padding,
                            margin: window.getComputedStyle(card).margin,
                        }
                    }));
                }
            """)
            
            logger.info(f"  → 找到{len(elements_info)}个.card元素")
            for i, elem in enumerate(elements_info):
                logger.info(f"    元素{i+1}: {elem['className']}")
                logger.info(f"      位置: ({elem['boundingBox']['x']:.0f}, {elem['boundingBox']['y']:.0f})")
                logger.info(f"      尺寸: {elem['boundingBox']['width']:.0f} x {elem['boundingBox']['height']:.0f}")
                logger.info(f"      Grid: {elem['computedStyle']['gridColumn']} / {elem['computedStyle']['gridRow']}")
                logger.info(f"      内容预览: {elem['text'][:50]}...")
        
        # 保持浏览器打开一段时间，方便查看
        logger.info("浏览器将保持打开30秒，请查看渲染效果...")
        await page.wait_for_timeout(30000)
        
        await browser.close()

if __name__ == "__main__":
    # 查找最新的HTML调试目录
    base_dir = Path(__file__).parent
    output_base = base_dir / "output"
    
    # 查找最新的html_debug目录
    html_dirs = list(output_base.glob("*/html_debug"))
    if not html_dirs:
        logger.error("未找到html_debug目录，请先运行一次测试生成HTML文件")
        exit(1)
    
    latest_html_dir = max(html_dirs, key=lambda p: p.stat().st_mtime)
    logger.info(f"使用HTML目录: {latest_html_dir}")
    
    # 截图输出目录
    screenshot_dir = base_dir / "html_debug_screenshots"
    
    asyncio.run(debug_html_rendering(latest_html_dir, screenshot_dir))
    logger.info(f"✅ 调试完成！截图保存在: {screenshot_dir}")

