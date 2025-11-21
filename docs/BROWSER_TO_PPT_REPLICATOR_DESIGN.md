# 浏览器到PPT复刻方案设计

## 🎯 方案概述

### 核心思路
1. **浏览器端**：使用无头浏览器渲染，完美实现Ant Design/AntV规范
2. **复刻工具**：分析浏览器渲染结果，一比一复刻到PPT
3. **坐标系映射**：建立24栅格系统，映射浏览器到PPT画布

---

## 📊 可行性分析

### ✅ 完全可行的部分

#### 1. 浏览器渲染
- ✅ 已有`web_chart_generator.py`基础
- ✅ Playwright可以渲染完整HTML页面
- ✅ 可以截图整个页面或特定元素
- ✅ 可以获取DOM元素的位置、尺寸、样式

#### 2. 元素识别和提取
- ✅ 可以通过CSS选择器识别容器（div、section、Card等）
- ✅ 可以识别文本元素（p、h1-h6、span等）
- ✅ 可以获取元素的：
  - 位置（left, top）
  - 尺寸（width, height）
  - 样式（背景色、边框、圆角、阴影等）
  - 文本内容、字体、大小、颜色

#### 3. 坐标映射
- ✅ 浏览器端：1920px × 1080px (16:9)
- ✅ PPT端：33.867cm × 19.05cm (16:9)
- ✅ 比例关系：1px ≈ 0.0176cm
- ✅ 24栅格系统可以映射：
  - 浏览器：每格 = 1920px / 24 = 80px
  - PPT：每格 = 33.867cm / 24 ≈ 1.41cm

#### 4. 容器截图和插入
- ✅ Playwright可以截图特定元素
- ✅ python-pptx可以插入图片到指定位置
- ✅ 可以保持原始尺寸和位置

#### 5. 文本提取和复现
- ✅ 可以提取文本内容、字体、大小、颜色、对齐方式
- ✅ python-pptx可以设置文本样式
- ✅ 可以精确定位文本位置

---

## 🏗️ 架构设计

### 模块结构

```
browser_to_ppt_replicator/
├── __init__.py
├── browser_renderer.py      # 浏览器渲染器
├── element_analyzer.py      # 元素分析器
├── coordinate_mapper.py     # 坐标映射器（24栅格）
├── container_extractor.py  # 容器提取器（截图）
├── text_extractor.py        # 文本提取器
└── ppt_replicator.py        # PPT复刻器
```

### 工作流程

