# 坐标映射修复说明

## 问题描述

从生成的PPT截图来看，存在严重的布局问题：
- 文本是垂直排列的（从上到下，从右到左）
- 元素位置错乱
- 坐标系体系没有正确映射

## 根本原因

**坐标获取方式不正确**：
- 之前使用`offsetLeft/offsetTop`来获取元素位置
- 这对于CSS Grid布局不准确，因为Grid布局的元素位置不是通过offset计算的
- 导致获取的坐标不准确，映射到PPT时出现错位

## 修复方案

### 1. 修复元素分析器的坐标获取方式

**文件**: `browser_to_ppt_replicator/element_analyzer.py`

**修改内容**:
- 容器元素：使用`getBoundingClientRect()`获取相对于body的准确坐标
- 文本元素：使用`getBoundingClientRect()`获取相对于body的准确坐标
- 考虑`scrollX/Y`（虽然页面没有滚动，但为了准确性还是加上）

**代码示例**:
```javascript
const rect = el.getBoundingClientRect();
const bodyRect = document.body.getBoundingClientRect();
return {
    x: rect.left - bodyRect.left + window.scrollX,
    y: rect.top - bodyRect.top + window.scrollY,
    width: rect.width,
    height: rect.height
};
```

### 2. 增强坐标映射器的日志

**文件**: `browser_to_ppt_replicator/coordinate_mapper.py`

**修改内容**:
- 将debug日志改为info日志，以便更好地调试
- 添加了更详细的坐标映射信息，包括：
  - 浏览器坐标
  - 减去padding后的坐标
  - 内容区域坐标和尺寸
  - PPT坐标和尺寸
  - 比例计算

## 坐标映射流程

1. **元素分析器** (`element_analyzer.py`):
   - 使用`getBoundingClientRect()`获取元素相对于body的坐标
   - 返回`{x, y, width, height}`（相对于body）

2. **坐标映射器** (`coordinate_mapper.py`):
   - 接收浏览器坐标（相对于body）
   - 减去HTML padding（24px），得到相对于内容区域的坐标
   - 按比例映射到PPT内容区域（33.02cm × 18.20cm）
   - 返回PPT坐标（cm）

3. **PPT复刻器** (`ppt_replicator.py`):
   - 使用映射后的坐标插入元素到PPT
   - 使用`Cm(ppt_x)`和`Cm(ppt_y)`设置位置

## 预期效果

修复后，应该能够：
- ✅ 正确获取元素在浏览器中的位置
- ✅ 准确映射到PPT坐标
- ✅ 文本和容器元素正确对齐
- ✅ 不再出现垂直排列或错位问题

## 下一步

运行测试，验证修复效果：
```bash
python3 test_docx_to_ppt_full_flow.py
```

检查生成的PPT文件，确认：
1. 文本是否水平排列（不再垂直）
2. 元素位置是否正确对齐
3. 布局是否符合预期
