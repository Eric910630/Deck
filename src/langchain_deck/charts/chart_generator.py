"""
独立的图表生成模块
使用matplotlib生成各种类型的图表
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from loguru import logger

# 导入Ant Design和AntV主题
from ant_design_theme import ant_design_theme
from antv_chart_theme import antv_chart_theme

# 配置matplotlib使用Ant Design字体和样式
try:
    # Ant Design字体系统（优先中文字体，确保中文显示正常）
    plt.rcParams['font.sans-serif'] = [
        'Microsoft YaHei', 'SimHei',  # 中文字体优先
        '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 
        'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif'
    ]
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    plt.rcParams['font.size'] = ant_design_theme.typography.fontSize
except Exception:
    logger.warning("Failed to set Ant Design font, using default")


class ChartGenerator:
    """
    独立的图表生成器
    优先使用WebChartGenerator（无头浏览器+AntV），fallback到matplotlib
    """
    
    def __init__(self, output_dir: Optional[Path] = None, use_web: bool = True):
        """
        初始化图表生成器
        
        Args:
            output_dir: 图表输出目录
            use_web: 是否优先使用web渲染（Playwright + AntV），如果失败则fallback到matplotlib
        """
        if output_dir is None:
            output_dir = Path.cwd() / "charts"
        elif isinstance(output_dir, str):
            output_dir = Path(output_dir)
        
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.use_web = use_web
        
        # 尝试初始化WebChartGenerator
        self.web_generator = None
        if use_web:
            try:
                from web_chart_generator import WebChartGenerator
                self.web_generator = WebChartGenerator(output_dir=output_dir)
                logger.info("--- [ChartGenerator]: Using WebChartGenerator (Playwright + AntV)")
            except Exception as e:
                logger.warning(f"--- [ChartGenerator]: WebChartGenerator not available: {e}. Falling back to matplotlib")
                self.web_generator = None
        
        logger.info(f"--- [ChartGenerator]: Output directory: {self.output_dir}")
    
    def _prepare_data(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        准备数据，转换为DataFrame
        
        Args:
            data: 数据列表，每个元素是一个字典
            
        Returns:
            pandas DataFrame
        """
        if not data:
            raise ValueError("Data list is empty")
        
        return pd.DataFrame(data)
    
    def _save_chart(self, fig, filename: str, dpi: int = 300) -> str:
        """
        保存图表到文件
        
        Args:
            fig: matplotlib figure对象
            filename: 文件名
            dpi: 分辨率
            
        Returns:
            保存的文件路径
        """
        file_path = self.output_dir / filename
        fig.savefig(
            str(file_path),
            dpi=dpi,
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none'
        )
        plt.close(fig)  # 关闭图形以释放内存
        logger.info(f"--- [ChartGenerator]: Chart saved to {file_path}")
        return str(file_path)
    
    def generate_bar_chart(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Bar Chart",
        width: float = 10,
        height: float = 6,
        color: Optional[str] = None
    ) -> str:
        """
        生成柱状图
        优先使用WebChartGenerator（AntV），失败则使用matplotlib
        """
        # 尝试使用web渲染
        if self.web_generator:
            try:
                # 转换尺寸（matplotlib使用英寸，web使用像素）
                width_px = int(width * 96)  # 1英寸 = 96像素
                height_px = int(height * 96)
                return self.web_generator.generate_bar_chart(
                    data, x_key, y_key, title, width_px, height_px
                )
            except Exception as e:
                logger.warning(f"--- [ChartGenerator]: Web rendering failed: {e}. Using matplotlib fallback")
        
        # Fallback到matplotlib
        return self._generate_bar_chart_matplotlib(data, x_key, y_key, title, width, height, color)
    
    def _generate_bar_chart_matplotlib(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Bar Chart",
        width: float = 10,
        height: float = 6,
        color: Optional[str] = None
    ) -> str:
        """
        生成柱状图
        
        Args:
            data: 数据列表
            x_key: X轴数据键名
            y_key: Y轴数据键名
            title: 图表标题
            width: 图表宽度（英寸）
            height: 图表高度（英寸）
            color: 柱状图颜色
            
        Returns:
            保存的图表文件路径
        """
        # matplotlib实现
        df = self._prepare_data(data)
        
        # 使用AntV/Ant Design配色
        if color is None:
            color = antv_chart_theme.get_line_chart_color()
        
        # 如果是多系列，使用AntV分类色
        colors = antv_chart_theme.get_bar_chart_colors(len(df))
        
        fig, ax = plt.subplots(figsize=(width, height))
        
        # 应用Ant Design样式
        fig.patch.set_facecolor(ant_design_theme.colors.colorBgBase)
        ax.set_facecolor(ant_design_theme.colors.colorBgContainer)
        
        # 使用AntV配色方案
        if len(df) > 1:
            bars = ax.bar(df[x_key], df[y_key], color=colors[:len(df)], 
                         edgecolor=ant_design_theme.colors.colorBorder, linewidth=1)
        else:
            bars = ax.bar(df[x_key], df[y_key], color=color,
                         edgecolor=ant_design_theme.colors.colorBorder, linewidth=1)
        
        # 添加数值标签
        ax.bar_label(bars, padding=3)
        
        # 使用Ant Design字体和颜色
        ax.set_xlabel(x_key, fontsize=ant_design_theme.typography.fontSize, 
                     color=ant_design_theme.colors.colorText)
        ax.set_ylabel(y_key, fontsize=ant_design_theme.typography.fontSize,
                     color=ant_design_theme.colors.colorText)
        ax.set_title(title, fontsize=ant_design_theme.typography.fontSizeLG, 
                    fontweight='bold',
                    color=ant_design_theme.colors.colorText)
        
        # Ant Design网格样式
        ax.grid(axis='y', color=ant_design_theme.colors.colorBorderSecondary, 
               linestyle='-', linewidth=1, alpha=0.5)
        
        # 坐标轴颜色
        ax.spines['top'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['right'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['bottom'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['left'].set_color(ant_design_theme.colors.colorBorder)
        
        # 标签颜色
        ax.tick_params(colors=ant_design_theme.colors.colorTextSecondary)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        filename = f"bar_chart_{title.replace(' ', '_')}.png"
        return self._save_chart(fig, filename)
    
    def generate_line_chart(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Line Chart",
        width: float = 10,
        height: float = 6,
        color: Optional[str] = None
    ) -> str:
        """
        生成折线图
        优先使用WebChartGenerator（AntV），失败则使用matplotlib
        """
        if self.web_generator:
            try:
                width_px = int(width * 96)
                height_px = int(height * 96)
                return self.web_generator.generate_line_chart(
                    data, x_key, y_key, title, width_px, height_px
                )
            except Exception as e:
                logger.warning(f"--- [ChartGenerator]: Web rendering failed: {e}. Using matplotlib fallback")
        
        return self._generate_line_chart_matplotlib(data, x_key, y_key, title, width, height, color)
    
    def _generate_line_chart_matplotlib(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Line Chart",
        width: float = 10,
        height: float = 6,
        color: Optional[str] = None
    ) -> str:
        """
        生成折线图
        
        Args:
            data: 数据列表
            x_key: X轴数据键名
            y_key: Y轴数据键名
            title: 图表标题
            width: 图表宽度
            height: 图表高度
            color: 折线颜色
            
        Returns:
            保存的图表文件路径
        """
        # matplotlib实现
        df = self._prepare_data(data)
        df = df.sort_values(by=x_key)  # 按X轴排序
        
        # 使用AntV配色
        if color is None:
            color = antv_chart_theme.get_line_chart_color()
        
        fig, ax = plt.subplots(figsize=(width, height))
        
        # 应用Ant Design样式
        fig.patch.set_facecolor(ant_design_theme.colors.colorBgBase)
        ax.set_facecolor(ant_design_theme.colors.colorBgContainer)
        
        ax.plot(df[x_key], df[y_key], color=color, linewidth=2.5, 
               marker='o', markersize=6, markerfacecolor=color, 
               markeredgecolor=ant_design_theme.colors.colorBgBase,
               markeredgewidth=1)
        
        # 使用Ant Design字体和颜色
        ax.set_xlabel(x_key, fontsize=ant_design_theme.typography.fontSize,
                     color=ant_design_theme.colors.colorText)
        ax.set_ylabel(y_key, fontsize=ant_design_theme.typography.fontSize,
                     color=ant_design_theme.colors.colorText)
        ax.set_title(title, fontsize=ant_design_theme.typography.fontSizeLG,
                    fontweight='bold',
                    color=ant_design_theme.colors.colorText)
        
        # Ant Design网格样式
        ax.grid(True, color=ant_design_theme.colors.colorBorderSecondary,
               linestyle='-', linewidth=1, alpha=0.5)
        
        # 坐标轴样式
        ax.spines['top'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['right'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['bottom'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['left'].set_color(ant_design_theme.colors.colorBorder)
        ax.tick_params(colors=ant_design_theme.colors.colorTextSecondary)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        filename = f"line_chart_{title.replace(' ', '_')}.png"
        return self._save_chart(fig, filename)
    
    def generate_pie_chart(
        self,
        data: List[Dict[str, Any]],
        label_key: str,
        value_key: str,
        title: str = "Pie Chart",
        width: float = 10,
        height: float = 8
    ) -> str:
        """
        生成饼图
        
        Args:
            data: 数据列表
            label_key: 标签键名
            value_key: 数值键名
            title: 图表标题
            width: 图表宽度
            height: 图表高度
            
        Returns:
            保存的图表文件路径
        """
        # matplotlib实现
        df = self._prepare_data(data)
        
        # 使用AntV/Ant Design配色方案
        colors = antv_chart_theme.get_pie_chart_colors(len(df))
        
        fig, ax = plt.subplots(figsize=(width, height))
        
        # 应用Ant Design样式
        fig.patch.set_facecolor(ant_design_theme.colors.colorBgBase)
        
        wedges, texts, autotexts = ax.pie(
            df[value_key],
            labels=df[label_key],
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={
                'fontsize': ant_design_theme.typography.fontSizeSM,
                'color': ant_design_theme.colors.colorText
            },
            wedgeprops={'edgecolor': ant_design_theme.colors.colorBgBase, 'linewidth': 2}
        )
        
        # 设置百分比文本样式（Ant Design风格）
        for autotext in autotexts:
            autotext.set_color(ant_design_theme.colors.colorText)
            autotext.set_fontweight('bold')
        
        # 设置标签颜色
        for text in texts:
            text.set_color(ant_design_theme.colors.colorText)
            text.set_fontsize(ant_design_theme.typography.fontSizeSM)
        
        ax.set_title(title, fontsize=ant_design_theme.typography.fontSizeLG,
                    fontweight='bold',
                    color=ant_design_theme.colors.colorText, pad=20)
        plt.tight_layout()
        
        filename = f"pie_chart_{title.replace(' ', '_')}.png"
        return self._save_chart(fig, filename)
    
    def generate_grouped_bar_chart(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_keys: List[str],
        title: str = "Grouped Bar Chart",
        width: float = 12,
        height: float = 6
    ) -> str:
        """
        生成分组柱状图
        
        Args:
            data: 数据列表
            x_key: X轴数据键名
            y_keys: Y轴数据键名列表（多个系列）
            title: 图表标题
            width: 图表宽度
            height: 图表高度
            
        Returns:
            保存的图表文件路径
        """
        # matplotlib实现
        df = self._prepare_data(data)
        
        x = range(len(df))
        bar_width = 0.8 / len(y_keys)
        
        # 使用AntV/Ant Design配色方案
        colors = antv_chart_theme.get_bar_chart_colors(len(y_keys))
        
        fig, ax = plt.subplots(figsize=(width, height))
        
        # 应用Ant Design样式
        fig.patch.set_facecolor(ant_design_theme.colors.colorBgBase)
        ax.set_facecolor(ant_design_theme.colors.colorBgContainer)
        
        for i, y_key in enumerate(y_keys):
            offset = (i - len(y_keys) / 2 + 0.5) * bar_width
            bars = ax.bar(
                [xi + offset for xi in x],
                df[y_key],
                bar_width,
                label=y_key,
                color=colors[i % len(colors)],
                edgecolor=ant_design_theme.colors.colorBorder,
                linewidth=1
            )
            ax.bar_label(bars, padding=3, fontsize=ant_design_theme.typography.fontSizeSM,
                        color=ant_design_theme.colors.colorText)
        
        # 使用Ant Design样式
        ax.set_xlabel(x_key, fontsize=ant_design_theme.typography.fontSize,
                     color=ant_design_theme.colors.colorText)
        ax.set_ylabel('Value', fontsize=ant_design_theme.typography.fontSize,
                     color=ant_design_theme.colors.colorText)
        ax.set_title(title, fontsize=ant_design_theme.typography.fontSizeLG,
                    fontweight='bold',
                    color=ant_design_theme.colors.colorText)
        ax.set_xticks(x)
        ax.set_xticklabels(df[x_key], rotation=45, ha='right',
                          fontsize=ant_design_theme.typography.fontSizeSM,
                          color=ant_design_theme.colors.colorTextSecondary)
        ax.legend(loc='upper left', fontsize=ant_design_theme.typography.fontSizeSM,
                 frameon=True, fancybox=True, shadow=False,
                 framealpha=0.9, facecolor=ant_design_theme.colors.colorBgContainer,
                 edgecolor=ant_design_theme.colors.colorBorder)
        ax.grid(axis='y', color=ant_design_theme.colors.colorBorderSecondary,
               linestyle='-', linewidth=1, alpha=0.5)
        
        # 坐标轴样式
        ax.spines['top'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['right'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['bottom'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['left'].set_color(ant_design_theme.colors.colorBorder)
        ax.tick_params(colors=ant_design_theme.colors.colorTextSecondary)
        
        plt.tight_layout()
        
        filename = f"grouped_bar_chart_{title.replace(' ', '_')}.png"
        return self._save_chart(fig, filename)
    
    def generate_chart_from_insight(
        self,
        insight_details: Dict[str, Any],
        project_id: str = "deck"
    ) -> Dict[str, Any]:
        """
        从数据洞察生成图表
        
        Args:
            insight_details: 数据洞察字典，包含：
                - insightId 或 insight_id: 洞察ID
                - type: 图表类型（bar_chart, line_chart, pie_chart, grouped_bar_chart）
                - title: 图表标题
                - data: 数据列表
                - x_key: X轴数据键名（可选，自动推断）
                - y_key: Y轴数据键名（可选，自动推断）
            project_id: 项目ID，用于组织输出目录
            
        Returns:
            包含 'chart_image_path' 和 'insight_id' 的字典，失败时包含 'error'
        """
        try:
            insight_id = insight_details.get("insightId") or insight_details.get("insight_id", "unknown")
            chart_type = insight_details.get("type", "bar_chart")
            title = insight_details.get("title", "Chart")
            data = insight_details.get("data", [])
            
            if not data:
                raise ValueError("Data is empty")
            
            # 自动推断键名（如果未提供）
            if isinstance(data[0], dict):
                keys = list(data[0].keys())
                x_key = insight_details.get("x_key", keys[0])
                y_key = insight_details.get("y_key", keys[1] if len(keys) > 1 else keys[0])
                y_keys = insight_details.get("y_keys", None)
            else:
                raise ValueError("Data must be a list of dictionaries")
            
            # 根据类型生成图表
            if chart_type == "bar_chart":
                chart_path = self.generate_bar_chart(data, x_key, y_key, title)
            elif chart_type == "line_chart":
                chart_path = self.generate_line_chart(data, x_key, y_key, title)
            elif chart_type == "pie_chart":
                chart_path = self.generate_pie_chart(data, x_key, y_key, title)
            elif chart_type == "grouped_bar_chart":
                if not y_keys:
                    # 如果没有指定y_keys，尝试从数据中推断
                    df = pd.DataFrame(data)
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    if x_key in numeric_cols:
                        numeric_cols.remove(x_key)
                    y_keys = numeric_cols[:3]  # 最多3个系列
                chart_path = self.generate_grouped_bar_chart(data, x_key, y_keys, title)
            else:
                # 默认使用柱状图
                logger.warning(f"Unknown chart type '{chart_type}', using bar_chart")
                chart_path = self.generate_bar_chart(data, x_key, y_key, title)
            
            return {
                "chart_image_path": chart_path,
                "insight_id": insight_id
            }
            
        except Exception as e:
            logger.error(f"--- [ChartGenerator]: Failed to generate chart: {e}", exc_info=True)
            return {
                "error": str(e),
                "insight_id": insight_details.get("insightId") or insight_details.get("insight_id", "unknown")
            }
    
    async def generate_charts_from_insights(
        self,
        insights: List[Dict[str, Any]],
        project_id: str = "deck"
    ) -> Dict[str, str]:
        """
        批量生成图表
        
        Args:
            insights: 数据洞察列表
            project_id: 项目ID
            
        Returns:
            图表路径映射字典，键是insight_id，值是图表路径
        """
        chart_paths = {}
        
        for insight in insights:
            insight_id = insight.get("insightId") or insight.get("insight_id", "unknown")
            logger.info(f"--- [ChartGenerator]: Generating chart for insight: {insight_id}")
            
            result = self.generate_chart_from_insight(insight, project_id)
            
            if "error" in result:
                logger.error(f"--- [ChartGenerator]: Failed to generate chart for {insight_id}: {result['error']}")
            else:
                chart_paths[insight_id] = result["chart_image_path"]
                logger.success(f"--- [ChartGenerator]: Chart generated: {result['chart_image_path']}")
        
        return chart_paths

