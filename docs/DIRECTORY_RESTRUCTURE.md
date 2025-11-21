# 项目目录重构说明

## 重构日期
2025-11-21

## 重构目标
将根目录下的文件进行模块化组织，提高代码可维护性和可读性。

## 新的目录结构

```
Deck/
├── cli.py                      # 命令行入口（保留在根目录）
├── config/                     # 配置文件（保留）
├── docs/                       # 文档（保留）
├── scripts/                    # 一次性脚本、调试脚本
│   ├── analyze_demo_docx.py
│   ├── create_framework_ppt.py
│   ├── verify_fixes.py
│   ├── generate_tree.py
│   ├── generate_snapshot.py
│   └── ...
├── src/                        # 核心源代码 [NEW]
│   ├── __init__.py
│   ├── core/                   # 核心业务逻辑
│   │   ├── ppt_generator.py
│   │   ├── ppt_filler.py
│   │   └── llm_service.py
│   ├── analysis/               # 解析与分析模块
│   │   ├── ppt_parser.py
│   │   ├── deep_parser.py
│   │   ├── semantic_analyzer.py
│   │   └── human_centered_analyzer.py
│   ├── planning/               # 策略与规划模块
│   │   ├── content_strategy_generator.py
│   │   ├── content_polisher.py
│   │   ├── presentation_planner.py
│   │   ├── layout_planner.py
│   │   └── presentation_schema.py
│   ├── rendering/              # 渲染模块 (Web & HTML)
│   │   ├── html_generator.py
│   │   ├── html_canvas_generator.py
│   │   ├── html_flow_layout_generator.py
│   │   └── browser_to_ppt_replicator/
│   ├── theme/                  # 设计规范与主题
│   │   ├── ant_design_theme.py
│   │   ├── chinese_ppt_theme.py
│   │   └── color_configurator.py
│   └── charts/                 # 图表模块
│       ├── chart_generator.py
│       ├── chart_integrator.py
│       ├── web_chart_generator.py
│       └── antv_chart_theme.py
└── tests/                      # 测试代码（保持现状）
```

## 文件移动映射

### Core 模块
- `ppt_generator.py` → `src/core/ppt_generator.py`
- `ppt_filler.py` → `src/core/ppt_filler.py`
- `llm_service.py` → `src/core/llm_service.py`

### Analysis 模块
- `ppt_parser.py` → `src/analysis/ppt_parser.py`
- `deep_parser.py` → `src/analysis/deep_parser.py`
- `enhanced_ppt_parser.py` → `src/analysis/enhanced_ppt_parser.py`
- `semantic_analyzer.py` → `src/analysis/semantic_analyzer.py`
- `human_centered_analyzer.py` → `src/analysis/human_centered_analyzer.py`
- `supporting_materials_analyzer.py` → `src/analysis/supporting_materials_analyzer.py`

### Planning 模块
- `content_strategy_generator.py` → `src/planning/content_strategy_generator.py`
- `content_polisher.py` → `src/planning/content_polisher.py`
- `presentation_planner.py` → `src/planning/presentation_planner.py`
- `layout_planner.py` → `src/planning/layout_planner.py`
- `presentation_schema.py` → `src/planning/presentation_schema.py`

### Rendering 模块
- `html_generator.py` → `src/rendering/html_generator.py`
- `html_canvas_generator.py` → `src/rendering/html_canvas_generator.py`
- `html_flow_layout_generator.py` → `src/rendering/html_flow_layout_generator.py`
- `browser_to_ppt_replicator/` → `src/rendering/browser_to_ppt_replicator/`

### Theme 模块
- `ant_design_theme.py` → `src/theme/ant_design_theme.py`
- `chinese_ppt_theme.py` → `src/theme/chinese_ppt_theme.py`
- `color_configurator.py` → `src/theme/color_configurator.py`

### Charts 模块
- `chart_generator.py` → `src/charts/chart_generator.py`
- `chart_integrator.py` → `src/charts/chart_integrator.py`
- `web_chart_generator.py` → `src/charts/web_chart_generator.py`
- `antv_chart_theme.py` → `src/charts/antv_chart_theme.py`

### Scripts 目录
- `analyze_demo_docx.py` → `scripts/analyze_demo_docx.py`
- `deep_analyze_demo_docx.py` → `scripts/deep_analyze_demo_docx.py`
- `create_framework_ppt.py` → `scripts/create_framework_ppt.py`
- `verify_fixes.py` → `scripts/verify_fixes.py`
- `quick_debug_html.py` → `scripts/quick_debug_html.py`
- `test_canvas_generator.py` → `scripts/test_canvas_generator.py`
- `vinci_integration.py` → `scripts/vinci_integration.py`
- `layout_generator.py` → `scripts/layout_generator.py`
- `generate_tree.py` → `scripts/generate_tree.py`
- `generate_snapshot.py` → `scripts/generate_snapshot.py`
- `generate_snapshot_optimized.py` → `scripts/generate_snapshot_optimized.py`

## 导入路径更新

### 相对导入示例

**之前：**
```python
from ppt_filler import PPTFiller
from html_generator import HTMLGenerator
from layout_planner import LayoutPlanner
```

**之后：**
```python
from src.core.ppt_filler import PPTFiller
from src.rendering.html_generator import HTMLGenerator
from src.planning.layout_planner import LayoutPlanner
```

### 模块内部相对导入

**在 `src/core/ppt_filler.py` 中：**
```python
from ..analysis.ppt_parser import PPTParser
from .llm_service import LLMService
from ..planning.layout_planner import LayoutPlanner
from ..rendering.html_generator import HTMLGenerator
```

**在 `src/planning/layout_planner.py` 中：**
```python
from ..core.llm_service import LLMService
```

**在 `src/charts/chart_integrator.py` 中：**
```python
from .chart_generator import ChartGenerator
from ..analysis.supporting_materials_analyzer import SupportingMaterialsAnalyzer
```

## 测试文件更新

测试文件需要更新导入路径：

**之前：**
```python
from html_generator import HTMLGenerator
from html_canvas_generator import HTMLCanvasGenerator
```

**之后：**
```python
from src.rendering.html_generator import HTMLGenerator
from src.rendering.html_canvas_generator import HTMLCanvasGenerator
```

## CLI 更新

`cli.py` 已更新导入路径：

```python
from src.core.ppt_generator import PPTGenerator
from src.core.ppt_filler import PPTFiller
from src.core.llm_service import create_llm_service
from scripts.vinci_integration import create_vinci_integration
from scripts.layout_generator import create_layout_generator
```

## 验证状态

✅ 核心模块导入测试通过
- `src.core.ppt_filler` 导入成功
- `src.rendering.html_generator` 导入成功

## 注意事项

1. **脚本执行**：如果脚本需要导入模块，需要确保 `sys.path` 包含项目根目录
2. **测试文件**：所有测试文件需要更新导入路径
3. **IDE 配置**：可能需要重新配置 IDE 的 Python 路径
4. **相对导入**：模块内部使用相对导入（`..` 和 `.`），外部使用绝对导入（`src.xxx`）

## 后续工作

- [ ] 更新所有测试文件的导入路径
- [ ] 更新 scripts/ 目录下脚本的导入路径
- [ ] 验证所有功能正常工作
- [ ] 更新 README.md 中的导入示例

