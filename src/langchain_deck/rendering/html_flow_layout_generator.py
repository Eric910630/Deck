"""
流式布局 HTML 生成器
按照新架构原则：LLM 负责"定性"，生成流式布局 HTML（Flex/Grid）

核心原则：
1. 不使用绝对定位（position: absolute）
2. 使用 Ant Design 的 Flex/Grid 布局
3. 应用 Design Tokens（CSS 变量）
4. 为每个元素添加 data-ppt-element 属性，便于浏览器提取坐标
"""

from typing import Dict, Any, List, Optional
from loguru import logger
from ant_design_theme import ant_design_theme


class FlowLayoutHTMLGenerator:
    """
    流式布局 HTML 生成器
    
    生成符合 Ant Design 规范的流式布局 HTML
    让浏览器负责计算坐标，而不是 Python 计算
    """
    
    CANVAS_WIDTH = 1920
    CANVAS_HEIGHT = 1080
    
    def __init__(self):
        """初始化流式布局生成器"""
        logger.info("--- [FlowLayoutHTMLGenerator]: Initialized")
    
    def generate_flow_layout_html(
        self,
        layout_structure: Dict[str, Any],
        polished_slide: Dict[str, Any],
        color_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        生成流式布局 HTML
        
        Args:
            layout_structure: 布局结构（Ant Design 组件树）
            polished_slide: 润色后的幻灯片内容
            color_config: 颜色配置
            
        Returns:
            完整的 HTML 字符串
        """
        # 生成 CSS（包含 Design Tokens）
        css = self._generate_css_with_tokens()
        
        # 生成 HTML 结构（Flex/Grid 布局）
        html_body = self._generate_flow_layout_body(
            layout_structure, polished_slide, color_config
        )
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{polished_slide.get('title', 'Slide')}</title>
    <style>
        {css}
    </style>
</head>
<body>
    {html_body}
</body>
</html>"""
        
        return html
    
    def _generate_css_with_tokens(self) -> str:
        """
        生成包含 Design Tokens 的 CSS
        
        使用 CSS 变量统一管理样式
        """
        return f"""
        :root {{
            /* --- Ant Design Color Tokens --- */
            --ant-color-primary: #1677FF;
            --ant-color-success: #52C41A;
            --ant-color-warning: #FA8C16;
            --ant-color-error: #F5222D;
            
            /* --- Text Colors --- */
            --ant-text-color: rgba(0, 0, 0, 0.88);
            --ant-text-color-secondary: rgba(0, 0, 0, 0.65);
            --ant-text-color-tertiary: rgba(0, 0, 0, 0.45);
            
            /* --- Backgrounds --- */
            --ant-bg-color-layout: #F0F2F5;
            --ant-bg-color-container: #FFFFFF;
            
            /* --- Borders & Shadows --- */
            --ant-border-color: #F0F0F0;
            --ant-border-radius-base: 8px;
            --ant-box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            width: {self.CANVAS_WIDTH}px;
            height: {self.CANVAS_HEIGHT}px;
            background-color: var(--ant-bg-color-layout);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            padding: 40px;
            /* 使用 Flex 布局，让浏览器自动计算位置 */
            display: flex;
            flex-direction: column;
        }}
        
        /* Ant Design 风格的卡片 */
        .ant-card {{
            background-color: var(--ant-bg-color-container);
            border-radius: var(--ant-border-radius-base);
            box-shadow: var(--ant-box-shadow);
            padding: 24px;
            border-top: 4px solid var(--ant-color-primary);
        }}
        
        /* 标题样式 */
        .ant-typography-title {{
            color: var(--ant-color-primary);
            font-size: 48px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 24px;
        }}
        
        /* 副标题样式 */
        .ant-typography-subtitle {{
            color: var(--ant-text-color-secondary);
            font-size: 24px;
            font-weight: 400;
            text-align: center;
            margin-bottom: 40px;
        }}
        
        /* Flex 容器 */
        .ant-flex {{
            display: flex;
        }}
        
        .ant-flex-row {{
            flex-direction: row;
        }}
        
        .ant-flex-column {{
            flex-direction: column;
        }}
        
        .ant-flex-center {{
            justify-content: center;
            align-items: center;
        }}
        
        .ant-flex-space-between {{
            justify-content: space-between;
        }}
        
        .ant-flex-gap-small {{
            gap: 16px;
        }}
        
        .ant-flex-gap-medium {{
            gap: 24px;
        }}
        
        .ant-flex-gap-large {{
            gap: 32px;
        }}
        """
    
    def _generate_flow_layout_body(
        self,
        layout_structure: Dict[str, Any],
        polished_slide: Dict[str, Any],
        color_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        生成流式布局的 HTML body
        
        根据布局结构生成 Flex/Grid 布局
        """
        # 提取元素
        visual_elements = polished_slide.get('visual_elements_detail', [])
        
        # 构建颜色映射
        color_map = {}
        if color_config:
            for elem_color in color_config.get('color_config', {}).get('element_colors', []):
                elem_id = elem_color.get('element_id', '')
                if elem_id:
                    color_map[elem_id] = elem_color
        
        # 生成标题
        title_html = ""
        title_elem = next((e for e in visual_elements if 'title' in e.get('element_type', '') and 'subtitle' not in e.get('element_type', '')), None)
        if title_elem:
            title_html = f"""
            <h1 class="ant-typography-title ppt-element" 
                data-ppt-element="true"
                data-ppt-element-id="{title_elem.get('element_id', '')}"
                data-ppt-element-type="title">
                {title_elem.get('title', '')}
            </h1>"""
        
        # 生成副标题
        subtitle_html = ""
        subtitle_elem = next((e for e in visual_elements if 'subtitle' in e.get('element_type', '')), None)
        if subtitle_elem:
            subtitle_html = f"""
            <p class="ant-typography-subtitle ppt-element"
               data-ppt-element="true"
               data-ppt-element-id="{subtitle_elem.get('element_id', '')}"
               data-ppt-element-type="text">
                {subtitle_elem.get('title', '')}<br/>{subtitle_elem.get('content', '')}
            </p>"""
        
        # 生成卡片（使用 Flex 布局）
        card_elements = [e for e in visual_elements if 'card' in e.get('element_type', '')]
        cards_html = ""
        if card_elements:
            cards_html = '<div class="ant-flex ant-flex-row ant-flex-center ant-flex-gap-medium" style="flex: 1; align-items: stretch;">'
            for card_elem in card_elements:
                elem_id = card_elem.get('element_id', '')
                # 确保有唯一的ID给子元素
                title_id = f"{elem_id}_title"
                content_id = f"{elem_id}_content"
                
                accent_color = color_map.get(elem_id, {}).get('border_color', '#1677FF')
                
                # 【关键修复】把颜色直接写入 data 属性，绕过 CSS 解析的坑
                cards_html += f"""
                <div class="ant-card ppt-element"
                     data-ppt-element="true"
                     data-ppt-element-id="{elem_id}"
                     data-ppt-element-type="card"
                     data-ppt-style-border-color="{accent_color}"
                     style="border-top-color: {accent_color}; flex: 1; position: relative;">
                    
                    <!-- 【修复】给内部标题添加 data-ppt-element 标记 -->
                    <h3 data-ppt-element="true"
                        data-ppt-element-id="{title_id}"
                        data-ppt-element-type="text"
                        style="margin: 0 0 12px 0; font-size: 20px; font-weight: 600; color: {accent_color};">
                        {card_elem.get('title', '')}
                    </h3>
                    
                    <!-- 【修复】给内部内容添加 data-ppt-element 标记 -->
                    <p data-ppt-element="true"
                       data-ppt-element-id="{content_id}"
                       data-ppt-element-type="text"
                       style="margin: 0; font-size: 14px; color: var(--ant-text-color-secondary); line-height: 1.6;">
                        {card_elem.get('content', '')}
                    </p>
                </div>"""
            cards_html += '</div>'
        
        # 组装完整 body
        body_html = f"""
        <div class="ant-flex ant-flex-column" style="height: 100%;">
            {title_html}
            {subtitle_html}
            {cards_html}
        </div>"""
        
        return body_html

