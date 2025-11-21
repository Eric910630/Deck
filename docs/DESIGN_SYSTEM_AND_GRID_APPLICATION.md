# Ant Design & AntV 设计规范与24栅格坐标系应用

本文档详细说明 Ant Design 和 AntV 的完整设计规范，以及24栅格坐标系系统在本项目中的应用方式。

---

## 一、Ant Design 设计规范完整版

### 1.1 颜色系统（Color System）

#### 1.1.1 主色调（Primary Colors）

Ant Design 使用完整的色板系统，每个颜色有10个色阶：

**蓝色（Blue）** - 主色调：
```javascript
['#E6F4FF', '#BAE0FF', '#91CAFF', '#69B1FF', '#4096FF', '#1677FF', '#0958D9', '#003EB3', '#002C8C', '#001D66']
// 主色: #1677FF (v5) 或 #1890ff (v4)
```

**绿色（Green）** - 成功色：
```javascript
['#F6FFED', '#D9F7BE', '#B7EB8F', '#95DE64', '#73D13D', '#52C41A', '#389E0D', '#237804', '#135200', '#092B00']
// 主色: #52C41A
```

**橙色（Orange）** - 警告色：
```javascript
['#FFF7E6', '#FFE7BA', '#FFD591', '#FFC069', '#FFA940', '#FA8C16', '#D46B08', '#AD4E00', '#873800', '#612500']
// 主色: #FA8C16
```

**红色（Red）** - 错误色：
```javascript
['#FFF1F0', '#FFCCC7', '#FFA39E', '#FF7875', '#FF4D4F', '#F5222D', '#CF1322', '#A8071A', '#820014', '#5C0011']
// 主色: #F5222D
```

#### 1.1.2 文本颜色（Text Colors）

| 类型 | 颜色值 | 使用场景 |
|-----|--------|---------|
| 主文本（Primary Text） | `rgba(0, 0, 0, 0.85)` 或 `#262626` | 正文、标题 |
| 次文本（Secondary Text） | `rgba(0, 0, 0, 0.65)` 或 `#595959` | 副标题、说明文字 |
| 辅助文本（Tertiary Text） | `rgba(0, 0, 0, 0.45)` 或 `#8C8C8C` | 辅助信息 |
| 禁用文本（Disabled Text） | `rgba(0, 0, 0, 0.25)` 或 `#BFBFBF` | 禁用状态 |

#### 1.1.3 背景颜色（Background Colors）

| 类型 | 颜色值 | 使用场景 |
|-----|--------|---------|
| 页面背景（Page Background） | `#F5F5F5` 或 `#F0F2F5` | 页面整体背景 |
| 容器背景（Container Background） | `#FFFFFF` | 卡片、容器背景 |
| 禁用背景（Disabled Background） | `rgba(0, 0, 0, 0.04)` | 禁用状态背景 |
| 悬停背景（Hover Background） | `rgba(0, 0, 0, 0.06)` | 悬停状态背景 |
| 选中背景（Selected Background） | `#E6F4FF` (蓝色系) | 选中状态背景 |

#### 1.1.4 边框颜色（Border Colors）

| 类型 | 颜色值 | 使用场景 |
|-----|--------|---------|
| 基础边框（Base Border） | `#D9D9D9` | 默认边框 |
| 次要边框（Secondary Border） | `#F0F0F0` | 次要元素边框 |
| 悬停边框（Hover Border） | `#4096FF` (蓝色) | 悬停状态边框 |
| 激活边框（Active Border） | `#1677FF` (蓝色) | 激活状态边框 |
| 禁用边框（Disabled Border） | `rgba(0, 0, 0, 0.06)` | 禁用状态边框 |

#### 1.1.5 分类色（Category Colors）- 用于图表

Ant Design 提供10种分类色，用于数据可视化：

```javascript
colors10 = [
  '#1677FF', // 蓝色
  '#52C41A', // 绿色
  '#FA8C16', // 橙色
  '#F5222D', // 红色
  '#722ED1', // 紫色
  '#13C2C2', // 青色
  '#EB2F96', // 粉色
  '#FA541C', // 橙红
  '#A0D911', // 黄绿
  '#2F54EB'  // 深蓝
]
```

**代码实现位置**: `ant_design_theme.py` → `AntDesignColors.category10`

### 1.2 间距系统（Spacing System）

Ant Design 的间距系统基于 **8px 基础单位**，提供预设尺寸和自定义数值。

