"""
Fixer - PPT生成工具
独立的PPT组装工具，可以根据指定的架构内容（VML计划）生成PPT文件
支持可选的Vinci图表生成集成
"""

from .ppt_generator import PPTGenerator

try:
    from .vinci_integration import VinciIntegration, create_vinci_integration
    __all__ = ["PPTGenerator", "VinciIntegration", "create_vinci_integration"]
except ImportError:
    __all__ = ["PPTGenerator"]
