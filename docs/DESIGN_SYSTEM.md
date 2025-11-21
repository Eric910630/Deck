# Ant Design & AntV 完整设计规范

本文档基于 Ant Design 和 AntV 官方设计规范，提供完整的设计系统参考。

---

## 1. Ant Design 设计规范

### 1.1 颜色系统

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

- **主文本（Primary Text）**: `rgba(0, 0, 0, 0.85)` 或 `#262626`
- **次文本（Secondary Text）**: `rgba(0, 0, 0, 0.65)` 或 `#595959`
- **辅助文本（Tertiary Text）**: `rgba(0, 0, 0, 0.45)` 或 `#8C8C8C`
- **禁用文本（Disabled Text）**: `rgba(0, 0, 0, 0.25)` 或 `#BFBFBF`
- **占位符文本（Placeholder Text）**: `rgba(0, 0, 0, 0.25)` 或 `#BFBFBF`

#### 1.1.3 背景颜色（Background Colors）

- **页面背景（Page Background）**: `#F5F5F5` 或 `#F0F2F5`
- **容器背景（Container Background）**: `#FFFFFF`
- **禁用背景（Disabled Background）**: `rgba(0, 0, 0, 0.04)`
- **悬停背景（Hover Background）**: `rgba(0, 0, 0, 0.06)`
- **选中背景（Selected Background）**: `#E6F4FF` (蓝色系) 或 `rgba(0, 0, 0, 0.04)`

#### 1.1.4 边框颜色（Border Colors）

- **基础边框（Base Border）**: `#D9D9D9`
- **次要边框（Secondary Border）**: `#F0F0F0`
- **悬停边框（Hover Border）**: `#4096FF` (蓝色)
- **激活边框（Active Border）**: `#1677FF` (蓝色)
- **禁用边框（Disabled Border）**: `rgba(0, 0, 0, 0.06)`

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

#### 1.2.3 组件内边距（Component Padding）

**Card 组件内边距**：
- 标准尺寸：`bodyPadding: 24px`, `headerPadding: 16px`
- 小尺寸：`bodyPaddingSM: 12px`, `headerPaddingSM: 12px`

**Input 组件内边距**：
- 标准：`paddingInline: 11px`, `paddingBlock: 4px`
- 大尺寸：`paddingInlineLG: 15px`, `paddingBlockLG: 7px`
- 小尺寸：`paddingInlineSM: 7px`, `paddingBlockSM: 0px`

**Button 组件内边距**：
- 标准：`paddingInline: 15px`, `paddingBlock: 4px`
- 大尺寸：`paddingInlineLG: 23px`, `paddingBlockLG: 7px`
- 小尺寸：`paddingInlineSM: 7px`, `paddingBlockSM: 0px`

#### 1.2.4 元素间距（Element Spacing）

使用 `Space` 组件或 `Flex` 组件的 `gap` 属性：

```jsx
// 预设尺寸
<Space size="small">   // 8px
<Space size="middle">  // 16px
<Space size="large">   // 24px

// 自定义数值
<Space size={20}>      // 20px
<Flex gap={16}>        // 16px
```

### 1.3 字体系统（Typography System）

#### 1.3.1 字体族（Font Family）

Ant Design 使用系统字体栈，确保跨平台一致性：

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
             'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 
             'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 
             'Noto Color Emoji';