#### 1.2.1 预设尺寸（Preset Sizes）

| 尺寸名称 | 数值 | 说明 | 使用场景 |
|---------|------|------|---------|
| `small` | 8px | 小间距 | 紧密排列的元素 |
| `middle` | 16px | 中间距 | 默认间距 |
| `large` | 24px | 大间距 | 区块之间的间距 |

#### 1.2.2 标准间距值（Standard Spacing Values）

```
8px   (0.4cm)  - XS  - 最小间距
12px  (0.6cm)  - SM  - 小间距
16px  (0.8cm)  - MD  - 基础间距（最常用）
24px  (1.2cm)  - LG  - 大间距
32px  (1.6cm)  - XL  - 超大间距
48px  (2.4cm)  - XXL - 最大间距
```

**代码实现位置**: `ant_design_theme.py` → `AntDesignSpacing`

#### 1.2.3 组件内边距（Component Padding）

**Card 组件内边距**：
- 标准尺寸：`bodyPadding: 24px`, `headerPadding: 16px`
- 小尺寸：`bodyPaddingSM: 12px`, `headerPaddingSM: 12px`

**Input 组件内边距**：
- 标准：`paddingInline: 11px`, `paddingBlock: 4px`
- 大尺寸：`paddingInlineLG: 15px`, `paddingBlockLG: 7px`
- 小尺寸：`paddingInlineSM: 7px`, `paddingBlockSM: 0px`

### 1.3 字体系统（Typography System）

#### 1.3.1 字体族（Font Family）

Ant Design 使用系统字体栈，确保跨平台一致性：

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
             'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 
             'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 
             'Noto Color Emoji';
```

**代码实现位置**: `ant_design_theme.py` → `AntDesignTypography.fontFamily`

#### 1.3.2 字号系统（Font Size）

| 级别 | 字号 | 行高 | 字重 | 使用场景 |
|-----|------|------|------|---------|
| H1 | 38pt | 1.21 | 600 (SemiBold) | 主标题 |
| H2 | 30pt | 1.27 | 600 (SemiBold) | 二级标题 |
| H3 | 24pt | 1.33 | 600 (SemiBold) | 三级标题 |
| H4 | 20pt | 1.4 | 600 (SemiBold) | 四级标题 |
| Body | 14pt | 1.57 | 400 (Normal) | 正文 |
| Small | 12pt | 1.67 | 400 (Normal) | 辅助文本 |

**代码实现位置**: `ant_design_theme.py` → `AntDesignTypography`

### 1.4 圆角系统（Border Radius）

| 尺寸 | 数值 | 使用场景 |
|-----|------|---------|
| 小（Small） | 2px | 小元素、标签 |
| 基础（Base） | 6px | 按钮、输入框、卡片（默认） |
| 大（Large） | 8px | 大卡片、模态框 |

**特殊圆角**：
- **圆形**: `50%` - 头像、徽章
- **完全圆角**: `9999px` - 胶囊按钮

**代码实现位置**: `ant_design_theme.py` → `AntDesignBorderRadius`

### 1.5 阴影系统（Shadow System）

| 级别 | 阴影值 | 使用场景 |
|-----|--------|---------|
| 基础阴影 | `0 2px 8px rgba(0, 0, 0, 0.15)` | 卡片、下拉菜单 |
| 中等阴影 | `0 4px 12px rgba(0, 0, 0, 0.15)` | 模态框、弹出层 |
| 大阴影 | `0 8px 24px rgba(0, 0, 0, 0.12)` | 大型模态框 |

**Card 组件阴影**：
- 默认：`0 1px 2px rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px rgba(0, 0, 0, 0.02)`
- 悬停：提升阴影效果

### 1.6 设计令牌（Design Tokens）

Ant Design 5.x 使用 Design Tokens 系统，支持主题定制：

**颜色令牌**：
```css
--color-primary: #1677FF;
--color-success: #52C41A;
--color-warning: #FA8C16;
--color-error: #F5222D;
--color-text: rgba(0, 0, 0, 0.85);
--color-text-secondary: rgba(0, 0, 0, 0.65);
--color-bg-container: #FFFFFF;
--color-border: #D9D9D9;
```

**间距令牌**：
```css
--padding-xs: 8px;
--padding-sm: 12px;
--padding-md: 16px;
--padding-lg: 24px;
--padding-xl: 32px;
```

**代码实现位置**: `ant_design_theme.py` → `AntDesignTheme`

---

## 二、AntV 图表设计规范完整版

### 2.1 G2Plot 设计规范

#### 2.1.1 主题系统（Theme System）

**内置主题**：
- `default` - 默认主题（亮色）
- `dark` - 暗色主题

**主题配置**：
```typescript
{
  theme: 'default', // 或 'dark'
  // 或自定义主题对象
  theme: {
    defaultColor: '#1677FF',
    colors10: [...], // 10种分类色
    colors20: [...], // 20种分类色
    styleSheet: {
      fontFamily: 'Avenir',
      // 其他样式
    }
  }
}
```

**代码实现位置**: `web_chart_generator.py` → `_generate_chart_config`

#### 2.1.2 配色方案（Color Palette）

**分类色（Category Colors）**：
- `colors10`: 10种分类色（用于 ≤10 个分类）
- `colors20`: 20种分类色（用于 11-20 个分类）

默认使用 Ant Design 分类色：
```javascript
colors10 = [
  '#1677FF', '#52C41A', '#FA8C16', '#F5222D', '#722ED1',
  '#13C2C2', '#EB2F96', '#FA541C', '#A0D911', '#2F54EB'
]
```

**代码实现位置**: `antv_chart_theme.py` → `AntVChartTheme.get_default_colors()`

#### 2.1.3 图表样式（Chart Styles）

**背景样式**：
- 图表背景：`#FFFFFF`（白色）
- 图表内边距：建议 16px 或 24px

