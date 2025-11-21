"""
HTML画布生成器
先创建标准的16:9白色画布，建立坐标系，然后放置元素
"""

from typing import Dict, Any, List, Optional, Tuple
from loguru import logger


class HTMLCanvasGenerator:
    """
    HTML画布生成器
    按照正确的工作顺序：
    1. 先创建16:9白色画布
    2. 建立坐标系（左下角为原点）
    3. 绘制栅格标准尺
    4. 然后根据坐标放置元素
    """
    
    # 16:9画布尺寸（像素）
    CANVAS_WIDTH = 1920
    CANVAS_HEIGHT = 1080
    
    # 24栅格系统
    GRID_COLUMNS = 24
    GRID_ROWS = 13.5
    
    # 栅格单元尺寸（基于画布尺寸）
    CELL_WIDTH = CANVAS_WIDTH / GRID_COLUMNS  # 80px
    CELL_HEIGHT = CANVAS_HEIGHT / GRID_ROWS   # 80px
    
    def __init__(self):
        """初始化画布生成器"""
        logger.info("--- [HTMLCanvasGenerator]: Initialized")
    
    def create_canvas_html(
        self,
        elements: List[Dict[str, Any]],
        show_grid: bool = True
    ) -> str:
        """
        创建完整的HTML画布
        
        Args:
            elements: 元素列表，每个元素包含：
                - id: 元素ID
                - type: 元素类型（card, text, title等）
                - content: 内容
                - coordinates: 坐标信息
                    - left: 距离左边缘的像素
                    - right: 距离右边缘的像素（可选）
                    - top: 距离上边缘的像素
                    - bottom: 距离下边缘的像素（可选）
                    - width: 宽度（像素）
                    - height: 高度（像素）
            show_grid: 是否显示栅格标准尺
            
        Returns:
            完整的HTML字符串
        """
        # 1. 生成画布基础HTML结构
        canvas_html = self._generate_canvas_structure()
        
        # 2. 生成CSS样式（包含坐标系和栅格标准尺）
        css = self._generate_canvas_css(show_grid=show_grid)
        
        # 3. 生成栅格标准尺HTML（如果启用）
        grid_ruler_html = ""
        if show_grid:
            grid_ruler_html = self._generate_grid_ruler_html()
        
        # 4. 生成元素HTML（根据坐标放置）
        elements_html = self._generate_elements_html(elements)
        
        # 5. 组装完整HTML（栅格标准尺和元素都放在canvas内部）
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>16:9画布 - 坐标系演示</title>
    <style>
        {css}
    </style>
</head>
<body>
    {canvas_html.replace('<!-- 栅格标准尺和元素将放置在这里 -->', f'{grid_ruler_html}\n            {elements_html}')}
