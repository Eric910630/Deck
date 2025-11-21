# Native Shape Compiler (原生形状编译器)

## 概述

Native Shape Compiler 是 Deck 的**终极渲染方案**，完全废弃截图方式，将 HTML/CSS 样式精准翻译成 python-pptx 的原生 Shape 属性。

## 核心优势

1. **完全可编辑**：所有元素都是原生 PPT 对象，可以直接编辑文字、调整样式
2. **精准还原**：CSS 样式（位置、尺寸、颜色、圆角、阴影、边框）精确映射到 PPT
3. **文件体积小**：不使用图片，PPT 文件体积大幅减小
4. **性能优秀**：原生绘制比截图+插入图片更快

## 架构设计

### 工作流程

```
HTML/CSS (LLM生成)
    ↓
Playwright (浏览器渲染)
    ↓
DOMAnalyzer (提取样式)
    ↓
NativeCompositor (原生绘制)
    ↓
PPTX (可编辑的PPT)
```

### 核心模块

#### 1. `src/rendering/dom_analyzer.py`

**职责**：在浏览器端提取元素的精确计算样式

**功能**：
- 使用 Playwright 加载 HTML
- 执行 JavaScript 提取所有 `data-ppt-element` 元素的 Computed Style
- 提取几何信息（位置、尺寸）
- 提取视觉样式（颜色、字体、边框、圆角、阴影等）

**输出**：`LayoutData` - 包含所有元素的样式信息列表

#### 2. `src/rendering/native_compositor.py`

**职责**：将 DOM 样式数据编译为 python-pptx 原生对象

**功能**：
- **位置映射**：px -> cm (使用 CoordinateMapper)
- **颜色映射**：CSS 颜色 (hex/rgb) -> RGBColor
- **圆角映射**：px -> Adjustment (0.0-0.5)
- **阴影映射**：CSS Shadow -> PPT Shadow (近似模拟)
- **字体映射**：CSS font-family -> Windows 安全字体
- **边框处理**：支持装饰条（border-top）的特殊处理

**绘制能力**：
- 卡片（背景、边框、圆角、阴影、装饰条）
- 文本框（文字、字体、颜色、对齐、粗体）

## 样式映射规则

### 1. 位置和尺寸

```python
# 浏览器坐标 (px) -> PPT 坐标 (cm)
left, top = coordinate_mapper.browser_to_ppt(x, y)
width, height = coordinate_mapper.browser_size_to_ppt(w, h)
```

### 2. 颜色

**支持的格式**：
- Hex: `#ffffff`, `#fff`
- RGB: `rgb(255, 255, 255)`
- RGBA: `rgba(255, 255, 255, 0.5)` (透明度会被忽略)

**映射**：
```python
RGBColor(r, g, b)  # 应用到 fill.color 或 font.color
```

### 3. 圆角

**算法**：
```python
adjustment = borderRadius / min(width, height)
adjustment = max(0.0, min(0.5, adjustment))  # 限制在有效范围
```

**形状类型**：
- `borderRadius > 0`: 使用 `MSO_SHAPE.ROUNDED_RECTANGLE`
- `borderRadius == 0`: 使用 `MSO_SHAPE.RECTANGLE`

### 4. 阴影

**近似模拟**：
```python
shape.shadow.blur_radius = Pt(10)
shape.shadow.distance = Pt(3)
shape.shadow.transparency = 0.6
shape.shadow.color.rgb = RGBColor(0, 0, 0)  # 默认灰色
```

**注意**：CSS `box-shadow` 的复杂参数（多个阴影、颜色、模糊半径）会被简化为单一阴影效果。

### 5. 字体

**字体映射表**：
- `Microsoft YaHei` / `YaHei` / `Hei` → `Microsoft YaHei`
- `SimSun` / `Song` → `SimSun`
- `Arial` → `Arial`
- `Times` → `Times New Roman`
- 默认 → `Microsoft YaHei` (中文 PPT 安全字体)

**字号转换**：
```python
# 浏览器 96dpi: 1px = 0.75pt
font_size_pt = fontSize_px * 0.75
```

### 6. 边框和装饰条

**统一边框**：
- PPT 只支持统一边框，CSS 的 `border-top` 等会被转换为全边框

**装饰条处理**：
- 如果 CSS 有 `border-top: 4px solid blue`，会额外绘制一个细长矩形作为装饰条
- 装饰条位于卡片顶部，颜色与 `borderTopColor` 一致

## 使用示例

### 基本用法

```python
from src.rendering.dom_analyzer import DOMAnalyzer
from src.rendering.native_compositor import NativeCompositor
from playwright.async_api import async_playwright
from pptx import Presentation

# 1. 加载 HTML
async with async_playwright() as p:
    browser = await p.chromium.launch()
    page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
    await page.set_content(html_content)
    
    # 2. 提取样式
    analyzer = DOMAnalyzer()
    layout_data = await analyzer.extract_layout_data(page)
    
    await browser.close()

# 3. 绘制到 PPT
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])

compositor = NativeCompositor()
compositor.composite_slide(slide, layout_data)

prs.save('output.pptx')
```

### 集成到 PPTFiller

在 `src/core/ppt_filler.py` 中，可以添加一个新的渲染模式：

```python
# 在 _fill_with_browser_rendering 方法中
if use_native_compositor:
    from ..rendering.dom_analyzer import DOMAnalyzer
    from ..rendering.native_compositor import NativeCompositor
    
    analyzer = DOMAnalyzer()
    layout_data = await analyzer.extract_layout_data(page)
    
    compositor = NativeCompositor()
    compositor.composite_slide(slide, layout_data)
else:
    # 原有的截图方式
    ...
```

## 测试

运行测试脚本：

```bash
python3 tests/test_native_compositor.py
```

**前置条件**：
- 需要先运行 `tests/test_single_slide_layout.py` 生成测试 HTML
- 需要安装 Playwright: `pip install playwright && playwright install chromium`

## 限制和注意事项

### 1. CSS 特性支持

**完全支持**：
- ✅ 位置和尺寸
- ✅ 背景颜色
- ✅ 文字颜色、字体、字号、粗体
- ✅ 圆角（简单情况）
- ✅ 边框（统一边框）
- ✅ 装饰条（border-top）

**部分支持**：
- ⚠️ 阴影（简化为单一阴影效果）
- ⚠️ 复杂边框（只支持统一边框）
- ⚠️ 渐变背景（不支持，会使用主色）

**不支持**：
- ❌ 图片背景
- ❌ 复杂阴影（多个阴影、内阴影）
- ❌ CSS Grid/Flex 布局的复杂嵌套
- ❌ 动画和过渡效果

### 2. 字体限制

- 只能使用 Windows 系统已安装的字体
- 字体映射可能不完全准确
- 建议在 CSS 中使用 Windows 安全字体

### 3. 性能考虑

- 大量元素时，原生绘制可能比截图慢
- 建议对复杂页面进行性能测试

## 未来改进方向

1. **更精确的阴影映射**：解析 CSS `box-shadow` 的完整参数
2. **渐变背景支持**：将 CSS 渐变转换为 PPT 渐变填充
3. **图片处理**：支持 `<img>` 标签的图片插入
4. **复杂布局**：更好地处理 Flex/Grid 布局的嵌套结构
5. **字体回退**：更智能的字体映射和回退机制

## 相关文档

- [CSS-First Architecture](./CSS_FIRST_ARCHITECTURE.md)
- [Directory Restructure](./DIRECTORY_RESTRUCTURE.md)
- [Design System and Grid Application](./DESIGN_SYSTEM_AND_GRID_APPLICATION.md)

