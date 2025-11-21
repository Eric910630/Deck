"""
HTML生成器
根据内容和Ant Design规范生成HTML模板
融合中国述职PPT风格
"""

from typing import Dict, Any, List, Optional, Tuple
from loguru import logger
from ..theme.ant_design_theme import ant_design_theme
from ..theme.chinese_ppt_theme import chinese_ppt_theme
from .html_canvas_generator import HTMLCanvasGenerator


class HTMLGenerator:
    """
    HTML生成器
    生成符合Ant Design规范的HTML模板（16:9画布，24栅格系统）
    
    坐标系系统：
    - 原点：左下角 (0, 0)
    - X轴：向右为正
    - Y轴：向上为正
    - 画布尺寸：1920px × 1080px (16:9)
    - 内容区域：1872px × 1032px (减去padding 24px)
    - 栅格系统：24列 × 13.5行
    """
    
    # 16:9画布尺寸
    CANVAS_WIDTH = 1920
    CANVAS_HEIGHT = 1080
    GRID_COLUMNS = 24
    GRID_ROWS = 13.5
    
    # Padding（与坐标映射器保持一致）
    HTML_PADDING = 24  # px
    
    # 内容区域尺寸（减去padding）
    CONTENT_WIDTH = CANVAS_WIDTH - 2 * HTML_PADDING  # 1872px
    CONTENT_HEIGHT = CANVAS_HEIGHT - 2 * HTML_PADDING  # 1032px
    
    # 栅格单元尺寸
    CELL_WIDTH = CONTENT_WIDTH / GRID_COLUMNS  # ≈ 78px
    CELL_HEIGHT = CONTENT_HEIGHT / GRID_ROWS   # ≈ 76.4px
    
    def __init__(self):
        """初始化HTML生成器"""
        logger.info("--- [HTMLGenerator]: Initialized")
        # 初始化画布生成器
        self.canvas_generator = HTMLCanvasGenerator()
    
    def _grid_to_pixel(self, grid_x: float, grid_y: float, span_x: float, span_y: float) -> tuple:
        """
        将栅格坐标转换为像素坐标（左下角为原点）
        
        Args:
            grid_x: 栅格列位置（0-23）
            grid_y: 栅格行位置（0-12.5，从下往上）
            span_x: 占据的列数
            span_y: 占据的行数
        
        Returns:
            (left, top, width, height) 像素值（CSS使用top-left原点）
        """
        # 计算像素位置（左下角为原点）
        left_px = self.HTML_PADDING + grid_x * self.CELL_WIDTH
        bottom_px = self.HTML_PADDING + grid_y * self.CELL_HEIGHT
        width_px = span_x * self.CELL_WIDTH
        height_px = span_y * self.CELL_HEIGHT
        
        # 转换为CSS的top定位（CSS使用top-left原点）
        # top = 画布高度 - bottom - height
        top_px = self.CANVAS_HEIGHT - bottom_px - height_px
        
        return (left_px, top_px, width_px, height_px)
    
    def generate_slide_html(
        self,
        title: Optional[str] = None,
        content_blocks: Optional[List[Dict[str, Any]]] = None,
        layout: str = "standard"
    ) -> str:
        """
        生成单张幻灯片的HTML
        
        Args:
            title: 标题
            content_blocks: 内容块列表，每个块包含：
                - text: 文本内容
                - type: 类型（title, subtitle, body, key_points, data_highlight, case_study）
                - grid_position: 栅格位置 {'x': 0, 'y': 0, 'span_x': 12, 'span_y': 4}
            layout: 布局类型（standard, centered, two_column）
            
        Returns:
            HTML字符串
        """
        content_blocks = content_blocks or []
        
        # 生成HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title or 'Slide'}</title>
    <style>
        {self._generate_css()}
    </style>