</body>
</html>"""
        
        return html
    
    def _generate_canvas_structure(self) -> str:
        """
        生成画布基础HTML结构
        创建一个16:9的白色画布容器
        """
        return f"""
    <!-- 16:9白色画布容器 -->
    <div id="canvas-container" class="canvas-container">
        <!-- 画布（左下角为坐标原点） -->
        <div id="canvas" class="canvas">
            <!-- 栅格标准尺和元素将放置在这里 -->
        </div>
    </div>"""
    
    def _generate_canvas_css(self, show_grid: bool = True) -> str:
        """
        生成画布CSS样式
        建立坐标系：左下角为原点
        应用 Ant Design Design Tokens
        """
        return f"""
        :root {{
            /* --- Ant Design Color Tokens --- */
            --ant-color-primary: #1677FF;
            --ant-color-success: #52C41A;
            --ant-color-warning: #FA8C16;
            --ant-color-error: #F5222D;
            
            /* --- Text Colors --- */
            --ant-text-color: rgba(0, 0, 0, 0.88);       /* 主文本 */
            --ant-text-color-secondary: rgba(0, 0, 0, 0.65); /* 次文本/副标题 */
            --ant-text-color-tertiary: rgba(0, 0, 0, 0.45);  /* 辅助文本 */
            
            /* --- Backgrounds --- */
            --ant-bg-color-layout: #F0F2F5;  /* 页面背景灰 */
            --ant-bg-color-container: #FFFFFF; /* 卡片背景白 */
            
            /* --- Borders & Shadows --- */
            --ant-border-color: #F0F0F0;
            --ant-border-radius-base: 8px;
            --ant-box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02);
            --ant-box-shadow-hover: 0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 9px 28px 8px rgba(0, 0, 0, 0.05);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            margin: 0;
            padding: 20px;
            background-color: #e6e6e6; /* 浏览器背景，非画布背景 */
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: flex-start; /* 改为顶部对齐，避免垂直居中导致的问题 */
            min-height: 100vh;
            /* 确保横版显示 */
            width: 100%;
            overflow-x: auto; /* 如果画布太宽，允许横向滚动 */
        }}
        
        /* 画布容器 */
        .canvas-container {{
            position: relative;
            width: {self.CANVAS_WIDTH}px;
            height: {self.CANVAS_HEIGHT}px;
            background: #ffffff; /* 白色画布 */
            border: 2px solid #d9d9d9;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        
        /* 画布（坐标系容器） */
        .canvas {{
            position: relative;
            width: 100%;
            height: 100%;
            /* 强制应用 Ant Design 页面背景色 */
            background-color: var(--ant-bg-color-layout) !important;
            /* 坐标系：左下角为原点 */
            /* CSS默认使用top-left原点，我们需要通过transform或计算来模拟左下角原点 */
        }}
        
        /* 栅格标准尺样式 */
        .grid-ruler {{
            position: absolute;
            pointer-events: none;
            z-index: 1;
        }}
        
        .grid-ruler-line {{
            stroke: #e8e8e8;
            stroke-width: 1;
            stroke-dasharray: 2, 2;
        }}
        
        .grid-ruler-label {{
            font-size: 10px;
            fill: #999;
            text-anchor: middle;
        }}
        
        /* 元素样式 */
        .element {{
            position: absolute;
            /* 坐标将通过style属性动态设置 */
        }}
        
        .element-card {{
            background: #ffffff;
            border: 1px solid #d9d9d9;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            padding: 16px;
            overflow: hidden;
        }}
        
        .element-text {{
            color: #262626;
            word-wrap: break-word;
            word-break: break-word;
            white-space: normal;
            font-size: 18px;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        
        .element-title {{
            font-size: 48px;
            font-weight: 700;
            color: #1890ff;
            margin: 0;
            padding: 0;
            line-height: 1.2;
        }}
        
        .element-body {{
            font-size: 16px;
            line-height: 1.6;
            color: #595959;
            margin: 0;
            padding: 0;
        }}
        
        /* 坐标原点标记 */
        .origin-marker {{
            position: absolute;
            left: 0;
            bottom: 0;
            width: 20px;
            height: 20px;
            background: #ff4d4f;
            border-radius: 50%;
            z-index: 1000;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .origin-marker::after {{
            content: 'O';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 12px;
            font-weight: bold;
        }}"""
    
    def _generate_grid_ruler_html(self) -> str:
        """
        生成栅格标准尺HTML
        在画布四周绘制24列×13.5行的栅格线
        """
        svg_lines = []
        svg_labels = []
        
        # 绘制垂直栅格线（24列）
        for col in range(self.GRID_COLUMNS + 1):
            x = col * self.CELL_WIDTH
            # 垂直线
            svg_lines.append(f'<line class="grid-ruler-line" x1="{x}" y1="0" x2="{x}" y2="{self.CANVAS_HEIGHT}"/>')
            # 底部标签
            svg_labels.append(f'<text class="grid-ruler-label" x="{x}" y="{self.CANVAS_HEIGHT + 15}" fill="#999">{col}</text>')
            # 顶部标签
            svg_labels.append(f'<text class="grid-ruler-label" x="{x}" y="-5" fill="#999">{col}</text>')
        
        # 绘制水平栅格线（13.5行，向上从底部开始）
        for row in range(int(self.GRID_ROWS) + 1):
            # CSS使用top定位，所以需要从顶部计算
            y_from_top = self.CANVAS_HEIGHT - (row * self.CELL_HEIGHT)
            # 水平线
            svg_lines.append(f'<line class="grid-ruler-line" x1="0" y1="{y_from_top}" x2="{self.CANVAS_WIDTH}" y2="{y_from_top}"/>')
            # 左侧标签（从底部开始，row=0是底部）
            svg_labels.append(f'<text class="grid-ruler-label" x="-15" y="{y_from_top + 4}" fill="#999">{row}</text>')
            # 右侧标签
            svg_labels.append(f'<text class="grid-ruler-label" x="{self.CANVAS_WIDTH + 15}" y="{y_from_top + 4}" fill="#999">{row}</text>')
        
        return f"""
            <!-- 栅格标准尺 -->
            <svg class="grid-ruler" width="{self.CANVAS_WIDTH}" height="{self.CANVAS_HEIGHT}" style="position: absolute; top: 0; left: 0;">
                {''.join(svg_lines)}
                {''.join(svg_labels)}
            </svg>
            
            <!-- 坐标原点标记（左下角） -->
            <div class="origin-marker" title="坐标原点 (0, 0)"></div>"""
    
    def _generate_elements_html(self, elements: List[Dict[str, Any]]) -> str:
        """
        生成元素HTML
        根据坐标信息放置元素
        
        Args:
            elements: 元素列表，每个元素包含坐标信息
            
        Returns:
            元素HTML字符串
        """
        elements_html = []
        
        for elem in elements:
            elem_id = elem.get('id', '')
            elem_type = elem.get('type', 'card')
            content = elem.get('content', '')
            coordinates = elem.get('coordinates', {})
            
            # 解析坐标
            # 坐标系：左下角为原点
            # CSS使用top-left原点，需要转换
            left = coordinates.get('left', 0)
            right = coordinates.get('right')
            top = coordinates.get('top')
            bottom = coordinates.get('bottom', 0)
            width = coordinates.get('width', 200)
            height = coordinates.get('height', 100)
            
            # 计算CSS位置（从左下角原点转换为top-left原点）
            css_left = left
            if right is not None:
                css_left = self.CANVAS_WIDTH - right - width
            
            css_top = None
            if top is not None:
                css_top = top
            elif bottom is not None:
                # 从底部距离转换为顶部距离
                css_top = self.CANVAS_HEIGHT - bottom - height
            
            # 获取原始颜色配置（来自 ColorConfigurator）
            raw_style = elem.get('style_config', {})
            accent_color = raw_style.get('border_color', '#1677FF')  # 提取"特征色"，默认主色
            
            # 生成基础样式
            style_list = [
                f"left: {css_left}px;",
                f"top: {css_top}px;",
                f"width: {width}px;",
                f"height: {height}px;",
                "position: absolute;",
                "box-sizing: border-box;"
            ]
            
            # --- 针对不同类型的"设计感"处理 ---
            
            # 1. 标题 (Title)
            if 'title' in elem_type and 'subtitle' not in elem_type:
                # 使用主色或主文本色
                text_color = raw_style.get('text_color', 'var(--ant-color-primary)')
                style_list.append(f"color: {text_color};")
                style_list.append("font-size: 48px;")  # 加大字号
                style_list.append("font-weight: 600;")
                style_list.append("text-align: center;")
                style_list.append("line-height: 1.2;")
                # 移除背景色，标题通常是透明背景
                style_list.append("margin: 0;")
                
            # 2. 副标题 (Subtitle)
            elif 'subtitle' in elem_type or (elem_type == 'text' and 'subtitle' in elem_id):
                style_list.append("color: var(--ant-text-color-secondary);")
                style_list.append("font-size: 24px;")
                style_list.append("font-weight: 400;")
                style_list.append("text-align: center;")
                style_list.append("line-height: 1.5;")
                style_list.append("margin: 0;")
            
            # 3. 价值卡片 (Card) - 重点改造
            elif 'card' in elem_type or 'value' in elem_type:
                # 强制白色背景
                style_list.append("background-color: var(--ant-bg-color-container);")
                
                # 添加高级感阴影
                style_list.append("box-shadow: var(--ant-box-shadow);")
                
                # 圆角
                style_list.append("border-radius: var(--ant-border-radius-base);")
                
                # 内边距
                style_list.append("padding: 24px;")
                
                # 【设计核心】使用 accent_color 做顶部装饰条，而不是全背景
                # 这样既区分了颜色（蓝/绿/橙），又保持了统一的白色卡片风格
                style_list.append(f"border-top: 4px solid {accent_color};")
                
                # 布局
                style_list.append("display: flex;")
                style_list.append("flex-direction: column;")
                style_list.append("justify-content: center;")  # 内容垂直居中
                style_list.append("align-items: flex-start;")  # 内容左对齐
                
            # 4. 其他通用元素
            else:
                bg_color = raw_style.get('background_color', 'transparent')
                if bg_color and bg_color != 'transparent':
                    style_list.append(f"background-color: {bg_color};")
            
            # 组装 style 字符串
            style_str = " ".join(style_list)
            
            # --- 内容内部 HTML 优化 ---
            final_html = ""
            
            if 'card' in elem_type or 'value' in elem_type:
                # 卡片标题样式 - 使用accent_color作为标题颜色（可选，更高级）
                h3_color = accent_color  # 卡片标题使用特征色
                h3_style = f"margin: 0 0 12px 0; font-size: 20px; font-weight: 600; color: {h3_color};"
                # 卡片内容样式
                p_style = f"margin: 0; font-size: 14px; color: var(--ant-text-color-secondary); line-height: 1.6;"
                
                processed_content = content
                processed_content = processed_content.replace('<h3>', f'<h3 style="{h3_style}">')
                processed_content = processed_content.replace('<p>', f'<p style="{p_style}">')
                
                final_html = f'<div id="{elem_id}" class="element-card" style="{style_str}">{processed_content}</div>'
                
            elif 'title' in elem_type:
                final_html = f'<h1 id="{elem_id}" style="{style_str}">{content}</h1>'
                
            else:
                final_html = f'<div id="{elem_id}" style="{style_str}">{content}</div>'
            
            elements_html.append(final_html)
        
        return "\n            ".join(elements_html)
    
    def coordinate_to_css(
        self,
        left: float,
        bottom: float,
        width: float,
        height: float
    ) -> Dict[str, float]:
        """
        将坐标系坐标转换为CSS位置
        坐标系：左下角为原点
        CSS：top-left为原点
        
        Args:
            left: 距离左边缘的像素
            bottom: 距离下边缘的像素
            width: 宽度
            height: 高度
            
        Returns:
            CSS位置字典 {left, top, width, height}
        """
        # 转换为CSS的top位置
        css_top = self.CANVAS_HEIGHT - bottom - height
        
        return {
            'left': left,
            'top': css_top,
            'width': width,
            'height': height
        }