**网格线样式**：
- 网格线颜色：`#F0F0F0`（浅灰）
- 网格线宽度：1px
- 网格线类型：实线或虚线

**坐标轴样式**：
- 坐标轴颜色：`#D9D9D9`（灰色）
- 坐标轴宽度：1px
- 坐标轴标签：使用 Ant Design 文本色系统

**图例样式**：
- 图例位置：`top`, `bottom`, `left`, `right`
- 图例间距：16px
- 图例文本：14pt，rgba(0,0,0,0.85)

**代码实现位置**: `web_chart_generator.py` → `_generate_html_template`

#### 2.1.4 图表内边距（Chart Padding）

**推荐内边距**：
- 小图表：16px
- 中等图表：24px
- 大图表：32px

**内边距配置**：
```typescript
{
  padding: [24, 24, 24, 24], // [top, right, bottom, left]
  // 或
  padding: 'auto' // 自动计算
}
```

**代码实现位置**: `web_chart_generator.py` → `_generate_chart_config`

---

## 三、24栅格系统规范

### 3.1 Ant Design 24栅格系统

Ant Design 使用 **24栅格系统** 进行布局：

**基本概念**：
- 将容器分为 24 等份
- 每个 `Col` 的 `span` 值表示占据的栅格数（1-24）
- 一行最多 24 个栅格

**响应式断点**：
```javascript
{
  xs: '< 576px',   // 超小屏
  sm: '≥ 576px',   // 小屏
  md: '≥ 768px',   // 中屏
  lg: '≥ 992px',   // 大屏
  xl: '≥ 1200px',  // 超大屏
  xxl: '≥ 1600px'  // 超超大屏
}
```

**Row 组件属性**：
- `gutter`: 栅格间距（数字、对象或数组 `[horizontal, vertical]`）
- `align`: 垂直对齐（`top`, `middle`, `bottom`, `stretch`）
- `justify`: 水平排列（`start`, `end`, `center`, `space-around`, `space-between`, `space-evenly`）
- `wrap`: 是否换行（默认 `true`）

**Col 组件属性**：
- `span`: 栅格数（1-24）
- `offset`: 栅格左侧偏移量
- `push`: 栅格向右移动
- `pull`: 栅格向左移动
- `order`: Flex 排序

---

## 四、24栅格坐标系在本系统中的应用

### 4.1 系统坐标系设计

#### 4.1.1 画布规格

**16:9横版画布**：
- **宽度**: 1920px
- **高度**: 1080px
- **宽高比**: 16:9

**代码实现位置**: 
- `html_generator.py` → `CANVAS_WIDTH = 1920`, `CANVAS_HEIGHT = 1080`
- `html_canvas_generator.py` → `CANVAS_WIDTH = 1920`, `CANVAS_HEIGHT = 1080`

#### 4.1.2 坐标系定义