</head>
<body>
    <div class="canvas">
        <div class="container">
            {self._generate_title_html(title)}
            {self._generate_content_blocks_html(content_blocks)}
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_css(self) -> str:
        """生成CSS样式（Ant Design规范）"""
        # 将cm转换为px（1cm ≈ 37.8px at 96dpi）
        cm_to_px = 37.8
        padding_lg_px = int(ant_design_theme.get_spacing_cm('lg') * cm_to_px)  # 24px
        padding_md_px = int(ant_design_theme.get_spacing_cm('md') * cm_to_px)  # 16px
        padding_sm_px = int(ant_design_theme.get_spacing_cm('sm') * cm_to_px)  # 12px
        padding_xs_px = int(ant_design_theme.get_spacing_cm('xs') * cm_to_px)  # 8px
        
        return f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            width: {self.CANVAS_WIDTH}px;
            height: {self.CANVAS_HEIGHT}px;
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            /* 渐变背景 - 提升美感 */
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            overflow: visible; /* 允许内容溢出，不截断 */
            position: relative;
        }}
        
        /* 装饰性背景元素 */
        body::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 40%;
            height: 100%;
            background: linear-gradient(135deg, rgba(24, 144, 255, 0.05) 0%, rgba(24, 144, 255, 0.02) 100%);
            pointer-events: none;
        }}
        
        .canvas {{
            width: 100%;
            height: 100%;
            position: relative; /* 为绝对定位的子元素提供定位上下文 */
            padding: 0; /* 移除padding，使用绝对定位 */
        }}
        
        .container {{
            position: relative; /* 为绝对定位的子元素提供定位上下文 */
            width: 100%;
            height: 100%;
            /* 不再使用Grid布局，改用绝对定位 */
        }}
        
        /* Card样式（融合Ant Design间距原则与中式布局习惯） */
        .card {{
            position: absolute; /* 使用绝对定位，基于坐标系 */
            background: {ant_design_theme.colors.colorBgContainer}; /* 使用Ant Design背景色 */
            border: 1px solid {ant_design_theme.colors.colorBorder}; /* 使用Ant Design边框色 */
            border-radius: {ant_design_theme.borderRadius.borderRadius}px; /* 使用Ant Design圆角 */
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            padding: {padding_lg_px}px; /* 24px，基于Ant Design 8px原则 */
            display: flex;
            flex-direction: row; /* 水平排列，确保文字水平显示 */
            flex-wrap: wrap; /* 允许换行 */
            align-items: flex-start; /* 中式PPT习惯：内容左对齐 */
            overflow: visible; /* 允许内容溢出，不截断 */
            word-wrap: break-word; /* 允许长单词换行 */
            word-break: break-word; /* 允许在任意字符间换行（中文友好） */
            overflow-wrap: break-word; /* 现代浏览器支持 */
            writing-mode: horizontal-tb; /* 确保水平文字方向 */
        }}
        
        /* 标题样式（中式布局，但保持Ant Design配色，增强美感） */
        .title {{
            font-family: {chinese_ppt_theme.typography.fontFamilyHeading};
            font-size: {chinese_ppt_theme.typography.fontSizeHeading1}px;
            font-weight: {chinese_ppt_theme.typography.fontWeightStrong};
            /* 渐变文字效果 - 提升美感 */
            background: linear-gradient(135deg, {ant_design_theme.colors.colorPrimary} 0%, #40a9ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin: 0;
            word-wrap: break-word;
            word-break: break-word;
            line-height: {chinese_ppt_theme.typography.lineHeightHeading};
            position: relative;
            letter-spacing: 2px; /* 增加字间距，更优雅 */
        }}
        
        /* 标题装饰线 */
        .title::after {{
            content: '';
            position: absolute;
            bottom: -{padding_sm_px}px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, transparent, {ant_design_theme.colors.colorPrimary}, transparent);
            border-radius: 2px;
        }}
        
        .subtitle {{
            font-family: {chinese_ppt_theme.typography.fontFamilyHeading};
            font-size: {chinese_ppt_theme.typography.fontSizeHeading3}px;
            font-weight: {chinese_ppt_theme.typography.fontWeightStrong};
            color: {ant_design_theme.colors.colorText}; /* 使用Ant Design文本色 */
            text-align: left; /* 中式PPT习惯：左对齐 */
            margin-bottom: {padding_md_px}px;
            word-wrap: break-word;
            word-break: break-word;
        }}
        
        /* 正文样式（中式布局：左对齐，但保持Ant Design配色） */
        .body-text {{
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            font-weight: {chinese_ppt_theme.typography.fontWeight};
            color: {ant_design_theme.colors.colorText}; /* 使用Ant Design文本色 */
            line-height: {chinese_ppt_theme.typography.lineHeight};
            margin: {padding_sm_px}px 0;
            text-align: left; /* 中式PPT习惯：左对齐 */
            word-wrap: break-word;
            word-break: break-word;
            overflow-wrap: break-word;
            white-space: normal; /* 允许换行 */
            overflow: visible; /* 不截断内容 */
            max-width: 100%; /* 确保不超出容器 */
        }}
        
        /* 正文段落间距 */
        .body-text p {{
            margin: {padding_sm_px}px 0;
        }}
        
        /* 关键要点样式（中式布局：左对齐，但保持Ant Design配色） */
        .key-points {{
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            font-weight: {chinese_ppt_theme.typography.fontWeightStrong};
            color: {ant_design_theme.colors.colorText}; /* 使用Ant Design文本色 */
            line-height: {chinese_ppt_theme.typography.lineHeight};
            text-align: left; /* 中式PPT习惯：左对齐 */
            word-wrap: break-word;
            word-break: break-word;
            overflow-wrap: break-word;
            white-space: normal; /* 允许换行 */
            overflow: visible; /* 不截断内容 */
            max-width: 100%; /* 确保不超出容器 */
            margin: 0;
            padding: 0;
        }}
        
        /* 关键要点列表项样式 */
        .key-points li {{
            margin-bottom: {padding_md_px}px;
            padding-left: {padding_lg_px}px;
            position: relative;
        }}
        
        .key-points li::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: {ant_design_theme.colors.colorPrimary};
            font-weight: bold;
            font-size: {chinese_ppt_theme.typography.fontSizeHeading3}px;
        }}
        
        /* 数据高亮样式（根据重要性优化） */
        .data-highlight {{
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            color: {ant_design_theme.colors.colorText};
            text-align: left;
            margin: {padding_md_px}px 0;
            padding: {padding_md_px}px;
            background: {ant_design_theme.colors.colorBgLayout};
            border-radius: {ant_design_theme.borderRadius.borderRadius}px;
        }}
        
        .data-highlight-important {{
            background: linear-gradient(135deg, #e6f7ff 0%, #bae7ff 100%);
            border-left: 4px solid {ant_design_theme.colors.colorPrimary};
            padding: {padding_lg_px}px;
            margin: {padding_md_px}px 0;
            border-radius: {ant_design_theme.borderRadius.borderRadius + 2}px;
            box-shadow: 
                0 4px 12px rgba(24, 144, 255, 0.15),
                0 2px 4px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }}
        
        /* 数据高亮装饰效果 */
        .data-highlight-important::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, rgba(24, 144, 255, 0.1) 0%, transparent 70%);
            border-radius: 50%;
            transform: translate(30%, -30%);
        }}
        
        .data-value {{
            font-size: {chinese_ppt_theme.typography.fontSizeHeading2}px;
            font-weight: {chinese_ppt_theme.typography.fontWeightStrong};
            /* 渐变文字效果 */
            background: linear-gradient(135deg, {ant_design_theme.colors.colorPrimary} 0%, #40a9ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            display: inline-block;
            margin-right: {padding_md_px}px;
            text-shadow: 0 2px 4px rgba(24, 144, 255, 0.2);
        }}
        
        .data-label {{
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            color: {ant_design_theme.colors.colorText};
            display: inline-block;
        }}
        
        /* 案例研究样式（结构化展示） */
        .case-study {{
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            color: {ant_design_theme.colors.colorText};
            text-align: left;
            margin: {padding_lg_px}px 0;
            padding: {padding_lg_px}px;
            background: {ant_design_theme.colors.colorBgLayout};
            border-radius: {ant_design_theme.borderRadius.borderRadius}px;
            border-left: 4px solid {ant_design_theme.colors.colorSuccess};
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .case-header {{
            font-weight: {chinese_ppt_theme.typography.fontWeightStrong};
            margin-bottom: {padding_md_px}px;
        }}
        
        .case-company {{
            font-size: {chinese_ppt_theme.typography.fontSizeHeading4}px;
            color: {ant_design_theme.colors.colorPrimary};
        }}
        
        .case-industry {{
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            color: {ant_design_theme.colors.colorTextSecondary};
            margin-left: {padding_md_px}px;
        }}
        
        .case-content {{
            margin: {padding_md_px}px 0;
        }}
        
        .case-key-points {{
            margin-top: {padding_md_px}px;
            padding-left: {padding_lg_px}px;
        }}
        
        /* 列表样式 */
        .key-points ul {{
            margin: 0;
            padding-left: {padding_lg_px}px;
            word-wrap: break-word;
            word-break: break-word;
            list-style: none; /* 移除默认列表样式，使用自定义样式 */
        }}
        
        .key-points li {{
            margin-bottom: {padding_md_px}px;
            word-wrap: break-word;
            word-break: break-word;
            padding-left: {padding_lg_px}px;
            position: relative;
        }}
        
        .key-points li::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: {ant_design_theme.colors.colorPrimary};
            font-weight: bold;
            font-size: {chinese_ppt_theme.typography.fontSizeHeading3}px;
        }}
        
        /* 不同类型内容块的视觉区分 - 增强美感 */
        .card.key-points {{
            background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
            border-left: 4px solid {ant_design_theme.colors.colorPrimary};
            box-shadow: 
                0 4px 16px rgba(24, 144, 255, 0.1),
                0 2px 8px rgba(0, 0, 0, 0.06),
                0 0 0 1px rgba(24, 144, 255, 0.05);
            padding: {padding_lg_px}px !important; /* 确保内边距 */
        }}
        
        /* 单个要点卡片样式（独立卡片设计） */
        .card.key-point-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
            border-left: 4px solid {ant_design_theme.colors.colorPrimary};
            box-shadow: 
                0 4px 16px rgba(24, 144, 255, 0.1),
                0 2px 8px rgba(0, 0, 0, 0.06),
                0 0 0 1px rgba(24, 144, 255, 0.05);
            padding: {padding_lg_px}px !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        .key-point-title {{
            font-family: {chinese_ppt_theme.typography.fontFamilyHeading};
            font-size: {chinese_ppt_theme.typography.fontSizeHeading3}px;
            font-weight: {chinese_ppt_theme.typography.fontWeightStrong};
            color: {ant_design_theme.colors.colorPrimary};
            margin: 0 0 {padding_sm_px}px 0;
        }}
        
        .key-point-desc {{
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            color: {ant_design_theme.colors.colorText};
            margin: 0;
            line-height: {chinese_ppt_theme.typography.lineHeight};
        }}
        
        .key-point-text {{
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            color: {ant_design_theme.colors.colorText};
            margin: 0;
            line-height: {chinese_ppt_theme.typography.lineHeight};
        }}
        
        .card.data-highlight {{
            background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
            border-left: 4px solid {ant_design_theme.colors.colorPrimary};
            box-shadow: 
                0 4px 16px rgba(24, 144, 255, 0.1),
                0 2px 8px rgba(0, 0, 0, 0.06),
                0 0 0 1px rgba(24, 144, 255, 0.05);
            padding: {padding_lg_px}px !important; /* 确保内边距 */
        }}
        
        .card.case-study {{
            background: linear-gradient(135deg, #f6ffed 0%, #f0f9e8 100%);
            border-left: 4px solid {ant_design_theme.colors.colorSuccess};
            box-shadow: 
                0 4px 16px rgba(82, 196, 26, 0.1),
                0 2px 8px rgba(0, 0, 0, 0.06),
                0 0 0 1px rgba(82, 196, 26, 0.05);
            padding: {padding_lg_px}px !important; /* 确保内边距 */
        }}
        
        /* 数据高亮样式 */
        .data-highlight {{
            background: {ant_design_theme.colors.colorBgLayout};
            border-left: 3px solid {ant_design_theme.colors.colorPrimary};
            padding-left: {padding_md_px}px;
        }}
        
        /* 案例样式 */
        .case-study {{
            font-style: italic;
            color: {ant_design_theme.colors.colorTextSecondary};
        }}
        
        /* 列表样式 */
        ul, ol {{
            margin: {padding_sm_px}px 0;
            padding-left: {padding_lg_px}px;
        }}
        
        li {{
            margin: {padding_xs_px}px 0;
            line-height: {ant_design_theme.typography.lineHeight};
        }}
        """
    
    def _generate_title_html(self, title: Optional[str]) -> str:
        """生成标题HTML"""
        if not title:
            logger.debug("--- [HTMLGenerator]: 无标题，跳过标题HTML生成")
            return ""
        
        logger.info(f"--- [HTMLGenerator]: 【标题】生成标题HTML: {title[:50]}...")
        logger.info(f"    栅格位置: 列 2-24, 行 1-3 (留左右边距)")
        
        # 标题容器：留一些边距，不占满整行（例如：列2-24，留左右边距）
        # 使用坐标转换：grid_x=2, grid_y=0, span_x=22, span_y=2
        left, top, width, height = self._grid_to_pixel(2, 0, 22, 2)
        return f"""
        <div class="card" style="left: {left}px; top: {top}px; width: {width}px; height: {height}px; justify-content: center; align-items: center;">
            <h1 class="title">{title}</h1>
        </div>
        """
    
    def _generate_content_blocks_html(self, content_blocks: List[Dict[str, Any]]) -> str:
        """生成内容块HTML"""
        if not content_blocks:
            logger.debug("--- [HTMLGenerator]: 无内容块，返回空")
            return ""
        
        html_parts = []
        
        # 智能布局分配
        num_blocks = len(content_blocks)
        logger.info(f"--- [HTMLGenerator]: 开始生成{num_blocks}个内容块的HTML")
        
        # 根据内容块数量和类型分配布局
        grid_positions = []
        
        if num_blocks == 1:
            # 单个内容块：居中，留边距，增加高度以容纳更多内容
            grid_positions = [{'x': 3, 'y': 4, 'span_x': 18, 'span_y': 8}]
        elif num_blocks == 2:
            # 两个内容块：根据类型智能布局
            left_type = content_blocks[0].get('type', 'body')
            right_type = content_blocks[1].get('type', 'body')
            left_content = content_blocks[0].get('text', '').strip()
            right_content = content_blocks[1].get('text', '').strip()
            left_len = len(left_content)
            right_len = len(right_content)
            
            # 如果一个是关键要点，一个是数据高亮，使用上下布局
            if (left_type == 'key_points' and right_type == 'data_highlight') or \
               (left_type == 'data_highlight' and right_type == 'key_points'):
                # 关键要点在上，数据高亮在下（或反之）
                if left_type == 'key_points':
                    grid_positions = [
                        {'x': 3, 'y': 4, 'span_x': 18, 'span_y': 5},  # 上：关键要点
                        {'x': 3, 'y': 10, 'span_x': 18, 'span_y': 3}  # 下：数据高亮
                    ]
                else:
                    grid_positions = [
                        {'x': 3, 'y': 4, 'span_x': 18, 'span_y': 3},  # 上：数据高亮
                        {'x': 3, 'y': 8, 'span_x': 18, 'span_y': 5}   # 下：关键要点
                    ]
            else:
                # 其他情况：左右对称布局
                length_diff = abs(left_len - right_len)
                length_ratio = max(left_len, right_len) / max(min(left_len, right_len), 1)
                
                if length_ratio > 3 and length_diff > 150:
                    # 内容长度差异很大：主次分明布局
                    if left_len > right_len:
                        grid_positions = [
                            {'x': 2, 'y': 4, 'span_x': 13, 'span_y': 8},  # 左：主
                            {'x': 16, 'y': 4, 'span_x': 6, 'span_y': 8}   # 右：次
                        ]
                    else:
                        grid_positions = [
                            {'x': 2, 'y': 4, 'span_x': 6, 'span_y': 8},   # 左：次
                            {'x': 9, 'y': 4, 'span_x': 13, 'span_y': 8}   # 右：主
                        ]
                else:
                    # 对称均衡布局
                    grid_positions = [
                        {'x': 2, 'y': 4, 'span_x': 10, 'span_y': 8},  # 左
                        {'x': 13, 'y': 4, 'span_x': 10, 'span_y': 8}  # 右
                    ]
                    logger.info(f"--- [HTMLGenerator]: 使用对称均衡布局（中国述职PPT风格）")
        elif num_blocks == 3:
            # 三个内容块：根据类型智能布局
            # 常见情况：关键要点 + 数据高亮 + 案例说明
            block_types = [b.get('type', 'body') for b in content_blocks]
            
            if 'key_points' in block_types and 'data_highlight' in block_types:
                # 关键要点在上，数据和案例在下
                key_idx = next(i for i, t in enumerate(block_types) if t == 'key_points')
                data_idx = next(i for i, t in enumerate(block_types) if t == 'data_highlight')
                other_idx = next(i for i in range(3) if i not in [key_idx, data_idx])
                
                grid_positions = [None] * 3
                grid_positions[key_idx] = {'x': 3, 'y': 4, 'span_x': 18, 'span_y': 4}  # 上：关键要点
                grid_positions[data_idx] = {'x': 2, 'y': 9, 'span_x': 10, 'span_y': 4}  # 左下：数据
                grid_positions[other_idx] = {'x': 13, 'y': 9, 'span_x': 10, 'span_y': 4}  # 右下：其他
            else:
                # 默认：上1下2
                grid_positions = [
                    {'x': 3, 'y': 4, 'span_x': 18, 'span_y': 3},  # 上：居中
                    {'x': 2, 'y': 8, 'span_x': 10, 'span_y': 5},   # 左下
                    {'x': 13, 'y': 8, 'span_x': 10, 'span_y': 5}   # 右下
                ]
        else:
            # 多个内容块：网格布局，留边距，增加高度
            cols = 2
            rows = (num_blocks + cols - 1) // cols
            for idx in range(num_blocks):
                col = idx % cols
                row = idx // cols
                grid_positions.append({
                    'x': 2 + col * 11,  # 从第2列开始，每列占11格
                    'y': 4 + row * 3,
                    'span_x': 10,  # 每个块占10列
                    'span_y': 3  # 增加高度
                })
        
        for idx, block in enumerate(content_blocks):
            block_type = block.get('type', 'body')
            text = block.get('text', '').strip()
            block_key = block.get('key', f'block_{idx}')
            
            # 跳过空内容
            if not text:
                logger.debug(f"--- [HTMLGenerator]: 跳过空内容块 {idx} ({block_key})")
                continue
            
            # 获取栅格位置
            grid_pos = grid_positions[idx] if idx < len(grid_positions) else grid_positions[-1]
            
            # 【日志探针】记录布局信息
            logger.info(f"--- [HTMLGenerator]: 【布局】内容块 {idx+1}/{num_blocks}")
            logger.info(f"    Key: {block_key}")
            logger.info(f"    类型: {block_type}")
            logger.info(f"    内容长度: {len(text)} 字符")
            logger.info(f"    内容预览: {text[:50]}...")
            logger.info(f"    栅格位置: x={grid_pos['x']}, y={grid_pos['y']}, span_x={grid_pos['span_x']}, span_y={grid_pos['span_y']}")
            logger.info(f"    实际位置: 列 {grid_pos['x']}-{grid_pos['x']+grid_pos['span_x']}, 行 {grid_pos['y']}-{grid_pos['y']+grid_pos['span_y']}")
            
            # 检查重叠
            for prev_idx, prev_block in enumerate(content_blocks[:idx]):
                if prev_block.get('text', '').strip():
                    prev_grid_pos = grid_positions[prev_idx] if prev_idx < len(grid_positions) else grid_positions[-1]
                    # 检查是否重叠
                    x_overlap = not (grid_pos['x'] >= prev_grid_pos['x'] + prev_grid_pos['span_x'] or 
                                   grid_pos['x'] + grid_pos['span_x'] <= prev_grid_pos['x'])
                    y_overlap = not (grid_pos['y'] >= prev_grid_pos['y'] + prev_grid_pos['span_y'] or 
                                   grid_pos['y'] + grid_pos['span_y'] <= prev_grid_pos['y'])
                    if x_overlap and y_overlap:
                        logger.warning(f"--- [HTMLGenerator]: ⚠️ 检测到重叠！")
                        logger.warning(f"    块 {prev_idx+1} ({prev_grid_pos}) 与 块 {idx+1} ({grid_pos}) 重叠")
            
            # 生成CSS类名
            css_class = self._get_css_class_for_type(block_type)
            
            # 生成HTML
            # 使用坐标转换函数计算像素位置
            left, top, width, height = self._grid_to_pixel(
                grid_pos['x'], 
                grid_pos['y'], 
                grid_pos['span_x'], 
                grid_pos['span_y']
            )
            grid_style = (
                f"left: {left}px; "
                f"top: {top}px; "
                f"width: {width}px; "
                f"height: {height}px;"
            )
            
            html_parts.append(f"""
            <div class="card {css_class}" style="{grid_style}">
                {self._format_text_content(text, block_type)}
            </div>
            """)
        
        logger.info(f"--- [HTMLGenerator]: 完成生成{len(html_parts)}个内容块的HTML")
        return "\n".join(html_parts)
    
    def _get_css_class_for_type(self, block_type: str) -> str:
        """根据内容类型获取CSS类名"""
        type_map = {
            'title': '',
            'subtitle': 'subtitle',
            'body': 'body-text',
            'key_points': 'key-points',
            'key_point_card': 'key-point-card',  # 单个要点卡片
            'data_highlight': 'data-highlight',
            'case_study': 'case-study',
        }
        return type_map.get(block_type, 'body-text')
    
    def _format_text_content(self, text: str, block_type: str) -> str:
        """格式化文本内容（中式布局：左对齐，支持数据高亮和案例结构化展示）"""
        if block_type == 'key_point_card':
            # 单个要点卡片：作为独立的卡片内容，不显示列表符号
            # 尝试提取标题和描述（如果有冒号分隔）
            if ':' in text or '：' in text:
                # 支持中英文冒号
                separator = ':' if ':' in text else '：'
                parts = text.split(separator, 1)
                title = parts[0].strip()
                desc = parts[1].strip() if len(parts) > 1 else ""
                if desc:
                    return f"""
                    <h3 class='key-point-title'>{title}</h3>
                    <p class='key-point-desc'>{desc}</p>
                    """
            
            # 【改进】如果没有冒号，智能提取标题
            # 方法1: 如果内容较长（>20字），提取前几个关键词作为标题
            if len(text) > 20:
                # 尝试提取关键词（常见模式：前几个字 + 逗号/句号）
                import re
                # 模式1: 提取前几个字（到第一个逗号或句号）
                match = re.match(r'^([^，。、；：！？]{4,12})[，。、；：！？]', text)
                if match:
                    title = match.group(1)
                    desc = text[len(title):].lstrip('，。、；：！？').strip()
                    if desc:
                        return f"""
                        <h3 class='key-point-title'>{title}</h3>
                        <p class='key-point-desc'>{desc}</p>
                        """
                
                # 模式2: 提取关键词（如"多元化"、"外部合作"等）
                # 常见关键词模式：2-4字的词
                keywords = re.findall(r'[多元化|外部|合作|生态|体系|渠道|平台|系统|团队|模式|转型|推广|集成|对接]{2,4}', text[:30])
                if keywords:
                    # 取第一个关键词作为标题
                    title = keywords[0]
                    desc = text
                    return f"""
                    <h3 class='key-point-title'>{title}</h3>
                    <p class='key-point-desc'>{desc}</p>
                    """
            
            # 如果内容较短或无法提取，直接显示文本（但格式化为标题样式）
            if len(text) <= 15:
                # 短文本：作为标题
                return f"<h3 class='key-point-title'>{text}</h3>"
            else:
                # 长文本：提取前几个字作为标题，剩余作为描述
                title = text[:8] + '...' if len(text) > 8 else text
                desc = text
                return f"""
                <h3 class='key-point-title'>{title}</h3>
                <p class='key-point-desc'>{desc}</p>
                """
        elif block_type == 'key_points':
            # 关键要点：转换为列表，左对齐（保留兼容性）
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            list_items = "\n".join([f"<li style='text-align: left;'>{line}</li>" for line in lines])
            return f"<ul class='key-points' style='text-align: left;'>{list_items}</ul>"
        elif block_type == 'subtitle':
            # 副标题：左对齐
            return f"<h2 class='subtitle' style='text-align: left;'>{text}</h2>"
        elif block_type == 'data_highlight':
            # 数据高亮：结构化展示
            # 尝试解析数据格式（如"40-60% (成本降低)"或"• 40-60%"）
            import re
            data_match = re.search(r'(\d+[%％]|\d+\.\d+%|\d+[-\d]*%)', text)
            if data_match:
                data_value = data_match.group(1)
                label = text.replace(data_value, '').strip(' •()')
                return f"""
                <div class="data-highlight-important">
                    <span class="data-value">{data_value}</span>
                    {f'<span class="data-label">{label}</span>' if label else ''}
                </div>
                """
            else:
                # 简单格式
                return f"<div class='data-highlight'>{text}</div>"
        elif block_type == 'case_study':
            # 案例研究：结构化展示
            return f"""
            <div class="case-study">
                <div class="case-content">
                    <p>{text}</p>
                </div>
            </div>
            """
        else:
            # 正文：保留换行，左对齐
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
            para_html = "\n".join([f"<p class='body-text' style='text-align: left;'>{p}</p>" for p in paragraphs])
            return para_html
    
    def generate_from_content_map(
        self,
        content_map: Dict[str, str],
        slide_structure: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        根据内容映射生成HTML
        
        Args:
            content_map: 内容映射字典 {key: content}
            slide_structure: 幻灯片结构信息
            
        Returns:
            HTML字符串
        """
        logger.info("="*80)
        logger.info("--- [HTMLGenerator]: 开始生成HTML")
        logger.info(f"    内容映射项数: {len(content_map)}")
        logger.info("="*80)
        
        # 按幻灯片分组内容
        slides_content = {}
        
        for key, content in content_map.items():
            logger.debug(f"--- [HTMLGenerator]: 处理内容项: {key} (长度: {len(content)} 字符)")
            # 解析slide_idx
            slide_idx = 0
            if 'slide_' in key:
                try:
                    slide_idx = int(key.split('_')[1])
                except:
                    pass
            
            if slide_idx not in slides_content:
                slides_content[slide_idx] = {
                    'title': None,
                    'content_blocks': []
                }
            
            # 判断是否为标题
            is_title = 'placeholder_0' in key or ('title' in key.lower() and 'placeholder' in key)
            logger.debug(f"--- [HTMLGenerator]: Key={key}, Slide={slide_idx}, IsTitle={is_title}")
            
            if is_title:
                # 只取第一个标题，避免重复
                if slides_content[slide_idx]['title'] is None:
                    slides_content[slide_idx]['title'] = content
                    logger.info(f"--- [HTMLGenerator]: 【标题】幻灯片{slide_idx}: {content[:50]}...")
                else:
                    logger.warning(f"--- [HTMLGenerator]: ⚠️ 跳过重复标题 (幻灯片{slide_idx}): {content[:50]}...")
            else:
                # 判断内容类型
                block_type = self._detect_content_type(content)
                
                # 【改进】根据key名称更精确地识别内容类型
                if 'key_points' in key.lower() or content.strip().startswith('•'):
                    # 关键要点：以•开头或key包含key_points
                    block_type = 'key_points'
                elif 'data' in key.lower() or '📊' in content:
                    # 数据高亮：包含📊或key包含data
                    block_type = 'data_highlight'
                elif 'case' in key.lower() or '💡' in content:
                    # 案例说明：包含💡或key包含case
                    block_type = 'case_study'
                
                logger.debug(f"--- [HTMLGenerator]: 内容块类型检测: {block_type} (Key: {key})")
                
                # 【关键改进】如果是关键要点类型，且包含多个要点，拆分成独立的卡片
                if block_type == 'key_points':
                    # 检测是否包含多个要点（以•开头或换行分隔）
                    lines = [line.strip() for line in content.split('\n') if line.strip()]
                    points = []
                    for line in lines:
                        # 移除开头的•或●等符号
                        clean_line = line.lstrip('•●·- ')
                        if clean_line:
                            points.append(clean_line)
                    
                    if len(points) > 1:
                        # 多个要点：拆分成独立的卡片
                        logger.info(f"--- [HTMLGenerator]: 【设计改进】检测到{len(points)}个关键要点，拆分成独立卡片")
                        for point_idx, point in enumerate(points):
                            slides_content[slide_idx]['content_blocks'].append({
                                'text': point,
                                'type': 'key_point_card',  # 新的类型：单个要点卡片
                                'key': f"{key}_point_{point_idx}"
                            })
                    else:
                        # 单个要点：作为普通内容块
                        slides_content[slide_idx]['content_blocks'].append({
                            'text': content,
                            'type': block_type,
                            'key': key
                        })
                else:
                    # 其他类型：正常添加
                    slides_content[slide_idx]['content_blocks'].append({
                        'text': content,
                        'type': block_type,
                        'key': key  # 保留key用于调试
                    })
        
        logger.info(f"--- [HTMLGenerator]: 幻灯片分组完成，共{len(slides_content)}张")
        logger.info(f"--- [HTMLGenerator]: 【探针】幻灯片内容分布:")
        for slide_idx in sorted(slides_content.keys()):
            slide_data = slides_content[slide_idx]
            logger.info(f"   幻灯片{slide_idx}: 标题={'有' if slide_data['title'] else '无'}, 内容块数={len(slide_data['content_blocks'])}")
        
        if slides_content:
            # 【探针】检查是否应该生成多张幻灯片
            # 如果有多张幻灯片且每张都有内容，应该生成多张
            # 但目前浏览器渲染只支持单张，所以合并所有内容
            # TODO: 未来可以扩展为支持多张幻灯片
            
            first_slide_idx = min(slides_content.keys())
            first_slide = slides_content[first_slide_idx]
            logger.info(f"--- [HTMLGenerator]: 第一张幻灯片: {first_slide_idx}")
            logger.info(f"    标题: {first_slide['title'][:50] if first_slide['title'] else '(无)'}...")
            logger.info(f"    内容块数: {len(first_slide['content_blocks'])}")
            
            # 如果没有标题，尝试从其他幻灯片获取
            if first_slide['title'] is None:
                logger.warning("--- [HTMLGenerator]: ⚠️ 第一张幻灯片无标题，尝试从其他幻灯片获取")
                for slide_idx in sorted(slides_content.keys()):
                    if slides_content[slide_idx]['title']:
                        first_slide['title'] = slides_content[slide_idx]['title']
                        logger.info(f"--- [HTMLGenerator]: 从幻灯片{slide_idx}获取标题: {first_slide['title'][:50]}...")
                        break
            
            # 【修复】支持多张幻灯片：为每张幻灯片生成独立的HTML
            if len(slides_content) == 1:
                logger.info("--- [HTMLGenerator]: 单张幻灯片模式")
                return [self.generate_slide_html(
                    title=first_slide['title'],
                    content_blocks=first_slide['content_blocks']
                )]
            else:
                # 多张幻灯片：为每张生成独立的HTML
                logger.info(f"--- [HTMLGenerator]: 检测到{len(slides_content)}张幻灯片，为每张生成独立的HTML")
                logger.info(f"--- [HTMLGenerator]: 【探针】各幻灯片内容块数:")
                for slide_idx in sorted(slides_content.keys()):
                    logger.info(f"   幻灯片{slide_idx}: {len(slides_content[slide_idx]['content_blocks'])}个内容块")
                
                html_slides = []
                for slide_idx in sorted(slides_content.keys()):
                    slide_data = slides_content[slide_idx]
                    logger.info(f"--- [HTMLGenerator]: 生成幻灯片{slide_idx}的HTML")
                    html_slide = self.generate_slide_html(
                        title=slide_data['title'],
                        content_blocks=slide_data['content_blocks']
                    )
                    html_slides.append(html_slide)
                
                logger.info(f"--- [HTMLGenerator]: 总计生成{len(html_slides)}张独立的HTML幻灯片")
                return html_slides
        
        logger.warning("--- [HTMLGenerator]: ⚠️ 无内容，生成空幻灯片")
        return self.generate_slide_html()
    
    def _detect_content_type(self, content: str) -> str:
        """检测内容类型"""
        if not content:
            return 'body'
        
        content_lower = content.lower()
        content_stripped = content.strip()
        
        # 关键要点：包含"关键要点"或以项目符号开头
        if '关键要点' in content or content_stripped.startswith('•') or content_stripped.startswith('-'):
            return 'key_points'
        # 数据高亮：包含"数据"或百分比
        elif '数据' in content or '%' in content or '增长' in content or '提升' in content:
            return 'data_highlight'
        # 案例研究：包含"案例"或"例子"
        elif '案例' in content or '例子' in content or '实例' in content:
            return 'case_study'
        # 副标题：短文本且可能是标题
        elif len(content_stripped) < 50 and ('介绍' in content or '概述' in content or '解析' in content):
            return 'subtitle'
        else:
            return 'body'
    
    def generate_from_layout_plan(
        self,
        layout_plans: List[Dict[str, Any]],
        polished_slides: List[Dict[str, Any]],
        color_configs: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """
        根据布局规划生成HTML（精确布局）
        
        Args:
            layout_plans: 布局规划列表，每个元素包含：
                - slide_index: 幻灯片索引
                - layout_plan: 布局规划详情
                    - overall_structure: 整体布局结构描述
                    - element_positions: 元素位置列表
                        - element_id: 元素ID
                        - element_type: 元素类型
                        - position_description: 位置描述
                        - size_description: 尺寸描述
                        - alignment: 对齐方式
                        - spacing: 间距对象
                    - element_spacing: 元素间距说明
                    - visual_hierarchy: 视觉层次说明
                    - design_specifications: 设计规范说明
            polished_slides: 润色后的幻灯片列表，每个元素包含：
                - slide_index: 幻灯片索引
                - title: 标题
                - content: 内容描述
                - visual_elements_detail: 视觉元素详情列表
                    - element_id: 元素ID
                    - element_type: 元素类型
                    - title: 标题
                    - content: 内容
                    - data: 数据
                    - description: 描述
                    
        Returns:
            HTML字符串列表，每个元素对应一张幻灯片
        """
        logger.info("="*80)
        logger.info("--- [HTMLGenerator]: 根据布局规划和颜色配置生成HTML（精确布局+颜色）")
        logger.info(f"    布局规划数量: {len(layout_plans)}")
        logger.info(f"    润色幻灯片数量: {len(polished_slides)}")
        logger.info(f"    颜色配置数量: {len(color_configs) if color_configs else 0}")
        logger.info("="*80)
        
        # 【探针】检查输入数据
        logger.info("="*80)
        logger.info("--- [HTMLGenerator]: 【探针0】generate_from_layout_plan输入数据检查")
        logger.info(f"--- [HTMLGenerator]: layout_plans数量: {len(layout_plans)}")
        logger.info(f"--- [HTMLGenerator]: polished_slides数量: {len(polished_slides)}")
        logger.info(f"--- [HTMLGenerator]: color_configs数量: {len(color_configs) if color_configs else 0}")
        
        # 检查slide_index分布
        if layout_plans:
            layout_indices = [l.get('slide_index', 0) for l in layout_plans]
            logger.info(f"--- [HTMLGenerator]: layout_plans的slide_index范围: {min(layout_indices)} - {max(layout_indices)}")
        
        if polished_slides:
            polished_indices = [p.get('slide_index', 0) for p in polished_slides]
            logger.info(f"--- [HTMLGenerator]: polished_slides的slide_index范围: {min(polished_indices)} - {max(polished_indices)}")
        
        logger.info("="*80)
        
        html_slides = []
        
        # 按slide_index排序
        layout_plans_sorted = sorted(layout_plans, key=lambda x: x.get('slide_index', 0))
        polished_slides_sorted = sorted(polished_slides, key=lambda x: x.get('slide_index', 0))
        color_configs_sorted = sorted(color_configs, key=lambda x: x.get('slide_index', 0)) if color_configs else []
        
        # 创建润色内容的索引（使用(slide_index, element_id)作为键，避免冲突）
        polished_content_map = {}
        logger.info("="*80)
        logger.info("--- [HTMLGenerator]: 【探针1】构建polished_content_map（使用(slide_index, element_id)作为键）")
        logger.info(f"--- [HTMLGenerator]: polished_slides数量: {len(polished_slides_sorted)}")
        
        for polished_slide in polished_slides_sorted:
            slide_idx = polished_slide.get('slide_index', 0)
            visual_elements = polished_slide.get('visual_elements_detail', [])
            logger.info(f"--- [HTMLGenerator]: 幻灯片{slide_idx}: {len(visual_elements)}个视觉元素")
            
            for elem in visual_elements:
                elem_id = elem.get('element_id', '')
                if elem_id:
                    # 使用(slide_index, element_id)作为键，避免不同幻灯片的相同element_id冲突
                    key = (slide_idx, elem_id)
                    polished_content_map[key] = {
                        'slide_index': slide_idx,
                        'element': elem,
                        'polished_slide': polished_slide
                    }
                else:
                    logger.warning(f"--- [HTMLGenerator]: ⚠️ 幻灯片{slide_idx}发现缺失element_id的元素: {elem.get('element_type', 'unknown')}")
        
        logger.info(f"--- [HTMLGenerator]: polished_content_map键数量: {len(polished_content_map)}")
        logger.info("="*80)
        
        # 创建颜色配置的索引（使用(slide_index, element_id)作为键，避免冲突）
        color_map = {}
        for color_config in color_configs_sorted:
            slide_idx = color_config.get('slide_index', 0)
            element_colors = color_config.get('color_config', {}).get('element_colors', [])
            for elem_color in element_colors:
                elem_id = elem_color.get('element_id', '')
                if elem_id:
                    # 使用(slide_index, element_id)作为键，避免不同幻灯片的相同element_id冲突
                    key = (slide_idx, elem_id)
                    color_map[key] = elem_color
        
        # 为每张布局规划生成HTML
        logger.info("="*80)
        logger.info("--- [HTMLGenerator]: 【探针2】开始生成HTML，检查slide_index匹配")
        logger.info(f"--- [HTMLGenerator]: layout_plans数量: {len(layout_plans_sorted)}")
        logger.info(f"--- [HTMLGenerator]: polished_slides数量: {len(polished_slides_sorted)}")
        
        # 检查slide_index分布
        layout_slide_indices = [l.get('slide_index', 0) for l in layout_plans_sorted]
        polished_slide_indices = [p.get('slide_index', 0) for p in polished_slides_sorted]
        logger.info(f"--- [HTMLGenerator]: layout_plans的slide_index列表: {sorted(set(layout_slide_indices))}")
        logger.info(f"--- [HTMLGenerator]: polished_slides的slide_index列表: {sorted(set(polished_slide_indices))}")
        
        # 检查是否有重复的slide_index
        if len(layout_slide_indices) != len(set(layout_slide_indices)):
            logger.warning(f"--- [HTMLGenerator]: ⚠️ layout_plans中有重复的slide_index")
            from collections import Counter
            duplicates = [k for k, v in Counter(layout_slide_indices).items() if v > 1]
            logger.warning(f"--- [HTMLGenerator]:   重复的slide_index: {duplicates}")
        
        if len(polished_slide_indices) != len(set(polished_slide_indices)):
            logger.warning(f"--- [HTMLGenerator]: ⚠️ polished_slides中有重复的slide_index")
            from collections import Counter
            duplicates = [k for k, v in Counter(polished_slide_indices).items() if v > 1]
            logger.warning(f"--- [HTMLGenerator]:   重复的slide_index: {duplicates}")
        
        logger.info("="*80)
        
        for layout_plan_data in layout_plans_sorted:
            slide_idx = layout_plan_data.get('slide_index', 0)
            layout_plan = layout_plan_data.get('layout_plan', {})
            
            logger.info(f"--- [HTMLGenerator]: 生成幻灯片{slide_idx}的HTML（基于布局规划+颜色配置）")
            
            # 找到对应的润色内容
            polished_slide = None
            matched_slides = []
            for ps in polished_slides_sorted:
                if ps.get('slide_index', 0) == slide_idx:
                    matched_slides.append(ps)
                    if polished_slide is None:
                        polished_slide = ps
            
            if len(matched_slides) > 1:
                logger.warning(f"--- [HTMLGenerator]: ⚠️ 幻灯片{slide_idx}匹配到{len(matched_slides)}个polished_slide，使用第一个")
            
            if not polished_slide:
                logger.warning(f"--- [HTMLGenerator]: ⚠️ 未找到幻灯片{slide_idx}的润色内容，使用默认内容")
                continue
            
            # 找到对应的颜色配置
            color_config = None
            for cc in color_configs_sorted:
                if cc.get('slide_index', 0) == slide_idx:
                    color_config = cc
                    break
            
            # 生成HTML
            html_content = self._generate_html_from_layout_plan(
                layout_plan=layout_plan,
                polished_slide=polished_slide,
                polished_content_map=polished_content_map,
                color_map=color_map
            )
            html_slides.append(html_content)
        
        logger.info(f"--- [HTMLGenerator]: ✅ 总计生成{len(html_slides)}张HTML幻灯片（基于布局规划）")
        return html_slides
    
    def generate_merged_html(
        self,
        layout_plans: List[Dict[str, Any]],
        polished_slides: List[Dict[str, Any]],
        color_configs: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        生成合并的HTML文件（所有幻灯片在一个文件中）
        使用新的画布生成器，确保每张幻灯片独立显示
        
        Args:
            layout_plans: 布局规划列表
            polished_slides: 润色后的幻灯片列表
            color_configs: 颜色配置列表
            
        Returns:
            合并后的HTML字符串
        """
        logger.info("="*80)
        logger.info("--- [HTMLGenerator]: 生成合并的HTML文件（所有幻灯片）")
        logger.info(f"    布局规划数量: {len(layout_plans)}")
        logger.info(f"    润色幻灯片数量: {len(polished_slides)}")
        logger.info("="*80)
        
        # 先生成所有单独的HTML幻灯片
        html_slides = self.generate_from_layout_plan(
            layout_plans=layout_plans,
            polished_slides=polished_slides,
            color_configs=color_configs
        )
        
        # 提取每张幻灯片的canvas-container内容（只提取画布部分，避免重复）
        slide_canvases = []
        for idx, html_content in enumerate(html_slides):
            # 提取canvas-container及其内容
            import re
            # 匹配canvas-container及其内部所有内容（包括嵌套的div）
            # 使用更精确的匹配，找到canvas-container的开始和结束
            canvas_start = re.search(r'<div[^>]*id=["\']canvas-container["\'][^>]*>', html_content)
            if canvas_start:
                start_pos = canvas_start.start()
                # 从开始位置查找匹配的结束标签
                depth = 0
                pos = start_pos
                while pos < len(html_content):
                    if html_content[pos:pos+4] == '<div':
                        depth += 1
                        pos = html_content.find('>', pos) + 1
                    elif html_content[pos:pos+6] == '</div>':
                        depth -= 1
                        if depth == 0:
                            end_pos = pos + 6
                            canvas_content = html_content[start_pos:end_pos]
                            break
                        pos += 6
                    else:
                        pos += 1
                else:
                    # 如果没找到匹配的结束标签，使用简单匹配
                    canvas_match = re.search(
                        r'<div[^>]*id=["\']canvas-container["\'][^>]*>.*?</div>',
                        html_content,
                        re.DOTALL
                    )
                    if canvas_match:
                        canvas_content = canvas_match.group(0)
                    else:
                        canvas_content = None
            else:
                canvas_content = None
            
            if canvas_content:
                slide_canvases.append(f"""
        <!-- 幻灯片 {idx} -->
        <div class="slide" id="slide-{idx}">
            {canvas_content}
        </div>""")
            else:
                # 如果没找到canvas-container，尝试提取body内容
                body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
                if body_match:
                    body_content = body_match.group(1)
                    slide_canvases.append(f"""
        <!-- 幻灯片 {idx} -->
        <div class="slide" id="slide-{idx}">
            {body_content}
        </div>""")
        
        # 使用画布生成器的CSS样式
        canvas_css = self.canvas_generator._generate_canvas_css(show_grid=True)
        
        # 生成合并的HTML（使用新的画布样式）
        merged_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>演示文稿 - 所有幻灯片</title>
    <style>
        {canvas_css}
        
        /* 幻灯片容器样式 */
        .slide {{
            margin: 20px auto; /* 居中显示，上下间距20px */
            display: block; /* 确保每个幻灯片独立显示 */
        }}
        
        body {{
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            font-family: 'Microsoft YaHei', 'SimHei', 'Arial', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center; /* 水平居中 */
            min-height: 100vh;
        }}
    </style>
</head>
<body>
    {''.join(slide_canvases)}
</body>
</html>"""
        
        logger.info(f"--- [HTMLGenerator]: ✅ 合并HTML文件生成完成，包含{len(slide_canvases)}张幻灯片")
        return merged_html
    
    def _generate_html_from_layout_plan(
        self,
        layout_plan: Dict[str, Any],
        polished_slide: Dict[str, Any],
        polished_content_map: Dict[Tuple[int, str], Dict[str, Any]],
        color_map: Optional[Dict[Tuple[int, str], Dict[str, Any]]] = None
    ) -> str:
        """
        根据单张幻灯片的布局规划生成HTML
        
        【CSS-First 架构】：优先使用 LLM 生成的 HTML/CSS 代码
        【向后兼容】：如果没有 html_code，回退到 Python 坐标计算模式
        
        Args:
            layout_plan: 布局规划详情
            polished_slide: 润色后的幻灯片内容
            polished_content_map: 润色内容映射（按element_id索引）
            color_map: 颜色配置映射
            
        Returns:
            HTML字符串
        """
        # 【CSS-First 架构】优先检查新架构字段
        if 'html_code' in layout_plan:
            logger.info("🚀 [HTMLGenerator]: 检测到 CSS-First 新架构，使用 LLM 生成的 HTML...")
            return self._generate_html_from_llm_code(
                llm_html_code=layout_plan['html_code'],
                polished_slide=polished_slide,
                color_map=color_map
            )
        
        # 【向后兼容】回退到旧架构（Python 坐标计算模式）
        logger.info("⚠️ [HTMLGenerator]: 未检测到 html_code，回退到 Python 坐标计算模式...")
        return self._generate_html_legacy(
            layout_plan=layout_plan,
            polished_slide=polished_slide,
            polished_content_map=polished_content_map,
            color_map=color_map
        )
    
    def _generate_html_from_llm_code(
        self,
        llm_html_code: str,
        polished_slide: Dict[str, Any],
        color_map: Optional[Dict[Tuple[int, str], Dict[str, Any]]] = None
    ) -> str:
        """
        从 LLM 生成的 HTML 代码生成完整 HTML
        
        【核心职责】：不做数学计算，只做"拼装"
        - 注入 Design Tokens (CSS 变量)
        - 组装完整的 HTML 结构
        - 确保所有元素都有 data-ppt-element 属性
        
        Args:
            llm_html_code: LLM 生成的 HTML 代码（通常是 body 内容）
            polished_slide: 润色后的幻灯片内容（用于提取标题等元信息）
            color_map: 颜色配置映射
            
        Returns:
            完整的 HTML 字符串
        """
        logger.info("--- [HTMLGenerator]: 开始组装 CSS-First HTML...")
        
        # 1. 生成 Design Tokens (CSS 变量)
        css_vars = self._generate_css_design_tokens(color_map)
        
        # 2. 提取标题（用于 <title> 标签）
        slide_title = polished_slide.get('title', 'CSS-First PPT Slide')
        
        # 3. 组装完整 HTML
        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{slide_title}</title>
    <style>
        /* 全局重置 */
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        /* 注入 Ant Design Design Tokens */
        {css_vars}
        
        /* 基础样式 */
        html, body {{
            width: 100%;
            height: 100%;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: var(--ant-bg-color-layout, #F0F2F5);
            overflow: hidden; /* 防止滚动条 */
        }}
        
        /* Utility Classes (类似 Tailwind，方便 LLM 使用) */
        .flex {{ display: flex; }}
        .flex-col {{ flex-direction: column; }}
        .flex-row {{ flex-direction: row; }}
        .flex-1 {{ flex: 1; }}
        .h-full {{ height: 100%; }}
        .h-screen {{ height: 100vh; }}
        .w-full {{ width: 100%; }}
        .w-screen {{ width: 100vw; }}
        .items-center {{ align-items: center; }}
        .items-start {{ align-items: flex-start; }}
        .items-end {{ align-items: flex-end; }}
        .justify-center {{ justify-content: center; }}
        .justify-between {{ justify-content: space-between; }}
        .justify-start {{ justify-content: flex-start; }}
        .justify-end {{ justify-content: flex-end; }}
        .gap-4 {{ gap: 16px; }}
        .gap-6 {{ gap: 24px; }}
        .gap-8 {{ gap: 32px; }}
        .p-4 {{ padding: 16px; }}
        .p-6 {{ padding: 24px; }}
        .p-8 {{ padding: 32px; }}
        .p-12 {{ padding: 48px; }}
        .mb-4 {{ margin-bottom: 16px; }}
        .mb-6 {{ margin-bottom: 24px; }}
        .mb-8 {{ margin-bottom: 32px; }}
        .mt-4 {{ margin-top: 16px; }}
        .mt-6 {{ margin-top: 24px; }}
        .mt-8 {{ margin-top: 32px; }}
        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}
    </style>
</head>
<body>
    <!-- LLM 生成的 HTML 内容（直接嵌入） -->
    {llm_html_code}
</body>
</html>"""
        
        logger.info("--- [HTMLGenerator]: ✅ CSS-First HTML 组装完成")
        return full_html
    
    def _generate_css_design_tokens(
        self,
        color_map: Optional[Dict[Tuple[int, str], Dict[str, Any]]] = None
    ) -> str:
        """
        生成 Ant Design Design Tokens (CSS 变量)
        
        确保风格统一，即使 LLM 生成的 HTML 不同
        如果提供了 color_map，会从中提取颜色并动态调整 CSS 变量
        
        Args:
            color_map: 颜色配置映射（可选，用于动态调整颜色）
            格式: {(slide_idx, element_id): {'text_color': '#xxx', 'border_color': '#xxx', ...}}
            
        Returns:
            CSS 变量定义字符串
        """
        # 默认颜色值
        default_primary = "#1677FF"
        default_success = "#52C41A"
        default_warning = "#FA8C16"
        default_error = "#F5222D"
        
        # 从 color_map 中提取颜色（如果提供）
        if color_map:
            # 提取主色（从标题或第一个元素的 border_color）
            primary_colors = []
            for key, color_config in color_map.items():
                border_color = color_config.get('border_color', '')
                text_color = color_config.get('text_color', '')
                if border_color and border_color.startswith('#'):
                    primary_colors.append(border_color)
                elif text_color and text_color.startswith('#'):
                    primary_colors.append(text_color)
            
            if primary_colors:
                # 使用第一个找到的颜色作为主色
                default_primary = primary_colors[0]
                logger.info(f"--- [HTMLGenerator]: 从 color_map 提取主色: {default_primary}")
        
        return f"""
        :root {{
            /* --- Ant Design Color Tokens --- */
            --ant-color-primary: {default_primary};
            --ant-color-success: {default_success};
            --ant-color-warning: {default_warning};
            --ant-color-error: {default_error};
            --ant-color-info: {default_primary};
            
            /* --- Text Colors (文本语义色) --- */
            --ant-text-color: rgba(0, 0, 0, 0.88);
            --ant-text-color-heading: rgba(0, 0, 0, 0.88); /* #262626, 用于大标题 (H1, H2, H3) - 深黑色，庄重 */
            --ant-text-color-body: rgba(0, 0, 0, 0.65);    /* #595959, 用于正文 (段落文本) - 深灰 */
            --ant-text-color-secondary: rgba(0, 0, 0, 0.45); /* #8C8C8C, 用于Footer或辅助说明 - 浅灰 */
            --ant-text-color-tertiary: rgba(0, 0, 0, 0.45);
            --ant-text-color-disabled: rgba(0, 0, 0, 0.25);
            
            /* --- Backgrounds --- */
            --ant-bg-color-layout: #F0F2F5;
            --ant-bg-color-container: #FFFFFF;
            --ant-bg-color-elevated: #FFFFFF;
            
            /* --- Borders & Shadows --- */
            --ant-border-color: #F0F0F0;
            --ant-border-color-split: #F0F0F0;
            --ant-border-radius-base: 8px;
            --ant-border-radius-sm: 4px;
            --ant-border-radius-lg: 12px;
            --ant-box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02);
            --ant-box-shadow-card: 0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02);
            --ant-box-shadow-hover: 0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 9px 28px 8px rgba(0, 0, 0, 0.05);
            
            /* --- Spacing --- */
            --ant-padding-xs: 8px;
            --ant-padding-sm: 12px;
            --ant-padding-md: 16px;
            --ant-padding-lg: 24px;
            --ant-padding-xl: 32px;
            
            /* --- Typography --- */
            --ant-font-size-sm: 12px;
            --ant-font-size-base: 14px;
            --ant-font-size-lg: 16px;
            --ant-font-size-xl: 20px;
            --ant-font-size-xxl: 24px;
            --ant-font-size-title: 48px;
            --ant-line-height-base: 1.5715;
            --ant-line-height-lg: 1.5;
        }}
        """
    
    def _generate_html_legacy(
        self,
        layout_plan: Dict[str, Any],
        polished_slide: Dict[str, Any],
        polished_content_map: Dict[Tuple[int, str], Dict[str, Any]],
        color_map: Optional[Dict[Tuple[int, str], Dict[str, Any]]] = None
    ) -> str:
        """
        【向后兼容】旧架构：使用 Python 计算坐标
        
        当 LLM 没有生成 html_code 时，回退到此方法
        
        Args:
            layout_plan: 布局规划详情
            polished_slide: 润色后的幻灯片内容
            polished_content_map: 润色内容映射（按element_id索引）
            color_map: 颜色配置映射
            
        Returns:
            HTML字符串
        """
        element_positions = layout_plan.get('element_positions', [])
        overall_structure = layout_plan.get('overall_structure', '')
        visual_hierarchy = layout_plan.get('visual_hierarchy', '')
        design_specs = layout_plan.get('design_specifications', '')
        
        # 获取当前幻灯片的slide_index
        slide_idx = polished_slide.get('slide_index', 0)
        
        # 【新方法】使用画布生成器
        # 1. 将布局规划转换为画布元素格式
        canvas_elements = []
        
        # 按元素位置排序（确保渲染顺序正确）
        sorted_elements = sorted(element_positions, key=lambda x: self._parse_position_priority(x))
        
        logger.info("="*80)
        logger.info(f"--- [HTMLGenerator]: 【探针3】处理幻灯片{slide_idx}的元素")
        logger.info(f"--- [HTMLGenerator]: element_positions数量: {len(element_positions)}")
        logger.info(f"--- [HTMLGenerator]: polished_content_map键数量: {len(polished_content_map)}")
        
        # 去重：使用element_id和内容哈希去重，避免重复内容
        seen_ids = set()
        seen_content_hashes = set()
        
        missing_element_ids = []  # 记录缺失的element_id
        duplicate_element_ids = []  # 记录重复的element_id
        duplicate_content_hashes = []  # 记录重复的内容哈希
        
        # 【新增】统计元素类型，用于智能布局
        element_type_counts = {}
        for elem_pos in sorted_elements:
            elem_type = elem_pos.get('element_type', '')
            if 'card' in elem_type:
                element_type_counts['card'] = element_type_counts.get('card', 0) + 1
            elif 'title' in elem_type:
                element_type_counts['title'] = element_type_counts.get('title', 0) + 1
            elif 'text' in elem_type or 'content' in elem_type:
                element_type_counts['text'] = element_type_counts.get('text', 0) + 1
        
        # 【新增】记录已处理的元素，用于计算相对位置
        processed_elements = []  # 存储已处理的元素信息，用于计算后续元素的位置
        
        for elem_pos in sorted_elements:
            elem_id = elem_pos.get('element_id', '')
            elem_type = elem_pos.get('element_type', '')
            
            # 检查element_id是否缺失
            if not elem_id:
                logger.warning(f"--- [HTMLGenerator]: ⚠️ element_positions中发现缺失element_id的元素，类型: {elem_type}")
                continue
            
            # 跳过重复的元素ID（在同一张幻灯片内）
            if elem_id in seen_ids:
                duplicate_element_ids.append(elem_id)
                logger.warning(f"--- [HTMLGenerator]: ⚠️ 跳过重复元素ID {elem_id}（在同一张幻灯片内）")
                continue
            seen_ids.add(elem_id)
            
            # 从润色内容中获取实际内容（使用(slide_index, element_id)作为键）
            key = (slide_idx, elem_id)
            polished_content_entry = polished_content_map.get(key, {})
            elem_content_data = polished_content_entry.get('element', {})
            
            # 检查element_id是否在polished_content_map中
            if key not in polished_content_map:
                missing_element_ids.append(elem_id)
                logger.warning(f"--- [HTMLGenerator]: ⚠️ element_id {elem_id} (幻灯片{slide_idx}) 在polished_content_map中不存在！")
                logger.warning(f"--- [HTMLGenerator]:   元素类型: {elem_type}")
                logger.warning(f"--- [HTMLGenerator]:   位置描述: {elem_pos.get('position_description', '')[:50]}")
                # 继续处理，但使用空内容
                elem_content_data = {}
            else:
                logger.info(f"--- [HTMLGenerator]: ✅ element_id {elem_id} (幻灯片{slide_idx}) 匹配成功")
                logger.info(f"--- [HTMLGenerator]:   来源幻灯片: {polished_content_entry.get('slide_index', 'unknown')}")
                logger.info(f"--- [HTMLGenerator]:   元素标题: {elem_content_data.get('title', '')[:50]}")
            
            # 获取元素内容文本
            title = elem_content_data.get('title', '')
            content = elem_content_data.get('content', '')
            description = elem_content_data.get('description', '')
            
            # 生成内容哈希（用于去重）
            content_hash = hash(f"{title}|{content}|{description}")
            if content_hash in seen_content_hashes:
                duplicate_content_hashes.append({
                    'element_id': elem_id,
                    'title': title[:30] if title else '无标题'
                })
                logger.warning(f"--- [HTMLGenerator]: ⚠️ 跳过重复内容元素 {elem_id} (内容: {title[:30] if title else '无标题'}...)")
                continue
            seen_content_hashes.add(content_hash)
            
            # 组合内容
            # 【修复】根据元素类型生成不同的HTML结构，避免嵌套问题
            if 'title' in elem_type and 'subtitle' not in elem_type:
                # 标题元素：只显示标题文本，不嵌套h3标签（因为外层已经是h1）
                if title:
                    display_content = title
                elif content:
                    display_content = content
                else:
                    display_content = description or ''
            elif 'subtitle' in elem_type:
                # 副标题元素：显示标题和内容，使用换行符分隔，不嵌套h3/p标签
                if title and content:
                    display_content = f"{title}<br/>{content}"
                elif title:
                    display_content = title
                elif content:
                    display_content = content
                else:
                    display_content = description or ''
            else:
                # 其他元素（如卡片）：保持原有逻辑，可以嵌套h3/p标签
                if title:
                    display_content = f"<h3>{title}</h3>"
                    if content:
                        display_content += f"<p>{content}</p>"
                    elif description:
                        display_content += f"<p>{description}</p>"
                elif content:
                    display_content = content
                elif description:
                    display_content = description
                else:
                    continue  # 跳过空内容
            
            # 解析位置描述，转换为坐标
            position_desc = elem_pos.get('position_description', '')
            size_desc = elem_pos.get('size_description', '')
            alignment = elem_pos.get('alignment', 'center')
            spacing = elem_pos.get('spacing', {})
            
            # 【改进】优先使用spacing信息，然后从位置描述中解析
            # 传入已处理的元素信息，用于计算相对位置
            # 注意：在计算卡片位置时，需要知道当前卡片的索引
            # 所以先统计当前元素之前的同类型元素数量
            current_card_index = len([e for e in processed_elements if 'card' in e.get('element_type', '')])
            current_title_index = len([e for e in processed_elements if 'title' in e.get('element_type', '')])
            current_text_index = len([e for e in processed_elements if 'text' in e.get('element_type', '') or 'content' in e.get('element_type', '')])
            
            # 【新增】查找已处理的标题元素，用于计算副标题位置
            previous_title_element = None
            if 'subtitle' in elem_type:
                logger.info(f"--- [HTMLGenerator]: 【调试】查找标题元素，processed_elements数量: {len(processed_elements)}")
                # 查找最后一个标题元素
                for e in reversed(processed_elements):
                    elem_type_check = e.get('element_type', '')
                    if 'title' in elem_type_check and 'subtitle' not in elem_type_check:
                        previous_title_element = e
                        logger.info(f"--- [HTMLGenerator]: 【调试】找到标题元素: {e.get('element_id', 'unknown')}, element_type={elem_type_check}, coordinates={e.get('coordinates', {})}")
                        break
                if not previous_title_element:
                    logger.warning(f"--- [HTMLGenerator]: 【调试】未找到标题元素，processed_elements数量: {len(processed_elements)}")
                    for e in processed_elements:
                        logger.warning(f"--- [HTMLGenerator]: 【调试】已处理元素: {e.get('element_id', 'unknown')}, element_type={e.get('element_type', '')}, has_coordinates={'coordinates' in e}")
            
            coordinates = self._parse_coordinates_from_description(
                position_desc, size_desc, elem_type, alignment, spacing,
                processed_elements=processed_elements,
                element_type_counts=element_type_counts,
                current_card_index=current_card_index if 'card' in elem_type else None,
                current_title_index=current_title_index if 'title' in elem_type else None,
                current_text_index=current_text_index if ('text' in elem_type or 'content' in elem_type) else None,
                previous_title_element=previous_title_element
            )
            
            # 记录已处理的元素
            processed_elements.append({
                'element_id': elem_id,
                'element_type': elem_type,
                'coordinates': coordinates
            })
            
            # 转换为画布元素格式
            # 【修复】根据元素类型设置正确的type
            if 'title' in elem_type and 'subtitle' not in elem_type:
                elem_type_for_canvas = 'title'
            elif 'subtitle' in elem_type:
                elem_type_for_canvas = 'text'  # 副标题也使用text类型
            elif 'card' in elem_type:
                elem_type_for_canvas = 'card'
            else:
                elem_type_for_canvas = 'text'
            
            # 获取颜色配置（如果存在）
            style_config = {}
            if color_map:
                color_key = (slide_idx, elem_id)
                color_config = color_map.get(color_key, {})
                if color_config:
                    style_config = {
                        'text_color': color_config.get('text_color', ''),
                        'background_color': color_config.get('background_color', ''),
                        'border_color': color_config.get('border_color', '')
                    }
            
            canvas_elem = {
                'id': elem_id,
                'type': elem_type_for_canvas,
                'content': display_content,
                'coordinates': coordinates,
                'style_config': style_config  # 添加颜色配置
            }
            canvas_elements.append(canvas_elem)
        
        # 探针总结
        logger.info(f"--- [HTMLGenerator]: 【探针3总结】")
        logger.info(f"--- [HTMLGenerator]:   处理前element_positions数量: {len(element_positions)}")
        logger.info(f"--- [HTMLGenerator]:   处理后canvas_elements数量: {len(canvas_elements)}")
        logger.info(f"--- [HTMLGenerator]:   缺失element_id数量: {len(missing_element_ids)}")
        logger.info(f"--- [HTMLGenerator]:   重复element_id数量: {len(duplicate_element_ids)}")
        logger.info(f"--- [HTMLGenerator]:   重复内容哈希数量: {len(duplicate_content_hashes)}")
        if missing_element_ids:
            logger.warning(f"--- [HTMLGenerator]:   缺失的element_id列表: {missing_element_ids[:10]}")
        if duplicate_element_ids:
            logger.warning(f"--- [HTMLGenerator]:   重复的element_id列表: {duplicate_element_ids[:10]}")
        logger.info("="*80)
        
        # 2. 使用画布生成器生成HTML
        title = polished_slide.get('title', '')
        html = self.canvas_generator.create_canvas_html(
            elements=canvas_elements,
            show_grid=True  # 显示栅格标准尺
        )
        
        # 3. 替换标题
        html = html.replace('<title>16:9画布 - 坐标系演示</title>', f'<title>{title or "Slide"}</title>')
        
        return html
    
    def _parse_coordinates_from_description(
        self,
        position_description: str,
        size_description: str,
        element_type: str,
        alignment: str = 'center',
        spacing: Dict[str, Any] = None,
        processed_elements: List[Dict[str, Any]] = None,
        element_type_counts: Dict[str, int] = None,
        current_card_index: int = None,
        current_title_index: int = None,
        current_text_index: int = None,
        previous_title_element: Dict[str, Any] = None
    ) -> Dict[str, float]:
        """
        从位置描述中解析坐标
        返回坐标系坐标（左下角为原点）
        
        Args:
            position_description: 位置描述（如"位于页面顶部，距离上边距80px"）
            size_description: 尺寸描述（如"宽度占页面80%"）
            element_type: 元素类型
            alignment: 对齐方式（left|center|right）
            spacing: 间距信息（包含margin_top, margin_bottom, margin_left, margin_right）
            
        Returns:
            坐标字典 {left, bottom, width, height}
        """
        import re
        
        if spacing is None:
            spacing = {}
        if processed_elements is None:
            processed_elements = []
        if element_type_counts is None:
            element_type_counts = {}
        
        # ---------------------------------------------------------
        # 1. 初始位置计算 (Initial Position Calculation)
        # ---------------------------------------------------------
        logger.info(f"--- [HTMLGenerator]: 【调试】_parse_coordinates_from_description: element_type={element_type}, previous_title_element={previous_title_element is not None}")
        
        # 场景 A: 标题元素 (通常位于顶部)
        if 'title' in element_type and 'subtitle' not in element_type:
            width = self.CANVAS_WIDTH * 0.7  # 70%宽度
            height = 80
            left = (self.CANVAS_WIDTH - width) / 2  # 居中
            
            # 默认距离顶部 80px (或者使用 LayoutPlan 中的 margin_top)
            # 注意：bottom 是距离底部的距离
            default_top_margin = 80
            
            # 优先读取 spacing 中的 margin_top
            if spacing.get('margin_top'):
                m_top = str(spacing.get('margin_top'))
                match = re.search(r'(\d+)px', m_top)
                if match:
                    default_top_margin = float(match.group(1))
            
            # 核心修复公式：bottom = 画布高度 - 上边距 - 元素高度
            bottom = self.CANVAS_HEIGHT - default_top_margin - height
            logger.info(f"--- [HTMLGenerator]: 【修复】标题位置计算: margin_top={default_top_margin}px, bottom={bottom:.1f}px")
        
        # 场景 B: 副标题 (位于标题下方)
        elif 'subtitle' in element_type:
            width = self.CANVAS_WIDTH * 0.6  # 60%宽度
            height = 60
            left = (self.CANVAS_WIDTH - width) / 2  # 居中
            
            # 尝试找到前一个标题元素
            logger.info(f"--- [HTMLGenerator]: 【调试】副标题元素处理: previous_title_element={previous_title_element is not None}")
            if previous_title_element:
                prev_coords = previous_title_element.get('coordinates', {})
                prev_bottom = prev_coords.get('bottom', 0)
                prev_height = prev_coords.get('height', 0)
                logger.info(f"--- [HTMLGenerator]: 【调试】标题元素坐标: prev_bottom={prev_bottom:.1f}, prev_height={prev_height:.1f}")
                
                # 获取间距，默认为 24px (Ant Design Large Spacing)
                gap = 24
                if spacing.get('margin_top'):  # 如果副标题定义了上边距，用作与标题的间距
                    match = re.search(r'(\d+)px', str(spacing.get('margin_top')))
                    if match:
                        gap = float(match.group(1))
                
                # 核心修复公式：向下移动 = 减法
                # 副标题底部 = 标题底部 - 间距 - 副标题高度
                # prev_bottom 是标题的下边缘，副标题的下边缘应该在标题下边缘下方
                bottom = prev_bottom - gap - height
                logger.info(f"--- [HTMLGenerator]: 【修复】副标题位置计算: 基于标题元素, prev_bottom={prev_bottom:.1f}, gap={gap:.1f}px, bottom={bottom:.1f}px")
            else:
                # 如果没找到标题，默认放在较上方
                bottom = self.CANVAS_HEIGHT - 200 - height
                logger.warning(f"--- [HTMLGenerator]: 【调试】副标题位置计算: 未找到标题元素，使用默认位置, bottom={bottom:.1f}")
        # 卡片元素：根据卡片数量智能布局
        elif 'card' in element_type:
            card_count = element_type_counts.get('card', 1)
            # 计算每个卡片的宽度（考虑间距）
            card_spacing = 24  # 卡片之间的间距
            total_spacing = (card_count - 1) * card_spacing
            available_width = self.CANVAS_WIDTH - 200  # 左右各留100px边距
            width = (available_width - total_spacing) / card_count
            
            height = 200
            
            # 计算当前卡片的位置（使用传入的current_card_index）
            card_index = current_card_index if current_card_index is not None else 0
            logger.info(f"--- [HTMLGenerator]: 【调试】卡片布局计算: card_count={card_count}, card_index={card_index}, width={width:.1f}px")
            
            if card_count == 1:
                # 单个卡片：居中
                left = (self.CANVAS_WIDTH - width) / 2
            elif card_count == 2:
                # 两个卡片：左右分屏
                left = 100 + card_index * (width + card_spacing)
            elif card_count == 3:
                # 三个卡片：横向等分，居中分布
                total_width = card_count * width + (card_count - 1) * card_spacing
                start_left = (self.CANVAS_WIDTH - total_width) / 2
                left = start_left + card_index * (width + card_spacing)
                logger.info(f"--- [HTMLGenerator]: 【调试】三个卡片布局: start_left={start_left:.1f}px, left={left:.1f}px (card_index={card_index})")
            else:
                # 多个卡片：横向排列
                total_width = card_count * width + (card_count - 1) * card_spacing
                start_left = (self.CANVAS_WIDTH - total_width) / 2
                left = start_left + card_index * (width + card_spacing)
            
            # 卡片通常在中间区域
            bottom = (self.CANVAS_HEIGHT - height) / 2
        # 文本元素：较宽，居中
        elif 'text' in element_type or 'content' in element_type:
            width = self.CANVAS_WIDTH * 0.6  # 60%宽度
            height = 150
            left = (self.CANVAS_WIDTH - width) / 2  # 居中
            # 根据已处理的元素计算位置
            if processed_elements:
                # 在最后一个元素下方
                last_elem = processed_elements[-1]
                last_coords = last_elem.get('coordinates', {})
                last_bottom = last_coords.get('bottom', 0)
                last_height = last_coords.get('height', 0)
                bottom = last_bottom - last_height - 50  # 在下方50px
            else:
                bottom = 200
        # 其他元素：默认值
        else:
            width = 400
            height = 100
            left = 100
            bottom = 100
        
        # 解析位置
        # 【重要】对于副标题元素，如果已经通过previous_title_element计算了bottom，不要被position_description覆盖
        if 'subtitle' in element_type and previous_title_element:
            # 副标题：保持基于标题元素计算的结果，忽略position_description
            pass  # bottom已经在上面通过previous_title_element计算好了
        # 顶部
        elif '顶部' in position_description or '上方' in position_description:
            top_match = re.search(r'(\d+)px', position_description)
            if top_match:
                top_px = float(top_match.group(1))
                # 转换为bottom（从底部计算）
                bottom = self.CANVAS_HEIGHT - top_px - height
        # 中间
        elif '中间' in position_description or '中央' in position_description:
            bottom = (self.CANVAS_HEIGHT - height) / 2
        # 底部
        elif '底部' in position_description or '下方' in position_description:
            bottom_match = re.search(r'(\d+)px', position_description)
            if bottom_match:
                bottom = float(bottom_match.group(1))
            else:
                bottom = 50
        
        # 【改进】优先使用spacing信息（但不要覆盖智能布局计算的结果）
        # ---------------------------------------------------------
        # 2. Spacing 覆盖保护 (Spacing Override Protection)
        # ---------------------------------------------------------
        
        # 解析上边距（margin_top）
        # 【修复】对于标题和副标题，已经通过初始计算设置了bottom，不要被spacing覆盖
        if 'subtitle' in element_type and previous_title_element:
            # 副标题：保持基于标题元素计算的结果，忽略spacing中的margin_top
            pass  # bottom已经在上面通过previous_title_element计算好了
        elif 'title' in element_type and 'subtitle' not in element_type:
            # 标题：保持基于margin_top计算的结果，不再被spacing覆盖
            pass  # bottom已经在上面通过margin_top计算好了
        elif spacing.get('margin_top'):
            margin_top_str = str(spacing.get('margin_top', ''))
            if margin_top_str and margin_top_str != 'auto':
                top_match = re.search(r'(\d+)px', margin_top_str)
                if top_match:
                    top_px = float(top_match.group(1))
                    bottom = self.CANVAS_HEIGHT - top_px - height
        
        # 解析下边距（margin_bottom）
        # 【修复】仅当元素确实是"底部对齐"的组件(如页脚)时，才允许 margin_bottom 决定绝对位置
        # 否则 margin_bottom 只是用于把别的元素推开，不影响自己
        if 'subtitle' in element_type and previous_title_element:
            # 副标题：保持基于标题元素计算的结果，忽略spacing中的margin_bottom
            pass  # bottom已经在上面通过previous_title_element计算好了
        elif 'title' in element_type and 'subtitle' not in element_type:
            # 标题：保持基于margin_top计算的结果，忽略margin_bottom（防止被覆盖）
            pass  # bottom已经在上面通过margin_top计算好了
        elif spacing.get('margin_bottom') and 'footer' in element_type:
            # 仅对页脚元素，允许margin_bottom决定绝对位置
            margin_bottom_str = str(spacing.get('margin_bottom', ''))
            if margin_bottom_str and margin_bottom_str != 'auto':
                bottom_match = re.search(r'(\d+)px', margin_bottom_str)
                if bottom_match:
                    bottom = float(bottom_match.group(1))
                    logger.info(f"--- [HTMLGenerator]: 【修复】页脚元素使用margin_bottom: bottom={bottom:.1f}px")
        # 其他元素的margin_bottom被忽略（不作为绝对位置）
        
        # 解析左边距（margin_left）
        # 【重要】对于卡片元素，如果已经通过智能布局计算了left，不要被spacing覆盖
        # 卡片元素的智能布局优先级高于spacing信息
        if 'card' in element_type and current_card_index is not None:
            # 卡片元素：保持智能布局计算的结果，忽略spacing中的left/right
            pass  # left已经在上面通过智能布局计算好了
        elif spacing.get('margin_left'):
            margin_left_str = str(spacing.get('margin_left', ''))
            if margin_left_str == 'auto':
                # 居中
                left = (self.CANVAS_WIDTH - width) / 2
            elif margin_left_str and margin_left_str != 'auto':
                left_match = re.search(r'(\d+)px', margin_left_str)
                if left_match:
                    left = float(left_match.group(1))
        
        # 解析右边距（margin_right）
        # 【重要】对于卡片元素，如果已经通过智能布局计算了left，不要被spacing覆盖
        if 'card' in element_type and current_card_index is not None:
            # 卡片元素：保持智能布局计算的结果，忽略spacing中的left/right
            pass  # left已经在上面通过智能布局计算好了
        elif spacing.get('margin_right'):
            margin_right_str = str(spacing.get('margin_right', ''))
            if margin_right_str == 'auto':
                # 居中
                left = (self.CANVAS_WIDTH - width) / 2
            elif margin_right_str and margin_right_str != 'auto':
                right_match = re.search(r'(\d+)px', margin_right_str)
                if right_match:
                    right_px = float(right_match.group(1))
                    left = self.CANVAS_WIDTH - right_px - width
        
        # 解析水平位置（如果spacing没有提供，则从position_description解析）
        # 【重要】对于卡片元素，如果已经通过智能布局计算了left，不要被position_description覆盖
        if 'card' in element_type and current_card_index is not None:
            # 卡片元素：保持智能布局计算的结果，忽略position_description
            pass  # left已经在上面通过智能布局计算好了
        elif not spacing.get('margin_left') and not spacing.get('margin_right'):
            # 只有在spacing没有提供时才从position_description解析
            if '居中' in position_description or '水平居中' in position_description or alignment == 'center':
                # 先解析宽度，然后居中
                width_match = re.search(r'(\d+(?:\.\d+)?)%', size_description)
                if width_match:
                    width_pct = float(width_match.group(1))
                    width = (self.CANVAS_WIDTH * width_pct) / 100
                left = (self.CANVAS_WIDTH - width) / 2
            elif '左' in position_description or alignment == 'left':
                left_match = re.search(r'(\d+)px', position_description)
                if left_match:
                    left = float(left_match.group(1))
                else:
                    # 默认左对齐，留出边距
                    left = 100
            elif '右' in position_description or alignment == 'right':
                right_match = re.search(r'(\d+)px', position_description)
                if right_match:
                    right_px = float(right_match.group(1))
                    # 先解析宽度
                    width_match = re.search(r'(\d+(?:\.\d+)?)%', size_description)
                    if width_match:
                        width_pct = float(width_match.group(1))
                        width = (self.CANVAS_WIDTH * width_pct) / 100
                    left = self.CANVAS_WIDTH - right_px - width
                else:
                    # 默认右对齐，留出边距
                    left = self.CANVAS_WIDTH - width - 100
        
        # 解析尺寸
        if '宽度' in size_description:
            width_match = re.search(r'宽度[：:]\s*(\d+(?:\.\d+)?)%', size_description)
            if width_match:
                width_pct = float(width_match.group(1))
                width = (self.CANVAS_WIDTH * width_pct) / 100
            elif '栅格' in size_description:
                grid_match = re.search(r'(\d+)个?栅格', size_description)
                if grid_match:
                    grid_span = int(grid_match.group(1))
                    width = grid_span * self.canvas_generator.CELL_WIDTH
        
        if '高度' in size_description:
            height_match = re.search(r'高度[：:]\s*(\d+)px', size_description)
            if height_match:
                height = float(height_match.group(1))
            elif '栅格' in size_description:
                grid_match = re.search(r'(\d+)个?栅格', size_description)
                if grid_match:
                    grid_span = int(grid_match.group(1))
                    height = grid_span * self.canvas_generator.CELL_HEIGHT
        
        return {
            'left': left,
            'bottom': bottom,
            'width': width,
            'height': height
        }
    
    def _generate_css_with_layout_plan(
        self,
        layout_plan: Dict[str, Any],
        element_positions: List[Dict[str, Any]],
        color_map: Optional[Dict[Tuple[int, str], Dict[str, Any]]] = None,
        slide_idx: int = 0
    ) -> str:
        """
        生成包含布局规划样式的CSS
        
        Args:
            layout_plan: 布局规划详情
            element_positions: 元素位置列表
            
        Returns:
            CSS字符串
        """
        # 基础CSS
        base_css = self._generate_css()
        
        # 动态样式（基于布局规划）
        dynamic_styles = []
        
        for elem_pos in element_positions:
            elem_id = elem_pos.get('element_id', '')
            elem_type = elem_pos.get('element_type', '')
            position_desc = elem_pos.get('position_description', '')
            size_desc = elem_pos.get('size_description', '')
            alignment = elem_pos.get('alignment', 'center')
            spacing = elem_pos.get('spacing', {})
            
            # 尝试从位置描述中提取栅格坐标（如果布局规划器提供了）
            grid_x = elem_pos.get('grid_x')
            grid_y = elem_pos.get('grid_y')
            span_x = elem_pos.get('span_x')
            span_y = elem_pos.get('span_y')
            
            # 如果没有提供栅格坐标，尝试从位置描述中解析
            if grid_x is None or grid_y is None:
                grid_x, grid_y, span_x, span_y = self._parse_grid_from_description(
                    position_desc, size_desc, alignment
                )
            
            # 解析位置和尺寸（如果提供了栅格坐标，使用绝对定位）
            if grid_x is not None and grid_y is not None:
                # 使用坐标转换函数计算像素位置
                left, top, width, height = self._grid_to_pixel(grid_x, grid_y, span_x or 8, span_y or 2)
                css_props = f"position: absolute;\n            left: {left}px;\n            top: {top}px;\n            width: {width}px;\n            height: {height}px;"
            else:
                # 使用原来的方法（基于margin等）
                css_props = self._parse_position_to_css(
                    element_id=elem_id,
                    position_description=position_desc,
                    size_description=size_desc,
                    alignment=alignment,
                    spacing=spacing,
                    element_type=elem_type
                )
            
            # 【新增】应用颜色配置（使用(slide_idx, element_id)作为键）
            key = (slide_idx, elem_id)
            if color_map and key in color_map:
                elem_color = color_map[key]
                if elem_color.get('text_color'):
                    css_props += f"\n            color: {elem_color['text_color']};"
                if elem_color.get('background_color'):
                    css_props += f"\n            background-color: {elem_color['background_color']};"
                if elem_color.get('border_color'):
                    css_props += f"\n            border-color: {elem_color['border_color']};"
                    css_props += f"\n            border-width: 1px;"
                    css_props += f"\n            border-style: solid;"
            
            if css_props:
                dynamic_styles.append(f"""
        /* 元素: {elem_id} ({elem_type}) */
        #{elem_id} {{
            {css_props}
        }}""")
        
        return base_css + '\n'.join(dynamic_styles)
    
    def _parse_position_to_css(
        self,
        element_id: str,
        position_description: str,
        size_description: str,
        alignment: str,
        spacing: Dict[str, Any],
        element_type: str,
        grid_x: Optional[float] = None,
        grid_y: Optional[float] = None,
        span_x: Optional[float] = None,
        span_y: Optional[float] = None
    ) -> str:
        """
        解析位置描述，生成CSS属性
        
        Args:
            element_id: 元素ID
            position_description: 位置描述（文字）
            size_description: 尺寸描述（文字）
            alignment: 对齐方式
            spacing: 间距对象
            element_type: 元素类型
            
        Returns:
            CSS属性字符串
        """
        import re
        
        css_props = []
        
        # 1. 解析位置（margin-top, margin-left等）
        # 例如："距离上边距80px" → margin-top: 80px
        if '距离上边距' in position_description or '上' in position_description:
            margin_top_match = re.search(r'(\d+)px', position_description)
            if margin_top_match:
                css_props.append(f"margin-top: {margin_top_match.group(1)}px;")
            elif 'calc' in position_description:
                # 提取calc表达式
                calc_match = re.search(r'calc\([^)]+\)', position_description)
                if calc_match:
                    css_props.append(f"margin-top: {calc_match.group(0)};")
        
        if spacing.get('margin_top'):
            css_props.append(f"margin-top: {spacing['margin_top']};")
        if spacing.get('margin_bottom'):
            css_props.append(f"margin-bottom: {spacing['margin_bottom']};")
        if spacing.get('margin_left'):
            css_props.append(f"margin-left: {spacing['margin_left']};")
        if spacing.get('margin_right'):
            css_props.append(f"margin-right: {spacing['margin_right']};")
        
        # 2. 解析尺寸（width, height）
        # 例如："宽度占页面80%" → width: 80%
        if '宽度占页面' in size_description:
            width_match = re.search(r'(\d+(?:\.\d+)?)%', size_description)
            if width_match:
                css_props.append(f"width: {width_match.group(1)}%;")
        elif '宽度' in size_description:
            width_match = re.search(r'宽度[：:]\s*(\d+(?:\.\d+)?)%', size_description)
            if width_match:
                css_props.append(f"width: {width_match.group(1)}%;")
        
        # 栅格宽度（如"占据7个栅格宽度"）
        if '栅格' in size_description:
            grid_match = re.search(r'(\d+)个?栅格', size_description)
            if grid_match:
                grid_span = int(grid_match.group(1))
                # 计算百分比（24栅格系统）
                width_pct = (grid_span / 24) * 100
                css_props.append(f"width: {width_pct:.2f}%;")
        
        # 高度
        if '高度自适应' in size_description:
            css_props.append("height: auto;")
        elif '高度' in size_description:
            height_match = re.search(r'高度[：:]\s*(\d+)px', size_description)
            if height_match:
                css_props.append(f"height: {height_match.group(1)}px;")
            elif '最小高度' in size_description:
                min_height_match = re.search(r'(\d+)px', size_description)
                if min_height_match:
                    css_props.append(f"min-height: {min_height_match.group(1)}px;")
        
        # 3. 对齐方式
        if alignment == 'center':
            css_props.append("text-align: center;")
            css_props.append("margin-left: auto;")
            css_props.append("margin-right: auto;")
        elif alignment == 'left':
            css_props.append("text-align: left;")
        elif alignment == 'right':
            css_props.append("text-align: right;")
        
        # 4. 根据元素类型添加特定样式
        if 'card' in element_type:
            css_props.append("background: #ffffff;")
            css_props.append("border: 1px solid #d9d9d9;")
            css_props.append("border-radius: 6px;")
            css_props.append("box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);")
            css_props.append("padding: 24px;")
        elif 'title' in element_type:
            # 标题样式在基础CSS中已定义，这里可以覆盖特定属性
            pass
        
        # 5. 位置定位（如果需要绝对定位）
        if '居中' in position_description and '水平居中' in position_description:
            css_props.append("position: relative;")
            # 如果同时有垂直居中，使用flex或transform
            if '垂直' in position_description or '垂直和水平居中' in position_description:
                css_props.append("display: flex;")
                css_props.append("align-items: center;")
                css_props.append("justify-content: center;")
        
        return '\n            '.join(css_props) if css_props else ''
    
    def _parse_grid_from_description(
        self,
        position_description: str,
        size_description: str,
        alignment: str
    ) -> tuple:
        """
        从位置描述中解析栅格坐标（简化版本）
        
        Args:
            position_description: 位置描述
            size_description: 尺寸描述
            alignment: 对齐方式
            
        Returns:
            (grid_x, grid_y, span_x, span_y) 栅格坐标
        """
        import re
        
        # 默认值
        grid_x = 2
        grid_y = 0
        span_x = 20
        span_y = 2
        
        # 解析位置
        if '顶部' in position_description or '上方' in position_description:
            grid_y = 11.5  # 接近顶部
        elif '中间' in position_description or '中央' in position_description:
            grid_y = 5.75  # 中间
        elif '底部' in position_description or '下方' in position_description:
            grid_y = 0  # 底部
        
        # 解析对齐
        if alignment == 'center' or '居中' in position_description:
            # 居中：左右各留2列
            grid_x = 2
            span_x = 20
        elif alignment == 'left' or '左' in position_description:
            # 左对齐：左边留2列
            grid_x = 2
            span_x = 10
        elif alignment == 'right' or '右' in position_description:
            # 右对齐：右边留2列
            grid_x = 12
            span_x = 10
        
        # 解析尺寸
        if '栅格' in size_description:
            grid_match = re.search(r'(\d+)个?栅格', size_description)
            if grid_match:
                span_x = int(grid_match.group(1))
        
        return (grid_x, grid_y, span_x, span_y)
    
    def _parse_position_priority(self, element_position: Dict[str, Any]) -> int:
        """
        解析元素位置优先级（用于排序）
        
        Args:
            element_position: 元素位置对象
            
        Returns:
            优先级数值（越小越靠前）
        """
        position_desc = element_position.get('position_description', '')
        
        # 标题通常在顶部
        if '顶部' in position_desc or '上方' in position_desc:
            return 1
        # 内容在中间
        elif '中间' in position_desc or '中央' in position_desc:
            return 2
        # 底部内容
        elif '底部' in position_desc or '下方' in position_desc:
            return 3
        else:
            return 2
    
    def _generate_element_html(
        self,
        element_id: str,
        element_type: str,
        element_position: Dict[str, Any],
        element_content: Dict[str, Any],
        visual_hierarchy: str,
        color_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        生成单个元素的HTML
        
        Args:
            element_id: 元素ID
            element_type: 元素类型
            element_position: 元素位置信息
            element_content: 元素内容（从润色内容中获取）
            visual_hierarchy: 视觉层次说明
            
        Returns:
            HTML字符串
        """
        # 获取内容
        title = element_content.get('title', '')
        content = element_content.get('content', '')
        data = element_content.get('data', '')
        description = element_content.get('description', '')
        
        # 根据元素类型生成HTML
        if 'title_text' in element_type:
            text = title or content or description
            if text:
                # 解析字号（从visual_hierarchy中提取）
                font_size = self._extract_font_size(visual_hierarchy, element_id)
                return f'<h1 id="{element_id}" class="title" style="font-size: {font_size};">{text}</h1>'
        
        elif 'subtitle_text' in element_type:
            text = title or content or description
            if text:
                font_size = self._extract_font_size(visual_hierarchy, element_id, default='32pt')
                return f'<h2 id="{element_id}" class="subtitle" style="font-size: {font_size};">{text}</h2>'
        
        elif 'content_text' in element_type:
            text = content or description
            if text:
                font_size = self._extract_font_size(visual_hierarchy, element_id, default='20pt')
                return f'<p id="{element_id}" class="body-text" style="font-size: {font_size};">{text}</p>'
        
        elif 'card' in element_type:
            # 卡片元素
            card_title = title or ''
            card_content = content or description or ''
            card_data = data or ''
            
            card_html = f'<div id="{element_id}" class="card">'
            
            if card_title:
                card_html += f'<h3 class="card-title">{card_title}</h3>'
            
            if card_data:
                card_html += f'<div class="card-data">{card_data}</div>'
            
            if card_content:
                card_html += f'<div class="card-content">{card_content}</div>'
            
            card_html += '</div>'
            return card_html
        
        return ''
    
    def _extract_font_size(self, visual_hierarchy: str, element_id: str, default: str = '48pt') -> str:
        """
        从视觉层次说明中提取字号
        
        Args:
            visual_hierarchy: 视觉层次说明
            element_id: 元素ID
            default: 默认字号
            
        Returns:
            字号字符串（如"76pt"）
        """
        import re
        
        # 尝试从visual_hierarchy中提取
        if element_id in visual_hierarchy:
            # 查找该元素相关的字号
            pattern = rf'{element_id}[^。]*?(\d+)pt'
            match = re.search(pattern, visual_hierarchy)
            if match:
                return f"{match.group(1)}pt"
        
        # 查找通用字号描述
        if '76pt' in visual_hierarchy or '超大字号' in visual_hierarchy:
            return '76pt'
        elif '48pt' in visual_hierarchy or '大号字体' in visual_hierarchy:
            return '48pt'
        elif '32pt' in visual_hierarchy or '中等字号' in visual_hierarchy:
            return '32pt'
        elif '20pt' in visual_hierarchy or '小号字体' in visual_hierarchy:
            return '20pt'
        
        return default