```

#### 1.3.2 字号系统（Font Size）

| 级别 | 字号 | 行高 | 字重 | 使用场景 |
|-----|------|------|------|---------|
| H1 | 38pt | 1.21 | 600 (SemiBold) | 主标题 |
| H2 | 30pt | 1.27 | 600 (SemiBold) | 二级标题 |
| H3 | 24pt | 1.33 | 600 (SemiBold) | 三级标题 |
| H4 | 20pt | 1.4 | 600 (SemiBold) | 四级标题 |
| Body | 14pt | 1.57 | 400 (Normal) | 正文 |
| Small | 12pt | 1.67 | 400 (Normal) | 辅助文本 |

#### 1.3.3 字重（Font Weight）

- **Normal**: 400 - 正文、常规文本
- **SemiBold**: 600 - 标题、强调文本
- **Bold**: 700 - 特殊强调（较少使用）

#### 1.3.4 行高（Line Height）

- **标题行高**: 1.21 - 1.4（根据字号调整）
- **正文行高**: 1.57（14pt 字体）
- **小号行高**: 1.67（12pt 字体）

#### 1.3.5 文本样式（Text Styles）

**Typography 组件支持的样式**：
- `strong` - 加粗
- `italic` - 斜体
- `underline` - 下划线
- `delete` - 删除线
- `mark` - 标记（高亮）
- `code` - 代码样式
- `keyboard` - 键盘样式

**文本类型（Type）**：
- `secondary` - 次文本（rgba(0,0,0,0.65)）
- `success` - 成功（#52C41A）
- `warning` - 警告（#FA8C16）
- `danger` - 危险（#F5222D）

### 1.4 圆角系统（Border Radius）

| 尺寸 | 数值 | 使用场景 |
|-----|------|---------|
| 小（Small） | 2px | 小元素、标签 |
| 基础（Base） | 6px | 按钮、输入框、卡片（默认） |
| 大（Large） | 8px | 大卡片、模态框 |

**特殊圆角**：
- **圆形**: `50%` - 头像、徽章
- **完全圆角**: `9999px` - 胶囊按钮

### 1.5 阴影系统（Shadow System）

Ant Design 使用多层阴影系统：

| 级别 | 阴影值 | 使用场景 |
|-----|--------|---------|
| 基础阴影 | `0 2px 8px rgba(0, 0, 0, 0.15)` | 卡片、下拉菜单 |
| 中等阴影 | `0 4px 12px rgba(0, 0, 0, 0.15)` | 模态框、弹出层 |
| 大阴影 | `0 8px 24px rgba(0, 0, 0, 0.12)` | 大型模态框 |

**Card 组件阴影**：
- 默认：`0 1px 2px rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px rgba(0, 0, 0, 0.02)`
- 悬停：提升阴影效果

### 1.6 布局系统（Layout System）

#### 1.6.1 24栅格系统（24-Grid System）

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

**布局示例**：
```jsx
// 三等分布局
<Row gutter={16}>
  <Col span={8}>Column 1</Col>
  <Col span={8}>Column 2</Col>
  <Col span={8}>Column 3</Col>
</Row>

// 响应式布局
<Row gutter={[16, 16]}>
  <Col xs={24} sm={12} md={8} lg={6}>Column</Col>
</Row>
```

#### 1.6.2 Flex 布局（Flex Layout）

Ant Design 5.x 引入 `Flex` 组件，基于 CSS Flexbox：

**Flex 组件属性**：
- `gap`: 间距（`small`, `middle`, `large` 或数字）
- `vertical`: 垂直方向（默认 `false`）
- `wrap`: 是否换行
- `justify`: 主轴对齐（`start`, `end`, `center`, `space-between`, `space-around`, `space-evenly`）
- `align`: 交叉轴对齐（`start`, `end`, `center`, `stretch`, `baseline`）

### 1.7 卡片组件（Card Component）

#### 1.7.1 卡片尺寸（Card Sizes）

- **标准尺寸（Default）**: 
  - 内边距：`bodyPadding: 24px`, `headerPadding: 16px`
  - 标题字号：16pt
  - 内容字号：14pt

- **小尺寸（Small）**: 
  - 内边距：`bodyPaddingSM: 12px`, `headerPaddingSM: 12px`
  - 标题字号：14pt
  - 内容字号：14pt

#### 1.7.2 卡片样式（Card Styles）

**边框**：
- 默认：`border: 1px solid #D9D9D9`
- 无边框：`bordered={false}` 或 `variant="borderless"`

**圆角**：
- 默认：`borderRadius: 6px`
- 封面图片圆角：与卡片圆角一致

**阴影**：
- 默认：轻微阴影
- 悬停：`hoverable={true}` 时提升阴影

**背景**：
- 默认：`#FFFFFF`
- 可自定义：`style={{ background: '#F0F2F5' }}`

#### 1.7.3 卡片布局（Card Layout）

**Card.Grid** - 网格布局：
```jsx
<Card>
  <Card.Grid style={{ width: '25%', textAlign: 'center' }}>
    Content
  </Card.Grid>
</Card>
```

**Card.Meta** - 元数据布局：
- 包含 `avatar`, `title`, `description`

### 1.8 设计令牌（Design Tokens）

Ant Design 5.x 使用 Design Tokens 系统，支持主题定制：

#### 1.8.1 全局令牌（Global Tokens）

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

**字号令牌**：
```css
--font-size-sm: 12px;
--font-size-base: 14px;
--font-size-lg: 16px;
--font-size-xl: 20px;
--font-size-xxl: 24px;
```

#### 1.8.2 组件令牌（Component Tokens）

每个组件都有特定的设计令牌，例如：

**Card 组件令牌**：
```css
--card-body-padding: 24px;
--card-header-padding: 16px;
--card-body-padding-sm: 12px;
--card-header-padding-sm: 12px;
--card-border-radius: 6px;
```

**Button 组件令牌**：
```css
--button-padding-inline: 15px;
--button-padding-block: 4px;
--button-icon-gap: 8px;
--button-border-radius: 6px;
```