**坐标系系统**：
- **原点**: 左下角 (0, 0)
- **X轴**: 向右为正（0 → 1920px）
- **Y轴**: 向上为正（0 → 1080px）

**代码实现位置**: `html_generator.py` → 类注释中的坐标系说明

#### 4.1.3 24栅格系统参数

**栅格配置**：
- **列数（GRID_COLUMNS）**: 24列
- **行数（GRID_ROWS）**: 13.5行（为了适配16:9比例）
- **Padding**: 24px（左右各24px，上下各24px）

**内容区域尺寸**：
- **内容宽度**: `CANVAS_WIDTH - 2 * HTML_PADDING = 1920 - 48 = 1872px`
- **内容高度**: `CANVAS_HEIGHT - 2 * HTML_PADDING = 1080 - 48 = 1032px`

**栅格单元尺寸**：
- **栅格单元宽度（CELL_WIDTH）**: `CONTENT_WIDTH / GRID_COLUMNS = 1872 / 24 = 78px`
- **栅格单元高度（CELL_HEIGHT）**: `CONTENT_HEIGHT / GRID_ROWS = 1032 / 13.5 ≈ 76.4px`

**代码实现位置**: `html_generator.py` → 类常量定义

```python
# 16:9画布尺寸
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080
GRID_COLUMNS = 24
GRID_ROWS = 13.5

# Padding（与坐标映射器保持一致）
HTML_PADDING = 24  # px

# 内容区域尺寸（减去padding）
CONTENT_WIDTH = CANVAS_WIDTH - 2 * HTML_PADDING  # 1872px
CONTENT_HEIGHT = CANVAS_HEIGHT - 2 * HTML_PADDING  # 1032px

# 栅格单元尺寸
CELL_WIDTH = CONTENT_WIDTH / GRID_COLUMNS  # ≈ 78px
CELL_HEIGHT = CONTENT_HEIGHT / GRID_ROWS   # ≈ 76.4px
```

**注意**: `html_canvas_generator.py` 中的栅格计算略有不同：
```python
# 栅格单元尺寸（基于画布尺寸，不考虑padding）
CELL_WIDTH = CANVAS_WIDTH / GRID_COLUMNS  # 1920 / 24 = 80px
CELL_HEIGHT = CANVAS_HEIGHT / GRID_ROWS   # 1080 / 13.5 = 80px
```

### 4.2 坐标转换实现

#### 4.2.1 栅格坐标到像素坐标转换

**函数**: `_grid_to_pixel(grid_x, grid_y, span_x, span_y)`

**输入参数**：
- `grid_x`: 栅格列位置（0-23）
- `grid_y`: 栅格行位置（0-12.5，从下往上）
- `span_x`: 占据的列数
- `span_y`: 占据的行数

**转换公式**：
```python
# 计算像素位置（左下角为原点）
left_px = HTML_PADDING + grid_x * CELL_WIDTH
bottom_px = HTML_PADDING + grid_y * CELL_HEIGHT
width_px = span_x * CELL_WIDTH
height_px = span_y * CELL_HEIGHT

# 转换为CSS的top定位（CSS使用top-left原点）
top_px = CANVAS_HEIGHT - bottom_px - height_px
```

**代码实现位置**: `html_generator.py` → `_grid_to_pixel` 方法

```python
def _grid_to_pixel(self, grid_x: float, grid_y: float, span_x: float, span_y: float) -> tuple:
    """
    将栅格坐标转换为像素坐标（左下角为原点）
    
    Args:
        grid_x: 栅格列位置（0-23）
        grid_y: 栅格行位置（0-12.5，从下往上）
        span_x: 占据的列数
        span_y: 占据的行数
    
    Returns:
        (left, top, width, height) 像素值（CSS使用top-left原点）
    """
    # 计算像素位置（左下角为原点）
    left_px = self.HTML_PADDING + grid_x * self.CELL_WIDTH
    bottom_px = self.HTML_PADDING + grid_y * self.CELL_HEIGHT
    width_px = span_x * self.CELL_WIDTH
    height_px = span_y * self.CELL_HEIGHT
    
    # 转换为CSS的top定位（CSS使用top-left原点）
    top_px = self.CANVAS_HEIGHT - bottom_px - height_px
    
    return (left_px, top_px, width_px, height_px)
```

#### 4.2.2 坐标系转换（左下角原点 → CSS top-left原点）

**函数**: `coordinate_to_css(left, bottom, width, height)`

