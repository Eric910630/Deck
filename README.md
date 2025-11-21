# Deck - PPT生成工具

## 项目简介

基于LLM的智能PPT生成工具，支持从Word文档生成专业的PowerPoint演示文稿。

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基本使用

```bash
python cli.py --framework framework_template.pptx --fill-prompt "你的需求描述"
```

## 目录结构

```
Deck/
├── README.md                    # 项目说明（本文件）
├── requirements.txt              # Python依赖
├── Demo文档.docx                 # 示例文档
│
├── docs/                        # 📚 文档目录
│   ├── DIRECTORY_ORGANIZATION.md # 目录整理说明
│   ├── DESIGN_SYSTEM.md         # 设计系统文档
│   ├── TEST_GUIDE.md            # 测试指南
│   └── ...                      # 其他文档
│
├── logs/                        # 📝 日志目录
│   └── *.log                    # 所有日志文件
│
├── outputs/                     # 📊 输出目录
│   └── ppt/                     # PPT文件
│
├── tests/                       # 🧪 测试目录
│   └── test_*.py               # 测试脚本
│
├── debug/                       # 🐛 调试目录
│   ├── debug_*.py              # 调试脚本
│   ├── *.html                  # HTML调试文件
│   └── *.png                   # 截图文件
│
├── config/                      # ⚙️ 配置目录
│   └── *.json                  # 配置文件
│
├── examples/                    # 📖 示例目录
│   ├── demo_*.py               # 演示脚本
│   └── example_*.json          # 示例JSON
│
└── [核心代码模块]                # 核心Python模块
    ├── ppt_filler.py           # PPT填充器
    ├── html_generator.py       # HTML生成器
    ├── human_centered_analyzer.py # 人类中心化分析器
    └── ...
```

## 核心功能

### 1. 人类中心化分析
- 6层深度分析
- 智能识别文档结构和内容

### 2. 内容生成
- 内容润色（ContentPolisher）
- 展示策划（PresentationPlanner）
- 布局规划（LayoutPlanner）
- 颜色配置（ColorConfigurator）

### 3. HTML生成
- 基于Ant Design规范
- 24栅格系统布局
- 支持颜色配置

### 4. PPT转换
- 浏览器渲染（Playwright）
- 元素分析和提取
- 坐标映射和PPT复刻

## 使用模式

### HTML生成模式（推荐用于开发调试）

跳过PPT转换，仅生成HTML文件：

```python
output_path = await filler.fill_from_prompt(
    prompt=user_prompt,
    output_path="output.pptx",
    use_enhanced_analysis=True,
    skip_ppt_conversion=True  # 跳过PPT转换
)
```

HTML文件将保存在 `html_output/` 目录中。

### 完整PPT生成模式

生成完整的PPT文件：

```python
output_path = await filler.fill_from_prompt(
    prompt=user_prompt,
    output_path="output.pptx",
    use_enhanced_analysis=True,
    skip_ppt_conversion=False  # 默认值
)
```

## 测试

运行完整流程测试：

```bash
python tests/test_docx_to_ppt_full_flow.py
```

## 文档

详细文档请查看 `docs/` 目录：
- `docs/DIRECTORY_ORGANIZATION.md` - 目录结构说明
- `docs/DESIGN_SYSTEM.md` - 设计系统文档
- `docs/TEST_GUIDE.md` - 测试指南
- 更多文档...

## 开发

### 代码结构

- **核心模块**：保留在根目录，便于导入
- **工具脚本**：部分保留在根目录（如 `create_framework_ppt.py`）
- **测试脚本**：位于 `tests/` 目录
- **调试脚本**：位于 `debug/` 目录

### 目录整理规则

详见 `docs/DIRECTORY_ORGANIZATION.md`

## 许可证

[待添加]

## 贡献

[待添加]
