# Web图表生成器使用指南

## 概述

项目现在支持使用**无头浏览器（Playwright）+ AntV G2Plot**来生成图表，这样可以：

1. ✅ 使用真实的AntV/Ant Design组件渲染
2. ✅ 确保样式完全符合web设计规范
3. ✅ 获得更专业、更美观的图表效果
4. ✅ 自动fallback到matplotlib（如果Playwright不可用）

## 架构

```
ChartGenerator (统一接口)
    ├── WebChartGenerator (优先)
    │   ├── Playwright (无头浏览器)
    │   └── AntV G2Plot (真实web组件)
    └── Matplotlib (fallback)
```

## 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装Playwright浏览器

```bash
playwright install chromium
```

或者安装所有浏览器：

```bash
playwright install
```

## 使用方式

### 自动模式（推荐）

`ChartGenerator`会自动尝试使用web渲染，如果失败则fallback到matplotlib：

```python
from chart_generator import ChartGenerator

generator = ChartGenerator(use_web=True)  # 默认启用web渲染

# 自动使用WebChartGenerator（如果可用）
chart_path = generator.generate_bar_chart(
    data=[{'月份': '1月', '销售额': 1000}, {'月份': '2月', '销售额': 1500}],
    x_key='月份',
    y_key='销售额',
    title='销售数据'
)
```

### 仅使用Web渲染

```python
from web_chart_generator import WebChartGenerator

generator = WebChartGenerator()

# 同步方法
chart_path = generator.generate_bar_chart(
    data=[...],
    x_key='x',
    y_key='y',
    title='Chart'
)

# 异步方法（更高效）
import asyncio
chart_path = await generator.generate_bar_chart_async(
    data=[...],
    x_key='x',
    y_key='y',
    title='Chart'
)
```

### 仅使用Matplotlib（fallback）

```python
from chart_generator import ChartGenerator

generator = ChartGenerator(use_web=False)  # 禁用web渲染

# 直接使用matplotlib
chart_path = generator.generate_bar_chart(...)
```

## 支持的图表类型

### Web渲染（AntV G2Plot）

- ✅ **柱状图** (`bar_chart`) - 使用 `G2Plot.Bar`
- ✅ **折线图** (`line_chart`) - 使用 `G2Plot.Line`
- ✅ **饼图** (`pie_chart`) - 使用 `G2Plot.Pie`
- ✅ **分组柱状图** - 使用 `G2Plot.Column`

### Matplotlib（fallback）

- ✅ 所有上述图表类型
- ✅ 分组柱状图（`grouped_bar_chart`）

## 设计规范

Web渲染的图表自动应用：

- ✅ **Ant Design颜色系统** - 主色、文本色、背景色
- ✅ **Ant Design字体系统** - 系统字体栈
- ✅ **Ant Design间距系统** - 基于8px
- ✅ **AntV配色方案** - category10分类色
- ✅ **Ant Design圆角** - 6px基础圆角

## 性能对比

| 特性 | Web渲染 (AntV) | Matplotlib |
|------|---------------|------------|
| 样式准确性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 渲染速度 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 依赖复杂度 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 视觉效果 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 故障排除

### Playwright未安装

```bash
pip install playwright
playwright install chromium
```

### 浏览器下载失败

```bash
# 使用国内镜像（如果可用）
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright
playwright install chromium
```

### Web渲染失败

系统会自动fallback到matplotlib，无需手动处理。如果希望强制使用matplotlib：

```python
generator = ChartGenerator(use_web=False)
```

## 示例

### 完整示例

```python
from chart_generator import ChartGenerator

# 创建生成器（自动使用web渲染）
generator = ChartGenerator()

# 生成柱状图
data = [
    {'月份': '1月', '销售额': 1000},
    {'月份': '2月', '销售额': 1500},
    {'月份': '3月', '销售额': 1200}
]

chart_path = generator.generate_bar_chart(
    data=data,
    x_key='月份',
    y_key='销售额',
    title='月度销售数据',
    width=10,  # 英寸
    height=6   # 英寸
)

print(f"图表已保存: {chart_path}")
```

## 技术细节

### HTML模板生成

`WebChartGenerator`会生成包含以下内容的HTML：

1. **AntV G2Plot CDN** - 从unpkg加载最新版本
2. **Ant Design样式** - 应用颜色、字体、间距
3. **图表配置** - 根据数据类型自动配置
4. **响应式布局** - 适配不同尺寸

### 渲染流程

1. 生成HTML模板
2. 启动Playwright无头浏览器
3. 加载HTML内容
4. 等待G2Plot渲染完成（2秒）
5. 截图保存为PNG
6. 关闭浏览器

### 数据格式

数据必须是字典列表：

```python
[
    {'x': 'A', 'y': 10},
    {'x': 'B', 'y': 20}
]
```

## 注意事项

1. **首次运行**：需要安装Playwright浏览器（`playwright install chromium`）
2. **网络要求**：需要访问CDN加载AntV G2Plot（unpkg.com）
3. **渲染时间**：Web渲染需要2-3秒（等待图表完全渲染）
4. **内存使用**：无头浏览器会占用一定内存
5. **离线使用**：如果无法访问CDN，会自动fallback到matplotlib

## 未来改进

- [ ] 支持本地AntV G2Plot文件（离线使用）
- [ ] 支持更多图表类型（面积图、雷达图等）
- [ ] 支持自定义主题
- [ ] 支持动画导出（GIF/视频）
- [ ] 缓存机制（避免重复渲染）

