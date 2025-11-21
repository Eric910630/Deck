"""
图表生成集成模块（独立版本）
使用独立的ChartGenerator替代Vinci
"""

from pathlib import Path
from typing import Any, Optional

from loguru import logger

from chart_generator import ChartGenerator


class VinciIntegration:
    """
    图表生成集成类（独立版本）
    使用ChartGenerator生成图表，不依赖BeeWise项目
    """

    def __init__(self, chart_generator: Optional[ChartGenerator] = None, output_dir: Optional[Path] = None):
        """
        初始化图表生成集成
        
        Args:
            chart_generator: ChartGenerator实例，如果为None则创建新实例
            output_dir: 图表输出目录
        """
        if chart_generator is None:
            self._chart_generator = ChartGenerator(output_dir=output_dir)
        else:
            self._chart_generator = chart_generator
        
        logger.info("--- [VinciIntegration]: Initialized with ChartGenerator (standalone)")

    async def generate_chart_from_insight(
        self,
        insight_details: dict[str, Any],
        project_id: str = "deck"
    ) -> dict[str, Any]:
        """
        从数据洞察生成图表
        
        Args:
            insight_details: 数据洞察字典，包含：
                - insightId 或 insight_id: 洞察ID
                - type: 图表类型（如 'bar_chart', 'pie_chart', 'line_chart', 'grouped_bar_chart'）
                - title: 图表标题
                - data: 数据列表
            project_id: 项目ID，用于组织输出目录
            
        Returns:
            包含 'chart_image_path' 和 'insight_id' 的字典，失败时包含 'error'
        """
        return self._chart_generator.generate_chart_from_insight(insight_details, project_id)

    async def generate_charts_from_insights(
        self,
        insights: list[dict[str, Any]],
        project_id: str = "deck"
    ) -> dict[str, str]:
        """
        批量生成图表
        
        Args:
            insights: 数据洞察列表
            project_id: 项目ID
            
        Returns:
            图表路径映射字典，键是insight_id，值是图表路径
        """
        return await self._chart_generator.generate_charts_from_insights(insights, project_id)


def create_vinci_integration(
    chart_generator: Optional[ChartGenerator] = None,
    output_dir: Optional[Path] = None
) -> Optional[VinciIntegration]:
    """
    创建图表生成集成实例
    
    Args:
        chart_generator: ChartGenerator实例
        output_dir: 图表输出目录
        
    Returns:
        VinciIntegration实例
    """
    try:
        return VinciIntegration(chart_generator=chart_generator, output_dir=output_dir)
    except Exception as e:
        logger.error(f"--- [VinciIntegration] Failed to create integration: {e}", exc_info=True)
        return None
