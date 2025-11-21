# CSS-First 架构：真正的智能布局

## 核心原则

**用CSS描述意图，让浏览器计算坐标**

### 为什么这是正确的方向？

1. **CSS Flexbox/Grid 是为了"适应变化"而生的**
   - 2个卡片？自动变宽平分
   - 3个卡片？自动变窄
   - 字多了？卡片自动长高，Footer自动被挤下去（不会重叠！）

2. **Python 坐标计算是为了"固定死"而生的**
   - 需要写一堆 `if len(cards) == 2: width = 800; ...`
   - 维护成本高，扩展性差
   - 无法穷举所有美的可能性

## 工作流程

### 1. LLM 生成 HTML/CSS

**输入**：视觉元素列表 + 场景描述

**输出**：完整的 HTML/CSS 代码

```html
<div class="slide-container" style="display: flex; flex-direction: column; height: 100vh; padding: 40px;">
  <header style="margin-bottom: 60px; border-left: 12px solid var(--ant-color-primary); padding-left: 24px;">
    <h1 data-ppt-element="true" data-ppt-element-id="title_text_0" data-ppt-element-type="title">
      核心价值主张
    </h1>
  </header>
  <main style="flex: 1; display: flex; gap: 24px;">
    <div class="ant-card" data-ppt-element="true" data-ppt-element-id="value_card_0" data-ppt-element-type="card"
         style="flex: 1; ...">
      ...
    </div>
  </main>
</div>
```

### 2. 浏览器渲染

- 加载 HTML/CSS
- 浏览器自动计算所有元素的位置
- 完美支持 Flex/Grid 布局

### 3. Python 提取坐标

- 使用 `getBoundingClientRect()` 提取所有元素的坐标
- 识别带有 `data-ppt-element` 属性的元素

### 4. 混合渲染到 PPT

- 容器用图片（浏览器截图）
- 文本用原生（可编辑）

## 架构调整

### LayoutPlanner → CSSGenerator

**旧职责**：输出坐标描述（"位于页面顶部，距离上边距80px"）

**新职责**：输出完整的 HTML/CSS 代码

### HTMLGenerator

**旧职责**：根据坐标描述计算绝对定位

**新职责**：直接使用 LLM 生成的 HTML/CSS，添加必要的 Design Tokens

### BrowserRenderer

**职责**：渲染 HTML，提取坐标（保持不变）

## 优势

1. **真正的智能**：LLM 可以自由发挥，生成任意布局
2. **自动适应**：浏览器自动处理各种情况
3. **零维护**：不需要维护 Python 坐标计算逻辑
4. **无限扩展**：支持任何 CSS 布局（Masonry、交错排列等）

## 实现步骤

1. ✅ 修改 `LayoutPlanner` 的 Prompt，要求输出 HTML/CSS
2. ✅ 修改 `HTMLGenerator`，直接使用 LLM 生成的 HTML
3. ✅ 确保所有元素都有 `data-ppt-element` 属性
4. ✅ 浏览器渲染后提取坐标

