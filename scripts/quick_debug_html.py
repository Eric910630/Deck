"""
快速调试HTML渲染
直接生成一个示例HTML并截图查看
"""

import asyncio
from pathlib import Path
from loguru import logger
from playwright.async_api import async_playwright
from html_generator import HTMLGenerator

async def debug_sample_html():
    """生成示例HTML并截图"""
    
    # 生成示例HTML
    html_gen = HTMLGenerator()
    
    # 模拟一个典型的幻灯片内容
    sample_content_map = {
        "slide_0_placeholder_0": "外部合作生态构建",
        "slide_0_placeholder_1": "• 通过多元化外部合作渠道,建立完整的商业化生态体系\n• 渠道合作:与CIO协会等组织合作推广\n• 生态集成:对接电商平台、ERP等系统\n• 直销团队:业务增长顾问模式转型",
    }
    
    html_contents = html_gen.generate_from_content_map(sample_content_map)
    
    # generate_from_content_map返回列表，取第一个
    if isinstance(html_contents, list):
        html_content = html_contents[0] if html_contents else ""
    else:
        html_content = html_contents
    
    # 保存HTML文件
    html_file = Path("debug_sample.html")
    html_file.write_text(html_content, encoding='utf-8')
    logger.info(f"✅ 保存HTML到: {html_file}")
    
    # 使用Playwright打开并截图
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 非无头模式
        page = await browser.new_page(
            viewport={'width': 1920, 'height': 1080}
        )
        
        # 加载HTML
        await page.set_content(html_content, wait_until='networkidle')
        await page.wait_for_timeout(2000)
        
        # 截图
        screenshot_path = Path("debug_sample_screenshot.png")
        await page.screenshot(path=str(screenshot_path), full_page=True)
        logger.info(f"✅ 截图保存到: {screenshot_path}")
        
        # 获取元素信息
        elements_info = await page.evaluate("""
            () => {
                const cards = Array.from(document.querySelectorAll('.card'));
                const container = document.querySelector('.container');
                return {
                    cards: cards.map(card => ({
                        text: card.textContent.substring(0, 100),
                        className: card.className,
                        boundingBox: {
                            x: card.getBoundingClientRect().x,
                            y: card.getBoundingClientRect().y,
                            width: card.getBoundingClientRect().width,
                            height: card.getBoundingClientRect().height,
                        },
                        computedStyle: {
                            display: window.getComputedStyle(card).display,
                            gridColumn: window.getComputedStyle(card).gridColumn,
                            gridRow: window.getComputedStyle(card).gridRow,
                            padding: window.getComputedStyle(card).padding,
                            margin: window.getComputedStyle(card).margin,
                            backgroundColor: window.getComputedStyle(card).backgroundColor,
                            border: window.getComputedStyle(card).border,
                        }
                    })),
                    container: container ? {
                        boundingBox: {
                            width: container.getBoundingClientRect().width,
                            height: container.getBoundingClientRect().height,
                        },
                        computedStyle: {
                            display: window.getComputedStyle(container).display,
                            gridTemplateColumns: window.getComputedStyle(container).gridTemplateColumns,
                            gridTemplateRows: window.getComputedStyle(container).gridTemplateRows,
                            padding: window.getComputedStyle(container).padding,
                        }
                    } : null
                };
            }
        """)
        
        logger.info("="*80)
        logger.info("📊 页面元素分析:")
        logger.info("="*80)
        
        if elements_info['container']:
            logger.info(f"容器尺寸: {elements_info['container']['boundingBox']['width']:.0f} x {elements_info['container']['boundingBox']['height']:.0f}")
            logger.info(f"Grid列: {elements_info['container']['computedStyle']['gridTemplateColumns']}")
            logger.info(f"Grid行: {elements_info['container']['computedStyle']['gridTemplateRows']}")
            logger.info(f"容器内边距: {elements_info['container']['computedStyle']['padding']}")
        
        logger.info(f"\n找到 {len(elements_info['cards'])} 个.card元素:")
        for i, card in enumerate(elements_info['cards']):
            logger.info(f"\n  📦 卡片 {i+1}:")
            logger.info(f"    类名: {card['className']}")
            logger.info(f"    位置: ({card['boundingBox']['x']:.0f}, {card['boundingBox']['y']:.0f})")
            logger.info(f"    尺寸: {card['boundingBox']['width']:.0f} x {card['boundingBox']['height']:.0f}")
            logger.info(f"    Grid列: {card['computedStyle']['gridColumn']}")
            logger.info(f"    Grid行: {card['computedStyle']['gridRow']}")
            logger.info(f"    内边距: {card['computedStyle']['padding']}")
            logger.info(f"    背景色: {card['computedStyle']['backgroundColor']}")
            logger.info(f"    边框: {card['computedStyle']['border']}")
            logger.info(f"    内容预览: {card['text'][:80]}...")
        
        logger.info("\n" + "="*80)
        logger.info("💡 浏览器将保持打开30秒，请查看实际渲染效果...")
        logger.info("   如果发现问题，请记录：")
        logger.info("   1. 布局是否合理？")
        logger.info("   2. 间距是否合适？")
        logger.info("   3. 内容是否对齐？")
        logger.info("   4. 视觉层次是否清晰？")
        logger.info("="*80)
        
        await page.wait_for_timeout(30000)
        await browser.close()
    
    logger.info("✅ 调试完成！")

if __name__ == "__main__":
    asyncio.run(debug_sample_html())

