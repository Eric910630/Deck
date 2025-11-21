"""
基于无头浏览器的图表生成器
使用Playwright + AntV G2Plot渲染真实的web图表
"""

import json
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
from loguru import logger

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not installed. Install with: pip install playwright && playwright install chromium")

from ant_design_theme import ant_design_theme
from antv_chart_theme import antv_chart_theme


class WebChartGenerator:
    """
    基于无头浏览器的图表生成器
    使用Playwright渲染AntV G2Plot图表
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        初始化Web图表生成器
        
        Args:
            output_dir: 图表输出目录
        """
        if output_dir is None:
            output_dir = Path.cwd() / "charts"
        elif isinstance(output_dir, str):
            output_dir = Path(output_dir)
        
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True, parents=True)
        logger.info(f"--- [WebChartGenerator]: Output directory: {self.output_dir}")
        
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright is required for WebChartGenerator. "
                "Install with: pip install playwright && playwright install chromium"
            )
    
    def _generate_html_template(
        self,
        chart_type: str,
        data: List[Dict[str, Any]],
        config: Dict[str, Any]
    ) -> str:
        """
        生成包含AntV G2Plot图表的HTML模板
        
        Args:
            chart_type: 图表类型 (bar, line, pie, column)
            data: 数据列表
            config: 图表配置
            
        Returns:
            HTML字符串
        """
        # 转换数据为JavaScript格式
        data_json = json.dumps(data, ensure_ascii=False, indent=2)
        
        # 获取Ant Design/AntV配色
        colors = antv_chart_theme.get_default_colors()
        colors_json = json.dumps(colors)
        
        # 图表配置
        title = config.get('title', 'Chart')
        width = config.get('width', 800)
        height = config.get('height', 500)
        
        # 根据图表类型生成不同的G2Plot配置
        chart_config_js = self._generate_chart_config(chart_type, config)
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: {ant_design_theme.typography.fontFamily};
            background-color: {ant_design_theme.colors.colorBgBase};
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        #container {{
            width: {width}px;
            height: {height}px;
            background-color: {ant_design_theme.colors.colorBgContainer};
            border-radius: {ant_design_theme.borderRadius.borderRadius}px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            padding: 20px;
        }}
        .chart-title {{
            font-size: {ant_design_theme.typography.fontSizeLG}px;
            font-weight: {ant_design_theme.typography.fontWeightStrong};
            color: {ant_design_theme.colors.colorText};
            margin-bottom: 16px;
            text-align: center;
        }}
        #chart {{
            width: 100%;
            height: calc(100% - 50px);
        }}
    </style>
</head>
<body>
    <div id="container">
        <div class="chart-title">{title}</div>
        <div id="chart"></div>
    </div>
    
    <!-- AntV G2Plot CDN -->
    <script src="https://unpkg.com/@antv/g2plot@latest/dist/g2plot.min.js"></script>
    <script>
        const data = {data_json};
        const colors = {colors_json};
        
        // 图表配置
        const chartConfig = {{
            container: 'chart',
            data: data,
            {chart_config_js}
            theme: {{
                defaultColor: '{ant_design_theme.colors.colorPrimary}',
                styleSheet: {{
                    fontFamily: '{ant_design_theme.typography.fontFamily}',
                    fontSize: {ant_design_theme.typography.fontSize}
                }}
            }}
        }};
        
        // 创建图表
        let plot;
        const chartType = '{chart_type}';
        
        if (chartType === 'bar' || chartType === 'bar_chart') {{
            const {{ Bar }} = G2Plot;
            plot = new Bar(chartConfig);
        }} else if (chartType === 'line' || chartType === 'line_chart') {{
            const {{ Line }} = G2Plot;
            plot = new Line(chartConfig);
        }} else if (chartType === 'pie' || chartType === 'pie_chart') {{
            const {{ Pie }} = G2Plot;
            plot = new Pie(chartConfig);
        }} else if (chartType === 'column' || chartType === 'column_chart') {{
            const {{ Column }} = G2Plot;
            plot = new Column(chartConfig);
        }} else {{
            // 默认使用Bar
            const {{ Bar }} = G2Plot;
            plot = new Bar(chartConfig);
        }}
        
        plot.render();
        
        // 等待图表渲染完成
        setTimeout(() => {{
            console.log('Chart rendered');
        }}, 1000);
    </script>
