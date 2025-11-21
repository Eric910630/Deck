#!/usr/bin/env python3
"""
测试画布生成器
使用Playwright验证HTML渲染效果
"""

import asyncio
from pathlib import Path
from html_canvas_generator import HTMLCanvasGenerator
from loguru import logger


async def test_canvas_generator():
    """测试画布生成器"""
    logger.info("="*80)
    logger.info("测试HTML画布生成器")
    logger.info("="*80)
    
    # 创建画布生成器
    generator = HTMLCanvasGenerator()
    
    # 定义测试元素（使用坐标系：左下角为原点）
    test_elements = [
        {
            'id': 'title-1',
            'type': 'title',
            'content': '技术产品概览与价值主张',
            'coordinates': {
                'left': 100,      # 距离左边缘100px
                'bottom': 900,    # 距离下边缘900px（即距离顶部约80px）
                'width': 800,
                'height': 80
            }
        },
        {
            'id': 'card-1',
            'type': 'card',
            'content': '降低运营成本40-60%',
            'coordinates': {
                'left': 100,
                'bottom': 700,
                'width': 300,
                'height': 150
            }
        },
        {
            'id': 'card-2',
            'type': 'card',
            'content': '提升转化效率20-35%',
            'coordinates': {
                'left': 450,
                'bottom': 700,
                'width': 300,
                'height': 150
            }
        },
        {
            'id': 'card-3',
            'type': 'card',
            'content': '加速业务智能化转型',
            'coordinates': {
                'left': 800,
                'bottom': 700,
                'width': 300,
                'height': 150
            }
        }
    ]
    
    # 生成HTML
    html_content = generator.create_canvas_html(
        elements=test_elements,
        show_grid=True
    )
    
    # 保存HTML文件
    output_file = Path("html_output/test_canvas.html")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html_content, encoding='utf-8')
    logger.info(f"✅ HTML文件已保存: {output_file}")
    
    # 使用Playwright验证渲染效果
    try:
        from playwright.async_api import async_playwright
        
        logger.info("--- 使用Playwright验证HTML渲染...")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            
            # 加载HTML文件
            html_path = output_file.absolute().as_uri()
            await page.goto(html_path)
            
            # 等待页面加载
            await page.wait_for_load_state('networkidle')
            
            # 获取画布尺寸
            canvas = page.locator('#canvas')
            canvas_box = await canvas.bounding_box()
            logger.info(f"画布尺寸: {canvas_box['width']}px × {canvas_box['height']}px")
            
            # 检查元素位置
            for elem in test_elements:
                elem_id = elem['id']
                elem_locator = page.locator(f'#{elem_id}')
                if await elem_locator.count() > 0:
                    elem_box = await elem_locator.bounding_box()
                    logger.info(f"元素 {elem_id}:")
                    logger.info(f"  位置: left={elem_box['x']:.1f}px, top={elem_box['y']:.1f}px")
                    logger.info(f"  尺寸: width={elem_box['width']:.1f}px, height={elem_box['height']:.1f}px")
                else:
                    logger.warning(f"元素 {elem_id} 未找到")
            
            # 截图
            screenshot_path = Path("html_output/test_canvas_screenshot.png")
            await page.screenshot(path=str(screenshot_path), full_page=True)
            logger.info(f"✅ 截图已保存: {screenshot_path}")
            
            # 保持浏览器打开5秒以便查看
            await asyncio.sleep(5)
            await browser.close()
            
    except ImportError:
        logger.warning("Playwright未安装，跳过渲染验证")
        logger.info("安装命令: pip install playwright && playwright install chromium")
    except Exception as e:
        logger.error(f"Playwright验证失败: {e}", exc_info=True)
    
    logger.info("="*80)
    logger.info("测试完成")
    logger.info("="*80)


if __name__ == "__main__":
    asyncio.run(test_canvas_generator())

