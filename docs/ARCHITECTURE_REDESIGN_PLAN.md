# 架构重构计划：从"计算坐标"到"浏览器渲染"

## 核心原则对齐

### 当前问题

**旧架构**：LLM/Python 计算坐标 → HTML 绝对定位 → 截图/复刻 → PPT

**问题**：
1. LLM 不擅长几何计算，容易出错
2. 无法完美支持 Ant Design 的 Flex/Grid 布局
3. 缺乏设计感和随机性
4. 坐标计算复杂且易错

### 新架构原则

**新架构**：LLM 写 CSS 布局（流式布局） → 浏览器渲染并计算坐标 → 提取坐标 → PPT

**核心原则**：
1. **LLM 负责"定性"（审美和结构）**：写 HTML/CSS，不管坐标
2. **浏览器负责"定量"（精确计算）**：利用浏览器渲染引擎计算坐标
3. **利用 Design Tokens**：使用 CSS 变量统一管理样式
4. **遵循设计原则**：克制、统一、层级

---

## 需要调整的板块

### 1. LayoutPlanner（布局规划器）

**当前逻辑**：生成详细的坐标描述（"位于页面顶部，距离上边距80px"）

**新原则**：生成 Ant Design 布局组件描述（"使用 Row 和 Col 组件，gutter={16}"）

**调整方向**：
- 输出 Ant Design 组件结构（Row, Col, Flex, Space）
- 描述布局意图（"三个卡片等分排列"），而不是具体坐标
- 使用 Design Tokens（间距、颜色、字号）

### 2. HTMLGenerator（HTML生成器）

**当前逻辑**：根据坐标描述计算绝对定位（`left: 288px; top: 80px;`）

**新原则**：生成流式布局 HTML（Flex/Grid），让浏览器计算位置

**调整方向**：
- 生成流式布局 HTML（不使用 `position: absolute`）
- 使用 Ant Design 的 Flex/Grid 组件
- 应用 Design Tokens（CSS 变量）

### 3. BrowserRenderer（浏览器渲染器）

**当前逻辑**：加载已生成的 HTML，截图并提取坐标

**新原则**：加载流式布局 HTML，让浏览器渲染，然后提取计算好的坐标

**调整方向**：
- 加载流式布局 HTML
- 等待浏览器完成渲染
- 使用 `getBoundingClientRect()` 提取所有元素的最终坐标
- 提取样式信息（颜色、字体、阴影等）

### 4. ElementAnalyzer（元素分析器）

**当前逻辑**：识别容器和文本元素，提取坐标

**新原则**：识别所有 `.ppt-element` 标记的元素，提取完整信息

**调整方向**：
- 识别带有 `data-ppt-element` 属性的元素
- 提取坐标、样式、内容
- 支持嵌套元素结构

### 5. PPTReplicator（PPT复刻器）

**当前逻辑**：使用提取的坐标直接插入 PPT

**新原则**：使用浏览器计算好的坐标插入 PPT（保持不变，但数据来源改变）

**调整方向**：
- 接收浏览器计算好的坐标
- 保持现有的插入逻辑
- 应用提取的样式信息

---

## 实施步骤

### 阶段1：调整 LayoutPlanner

**目标**：让 LLM 输出 Ant Design 布局组件描述，而不是坐标描述

**修改点**：
1. 修改 Prompt，要求输出 Ant Design 组件结构
2. 输出格式改为组件树（Row/Col/Flex）
3. 使用 Design Tokens 描述样式

### 阶段2：调整 HTMLGenerator

**目标**：生成流式布局 HTML，而不是绝对定位

**修改点**：
1. 生成 Flex/Grid 布局 HTML
2. 使用 Ant Design CSS 类名
3. 应用 Design Tokens（CSS 变量）
4. 为每个元素添加 `data-ppt-element` 属性

### 阶段3：增强 BrowserRenderer

**目标**：提取浏览器计算好的坐标和样式

**修改点**：
1. 加载流式布局 HTML
2. 等待渲染完成
3. 使用 JavaScript 提取所有 `.ppt-element` 的坐标和样式
4. 返回完整的元素信息

### 阶段4：保持 PPTReplicator

**目标**：使用浏览器计算好的坐标插入 PPT

**修改点**：
- 无需修改，只需确保接收的数据格式正确

---

## 核心原则总结

1. **LLM 负责审美，浏览器负责计算**
2. **使用 Design Tokens 统一管理样式**
3. **遵循 Ant Design 设计原则（克制、统一、层级）**
4. **利用浏览器渲染引擎，而不是 Python 计算**

---

## 预期效果

1. **更美观**：LLM 可以自由发挥，使用 Flex/Grid 等现代布局
2. **更准确**：浏览器计算的坐标比 Python 计算更准确
3. **更灵活**：支持复杂布局（Masonry、交错排列等）
4. **更统一**：完美支持 Ant Design 规范

