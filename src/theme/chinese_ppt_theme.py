"""
中国述职PPT主题
融合Ant Design设计原则与中国述职PPT风格
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ChinesePPTColors:
    """中国述职PPT颜色系统（融合Ant Design间距原则）"""
    # 主色调（中国述职PPT常用）
    colorPrimary: str = "#d32f2f"  # 红色（权威、正式）
    colorAccent: str = "#ffb300"   # 金色（喜庆、重要）
    colorSecondary: str = "#1976d2"  # 深蓝（辅助、专业）
    
    # 文本色（基于Ant Design原则，但调整为中式风格）
    colorText: str = "#212121"      # 主文本（深灰，正式）
    colorTextSecondary: str = "#616161"  # 次文本（中灰）
    colorTextTertiary: str = "#9e9e9e"  # 辅助文本（浅灰）
    
    # 背景色（保持Ant Design的简洁原则）
    colorBgBase: str = "#ffffff"    # 基础背景（白色）
    colorBgContainer: str = "#fafafa"  # 容器背景（浅灰）
    colorBgLayout: str = "#f5f5f5"  # 布局背景（浅灰）
    
    # 边框色（保持Ant Design的简洁原则）
    colorBorder: str = "#e0e0e0"    # 基础边框（浅灰）
    colorBorderSecondary: str = "#f5f5f5"  # 次要边框（更浅）
    
    # 强调色（中国述职PPT常用）
    colorHighlight: str = "#ffb300"  # 高亮色（金色）
    colorWarning: str = "#ff9800"    # 警告色（橙色）
    colorSuccess: str = "#4caf50"   # 成功色（绿色）


@dataclass
class ChinesePPTTypography:
    """中国述职PPT字体系统"""
    # 标题字体（黑体、微软雅黑）
    fontFamilyHeading: str = "'Microsoft YaHei', 'SimHei', '黑体', 'Arial', sans-serif"
    
    # 正文字体（宋体、微软雅黑）
    fontFamilyBody: str = "'SimSun', '宋体', 'Microsoft YaHei', 'Arial', sans-serif"
    
    # 强调字体（楷体）
    fontFamilyEmphasis: str = "'KaiTi', '楷体', 'SimSun', serif"
    
    # 字号（基于Ant Design，但针对PPT优化）
    fontSizeHeading1: int = 76   # 主标题（PPT中约38pt）
    fontSizeHeading2: int = 60   # 副标题（PPT中约30pt）
    fontSizeHeading3: int = 48   # 三级标题（PPT中约24pt）
    fontSizeHeading4: int = 40   # 四级标题（PPT中约20pt）
    fontSizeHeading5: int = 32   # 五级标题（PPT中约16pt）
    fontSizeBody: int = 28       # 正文（PPT中约14pt）
    fontSizeSmall: int = 24      # 小号（PPT中约12pt）
    
    # 字重
    fontWeightStrong: int = 700  # 加粗（标题）
    fontWeight: int = 400        # 常规（正文）
    
    # 行高（基于Ant Design原则）
    lineHeight: float = 1.6      # 正文行高
    lineHeightHeading: float = 1.4  # 标题行高


@dataclass
class ChinesePPTSpacing:
    """中国述职PPT间距系统（基于Ant Design 8px原则）"""
    # 基础间距（基于8px）
    spacingXXS: int = 4   # 4px
    spacingXS: int = 8    # 8px
    spacingSM: int = 12   # 12px
    spacing: int = 16     # 16px
    spacingMD: int = 20   # 20px
    spacingLG: int = 24   # 24px
    spacingXL: int = 32   # 32px
    spacingXXL: int = 48  # 48px
    
    # 区块间距（中国述职PPT常用）
    sectionSpacing: int = 32  # 区块间距（32px）
    blockSpacing: int = 24    # 内容块间距（24px）


@dataclass
class ChinesePPTBorderRadius:
    """中国述职PPT圆角系统（保持Ant Design原则）"""
    borderRadius: int = 4      # 基础圆角（4px，比Ant Design稍小，更正式）
    borderRadiusSM: int = 2    # 小圆角（2px）
    borderRadiusLG: int = 6     # 大圆角（6px）


class ChinesePPTTheme:
    """中国述职PPT完整主题（融合Ant Design原则）"""
    
    def __init__(self):
        self.colors = ChinesePPTColors()
        self.typography = ChinesePPTTypography()
        self.spacing = ChinesePPTSpacing()
        self.borderRadius = ChinesePPTBorderRadius()
    
    def get_layout_mode(self, content_type: str) -> str:
        """
        根据内容类型获取布局模式
        
        Args:
            content_type: 内容类型（'title', 'content', 'summary'等）
            
        Returns:
            布局模式（'symmetric', 'hierarchical', 'centered'等）
        """
        layout_modes = {
            'title': 'centered',      # 标题页：居中
            'content': 'symmetric',   # 内容页：对称
            'summary': 'hierarchical', # 总结页：层次
            'default': 'symmetric'    # 默认：对称
        }
        return layout_modes.get(content_type, 'symmetric')
    
    def get_color_scheme(self, scheme_type: str = 'default') -> Dict[str, str]:
        """
        获取配色方案
        
        Args:
            scheme_type: 方案类型（'default', 'formal', 'warm'等）
            
        Returns:
            配色方案字典
        """
        schemes = {
            'default': {
                'primary': self.colors.colorPrimary,  # 红色
                'accent': self.colors.colorAccent,    # 金色
                'text': self.colors.colorText,        # 深灰
                'bg': self.colors.colorBgBase         # 白色
            },
            'formal': {
                'primary': '#1976d2',  # 深蓝（正式）
                'accent': '#424242',   # 深灰
                'text': '#212121',
                'bg': '#ffffff'
            },
            'warm': {
                'primary': '#ff6f00',  # 暖橙
                'accent': '#ffb300',   # 金色
                'text': '#212121',
                'bg': '#fff8e1'        # 浅黄
            }
        }
        return schemes.get(scheme_type, schemes['default'])


# 全局主题实例
chinese_ppt_theme = ChinesePPTTheme()

