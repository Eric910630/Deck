# 探针实现总结

## 已添加的探针

### 探针0: 输入数据检查 (`html_generator.py`)
**位置**: `generate_from_layout_plan` 方法开始处

**功能**:
- 检查输入数据的数量
- 检查`slide_index`的分布范围
- 记录`layout_plans`、`polished_slides`、`color_configs`的数量

**输出示例**:
```
--- [HTMLGenerator]: 【探针0】generate_from_layout_plan输入数据检查
--- [HTMLGenerator]: layout_plans数量: 24
--- [HTMLGenerator]: polished_slides数量: 24
--- [HTMLGenerator]: color_configs数量: 24
--- [HTMLGenerator]: layout_plans的slide_index范围: 0 - 23
--- [HTMLGenerator]: polished_slides的slide_index范围: 0 - 23
```

### 探针1: polished_content_map构建 (`html_generator.py`)
**位置**: `generate_from_layout_plan` 方法中，构建`polished_content_map`时

**功能**:
- 记录每个幻灯片的视觉元素数量
- 检测`element_id`冲突（不同幻灯片使用相同的`element_id`）
- 检测缺失的`element_id`
- 统计`polished_content_map`的键数量

**输出示例**:
```
--- [HTMLGenerator]: 【探针1】构建polished_content_map
--- [HTMLGenerator]: polished_slides数量: 24
--- [HTMLGenerator]: 幻灯片0: 5个视觉元素
--- [HTMLGenerator]: ⚠️ element_id title_text_0 冲突！幻灯片0 -> 4
--- [HTMLGenerator]: polished_content_map键数量: 120
--- [HTMLGenerator]: ⚠️ 发现3个element_id冲突
```

### 探针2: slide_index匹配检查 (`html_generator.py`)
**位置**: `generate_from_layout_plan` 方法中，开始生成HTML前

**功能**:
- 检查`layout_plans`和`polished_slides`的`slide_index`分布
- 检测重复的`slide_index`
- 记录匹配情况

**输出示例**:
```
--- [HTMLGenerator]: 【探针2】开始生成HTML，检查slide_index匹配
--- [HTMLGenerator]: layout_plans数量: 24
--- [HTMLGenerator]: polished_slides数量: 24
--- [HTMLGenerator]: layout_plans的slide_index列表: [0, 1, 2, ..., 23]
--- [HTMLGenerator]: polished_slides的slide_index列表: [0, 1, 2, ..., 23]
--- [HTMLGenerator]: ⚠️ layout_plans中有重复的slide_index
--- [HTMLGenerator]:   重复的slide_index: [0, 1]
```

### 探针3: 元素处理详情 (`html_generator.py`)
**位置**: `_generate_html_from_layout_plan` 方法中，处理元素时

**功能**:
- 记录每个幻灯片的`element_positions`数量
- 检测缺失的`element_id`（在`polished_content_map`中不存在）
- 检测重复的`element_id`（在同一张幻灯片内）
- 检测重复的内容哈希
- 记录匹配成功的`element_id`

**输出示例**:
```
--- [HTMLGenerator]: 【探针3】处理幻灯片0的元素
--- [HTMLGenerator]: element_positions数量: 5
--- [HTMLGenerator]: polished_content_map键数量: 120
--- [HTMLGenerator]: ⚠️ element_id title_text_0 在polished_content_map中不存在！
--- [HTMLGenerator]: ✅ element_id value_card_0 匹配成功
--- [HTMLGenerator]:   来源幻灯片: 0
--- [HTMLGenerator]:   元素标题: 降本
--- [HTMLGenerator]: 【探针3总结】
--- [HTMLGenerator]:   处理前element_positions数量: 5
--- [HTMLGenerator]:   处理后canvas_elements数量: 4
--- [HTMLGenerator]:   缺失element_id数量: 1
--- [HTMLGenerator]:   重复element_id数量: 0
--- [HTMLGenerator]:   重复内容哈希数量: 0
```

### 探针4: slide_index调整 (`ppt_filler.py`)
**位置**: `_generate_content_by_sections` 方法中，合并板块数据前

**功能**:
- 记录每个板块的`slide_index`分布
- 将板块内的`slide_index`转换为全局索引
- 记录调整前后的索引映射
- 统计合并后的总数

**输出示例**:
```
--- [PPTFiller]: 【探针】板块1的slide_index分布:
--- [PPTFiller]:   polished_slides: [0, 1, 2, 3]
--- [PPTFiller]:   layout_plans: [0, 1, 2, 3]
--- [PPTFiller]: 【探针】板块1的全局起始索引: 0
--- [PPTFiller]:   调整polished_slide: 0 -> 0
--- [PPTFiller]:   调整polished_slide: 1 -> 1
--- [PPTFiller]:   调整layout_plan: 0 -> 0
--- [PPTFiller]:   调整layout_plan: 1 -> 1
--- [PPTFiller]: 【探针】合并后总数: polished_slides=4, layout_plans=4
```

## 关键修复

### 修复1: slide_index全局化
**问题**: 不同板块的`slide_index`会重复（都是0, 1, 2...）

**修复**: 在`ppt_filler.py`中，合并板块数据前，将板块内的`slide_index`转换为全局索引

**代码**:
```python
# 计算全局起始索引
global_start_index = len(all_polished_slides)

# 调整slide_index
for slide in polished_slides:
    old_index = slide.get('slide_index', 0)
    new_index = global_start_index + old_index
    slide['slide_index'] = new_index
```

## 调试建议

### 步骤1: 运行测试并查看探针日志
```bash
cd /Users/eric/Desktop/Deck
python tests/test_docx_to_ppt_full_flow.py
```

### 步骤2: 查看关键探针输出
重点关注：
1. **探针1**: `element_id`冲突情况
2. **探针2**: `slide_index`重复情况
3. **探针3**: `element_id`匹配失败情况

### 步骤3: 根据探针结果定位问题
- 如果发现`element_id`冲突 → 需要修改`element_id`生成逻辑，加入`slide_index`前缀
- 如果发现`slide_index`重复 → 检查`slide_index`调整逻辑是否正确
- 如果发现`element_id`匹配失败 → 检查`polished_content_map`构建逻辑

## 下一步

根据探针输出结果，可以：
1. 识别具体的问题点（哪些`element_id`冲突、哪些`slide_index`重复）
2. 量化问题规模（冲突数量、重复数量）
3. 定位问题根源（是生成阶段还是合并阶段）

