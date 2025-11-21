# 目录整理说明

## 整理时间
2025-11-21

## 目录结构

### 根目录
保留核心代码文件和配置文件：
- `*.py` - 核心Python模块
- `README.md` - 项目说明
- `requirements.txt` - 依赖配置
- `Demo文档.docx` - 示例文档

### 子目录

#### `docs/` - 文档目录
存放所有Markdown文档文件（除README.md外）：
- 设计文档
- 分析报告
- 实现总结
- 测试指南
- 问题修复记录

#### `logs/` - 日志目录
存放所有日志文件（.log）：
- 测试日志
- 运行日志
- 调试日志

#### `outputs/ppt/` - PPT输出目录
存放所有生成的PPT文件（.pptx）：
- 测试输出
- 演示文件
- 框架模板

#### `tests/` - 测试目录
存放所有测试脚本（test_*.py）：
- 单元测试
- 集成测试
- 流程测试

#### `debug/` - 调试目录
存放调试相关文件：
- `debug_*.py` - 调试脚本
- `*.html` - HTML调试文件
- `*.png` - 截图文件

#### `config/` - 配置目录
存放配置文件（.json）：
- 内容策略配置
- 分析结果JSON
- 其他配置文件

#### `examples/` - 示例目录
存放示例文件：
- `demo_*.py` - 演示脚本
- `example_*.json` - 示例JSON
- `*.txt` - 示例文本文件

## 保留在根目录的文件

### Python模块
- `ppt_filler.py` - PPT填充器（核心）
- `ppt_parser.py` - PPT解析器
- `html_generator.py` - HTML生成器
- `human_centered_analyzer.py` - 人类中心化分析器
- `content_polisher.py` - 内容润色器
- `layout_planner.py` - 布局规划器
- `color_configurator.py` - 颜色配置器
- `chart_generator.py` - 图表生成器
- `chart_integrator.py` - 图表整合器
- `llm_service.py` - LLM服务
- `cli.py` - 命令行接口
- 其他核心模块...

### 配置文件
- `requirements.txt` - Python依赖
- `README.md` - 项目说明

### 数据文件
- `Demo文档.docx` - 示例文档

## 其他目录

### 代码目录
- `browser_to_ppt_replicator/` - 浏览器到PPT复刻器模块
- `charts/` - 图表相关文件
- `html_debug/` - HTML调试输出（运行时生成）
- `replicated_outputs/` - 复刻输出（运行时生成）
- `test_outputs/` - 测试输出（运行时生成）

## 整理规则

1. **文档文件**：所有.md文件（除README.md）移动到 `docs/`
2. **日志文件**：所有.log文件移动到 `logs/`
3. **PPT文件**：所有.pptx文件移动到 `outputs/ppt/`
4. **测试文件**：所有test_*.py文件移动到 `tests/`
5. **调试文件**：所有debug_*文件、.html、.png文件移动到 `debug/`
6. **配置文件**：所有.json文件移动到 `config/`
7. **示例文件**：所有demo_*.py、example_*.json、.txt文件移动到 `examples/`

## 注意事项

1. 运行时生成的目录（如 `html_debug/`, `replicated_outputs/`）保留在根目录
2. 核心代码模块保留在根目录，便于导入
3. README.md保留在根目录，作为项目入口文档
4. requirements.txt保留在根目录，便于安装依赖

## 后续维护

- 新生成的日志文件应保存到 `logs/` 目录
- 新生成的PPT文件应保存到 `outputs/ppt/` 目录
- 新的文档应保存到 `docs/` 目录
- 新的测试脚本应保存到 `tests/` 目录

