from typing import Optional, Type
from pathlib import Path
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import asyncio

from ..core.ppt_filler import PPTFiller


class DeckInput(BaseModel):
    """Deck 工具的输入参数"""
    prompt: str = Field(description="描述要生成的PPT内容，例如'帮我生成一份关于AI趋势的汇报PPT'。")
    template_path: Optional[str] = Field(default=None, description="可选：PPT模板文件的路径。")


class DeckPPTTool(BaseTool):
    name = "generate_native_pptx"
    description = (
        "一个能够生成原生、精美PowerPoint演示文稿的工具。"
        "它使用CSS-to-Native渲染引擎，支持阴影、圆角和复杂布局。"
        "当用户需要创建PPT、幻灯片或演示文稿时使用此工具。"
    )
    args_schema: Type[BaseModel] = DeckInput

    def _run(self, prompt: str, template_path: Optional[str] = None) -> str:
        """同步运行工具"""
        try:
            if template_path is None:
                default_template = Path(__file__).parent.parent.parent.parent / "framework_template.pptx"
                if not default_template.exists():
                    return f"PPT生成失败: 未找到默认模板文件 {default_template}"
                template_path = str(default_template)
            
            filler = PPTFiller(
                framework_path=template_path,
                use_browser_rendering=True
            )
            
            output_path = asyncio.run(filler.fill_from_prompt(prompt))
            
            return f"PPT生成成功！文件已保存至: {output_path}"
        except Exception as e:
            return f"PPT生成失败: {str(e)}"

    async def _arun(self, prompt: str, template_path: Optional[str] = None) -> str:
        """异步运行工具"""
        try:
            if template_path is None:
                default_template = Path(__file__).parent.parent.parent.parent / "framework_template.pptx"
                if not default_template.exists():
                    return f"PPT生成失败: 未找到默认模板文件 {default_template}"
                template_path = str(default_template)
            
            filler = PPTFiller(
                framework_path=template_path,
                use_browser_rendering=True
            )
            output_path = await filler.fill_from_prompt(prompt)
            return f"PPT生成成功！文件已保存至: {output_path}"
        except Exception as e:
            return f"PPT生成失败: {str(e)}"

