"""
浏览器到PPT复刻器
将浏览器渲染的Ant Design/AntV组件一比一复刻到PPT
"""

from .browser_renderer import BrowserRenderer
from .element_analyzer import ElementAnalyzer
from .coordinate_mapper import CoordinateMapper
from .container_extractor import ContainerExtractor
from .text_extractor import TextExtractor
from .ppt_replicator import PPTReplicator
from .replicator import BrowserToPPTReplicator

__all__ = [
    'BrowserRenderer',
    'ElementAnalyzer',
    'CoordinateMapper',
    'ContainerExtractor',
    'TextExtractor',
    'PPTReplicator',
    'BrowserToPPTReplicator',
]

