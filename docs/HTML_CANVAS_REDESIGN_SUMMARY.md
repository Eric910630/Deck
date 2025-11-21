# HTML画布重新设计总结

## 工作流程调整

按照用户要求，重新调整了HTML生成的工作顺序：

### 第一步：前端通过LLM生成AI文案内容
- 理解结果
- 润色方案
- 颜色布局方案
- 等等

### 第二步：将文案内容转换成HTML代码
- **先创建16:9白色画布**
- **建立坐标系（左下角为原点）**
- **绘制栅格标准尺（24列×13.5行）**
- **然后根据坐标放置元素**

## 实现细节

### 1. 画布创建 (`html_canvas_generator.py`)

#### 画布规格
- **尺寸**: 1920px × 1080px（横版16:9）
- **背景**: 白色
- **坐标系**: 左下角为原点 (0, 0)
- **X轴**: 向右为正（0 → 1920）
- **Y轴**: 向上为正（0 → 1080）

#### 栅格系统
- **列数**: 24列
- **行数**: 13.5行
- **栅格单元尺寸**: 80px × 80px
- **标准尺**: 在画布四周绘制，显示栅格编号

#### 坐标原点标记
- 左下角有一个红色圆形标记，显示"O"
- 表示坐标原点 (0, 0)

### 2. 元素坐标映射

#### 坐标系统
- **输入**: 使用左下角为原点的坐标系
  - `left`: 距离左边缘的像素
  - `bottom`: 距离下边缘的像素
  - `width`: 宽度（像素）
  - `height`: 高度（像素）

#### CSS转换
- **输出**: CSS使用top-left原点
  - `left`: 直接使用
  - `top`: 从底部距离转换为顶部距离
    ```python
    css_top = CANVAS_HEIGHT - bottom - height
    ```

### 3. 重复内容处理

在 `_generate_html_from_layout_plan` 方法中添加了去重逻辑：
```python
seen_ids = set()
for elem_pos in sorted_elements:
    elem_id = elem_pos.get('element_id', '')
    if elem_id in seen_ids:
        logger.warning(f"跳过重复元素 {elem_id}")
        continue
    seen_ids.add(elem_id)
```

### 4. 集成到主流程

`html_generator.py` 中的 `_generate_html_from_layout_plan` 方法：
1. 将布局规划转换为画布元素格式
2. 解析位置描述，转换为坐标
3. 使用 `HTMLCanvasGenerator` 生成HTML
4. 返回完整的HTML字符串

## 文件结构

### 新文件
- `html_canvas_generator.py`: 画布生成器
- `test_canvas_generator.py`: 测试脚本

### 修改文件
- `html_generator.py`: 集成画布生成器

## 测试验证

### 测试结果
- ✅ 画布尺寸正确：1920px × 1080px（横版16:9）
- ✅ 坐标系正确：左下角为原点
- ✅ 栅格标准尺正确显示
- ✅ 元素位置正确映射
- ✅ Playwright验证通过

### 测试文件
- `html_output/test_canvas.html`: 测试画布
- `html_output/test_canvas_screenshot.png`: 截图

## 下一步

1. ✅ 画布创建和坐标系建立
2. ✅ 栅格标准尺绘制
3. ⏳ 完善坐标解析（从布局规划描述中提取坐标）
4. ⏳ 修复重复内容问题（已添加去重逻辑，需要测试）
5. ⏳ 集成到完整测试流程

## 使用示例

```python
from html_canvas_generator import HTMLCanvasGenerator

generator = HTMLCanvasGenerator()

elements = [
    {
        'id': 'title-1',
        'type': 'title',
        'content': '技术产品概览与价值主张',
        'coordinates': {
            'left': 100,
            'bottom': 900,
            'width': 800,
            'height': 80
        }
    }
]

html = generator.create_canvas_html(
    elements=elements,
    show_grid=True
)
```

