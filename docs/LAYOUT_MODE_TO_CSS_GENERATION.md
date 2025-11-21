# 从"布局模式"到"CSS生成"的架构升级

## 核心问题

**旧思路**：在 Python 代码中写死坐标规则（`if layout_mode == 'corporate_reporting': left = 60; ...`）

**问题**：
- 只是从"一种模板"变成了"多种模板"
- 无法穷举所有美的可能性
- 维护成本高，扩展性差

## 新思路

**让 LLM 生成 CSS，让浏览器计算坐标**

### 工作流程

1. **用户输入**："帮我生成一页述职汇报PPT，关于AI提效。"

2. **LLM 思考**：
   - 场景：述职 -> 风格：严肃、清晰、结构化
   - 布局策略：左对齐标题 + 三列数据卡片

3. **LLM 生成 HTML/CSS**：
   ```html
   <div class="slide-container flex flex-col p-12 h-screen bg-gray-50">
     <header class="mb-8 border-l-8 border-blue-600 pl-6">
       <h1 class="text-5xl font-bold text-gray-900">核心价值主张</h1>
     </header>
     <main class="flex-1 grid grid-cols-3 gap-8">
       <div class="bg-white p-8 shadow-lg rounded-xl border-t-4 border-blue-500">
         ...
       </div>
     </main>
     <footer class="mt-8 text-center text-gray-500">
       全链路AI赋能解决方案...
     </footer>
   </div>
   ```

4. **浏览器渲染**：完美呈现，自动计算所有坐标

5. **Python 提取**：使用 `getBoundingClientRect()` 提取所有元素的坐标

## 架构调整

### 1. LayoutPlanner → CSSGenerator

**旧职责**：输出坐标描述（"位于页面顶部，距离上边距80px"）

**新职责**：输出完整的 HTML/CSS 代码（Flex/Grid 布局）

### 2. HTMLGenerator

**旧职责**：根据坐标描述计算绝对定位

**新职责**：直接使用 LLM 生成的 HTML/CSS，添加 `data-ppt-element` 属性

### 3. BrowserRenderer

**职责**：渲染 HTML，提取坐标（保持不变）

## 优势

1. **真正的智能**：LLM 可以自由发挥，生成任意布局
2. **自动适应**：浏览器自动处理各种情况（2个卡片、3个卡片、字数变化）
3. **零维护**：不需要维护 Python 坐标计算逻辑
4. **无限扩展**：支持任何 CSS 布局（Masonry、交错排列等）

## 实现步骤

1. 修改 `LayoutPlanner` 的 Prompt，要求输出 HTML/CSS
2. 修改 `HTMLGenerator`，直接使用 LLM 生成的 HTML
3. 确保所有元素都有 `data-ppt-element` 属性
4. 浏览器渲染后提取坐标

