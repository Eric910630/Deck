"""
DOM分析器
负责在Playwright中执行JS，提取所有元素的精确计算样式
"""

from typing import Dict, Any, List

from playwright.async_api import Page

from loguru import logger


class DOMAnalyzer:
    """
    DOM样式提取器
    提取所有带有 data-ppt-element 属性的元素的 Computed Style
    """
    
    async def extract_layout_data(self, page: Page) -> List[Dict[str, Any]]:
        """
        提取布局数据
        返回一个包含所有元素样式信息的列表
        """
        logger.info("--- [DOMAnalyzer]: 开始提取DOM样式数据...")
        
        # 等待页面稳定
        await page.wait_for_load_state('networkidle')
        
        # 执行浏览器端脚本
        elements_data = await page.evaluate("""
            () => {
                const results = [];
                
                // 查找所有标记元素
                const elements = document.querySelectorAll('[data-ppt-element]');
                
                elements.forEach(el => {
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    
                    // 辅助函数：解析颜色
                    const parseColor = (colorStr) => {
                        if (!colorStr || colorStr === 'rgba(0, 0, 0, 0)' || colorStr === 'transparent') return null;
                        return colorStr;
                    };

                    // 辅助函数：解析px值
                    const parsePx = (str) => parseFloat(str) || 0;

                    // 【关键修复】优先读取 data-ppt-style 属性，绕过 CSS 解析的坑
                    const manualBorderColor = el.getAttribute('data-ppt-style-border-color');

                    const data = {
                        id: el.getAttribute('data-ppt-element-id'),
                        type: el.getAttribute('data-ppt-element-type') || 'text',
                        content: el.innerText,
                        
                        // 几何信息 (相对于视口，假设无滚动)
                        geometry: {
                            x: rect.left,
                            y: rect.top,
                            width: rect.width,
                            height: rect.height
                        },
                        
                        // 视觉样式
                        style: {
                            backgroundColor: parseColor(style.backgroundColor),
                            
                            // 边框
                            borderTopWidth: parsePx(style.borderTopWidth),
                            borderTopColor: manualBorderColor || parseColor(style.borderTopColor),
                            borderLeftWidth: parsePx(style.borderLeftWidth),
                            borderLeftColor: parseColor(style.borderLeftColor),
                            // PPT只支持统一边框，取Top作为参考，或者Left
                            borderWidth: parsePx(style.borderWidth) || parsePx(style.borderTopWidth),
                            borderColor: parseColor(style.borderColor) || parseColor(style.borderTopColor),
                            
                            // 圆角 (取左上角作为参考)
                            borderRadius: parsePx(style.borderTopLeftRadius),
                            
                            // 阴影
                            boxShadow: style.boxShadow !== 'none' ? style.boxShadow : null,
                            
                            // 字体
                            color: parseColor(style.color),
                            fontSize: parsePx(style.fontSize),
                            fontWeight: style.fontWeight,
                            fontFamily: style.fontFamily,
                            textAlign: style.textAlign,
                            lineHeight: style.lineHeight,
                            
                            // 布局对齐
                            display: style.display,
                            alignItems: style.alignItems,
                            justifyContent: style.justifyContent
                        }
                    };
                    
                    results.push(data);
                });
                
                return results;
            }
        """)
        
        logger.info(f"--- [DOMAnalyzer]: 提取了 {len(elements_data)} 个元素的样式数据")
        
        # 【调试日志】打印每个元素的 backgroundColor
        for elem in elements_data:
            elem_id = elem.get('id', 'unknown')
            elem_type = elem.get('type', 'unknown')
            bg_color = elem.get('style', {}).get('backgroundColor', 'null')
            logger.info(f"--- [DOMAnalyzer]: 元素 {elem_id} (type={elem_type}) backgroundColor={bg_color}")
        
        return elements_data

