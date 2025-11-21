<div align="center">

# 🃏 Deck

**The Missing Presentation Layer for AI Agents.**  
**AI Agent 的演示文稿渲染引擎**

[![PyPI version](https://badge.fury.io/py/langchain-deck.svg)](https://badge.fury.io/py/langchain-deck)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by BeeWise](https://img.shields.io/badge/Powered%20by-BeeWise-blue)](https://github.com/Eric910630/Deck)

[English](#-english) | [中文文档](#-中文文档)

</div>

---

## 🇬🇧 English

### 🚀 Why Deck?

Building PowerPoint automations with `python-pptx` is painful. You have to calculate coordinates, handle text wrapping manually, and struggle with limited styling options.

**Deck** changes the game. It treats **PowerPoint generation as a rendering problem**:

1.  **LLMs write HTML/CSS** (which they are great at).
2.  **Deck renders it** using a headless browser to calculate precise layouts (Flexbox, Grid, Shadows).
3.  **Deck compiles it** into **NATIVE** PowerPoint shapes.

**Result:** You get the beauty of Web Design with the editability of Native PPT. **No screenshots. No background images. 100% Editable Shapes.**

### ✨ Features

- **CSS-First Architecture**: Design your slides using Flexbox, Grid, and CSS variables.
- **Native Compilation**: Converts HTML elements into native PPTX Shapes, TextFrames, and Tables.
- **100% Editable**: Text remains text. Colors remain colors. Users can edit everything in PowerPoint.
- **High-Fidelity**: Supports rounded corners, complex shadows, and transparency.
- **Ant Design System**: Built-in support for professional UI aesthetics.
- **LangChain Ready**: Designed to be the standard Presentation Tool for AI Agents.

### 📦 Installation

```bash
pip install langchain-deck
playwright install chromium
```

### 💻 Usage

```python
from langchain_deck.core.ppt_filler import PPTFiller
import asyncio

async def generate():
    # Initialize the engine
    filler = PPTFiller(use_browser_rendering=True)
    
    # Generate from a natural language prompt
    output_path = await filler.fill_from_prompt(
        "Create a 3-slide pitch deck for an AI startup."
    )
    print(f"PPT generated at: {output_path}")

if __name__ == "__main__":
    asyncio.run(generate())
```

---

## 🇨🇳 中文文档

### 🚀 为什么选择 Deck?

用 `python-pptx` 写代码生成 PPT 是极其痛苦的。你需要手动计算坐标、处理文字换行，而且很难做出好看的样式。

**Deck** 改变了这一切。它将 **PPT 生成视为一个渲染问题**：

1.  **让 LLM 写 HTML/CSS**（这是 LLM 最擅长的）。
2.  **Deck 进行渲染**：使用无头浏览器计算精确布局（Flexbox, Grid, 阴影）。
3.  **Deck 进行编译**：将渲染结果"编译"为 **原生的** PowerPoint 形状。

**结果：** 你拥有了 Web 设计的精美度，同时保留了 PPT 的原生可编辑性。**没有截图，没有背景图，所有元素都是原生可编辑的形状。**

### ✨ 核心特性

- **CSS 优先架构**：使用 Flexbox、Grid 和 CSS 变量设计幻灯片。
- **原生编译**：将 HTML 元素转换为原生的 PPTX 形状、文本框和表格。
- **100% 可编辑**：文字还是文字，颜色还是颜色。用户可以在 PPT 中修改任何内容。
- **高保真**：支持圆角、复杂阴影和透明度。
- **Ant Design 系统**：内置专业级 UI 审美。
- **LangChain 集成**：专为 AI Agent 设计的演示文稿工具。

### 📦 安装

```bash
pip install langchain-deck
playwright install chromium
```

### 💻 使用方法

#### 1. 基础用法 (Python)

```python
from langchain_deck.core.ppt_filler import PPTFiller
import asyncio

async def generate():
    # 初始化引擎
    filler = PPTFiller(
        framework_path="template.pptx", # 可选：基础模板
        use_browser_rendering=True      # 启用 CSS-to-Native 引擎
    )
    
    # 通过自然语言生成
    output_path = await filler.fill_from_prompt(
        "帮我生成一份关于企业搜索的 AI 创业计划书，共3页。"
    )
    print(f"PPT 已生成: {output_path}")

if __name__ == "__main__":
    asyncio.run(generate())
```

#### 2. 命令行使用 (CLI)

```bash
# 通过提示词生成
deck --generate "一份关于下季度销售目标的汇报" --output-dir ./my-slides
```

---

## 🦜🔗 LangChain 集成 (LangChain Integration)

Deck 旨在成为 LangChain Agent 的标准 **演示文稿工具 (Presentation Tool)**。

```python
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain_deck.tool import DeckPPTTool

# 1. 初始化工具
ppt_tool = DeckPPTTool()

# 2. 初始化 Agent
llm = OpenAI(temperature=0)
tools = [ppt_tool]
agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True
)

# 3. 运行
agent.run("分析上传的 CSV 数据，并生成一张总结性的 PPT 幻灯片。")
```

---

## 🏗 架构原理

Deck 的工作流分为三步：

1.  **Planning (大脑)**: LLM 根据内容策略生成布局方案和 HTML/CSS 代码。
2.  **Rendering (眼睛)**: 无头浏览器 (Playwright) 渲染 HTML。`DOMAnalyzer` 提取计算后的样式（几何信息、颜色、阴影、排版）。
3.  **Composition (手)**: `NativeCompositor` 将 DOM 数据映射为 `python-pptx` API 调用，以像素级精度绘制原生形状。

---

## 🤝 商业支持

Deck 是 **BeeWise** 的开源核心引擎。

如果您需要企业级解决方案，包括：
- 🏢 **企业知识库集成**
- 📄 **长文档分析 (PDF/Docx 转 PPT)**
- 🎨 **定制品牌模板**
- 👥 **团队协作空间**

请联系我们要 **BeeWise 商业版**。

---

## 📄 License

MIT License. 欢迎在您的商业项目中使用。
