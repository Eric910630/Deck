# 架构原则对齐总结

## 核心原则

### 1. **LLM 负责"定性"（审美和结构）**
- **原则**：LLM 只负责写 HTML/CSS，不管坐标
- **实现**：
  - `LayoutPlanner` 输出 Ant Design 组件结构（Flex/Grid），而不是坐标描述
  - `FlowLayoutHTMLGenerator` 生成流式布局 HTML（不使用 `position: absolute`）
  - 使用 Design Tokens（CSS 变量）统一管理样式

### 2. **浏览器负责"定量"（精确计算）**
- **原则**：利用浏览器渲染引擎计算坐标，而不是 Python 计算
- **实现**：
  - `BrowserRenderer` 加载流式布局 HTML
  - `HybridRenderer` 使用 `getBoundingClientRect()` 提取浏览器计算好的坐标
  - `ElementAnalyzer` 识别所有标记的元素，提取完整信息

### 3. **混合渲染法（Hybrid Rendering）**
- **原则**：容器用图片（浏览器截图，保留完美样式），内容用原生文本（保证可编辑性）
- **实现**：
  - `ContainerExtractor` 支持隐藏文字后截图（`hide_text=True`）
  - `PPTReplicator` 支持混合渲染模式（`use_hybrid_rendering=True`）
  - 底层：容器图片（带阴影、圆角、渐变）
  - 顶层：可编辑文本（原生 TextFrame）

### 4. **利用 Design Tokens**
- **原则**：使用 CSS 变量统一管理样式，而不是硬编码
- **实现**：
  - `FlowLayoutHTMLGenerator` 生成包含 Design Tokens 的 CSS
  - 所有样式通过 CSS 变量引用（`--ant-color-primary`, `--ant-box-shadow` 等）

---

## 模块调整详情

### 1. LayoutPlanner（布局规划器）

**调整前**：
- 输出详细的坐标描述（"位于页面顶部，距离上边距80px"）
- 要求 LLM 计算具体位置

**调整后**：
- 输出 Ant Design 组件结构（"使用 Flex 垂直布局，标题在顶部，三个卡片在下方水平排列"）
- 描述布局意图和组件属性，而不是坐标
- 使用 Design Tokens 描述样式

**关键修改**：
- 修改 Prompt，要求输出组件树（Row/Col/Flex）
- 输出格式改为 `layout_type`, `layout_props`, `element_styles`
- 不再输出 `position_description` 和 `size_description`

---

### 2. HTMLGenerator → FlowLayoutHTMLGenerator（新增）

**新模块**：
- 生成流式布局 HTML（Flex/Grid），而不是绝对定位
- 使用 Ant Design CSS 类名
- 应用 Design Tokens（CSS 变量）
- 为每个元素添加 `data-ppt-element` 属性，便于浏览器提取坐标

**关键特性**：
- 不使用 `position: absolute`
- 使用 `display: flex` 和 `display: grid`
- 通过 `gap`, `justify-content`, `align-items` 控制布局

---

### 3. BrowserRenderer（浏览器渲染器）

**调整前**：
- 加载已生成的 HTML（绝对定位）
- 截图并提取坐标

**调整后**：
- 加载流式布局 HTML
- 等待浏览器完成渲染
- 使用 `getBoundingClientRect()` 提取所有元素的最终坐标
- 提取样式信息（颜色、字体、阴影等）

**关键修改**：
- 保持现有逻辑，但接收的 HTML 格式改变（流式布局）

---

### 4. HybridRenderer（新增）

**新模块**：
- 从浏览器页面提取布局数据
- 识别所有带有 `data-ppt-element` 属性的元素
- 为卡片元素截图（隐藏文字，保留样式）
- 返回元素信息和截图路径

**关键方法**：
- `extract_layout_data()`: 提取所有元素的坐标和样式
- `_screenshot_card_without_text()`: 隐藏文字后截图卡片

---

### 5. ContainerExtractor（容器提取器）

**调整前**：
- 直接截图容器元素（文字包含在图片中）

**调整后**：
- 支持 `hide_text` 参数
- `hide_text=True`: 隐藏文字后截图（用于混合渲染）
- `hide_text=False`: 直接截图（文字包含在图片中）

**关键修改**：
- `extract_container()` 方法增加 `hide_text` 参数
- 使用 JavaScript 临时隐藏文字，截图后恢复

---

### 6. PPTReplicator（PPT复刻器）

**调整前**：
- 只插入容器图片，文本已包含在图片中

**调整后**：
- 支持 `use_hybrid_rendering` 参数
- `use_hybrid_rendering=True`: 混合渲染（容器用图片，文本用原生）
- `use_hybrid_rendering=False`: 旧方法（只插入容器图片）

**关键修改**：
- `replicate_slide()` 方法增加 `use_hybrid_rendering` 参数
- 新增 `_insert_text_on_container()` 方法：在容器上方插入可编辑文本
- 新增 `_parse_color()`, `_px_to_pt()` 辅助方法：解析样式

---

### 7. BrowserToPPTReplicator（主入口）

**调整**：
- 调用 `ContainerExtractor.extract_all_containers()` 时传入 `hide_text=True`
- 调用 `PPTReplicator.replicate_slide()` 时传入 `use_hybrid_rendering=True`

---

## 工作流程对比

### 旧流程（计算坐标）
```
LLM → 计算坐标 → HTML（绝对定位）→ 浏览器渲染 → 截图 → PPT
```

### 新流程（浏览器渲染）
```
LLM → 生成流式布局 HTML → 浏览器渲染并计算坐标 → 提取坐标 → 混合渲染 → PPT
                                    ↓
                            （容器截图 + 文本提取）
```

---

## 预期效果

1. **更美观**：LLM 可以自由发挥，使用 Flex/Grid 等现代布局
2. **更准确**：浏览器计算的坐标比 Python 计算更准确
3. **更灵活**：支持复杂布局（Masonry、交错排列等）
4. **更统一**：完美支持 Ant Design 规范
5. **可编辑**：PPT 中的文字可以编辑（混合渲染法）

---

## 下一步

1. **测试新架构**：使用 `FlowLayoutHTMLGenerator` 生成流式布局 HTML
2. **验证混合渲染**：确认容器截图和文本插入正确
3. **优化样式解析**：完善 `_parse_color()` 等方法，支持更多 CSS 格式
4. **集成到主流程**：在 `ppt_filler.py` 中集成新架构

---

## 注意事项

1. **向后兼容**：保留旧方法（`use_hybrid_rendering=False`），确保现有代码仍可运行
2. **错误处理**：如果浏览器提取坐标失败，回退到旧方法
3. **性能优化**：浏览器渲染需要时间，考虑缓存机制

