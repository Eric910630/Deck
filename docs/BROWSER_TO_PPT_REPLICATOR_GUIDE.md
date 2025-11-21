# 浏览器到PPT复刻器使用指南

## 🎯 功能概述

浏览器到PPT复刻器可以将浏览器渲染的Ant Design/AntV组件**一比一复刻**到PPT中：

1. **容器元素**（Card、div等）→ 截图保存为PNG，插入到PPT相同位置
2. **文本元素**（Typography等）→ 提取内容和样式，在PPT中精确复现
3. **24栅格系统** → 建立标准化坐标系，确保布局一致性

---

## 📦 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装Playwright浏览器

```bash
playwright install chromium
```

---

## 🚀 快速开始

### 基本使用

```python
import asyncio
from pathlib import Path
from browser_to_ppt_replicator import BrowserToPPTReplicator

async def main():
    # 创建复刻器
    replicator = BrowserToPPTReplicator()
    
    # HTML内容（包含Ant Design组件）
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                width: 1920px;
                height: 1080px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI';
                background: #f0f2f5;
                padding: 24px;
            }
            .card {
                background: #ffffff;
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
                padding: 24px;
                margin-bottom: 16px;
            }
            .title {
                font-size: 48px;
                font-weight: 600;
                color: #1890ff;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1 class="title">人工智能技术概述</h1>
        </div>
    </body>
    </html>
    """
    
    # 执行复刻
    output_path = await replicator.replicate(
        html_content,
        output_ppt_path=Path("output.pptx")
    )
    
    print(f"PPT已生成: {output_path}")

asyncio.run(main())
```

---

## 🏗️ 架构说明

### 模块结构

```
browser_to_ppt_replicator/
├── browser_renderer.py      # 浏览器渲染器（Playwright）
├── element_analyzer.py      # 元素分析器（识别容器和文本）
├── coordinate_mapper.py     # 坐标映射器（24栅格系统）
├── container_extractor.py   # 容器提取器（截图PNG）
├── text_extractor.py        # 文本提取器（内容和样式）
├── ppt_replicator.py        # PPT复刻器（插入图片和文本）
└── replicator.py            # 主入口（整合所有模块）
```

### 工作流程

```
1. 浏览器渲染HTML（1920x1080，16:9）
   ↓
2. 分析DOM结构
   ├── 识别容器元素（Card、div等）
   └── 识别文本元素（Typography等）
   ↓
3. 建立24栅格坐标系
   ├── 浏览器：1920px / 24 = 80px/格
   └── PPT：33.867cm / 24 ≈ 1.41cm/格
   ↓
4. 提取容器
   ├── 截图容器元素（PNG）
   └── 记录位置、尺寸（栅格坐标）
   ↓
5. 提取文本
   ├── 提取文本内容
   ├── 记录字体、大小、颜色
   └── 记录位置（栅格坐标）
   ↓
6. 复刻到PPT
   ├── 插入容器图片（相同位置）
   └── 插入文本（相同位置、样式）
```

---

## 📐 24栅格系统

### 坐标系映射

**浏览器端**：
- 尺寸：1920px × 1080px (16:9)
- 栅格：24列 × 13.5行
- 单元：80px × 80px

**PPT端**：
- 尺寸：33.867cm × 19.05cm (16:9)
- 栅格：24列 × 13.5行
- 单元：≈ 1.41cm × 1.41cm

### 坐标转换

```python
from browser_to_ppt_replicator import CoordinateMapper

mapper = CoordinateMapper()

# 浏览器坐标 → PPT坐标
ppt_x, ppt_y = mapper.browser_to_ppt(960, 540)  # 中心点
# 结果: (16.93cm, 9.53cm)

# 浏览器坐标 → 栅格坐标
grid_x, grid_y = mapper.browser_to_grid(960, 540)
# 结果: (12, 6)  # 第12列，第6行

# 栅格坐标 → PPT位置
position = mapper.grid_to_ppt(12, 6, span_x=2, span_y=2)
# 结果: {'left': 16.93cm, 'top': 9.53cm, 'width': 2.82cm, 'height': 2.82cm}
```

---

## 🎨 HTML模板要求

### 1. 画布尺寸

```html
<body style="width: 1920px; height: 1080px;">
    <!-- 内容 -->
</body>
```

