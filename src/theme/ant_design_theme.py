"""
Ant Design 设计规范集成
提供Ant Design的颜色、间距、字体等设计Token
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class AntDesignColors:
    """Ant Design 颜色系统"""
    # 主色调
    colorPrimary: str = "#1890ff"  # 蓝色
    colorSuccess: str = "#52c41a"  # 绿色
    colorWarning: str = "#faad14"  # 橙色
    colorError: str = "#f5222d"    # 红色
    colorInfo: str = "#1890ff"     # 信息色
    
    # 中性色（matplotlib兼容格式）
    colorText: str = "#262626"  # 主文本 rgba(0,0,0,0.85) ≈ #262626
    colorTextSecondary: str = "#595959"  # 次文本 rgba(0,0,0,0.65) ≈ #595959
    colorTextTertiary: str = "#8c8c8c"  # 辅助文本 rgba(0,0,0,0.45) ≈ #8c8c8c
    colorTextDisabled: str = "#bfbfbf"  # 禁用文本 rgba(0,0,0,0.25) ≈ #bfbfbf
    
    # 背景色
    colorBgBase: str = "#ffffff"  # 基础背景
    colorBgContainer: str = "#ffffff"  # 容器背景
    colorBgElevated: str = "#ffffff"  # 悬浮背景
    colorBgLayout: str = "#f0f2f5"  # 布局背景
    
    # 边框色
    colorBorder: str = "#d9d9d9"  # 基础边框
    colorBorderSecondary: str = "#f0f0f0"  # 次要边框
    
    # 分类色（用于图表）
    category10: List[str] = None
    
    def __post_init__(self):
        if self.category10 is None:
            # Ant Design 默认分类色
            self.category10 = [
                "#1890ff",  # 蓝色
                "#52c41a",  # 绿色
                "#faad14",  # 橙色
                "#f5222d",  # 红色
                "#722ed1",  # 紫色
                "#13c2c2",  # 青色
                "#eb2f96",  # 粉色
                "#fa8c16",  # 橙红
                "#a0d911",  # 黄绿
                "#2f54eb",  # 深蓝
            ]


@dataclass
class AntDesignSpacing:
    """Ant Design 间距系统（基于8px基础单位）"""
    # 基础间距
    paddingXXS: int = 4   # 4px
    paddingXS: int = 8    # 8px
    paddingSM: int = 12   # 12px
    padding: int = 16     # 16px
    paddingMD: int = 20   # 20px
    paddingLG: int = 24   # 24px
    paddingXL: int = 32   # 32px
    paddingXXL: int = 48  # 48px
    
    # 边距
    marginXXS: int = 4
    marginXS: int = 8
    marginSM: int = 12
    margin: int = 16
    marginMD: int = 20
    marginLG: int = 24
    marginXL: int = 32
    marginXXL: int = 48


@dataclass
class AntDesignTypography:
    """Ant Design 字体系统"""
    # 字体族
    fontFamily: str = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    fontFamilyCode: str = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace"
    
    # 字号（针对PPT显示优化，放大2倍以确保在PPT中清晰可见）
    fontSizeSM: int = 24   # 24px (原12px × 2)
    fontSize: int = 28     # 28px (原14px × 2)
    fontSizeLG: int = 32   # 32px (原16px × 2)
    fontSizeXL: int = 40   # 40px (原20px × 2)
    fontSizeXXL: int = 48  # 48px (原24px × 2)
    fontSizeHeading1: int = 76  # 76px (原38px × 2)
    fontSizeHeading2: int = 60  # 60px (原30px × 2)
    fontSizeHeading3: int = 48  # 48px (原24px × 2)
    fontSizeHeading4: int = 40  # 40px (原20px × 2)
    fontSizeHeading5: int = 32  # 32px (原16px × 2)
    
    # 字重
    fontWeightStrong: int = 600
    fontWeight: int = 400
    
    # 行高
    lineHeight: float = 1.5715
    lineHeightLG: float = 1.5
    lineHeightSM: float = 1.66


@dataclass
class AntDesignBorderRadius:
    """Ant Design 圆角系统"""
    borderRadius: int = 6      # 基础圆角 6px
    borderRadiusSM: int = 2    # 小圆角 2px
    borderRadiusLG: int = 8    # 大圆角 8px
    borderRadiusOuter: int = 4 # 外圆角 4px


class AntDesignTheme:
    """Ant Design 完整主题"""
    
    def __init__(self):
        self.colors = AntDesignColors()
        self.spacing = AntDesignSpacing()
        self.typography = AntDesignTypography()
        self.borderRadius = AntDesignBorderRadius()
    
    def get_color_palette(self, count: int = 10) -> List[str]:
        """获取颜色调色板"""
        if count <= len(self.colors.category10):
            return self.colors.category10[:count]
        # 如果需要更多颜色，可以扩展
        return self.colors.category10 * ((count // len(self.colors.category10)) + 1)[:count]
    
    def get_spacing_cm(self, spacing_key: str) -> float:
        """将间距转换为厘米（用于PPT）"""
        spacing_map = {
            'xxs': self.spacing.paddingXXS,
            'xs': self.spacing.paddingXS,
            'sm': self.spacing.paddingSM,
            'md': self.spacing.padding,
            'lg': self.spacing.paddingLG,
            'xl': self.spacing.paddingXL,
            'xxl': self.spacing.paddingXXL,
        }
        px = spacing_map.get(spacing_key.lower(), self.spacing.padding)
        # 转换为厘米 (1px ≈ 0.0264cm at 96dpi)
        return px * 0.0264
    
    def get_font_size_pt(self, size_key: str) -> int:
        """获取字号（转换为pt）
        
        注意：PPT中直接使用pt，不需要从px转换
        Ant Design的px值可以直接作为pt使用（在PPT中）
        """
        size_map = {
            'sm': self.typography.fontSizeSM,
            'base': self.typography.fontSize,
            'lg': self.typography.fontSizeLG,
            'xl': self.typography.fontSizeXL,
            'xxl': self.typography.fontSizeXXL,
            'h1': self.typography.fontSizeHeading1,
            'h2': self.typography.fontSizeHeading2,
            'h3': self.typography.fontSizeHeading3,
            'h4': self.typography.fontSizeHeading4,
            'h5': self.typography.fontSizeHeading5,
        }
        px = size_map.get(size_key.lower(), self.typography.fontSize)
        # PPT中直接使用px值作为pt（在屏幕显示中，1px ≈ 0.75pt，但PPT中通常直接使用）
        # 为了保持Ant Design的视觉效果，我们直接使用px值
        return int(px)


# 全局主题实例
ant_design_theme = AntDesignTheme()

