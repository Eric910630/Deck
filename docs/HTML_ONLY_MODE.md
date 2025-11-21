# HTML生成模式说明

## 修改概述

已修改代码，添加了 `skip_ppt_conversion` 参数，可以跳过HTML到PPT的转换流程，专注于生成优秀的HTML文件。

## 修改内容

### 1. `ppt_filler.py` 修改

#### 新增参数
- `fill_from_prompt()` 方法新增 `skip_ppt_conversion: bool = False` 参数
- `_fill_with_browser_rendering()` 方法新增 `skip_ppt_conversion: bool = False` 参数

#### 功能变更
- 当 `skip_ppt_conversion=True` 时：
  - 生成HTML后，跳过浏览器渲染步骤
  - 跳过元素分析和提取步骤
  - 跳过PPT复刻步骤
  - 跳过图表整合步骤
  - 直接返回HTML目录路径

- HTML文件保存位置：
  - 从 `html_debug` 改为 `html_output`（更明确的命名）
  - 文件命名：`slide_000.html`, `slide_001.html`, ...

### 2. `test_docx_to_ppt_full_flow.py` 修改

#### 测试配置
- 添加 `skip_ppt = True` 配置项
- 更新流程说明，标注可跳过的步骤
- 更新验证逻辑，支持验证HTML文件输出

## 使用方法

### 在代码中使用

```python
output_path = await filler.fill_from_prompt(
    prompt=user_prompt,
    output_path="output.pptx",  # 仅用于确定输出目录
    use_enhanced_analysis=True,
    skip_ppt_conversion=True  # 设置为True以跳过PPT转换
)

# output_path 将返回HTML目录路径，例如：
# "/path/to/html_output"
```

### 在测试文件中

测试文件已默认启用HTML生成模式：
```python
skip_ppt = True  # 设置为True以跳过HTML到PPT的转换，仅生成HTML文件
```

## 输出结果

### HTML文件位置
- 目录：`{output_path的父目录}/html_output/`
- 文件：`slide_000.html`, `slide_001.html`, ...

### 查看HTML
1. 直接在浏览器中打开HTML文件
2. 或使用本地服务器：
   ```bash
   cd html_output
   python3 -m http.server 8000
   # 然后在浏览器中访问 http://localhost:8000
   ```

## 优势

1. **快速迭代**：跳过耗时的浏览器渲染和PPT转换步骤
2. **专注HTML质量**：可以专注于优化HTML生成逻辑
3. **易于调试**：直接在浏览器中查看HTML效果
4. **节省资源**：不需要启动Playwright浏览器

## 恢复PPT转换

如果需要恢复PPT转换，只需将 `skip_ppt_conversion` 设置为 `False` 或删除该参数（默认为False）。

## 注意事项

- HTML文件使用Ant Design规范生成
- 包含24栅格系统布局
- 已应用颜色配置
- 基于布局规划和润色内容生成

