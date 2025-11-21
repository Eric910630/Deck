"""
AntV 图表设计规范集成
提供AntV/G2/G2Plot的图表配色和样式规范
"""

from typing import List, Dict, Any
from ant_design_theme import AntDesignTheme


class AntVChartTheme:
    """AntV 图表主题配置"""
    
    def __init__(self):
        self.ant_design = AntDesignTheme()
    
    def get_default_colors(self) -> List[str]:
        """获取AntV默认分类色（基于Ant Design）"""
        return self.ant_design.colors.category10
    
    def get_chart_style_config(self) -> Dict[str, Any]:
        """获取AntV图表样式配置"""
        return {
            # 基础样式
            "fontFamily": self.ant_design.typography.fontFamily,
            "fontSize": self.ant_design.typography.fontSize,
            
            # 颜色配置
            "defaultColor": self.ant_design.colors.colorPrimary,
            "category10": self.ant_design.colors.category10,
            
            # 背景色
            "backgroundColor": self.ant_design.colors.colorBgBase,
            
            # 网格线
            "gridLineStyle": {
                "stroke": self.ant_design.colors.colorBorderSecondary,
                "lineWidth": 1,
            },
            
            # 坐标轴
            "axisLabelStyle": {
                "fill": self.ant_design.colors.colorTextSecondary,
                "fontSize": self.ant_design.typography.fontSizeSM,
            },
            
            # 图例
            "legendStyle": {
                "fill": self.ant_design.colors.colorText,
                "fontSize": self.ant_design.typography.fontSizeSM,
            },
        }
    
    def get_bar_chart_colors(self, count: int = 1) -> List[str]:
        """获取柱状图颜色（使用Ant Design主色系）"""
        colors = self.ant_design.get_color_palette(count)
        return colors
    
    def get_pie_chart_colors(self, count: int = 1) -> List[str]:
        """获取饼图颜色"""
        return self.ant_design.get_color_palette(count)
    
    def get_line_chart_color(self) -> str:
        """获取折线图主色"""
        return self.ant_design.colors.colorPrimary


# 全局AntV主题实例
antv_chart_theme = AntVChartTheme()