---

## 2. AntV 图表设计规范

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

#### 2.1.5 图表元素样式

**柱状图/条形图背景**：
```typescript
{
  columnBackground: {
    style: {
      fill: '#000',
      fillOpacity: 0.25
    }
  }
}
```

**折线图样式**：
- 线条宽度：2px（默认）
- 点大小：4px（默认）
- 平滑曲线：`smooth: true`

**面积图样式**：
- 填充透明度：0.25 - 0.5
- 渐变填充：支持线性渐变

### 2.2 G2 设计规范

#### 2.2.1 图形语法（Grammar of Graphics）

G2 基于图形语法理论，支持声明式图表定义。

#### 2.2.2 标记（Marks）

- `point` - 点
- `line` - 线
- `area` - 面积
- `interval` - 区间（柱状图、条形图）
- `polygon` - 多边形
- `text` - 文本
- `cell` - 单元格
- `image` - 图片
- `path` - 路径
- `link` - 连接
- `box` - 箱线图
- `vector` - 向量
- `shape` - 自定义形状

#### 2.2.3 视觉通道（Visual Channels）

- `x`, `y` - 位置
- `color` - 颜色
- `size` - 大小
- `shape` - 形状
- `opacity` - 透明度
- `stroke` - 描边

---

## 3. PPT 尺寸规范

### 3.1 标准尺寸

**所有PPT统一为16:9横版**：
- **宽度**: 33.867cm (13.33英寸)
- **高度**: 19.05cm (7.5英寸)
- **宽高比**: 1.78 (16:9)
- **像素尺寸** (96 DPI): 1920px × 1080px

### 3.2 24栅格系统在PPT中的应用

将PPT画布分为24列，每列宽度：
- **每列宽度**: 33.867cm ÷ 24 = 1.411cm
- **每列像素**: 1920px ÷ 24 = 80px

---

## 4. 设计原则

### 4.1 一致性（Consistency）

- 使用统一的设计令牌
- 保持组件样式一致
- 遵循既定的设计模式

### 4.2 层次感（Hierarchy）

- 通过字号、字重、颜色建立视觉层次
- 使用间距和留白区分内容区块
- 使用阴影和边框增强层次感

### 4.3 留白（Whitespace）

- 充足的留白提升可读性
- 使用8px基础单位的倍数作为间距
- 避免内容过于拥挤

### 4.4 对齐（Alignment）

- 文本左对齐为主（中文阅读习惯）
- 标题和强调内容可居中
- 使用网格系统确保对齐

### 4.5 对比（Contrast）

- 确保文本与背景有足够的对比度
- 使用颜色对比突出重要信息
- 通过字号对比建立层次

---

## 5. 使用示例

### 5.1 在代码中使用 Ant Design 主题

```python
from ant_design_theme import ant_design_theme

# 获取颜色
primary_color = ant_design_theme.colors.colorPrimary  # #1677FF
text_color = ant_design_theme.colors.colorText  # rgba(0,0,0,0.85)

# 获取间距（转换为cm）
padding_cm = ant_design_theme.get_spacing_cm('lg')  # 24px = 0.63cm

# 获取字号（转换为pt）
title_size_pt = ant_design_theme.get_font_size_pt('h1')  # 38pt
```

### 5.2 在图表中使用 AntV 配色

```python
from antv_chart_theme import antv_chart_theme

# 获取分类色
colors = antv_chart_theme.get_bar_chart_colors(5)  # 返回5个AntV配色
```

### 5.3 布局规划参考

**三个卡片并排布局**：
- 每个卡片宽度：占页面宽度的 30%（或 7.2 栅格）
- 卡片间距：24px
- 卡片内边距：16px 或 24px
- 距离页面上边距：80px
- 以中间卡片为中心，左右各一个卡片，间距均匀

**两个元素左右分屏**：
- 左侧：60% 宽度（14.4 栅格）
- 右侧：40% 宽度（9.6 栅格）
- 中间间距：24px 或 32px

**四个元素2×2网格**：
- 每个元素：占页面宽度的 48%（11.52 栅格）
- 水平间距：16px
- 垂直间距：24px

---

## 6. 验证

运行测试脚本验证设计规范应用：

```bash
python test_deck.py
```

生成的PPT和图表都会自动应用 Ant Design 和 AntV 设计规范。

---

## 7. 参考资料

- [Ant Design 官方文档](https://ant.design)
- [AntV G2Plot 文档](https://g2plot.antv.antgroup.com)
- [AntV G2 文档](https://g2.antv.antgroup.com)
- [Ant Design 设计令牌](https://ant.design/docs/react/customize-theme)