**转换公式**：
```python
# 转换为CSS的top位置
css_top = CANVAS_HEIGHT - bottom - height
```

**代码实现位置**: `html_canvas_generator.py` → `coordinate_to_css` 方法

```python
def coordinate_to_css(
    self,
    left: float,
    bottom: float,
    width: float,
    height: float
) -> Dict[str, float]:
    """
    将坐标系坐标转换为CSS位置
    坐标系：左下角为原点
    CSS：top-left为原点
    
    Args:
        left: 距离左边缘的像素
        bottom: 距离下边缘的像素
        width: 宽度
        height: 高度
        
    Returns:
        CSS位置字典 {left, top, width, height}
    """
    # 转换为CSS的top位置
    css_top = self.CANVAS_HEIGHT - bottom - height
    
    return {
        'left': left,
        'top': css_top,
        'width': width,
        'height': height
    }
```

### 4.3 栅格标准尺实现

#### 4.3.1 栅格标准尺绘制

**功能**: 在画布四周绘制24列×13.5行的栅格线，并标注栅格编号

**实现方式**: 使用SVG绘制栅格线和标签

**代码实现位置**: `html_canvas_generator.py` → `_generate_grid_ruler_html` 方法

```python
def _generate_grid_ruler_html(self) -> str:
    """
    生成栅格标准尺HTML
    在画布四周绘制24列×13.5行的栅格线
    """
    svg_lines = []
    svg_labels = []
    
    # 绘制垂直栅格线（24列）
    for col in range(self.GRID_COLUMNS + 1):
        x = col * self.CELL_WIDTH
        # 垂直线
        svg_lines.append(f'<line class="grid-ruler-line" x1="{x}" y1="0" x2="{x}" y2="{self.CANVAS_HEIGHT}"/>')
        # 底部标签
        svg_labels.append(f'<text class="grid-ruler-label" x="{x}" y="{self.CANVAS_HEIGHT + 15}" fill="#999">{col}</text>')
        # 顶部标签
        svg_labels.append(f'<text class="grid-ruler-label" x="{x}" y="-5" fill="#999">{col}</text>')
    
    # 绘制水平栅格线（13.5行，向上从底部开始）
    for row in range(int(self.GRID_ROWS) + 1):
        # CSS使用top定位，所以需要从顶部计算
        y_from_top = self.CANVAS_HEIGHT - (row * self.CELL_HEIGHT)
        # 水平线
        svg_lines.append(f'<line class="grid-ruler-line" x1="0" y1="{y_from_top}" x2="{self.CANVAS_WIDTH}" y2="{y_from_top}"/>')
        # 左侧标签（从底部开始，row=0是底部）
        svg_labels.append(f'<text class="grid-ruler-label" x="-15" y="{y_from_top + 4}" fill="#999">{row}</text>')
        # 右侧标签
        svg_labels.append(f'<text class="grid-ruler-label" x="{self.CANVAS_WIDTH + 15}" y="{y_from_top + 4}" fill="#999">{row}</text>')
    
    return f"""
        <!-- 栅格标准尺 -->
        <svg class="grid-ruler" width="{self.CANVAS_WIDTH}" height="{self.CANVAS_HEIGHT}" style="position: absolute; top: 0; left: 0;">
            {''.join(svg_lines)}
            {''.join(svg_labels)}
        </svg>
        
        <!-- 坐标原点标记（左下角） -->
        <div class="origin-marker" title="坐标原点 (0, 0)"></div>"""
```

#### 4.3.2 坐标原点标记

**功能**: 在画布左下角显示红色圆形标记，表示坐标原点 (0, 0)

**实现方式**: CSS样式 + HTML元素

**代码实现位置**: `html_canvas_generator.py` → `_generate_canvas_css` 方法

```css
/* 坐标原点标记 */
.origin-marker {
    position: absolute;
    left: 0;
    bottom: 0;
    width: 20px;
    height: 20px;
    background: #ff4d4f;
    border-radius: 50%;
    z-index: 1000;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.origin-marker::after {
    content: 'O';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 12px;
    font-weight: bold;
}
```

### 4.4 元素定位实现

#### 4.4.1 绝对定位系统

**实现方式**: 使用CSS `position: absolute` 和动态计算的 `left`、`top`、`width`、`height`

**代码实现位置**: `html_canvas_generator.py` → `_generate_elements_html` 方法