### 2. 容器元素

容器元素需要有**可见的背景色或边框**才会被识别：

```html
<!-- ✅ 会被识别为容器 -->
<div class="card" style="background: #ffffff; border: 1px solid #d9d9d9;">
    内容
</div>

<!-- ❌ 不会被识别（无背景无边框） -->
<div>
    内容
</div>
```

### 3. 文本元素

文本元素会自动识别（h1-h6, p, span等）：

```html
<h1 class="title">标题</h1>
<p class="text">正文内容</p>
```

### 4. 使用CSS Grid（推荐）

```html
<style>
.container {
    display: grid;
    grid-template-columns: repeat(24, 1fr);
    grid-template-rows: repeat(13.5, 1fr);
    gap: 16px;
}
.card {
    grid-column: 1 / 13;  /* 占12列 */
    grid-row: 1 / 5;      /* 占4行 */
}
</style>
```

---

## 📊 输出结果

### 文件结构

```
replicated_outputs/
├── containers/              # 容器截图
│   ├── container_000.png
│   ├── container_001.png
│   └── ...
└── output.pptx             # 生成的PPT
```

### PPT内容

- ✅ **容器图片**：按z-index从后往前插入
- ✅ **文本内容**：精确复现位置、字体、大小、颜色
- ✅ **布局对齐**：基于24栅格系统，精确对齐

---

## 🔧 高级用法

### 自定义输出目录

```python
replicator = BrowserToPPTReplicator(
    output_dir=Path("custom_output")
)
```

### 从HTML文件复刻

```python
output_path = await replicator.replicate_from_file(
    html_file_path=Path("template.html"),
    output_ppt_path=Path("output.pptx")
)
```

### 单独使用各个模块

```python
from browser_to_ppt_replicator import (
    BrowserRenderer,
    ElementAnalyzer,
    CoordinateMapper,
    ContainerExtractor,
    TextExtractor,
    PPTReplicator
)

# 1. 渲染HTML
renderer = BrowserRenderer()
page = await renderer.render_html(html_content)

# 2. 分析元素
analyzer = ElementAnalyzer()
elements = await analyzer.analyze_elements(page)

# 3. 提取容器和文本
mapper = CoordinateMapper()
container_extractor = ContainerExtractor(Path("containers"))
text_extractor = TextExtractor()

containers = await container_extractor.extract_all_containers(elements['containers'])
texts = await text_extractor.extract_all_texts(elements['texts'])

# 4. 复刻到PPT
ppt_replicator = PPTReplicator(mapper)
ppt_replicator.replicate_slide(containers, texts)
ppt_replicator.save(Path("output.pptx"))
```

---

## ⚠️ 注意事项

### 1. 容器识别

- 容器需要有**可见的背景色或边框**
- 嵌套容器会被自动过滤（只保留最外层）
- 基于位置和尺寸去重

### 2. 文本提取

- 空文本会被过滤
- 重复文本会被去重（基于位置和内容）
- 样式信息（字体、大小、颜色）会被提取

### 3. 坐标精度

- 浏览器坐标（px）→ PPT坐标（cm）精确映射
- 24栅格系统确保布局一致性
- 位置误差 < 0.1cm

### 4. 性能

- 浏览器渲染：~1-2秒
- 元素分析：~0.1秒
- 容器截图：~0.1秒/个
- 文本提取：~0.01秒/个
- PPT生成：~0.1秒

---

## 🐛 故障排除

### Playwright未安装

```bash
pip install playwright
playwright install chromium
```

### 容器识别失败

- 检查HTML中容器是否有背景色或边框
- 使用`.card`类名或`[class*="card"]`选择器
- 检查元素是否在视口内

### 文本样式丢失

- 检查CSS样式是否正确应用
- 某些CSS属性可能无法完全复现（如渐变、复杂阴影）
- 文本颜色、字体、大小会被正确提取

---

## 📝 示例

完整示例请参考：`test_browser_to_ppt_replicator.py`

---

## 🎯 下一步

1. **集成到PPT生成流程**：将复刻器集成到`ppt_filler.py`
2. **支持Ant Design组件**：直接使用Ant Design React组件
3. **支持AntV图表**：集成G2Plot图表渲染
4. **LLM辅助**：使用LLM优化元素识别和布局