```
1. 浏览器渲染HTML（Ant Design组件）
   ↓
2. 分析DOM结构
   ├── 识别容器元素（Card、div等）
   └── 识别文本元素（Typography等）
   ↓
3. 建立24栅格坐标系
   ├── 浏览器端：1920px / 24 = 80px/格
   └── PPT端：33.867cm / 24 ≈ 1.41cm/格
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

## 💻 实现细节

### 1. 浏览器渲染器 (`browser_renderer.py`)

```python
class BrowserRenderer:
    """浏览器渲染器 - 渲染Ant Design组件"""
    
    async def render_html(self, html_content: str) -> Page:
        """渲染HTML内容"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                viewport={'width': 1920, 'height': 1080}  # 16:9
            )
            await page.set_content(html_content)
            await page.wait_for_load_state('networkidle')
            return page
```

### 2. 元素分析器 (`element_analyzer.py`)

```python
class ElementAnalyzer:
    """元素分析器 - 识别容器和文本"""
    
    async def analyze_elements(self, page: Page) -> Dict:
        """分析页面元素"""
        # 识别容器元素
        containers = await page.query_selector_all(
            '.ant-card, .container, [class*="card"], section, div[class*="box"]'
        )
        
        # 识别文本元素
        texts = await page.query_selector_all(
            'h1, h2, h3, h4, h5, h6, p, span, .ant-typography'
        )
        
        return {
            'containers': await self._extract_container_info(containers),
            'texts': await self._extract_text_info(texts)
        }
    
    async def _extract_container_info(self, elements):
        """提取容器信息"""
        containers = []
        for elem in elements:
            box = await elem.bounding_box()
            style = await elem.evaluate("""
                el => ({
                    backgroundColor: window.getComputedStyle(el).backgroundColor,
                    borderRadius: window.getComputedStyle(el).borderRadius,
                    border: window.getComputedStyle(el).border,
                    boxShadow: window.getComputedStyle(el).boxShadow
                })
            """)
            
            containers.append({
                'element': elem,
                'position': {'x': box['x'], 'y': box['y']},
                'size': {'width': box['width'], 'height': box['height']},
                'style': style,
                'grid_position': self._calculate_grid_position(box)
            })
        return containers
```

### 3. 坐标映射器 (`coordinate_mapper.py`)

```python
class CoordinateMapper:
    """坐标映射器 - 24栅格系统"""
    
    # 浏览器端：1920px × 1080px
    BROWSER_WIDTH = 1920
    BROWSER_HEIGHT = 1080
    GRID_COLUMNS = 24
    GRID_ROWS = 24 * (1080 / 1920)  # 保持16:9比例
    
    # PPT端：33.867cm × 19.05cm
    PPT_WIDTH_CM = 33.867
    PPT_HEIGHT_CM = 19.05
    
    def browser_to_ppt(self, browser_x: float, browser_y: float) -> Tuple[float, float]:
        """浏览器坐标转PPT坐标（cm）"""
        ppt_x = (browser_x / self.BROWSER_WIDTH) * self.PPT_WIDTH_CM
        ppt_y = (browser_y / self.BROWSER_HEIGHT) * self.PPT_HEIGHT_CM
        return ppt_x, ppt_y
    
    def browser_to_grid(self, browser_x: float, browser_y: float) -> Tuple[int, int]:
        """浏览器坐标转栅格坐标"""
        grid_x = int(browser_x / (self.BROWSER_WIDTH / self.GRID_COLUMNS))
        grid_y = int(browser_y / (self.BROWSER_HEIGHT / self.GRID_ROWS))
        return grid_x, grid_y
    
    def grid_to_ppt(self, grid_x: int, grid_y: int, grid_width: int, grid_height: int) -> Dict:
        """栅格坐标转PPT位置和尺寸"""
        cell_width_cm = self.PPT_WIDTH_CM / self.GRID_COLUMNS
        cell_height_cm = self.PPT_HEIGHT_CM / self.GRID_ROWS
        
        return {
            'left': grid_x * cell_width_cm,
            'top': grid_y * cell_height_cm,
            'width': grid_width * cell_width_cm,
            'height': grid_height * cell_height_cm
        }
```

### 4. 容器提取器 (`container_extractor.py`)

```python
class ContainerExtractor:
    """容器提取器 - 截图容器元素"""
    
    async def extract_container(self, page: Page, element, output_path: Path) -> str:
        """截图容器元素"""
        # 截图特定元素
        screenshot = await element.screenshot(path=str(output_path))
        
        # 获取元素信息
        box = await element.bounding_box()
        
        return {
            'image_path': str(output_path),
            'position': {'x': box['x'], 'y': box['y']},
            'size': {'width': box['width'], 'height': box['height']}
        }
```

### 5. 文本提取器 (`text_extractor.py`)

```python
class TextExtractor:
    """文本提取器 - 提取文本信息"""
    
    async def extract_text(self, element) -> Dict:
        """提取文本元素信息"""
        # 获取文本内容
        text = await element.inner_text()
        
        # 获取样式
        style = await element.evaluate("""
            el => ({
                fontSize: window.getComputedStyle(el).fontSize,
                fontFamily: window.getComputedStyle(el).fontFamily,
                fontWeight: window.getComputedStyle(el).fontWeight,
                color: window.getComputedStyle(el).color,
                textAlign: window.getComputedStyle(el).textAlign,
                lineHeight: window.getComputedStyle(el).lineHeight
            })
        """)
        
        # 获取位置
        box = await element.bounding_box()
        
        return {
            'text': text,
            'style': style,
            'position': {'x': box['x'], 'y': box['y']},
            'size': {'width': box['width'], 'height': box['height']}
        }
```

### 6. PPT复刻器 (`ppt_replicator.py`)

```python
class PPTReplicator:
    """PPT复刻器 - 将浏览器渲染结果复刻到PPT"""
    
    def __init__(self, coordinate_mapper: CoordinateMapper):
        self.mapper = coordinate_mapper
        self.prs = Presentation()
        self.prs.slide_width = Cm(33.867)
        self.prs.slide_height = Cm(19.05)
    
    def replicate_slide(
        self,
        containers: List[Dict],
        texts: List[Dict]
    ) -> Slide:
        """复刻一张幻灯片"""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])  # 空白布局
        
        # 1. 插入容器图片
        for container in containers:
            self._insert_container_image(slide, container)
        
        # 2. 插入文本
        for text in texts:
            self._insert_text(slide, text)
        
        return slide
    
    def _insert_container_image(self, slide: Slide, container: Dict):
        """插入容器图片"""
        # 转换坐标
        ppt_x, ppt_y = self.mapper.browser_to_ppt(
            container['position']['x'],
            container['position']['y']
        )
        ppt_width, ppt_height = self.mapper.browser_to_ppt(
            container['size']['width'],
            container['size']['height']
        )
        
        # 插入图片
        slide.shapes.add_picture(
            container['image_path'],
            Cm(ppt_x),
            Cm(ppt_y),
            Cm(ppt_width),
            Cm(ppt_height)
        )
    
    def _insert_text(self, slide: Slide, text: Dict):
        """插入文本"""
        # 转换坐标
        ppt_x, ppt_y = self.mapper.browser_to_ppt(
            text['position']['x'],
            text['position']['y']
        )
        ppt_width, ppt_height = self.mapper.browser_to_ppt(
            text['size']['width'],
            text['size']['height']
        )
        
        # 创建文本框
        textbox = slide.shapes.add_textbox(
            Cm(ppt_x),
            Cm(ppt_y),
            Cm(ppt_width),
            Cm(ppt_height)
        )
        
        # 设置文本和样式
        text_frame = textbox.text_frame
        text_frame.text = text['text']
        
        # 应用样式
        para = text_frame.paragraphs[0]
        run = para.runs[0]
        run.font.name = text['style']['fontFamily']
        run.font.size = Pt(self._px_to_pt(text['style']['fontSize']))
        run.font.color.rgb = self._hex_to_rgb(text['style']['color'])
        run.font.bold = text['style']['fontWeight'] in ['bold', '600', '700']
```

---

## 🎯 24栅格坐标系实现

### 浏览器端栅格系统

```javascript
// HTML模板中嵌入24栅格系统
const GRID_COLUMNS = 24;
const GRID_ROWS = 13.5; // 1080 / 80 = 13.5 (保持16:9)

// 每个栅格单元
const CELL_WIDTH = 1920 / GRID_COLUMNS;  // 80px
const CELL_HEIGHT = 1080 / GRID_ROWS;     // 80px

// CSS Grid布局
.container {
  display: grid;
  grid-template-columns: repeat(24, 1fr);
  grid-template-rows: repeat(13.5, 1fr);
  gap: 8px;
  width: 1920px;
  height: 1080px;
}
```

### PPT端栅格映射

```python
class GridMapper:
    """24栅格映射器"""
    
    # 浏览器：1920px / 24 = 80px/格
    BROWSER_CELL_WIDTH = 80
    BROWSER_CELL_HEIGHT = 80
    
    # PPT：33.867cm / 24 ≈ 1.41cm/格
    PPT_CELL_WIDTH_CM = 33.867 / 24  # ≈ 1.41cm
    PPT_CELL_HEIGHT_CM = 19.05 / (24 * 9/16)  # ≈ 1.41cm
    
    def browser_grid_to_ppt(self, grid_x: int, grid_y: int, 
                            span_x: int, span_y: int) -> Dict:
        """栅格坐标转PPT位置"""
        return {
            'left': Cm(grid_x * self.PPT_CELL_WIDTH_CM),
            'top': Cm(grid_y * self.PPT_CELL_HEIGHT_CM),
            'width': Cm(span_x * self.PPT_CELL_WIDTH_CM),
            'height': Cm(span_y * self.PPT_CELL_HEIGHT_CM)
        }
```

---

## 🔍 潜在挑战和解决方案

### 挑战1：元素识别准确性

**问题**：如何准确识别哪些是容器，哪些是文本？

**解决方案**：
- 使用CSS选择器（`.ant-card`, `.ant-typography`等）
- 分析DOM结构（有背景色/边框的div = 容器）
- 使用LLM辅助识别（如果结构复杂）

### 挑战2：样式复现完整性

**问题**：某些CSS效果可能无法完全复现（阴影、渐变）

**解决方案**：
- 容器：直接截图（保留所有视觉效果）
- 文本：提取样式信息，在PPT中尽可能复现
- 复杂效果：优先使用截图

### 挑战3：布局复杂性

**问题**：复杂的嵌套布局可能需要递归处理

**解决方案**：
- 按层级处理（先外层容器，再内层元素）
- 使用z-index确定层级关系
- 对于复杂嵌套，可以整体截图

### 挑战4：性能优化

**问题**：大量元素可能需要优化

**解决方案**：
- 批量处理元素
- 缓存截图
- 异步处理

---

## 📝 实现步骤

### Phase 1: 基础框架
1. ✅ 创建`browser_to_ppt_replicator`模块
2. ✅ 实现浏览器渲染器
3. ✅ 实现坐标映射器（24栅格）

### Phase 2: 元素提取
4. ✅ 实现元素分析器
5. ✅ 实现容器提取器（截图）
6. ✅ 实现文本提取器

### Phase 3: PPT复刻
7. ✅ 实现PPT复刻器
8. ✅ 实现容器图片插入
9. ✅ 实现文本复现

### Phase 4: 优化和完善
10. ✅ 优化元素识别准确性
11. ✅ 处理复杂布局
12. ✅ 性能优化

---

## ✅ 方案可行性结论

**完全可行！** ✅

### 优势
1. ✅ **完美视觉呈现**：浏览器端完全符合Ant Design规范
2. ✅ **精确复刻**：一比一复刻到PPT
3. ✅ **标准化布局**：24栅格系统确保一致性
4. ✅ **灵活性**：可以处理复杂布局

### 技术可行性
- ✅ 所有技术点都有成熟方案
- ✅ 已有基础（`web_chart_generator.py`）
- ✅ 可以逐步实现和优化

### 建议
- 先实现基础版本（简单布局）
- 逐步优化（复杂布局、性能）
- 可以结合LLM辅助元素识别（如果需要）