```python
def _generate_elements_html(self, elements: List[Dict[str, Any]]) -> str:
    """
    生成元素HTML
    根据坐标信息放置元素
    """
    elements_html = []
    
    for elem in elements:
        elem_id = elem.get('id', '')
        elem_type = elem.get('type', 'card')
        content = elem.get('content', '')
        coordinates = elem.get('coordinates', {})
        
        # 解析坐标
        # 坐标系：左下角为原点
        # CSS使用top-left原点，需要转换
        left = coordinates.get('left', 0)
        right = coordinates.get('right')
        top = coordinates.get('top')
        bottom = coordinates.get('bottom', 0)
        width = coordinates.get('width', 200)
        height = coordinates.get('height', 100)
        
        # 计算CSS位置（从左下角原点转换为top-left原点）
        css_left = left
        if right is not None:
            css_left = self.CANVAS_WIDTH - right - width
        
        css_top = None
        if top is not None:
            css_top = top
        elif bottom is not None:
            # 从底部距离转换为顶部距离
            css_top = self.CANVAS_HEIGHT - bottom - height
        
        # 生成样式
        style_parts = []
        if css_left is not None:
            style_parts.append(f"left: {css_left}px;")
        if css_top is not None:
            style_parts.append(f"top: {css_top}px;")
        style_parts.append(f"width: {width}px;")
        style_parts.append(f"height: {height}px;")
        
        style = " ".join(style_parts)
        
        # 根据元素类型生成HTML
        if elem_type == 'title':
            elem_html = f'<h1 id="{elem_id}" class="element element-title" style="{style}">{content}</h1>'
        elif elem_type == 'text':
            elem_html = f'<p id="{elem_id}" class="element element-text" style="{style}">{content}</p>'
        elif elem_type == 'card':
            elem_html = f'<div id="{elem_id}" class="element element-card" style="{style}">{content}</div>'
        else:
            elem_html = f'<div id="{elem_id}" class="element" style="{style}">{content}</div>'
        
        elements_html.append(elem_html)
    
    return "\n            ".join(elements_html)
```

### 4.5 布局规划中的应用

#### 4.5.1 布局规划器使用栅格系统

**功能**: `LayoutPlanner` 在生成布局规划时，会参考24栅格系统来规划元素位置

**代码实现位置**: `layout_planner.py` → `LayoutPlanner` 类

**系统提示词**：
```python
system_prompt = """你是一个专业的UI/UX设计师，精通Ant Design和AntV设计规范。
...
- 布局系统：遵循Ant Design 24栅格系统，合理规划元素位置
...
"""
```

#### 4.5.2 坐标解析

**功能**: 从布局规划的位置描述中解析栅格坐标

**代码实现位置**: `html_generator.py` → `_parse_grid_from_description` 方法

```python
def _parse_grid_from_description(
    self,
    position_description: str,
    size_description: str
) -> Tuple[Optional[float], Optional[float], Optional[float], Optional[float]]:
    """
    从位置描述中解析栅格坐标（简化版本）
    
    Returns:
        (grid_x, grid_y, span_x, span_y) 栅格坐标
    """
    grid_x = 2  # 默认左边距2栅格
    grid_y = 0  # 默认底部
    span_x = 20  # 默认宽度20栅格
    span_y = 2  # 默认高度2栅格
    
    # 解析位置
    if '顶部' in position_description:
        grid_y = 11.5  # 接近顶部
    elif '中间' in position_description:
        grid_y = 5.75  # 中间
    elif '底部' in position_description:
        grid_y = 0  # 底部
    
    if '左侧' in position_description:
        grid_x = 2
    elif '居中' in position_description:
        grid_x = 2
    elif '右侧' in position_description:
        grid_x = 12
    
    # 解析尺寸
    if '栅格' in size_description:
        grid_match = re.search(r'(\d+)个?栅格', size_description)
        if grid_match:
            span_x = int(grid_match.group(1))
    
    return (grid_x, grid_y, span_x, span_y)
```

---

## 五、设计规范在代码中的应用

### 5.1 Ant Design 主题应用

#### 5.1.1 颜色应用

**代码位置**: `html_generator.py` → `_generate_css_with_layout_plan` 方法

```python
from ant_design_theme import ant_design_theme

# 使用Ant Design颜色
background_color = ant_design_theme.colors.colorBgContainer  # #FFFFFF
border_color = ant_design_theme.colors.colorBorder  # #D9D9D9
text_color = ant_design_theme.colors.colorText  # #262626
```

