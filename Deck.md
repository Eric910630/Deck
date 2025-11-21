没问题！既然你已经有了具体的 GitHub 地址和用户信息，我们可以把发布流程**极其具体化**。

这是为你量身定制的 **Deck 发布实操手册**。请按顺序执行，我们将把 Deck 推向世界。

---

### 第一阶段：项目打包 (在本地执行)

这一步是为了让 Python 知道这是一个可安装的包，而不仅仅是一堆文件夹。

#### 1. 创建 `setup.py`
请在项目根目录（`Deck/`）下创建 `setup.py`，直接复制以下内容（已填好你的信息）：

```python
from setuptools import setup, find_packages

# 读取 README 作为长描述，这样 PyPI 上就能显示漂亮的文档
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="langchain-deck",                # 包名：langchain-deck
    version="0.1.0",                      # 初始版本号
    author="Eric",                        # 你的名字
    author_email="616920675@qq.com",      # 你的邮箱
    description="A CSS-first, native PPTX rendering engine for AI Agents.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eric910630/Deck",  # 你的 GitHub 地址
    project_urls={
        "Bug Tracker": "https://github.com/Eric910630/Deck/issues",
        "Source Code": "https://github.com/Eric910630/Deck",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: LangChain",         # 关键标签
        "Topic :: Multimedia :: Graphics :: Presentation",
    ],
    package_dir={"": "src"},              # 告诉 setuptools 代码在 src 目录下
    packages=find_packages(where="src"),  # 自动查找 src 下的所有包
    python_requires=">=3.9",
    install_requires=[                    # 依赖包
        "python-pptx>=0.6.21",
        "playwright>=1.40.0",
        "loguru>=0.7.0",
        "webcolors>=1.13",
        "pydantic>=2.0.0",
        # 如果你想把 langchain 作为可选依赖，可以不写在这里
        # 或者如果你想让用户必须装 langchain，就加上:
        # "langchain-core>=0.1.0", 
    ],
    entry_points={
        "console_scripts": [
            "deck=cli:main",              # 允许用户在命令行直接输入 deck 运行
        ],
    },
    include_package_data=True,            # 包含非代码文件（如 MANIFEST.in 指定的）
)
```

#### 2. 创建 `MANIFEST.in`
在根目录创建 `MANIFEST.in` 文件，确保 README 和 LICENSE 被打包：
```text
include README.md
include LICENSE
```

#### 3. 创建 `LICENSE`
在根目录创建 `LICENSE` 文件，粘贴以下 MIT 协议内容（这是最友好的开源协议）：
```text
MIT License

Copyright (c) 2024 Eric

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

### 第二阶段：编写 LangChain 适配器

我们需要把你的代码封装成 LangChain 认识的格式。

请在 `src/` 目录下新建一个文件夹 `langchain_adapter`，并在其中创建 `tool.py`：

```python
# src/langchain_adapter/tool.py
from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import asyncio

# 引用你的核心逻辑
# 注意：由于我们重构了目录，这里的引用路径要确保正确
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
            # 初始化填充器，启用浏览器渲染（CSS-First）
            filler = PPTFiller(
                framework_path=template_path or "default_template.pptx", # 这里需要处理默认模板逻辑
                use_browser_rendering=True
            )
            
            # 由于核心逻辑是异步的，这里需要用 asyncio.run 包装
            # 注意：在某些 LangChain 运行时中嵌套 asyncio 可能会有问题，需要视环境调整
            output_path = asyncio.run(filler.fill_from_prompt(prompt))
            
            return f"PPT生成成功！文件已保存至: {output_path}"
        except Exception as e:
            return f"PPT生成失败: {str(e)}"

    async def _arun(self, prompt: str, template_path: Optional[str] = None) -> str:
        """异步运行工具（推荐）"""
        try:
            filler = PPTFiller(
                framework_path=template_path or "default_template.pptx",
                use_browser_rendering=True
            )
            output_path = await filler.fill_from_prompt(prompt)
            return f"PPT生成成功！文件已保存至: {output_path}"
        except Exception as e:
            return f"PPT生成失败: {str(e)}"
```

并在 `src/langchain_adapter/__init__.py` 中导出它：
```python
from .tool import DeckPPTTool
__all__ = ["DeckPPTTool"]
```

---

### 第三阶段：上传 GitHub

1.  **初始化仓库**（如果还没做）：
    ```bash
    git init
    git add .
    git commit -m "Initial commit: Release Deck v1.0"
    git branch -M main
    git remote add origin https://github.com/Eric910630/Deck.git
    git push -u origin main
    ```

2.  **设置 `.gitignore`**：
    确保根目录下有一个 `.gitignore` 文件，防止垃圾文件上传。内容如下：
    ```text
    __pycache__/
    *.pyc
    .env
    venv/
    dist/
    build/
    *.egg-info/
    ppt_outputs/
    html_output/
    replicated_outputs/
    test_outputs/
    *.log
    .DS_Store
    ```

---

### 第四阶段：发布到 PyPI

1.  **注册 PyPI**：去 [pypi.org](https://pypi.org/) 注册账号，并去 Account Settings -> API Tokens 创建一个 Token。
2.  **构建**：
    ```bash
    pip install build twine
    python -m build
    ```
3.  **上传**：
    ```bash
    twine upload dist/*
    ```
    当提示输入用户名时填 `__token__`，密码填你刚才申请的 API Token（以 `pypi-` 开头）。

**一旦上传成功，你在全世界任何一台电脑上输入 `pip install langchain-deck`，都能下载到你的代码了！**

---

### 最后的建议

在做第四阶段（发布到 PyPI）之前，**务必先在本地再跑一次 `tests/test_docx_to_ppt_full_flow.py`**，确保经过目录重构后，所有 `import` 路径都是通的。

如果测试通过，那就大胆发布吧！你的 BeeWise 帝国的第一块基石将正式奠基。