# HTML生成修复计划

## 问题分析

### 1. 坐标系问题
- **当前问题**：使用CSS Grid布局，但没有固定的坐标系系统
- **需要**：建立固定坐标系，以16:9画布左下角为原点（x向右，y向上）
- **解决方案**：
  - 使用绝对定位（position: absolute）
  - 建立坐标系转换函数：grid坐标 → 像素坐标
  - 左下角为原点(0,0)，x向右为正，y向上为正

### 2. 24栅格系统固定
- **当前问题**：栅格系统没有固定在画布中
- **需要**：确保24栅格系统固定在16:9画布中
- **解决方案**：
  - 计算每个栅格单元的精确尺寸
  - 使用绝对定位，基于栅格坐标计算像素位置
  - 考虑padding，确保内容区域正确

### 3. 文字方向问题
- **当前问题**：文字垂直排列（从图片看）
- **需要**：文字水平排列
- **解决方案**：
  - 检查CSS的writing-mode属性
  - 确保flex-direction为row（水平）
  - 检查文本容器的display属性

### 4. HTML文件合并
- **当前问题**：每个幻灯片一个HTML文件（24个文件）
- **需要**：合并成一个HTML文件
- **解决方案**：
  - 创建一个包含所有幻灯片的HTML文件
  - 使用分页或滚动方式展示
  - 添加导航功能（可选）

## 实施步骤

### 步骤1：建立坐标系系统
1. 定义坐标系常量
   - 画布尺寸：1920px × 1080px
   - 内容区域：1872px × 1032px（减去padding 24px）
   - 栅格系统：24列 × 13.5行
   - 栅格单元尺寸：78px × 76.4px

2. 创建坐标转换函数
   ```python
   def grid_to_pixel(grid_x, grid_y, span_x, span_y):
       """
       将栅格坐标转换为像素坐标（左下角为原点）
       
       Args:
           grid_x: 栅格列位置（0-23）
           grid_y: 栅格行位置（0-12.5）
           span_x: 占据的列数
           span_y: 占据的行数
       
       Returns:
           (left, bottom, width, height) 像素值
       """
       cell_width = 1872 / 24  # 78px
       cell_height = 1032 / 13.5  # 76.4px
       
       # 左下角为原点
       left = 24 + grid_x * cell_width  # padding + x偏移
       bottom = 24 + grid_y * cell_height  # padding + y偏移
       width = span_x * cell_width
       height = span_y * cell_height
       
       # 转换为CSS的top定位（CSS使用top-left原点）
       top = 1080 - bottom - height
       
       return (left, top, width, height)
   ```

### 步骤2：修改CSS生成
1. 将Grid布局改为绝对定位
2. 使用坐标转换函数计算元素位置
3. 确保文字水平排列

### 步骤3：合并HTML文件
1. 创建新的生成方法 `generate_merged_html()`
2. 将所有幻灯片内容合并到一个HTML文件中
3. 使用分页或滚动展示

## 代码修改位置

1. `html_generator.py`:
   - 添加坐标转换函数
   - 修改CSS生成逻辑
   - 添加合并HTML生成方法

2. `ppt_filler.py`:
   - 修改HTML保存逻辑，支持合并模式