#### 5.1.2 间距应用

**代码位置**: `html_generator.py` → `_generate_css` 方法

```python
# 将cm转换为px（1cm ≈ 37.8px at 96dpi）
cm_to_px = 37.8
padding_lg_px = int(ant_design_theme.get_spacing_cm('lg') * cm_to_px)  # 24px
padding_md_px = int(ant_design_theme.get_spacing_cm('md') * cm_to_px)  # 16px
padding_sm_px = int(ant_design_theme.get_spacing_cm('sm') * cm_to_px)  # 12px
padding_xs_px = int(ant_design_theme.get_spacing_cm('xs') * cm_to_px)  # 8px
```

#### 5.1.3 字体应用

**代码位置**: `html_generator.py` → `_generate_css` 方法

```python
font-family: {chinese_ppt_theme.typography.fontFamilyBody};
```

### 5.2 AntV 图表主题应用

#### 5.2.1 图表配色应用

**代码位置**: `web_chart_generator.py` → `_generate_html_template` 方法

```python
from antv_chart_theme import antv_chart_theme

# 获取Ant Design/AntV配色
colors = antv_chart_theme.get_default_colors()
```

#### 5.2.2 图表样式应用

**代码位置**: `web_chart_generator.py` → `_generate_chart_config` 方法

```python
theme: {
    defaultColor: '{ant_design_theme.colors.colorPrimary}',
    styleSheet: {
        fontFamily: '{ant_design_theme.typography.fontFamily}',
        // 其他样式
    }
}
```

---

## 六、总结

### 6.1 设计规范应用流程

```
输入材料
  ├─ 布局规划（Layout Plan）
  │   └─ 参考24栅格系统规划元素位置
  ├─ 润色内容（Polished Content）
  └─ 颜色配置（Color Configuration）
       └─ 使用Ant Design颜色系统
       ↓
HTML生成器（HTMLGenerator）
  ├─ 应用Ant Design主题
  │   ├─ 颜色：ant_design_theme.colors
  │   ├─ 间距：ant_design_theme.spacing
  │   └─ 字体：ant_design_theme.typography
  ├─ 24栅格系统
  │   ├─ 栅格坐标 → 像素坐标转换
  │   ├─ 绘制栅格标准尺
  │   └─ 绝对定位元素
  └─ 画布生成（HTMLCanvasGenerator）
       ├─ 创建16:9画布（1920px × 1080px）
       ├─ 建立坐标系（左下角为原点）
       ├─ 绘制栅格标准尺（24列 × 13.5行）
       └─ 放置元素（根据坐标）
       ↓
输出HTML文件
```

### 6.2 关键代码文件

1. **`ant_design_theme.py`**: Ant Design 设计规范定义
2. **`antv_chart_theme.py`**: AntV 图表主题配置
3. **`html_generator.py`**: HTML生成器，应用设计规范和栅格系统
4. **`html_canvas_generator.py`**: 画布生成器，实现坐标系和栅格标准尺
5. **`web_chart_generator.py`**: 图表生成器，应用AntV主题

### 6.3 设计规范要点

1. **颜色系统**: 使用Ant Design标准颜色（主色、成功、警告、错误等）
2. **间距系统**: 基于8px基础单位（8px, 16px, 24px等）
3. **字体系统**: 使用系统字体栈，字号遵循Ant Design规范
4. **圆角系统**: 基础6px，小2px，大8px
5. **阴影系统**: 使用Ant Design标准阴影值
6. **24栅格系统**: 24列×13.5行，栅格单元尺寸78px×76.4px
7. **坐标系**: 左下角为原点，X轴向右，Y轴向上

### 6.4 坐标系要点

1. **画布尺寸**: 1920px × 1080px（16:9）
2. **坐标系原点**: 左下角 (0, 0)
3. **栅格系统**: 24列 × 13.5行
4. **坐标转换**: 左下角原点 → CSS top-left原点
5. **栅格标准尺**: SVG绘制，标注栅格编号
6. **元素定位**: 绝对定位，根据坐标动态计算位置

---

## 七、参考资料

- [Ant Design 官方文档](https://ant.design)
- [AntV G2Plot 文档](https://g2plot.antv.antgroup.com)
- [AntV G2 文档](https://g2.antv.antgroup.com)
- [Ant Design 设计令牌](https://ant.design/docs/react/customize-theme)