</body>
</html>"""
        return html
    
    def _generate_chart_config(self, chart_type: str, config: Dict[str, Any]) -> str:
        """
        生成G2Plot图表配置的JavaScript代码
        
        Args:
            chart_type: 图表类型
            config: 配置字典
            
        Returns:
            JavaScript配置代码字符串
        """
        x_key = config.get('x_key', 'x')
        y_key = config.get('y_key', 'y')
        label_key = config.get('label_key', 'label')
        value_key = config.get('value_key', 'value')
        
        if chart_type in ['pie', 'pie_chart']:
            # 饼图配置
            return f"""
            angleField: '{value_key}',
            colorField: '{label_key}',
            color: colors,
            label: {{
                type: 'outer',
                content: '{{name}}: {{percentage}}'
            }},
            interactions: [{{ type: 'element-active' }}],
            """
        elif chart_type in ['bar', 'bar_chart', 'column', 'column_chart']:
            # 柱状图配置
            return f"""
            xField: '{x_key}',
            yField: '{y_key}',
            color: '{ant_design_theme.colors.colorPrimary}',
            label: {{
                position: 'top',
                style: {{
                    fill: '{ant_design_theme.colors.colorText}',
                    fontSize: {ant_design_theme.typography.fontSizeSM}
                }}
            }},
            """
        elif chart_type in ['line', 'line_chart']:
            # 折线图配置
            return f"""
            xField: '{x_key}',
            yField: '{y_key}',
            color: '{ant_design_theme.colors.colorPrimary}',
            point: {{
                size: 4,
                shape: 'circle',
                style: {{
                    fill: '{ant_design_theme.colors.colorPrimary}',
                    stroke: '{ant_design_theme.colors.colorBgBase}',
                    lineWidth: 2
                }}
            }},
            smooth: true,
            """
        else:
            # 默认配置
            return f"""
            xField: '{x_key}',
            yField: '{y_key}',
            color: '{ant_design_theme.colors.colorPrimary}',
            """
    
    async def _render_chart(
        self,
        html_content: str,
        output_path: Path,
        width: int = 800,
        height: int = 500
    ) -> str:
        """
        使用Playwright渲染HTML并截图
        
        Args:
            html_content: HTML内容
            output_path: 输出文件路径
            width: 视口宽度
            height: 视口高度
            
        Returns:
            保存的文件路径
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                viewport={'width': width + 40, 'height': height + 100}  # 留出padding
            )
            
            # 加载HTML内容
            await page.set_content(html_content, wait_until='networkidle')
            
            # 等待图表渲染（G2Plot需要时间渲染）
            await page.wait_for_timeout(2000)  # 等待2秒确保图表完全渲染
            
            # 截图
            await page.screenshot(
                path=str(output_path),
                full_page=False,
                clip={'x': 0, 'y': 0, 'width': width + 40, 'height': height + 100}
            )
            
            await browser.close()
        
        logger.info(f"--- [WebChartGenerator]: Chart saved to {output_path}")
        return str(output_path)
    
    async def generate_bar_chart_async(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Bar Chart",
        width: int = 800,
        height: int = 500
    ) -> str:
        """
        异步生成柱状图
        
        Args:
            data: 数据列表
            x_key: X轴数据键名
            y_key: Y轴数据键名
            title: 图表标题
            width: 图表宽度
            height: 图表高度
            
        Returns:
            保存的图表文件路径
        """
        config = {
            'title': title,
            'width': width,
            'height': height,
            'x_key': x_key,
            'y_key': y_key
        }
        
        html = self._generate_html_template('bar', data, config)
        filename = f"web_bar_chart_{title.replace(' ', '_')}.png"
        output_path = self.output_dir / filename
        
        return await self._render_chart(html, output_path, width, height)
    
    async def generate_line_chart_async(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Line Chart",
        width: int = 800,
        height: int = 500
    ) -> str:
        """
        异步生成折线图
        """
        config = {
            'title': title,
            'width': width,
            'height': height,
            'x_key': x_key,
            'y_key': y_key
        }
        
        html = self._generate_html_template('line', data, config)
        filename = f"web_line_chart_{title.replace(' ', '_')}.png"
        output_path = self.output_dir / filename
        
        return await self._render_chart(html, output_path, width, height)
    
    async def generate_pie_chart_async(
        self,
        data: List[Dict[str, Any]],
        label_key: str,
        value_key: str,
        title: str = "Pie Chart",
        width: int = 800,
        height: int = 500
    ) -> str:
        """
        异步生成饼图
        """
        config = {
            'title': title,
            'width': width,
            'height': height,
            'label_key': label_key,
            'value_key': value_key
        }
        
        html = self._generate_html_template('pie', data, config)
        filename = f"web_pie_chart_{title.replace(' ', '_')}.png"
        output_path = self.output_dir / filename
        
        return await self._render_chart(html, output_path, width, height)
    
    # 同步包装方法
    def generate_bar_chart(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Bar Chart",
        width: int = 800,
        height: int = 500
    ) -> str:
        """同步生成柱状图"""
        return asyncio.run(self.generate_bar_chart_async(data, x_key, y_key, title, width, height))
    
    def generate_line_chart(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Line Chart",
        width: int = 800,
        height: int = 500
    ) -> str:
        """同步生成折线图"""
        return asyncio.run(self.generate_line_chart_async(data, x_key, y_key, title, width, height))
    
    def generate_pie_chart(
        self,
        data: List[Dict[str, Any]],
        label_key: str,
        value_key: str,
        title: str = "Pie Chart",
        width: int = 800,
        height: int = 500
    ) -> str:
        """同步生成饼图"""
        return asyncio.run(self.generate_pie_chart_async(data, label_key, value_key, title, width, height))

