# Deck 测试指南

## 快速测试

运行完整测试套件：

```bash
python test_deck.py
```

## 测试内容

测试脚本会运行以下5个测试：

### 1. LLM生成布局测试
- **功能**: 使用LLM根据自然语言提示生成VML布局
- **要求**: 需要配置LLM服务（`.env` 文件中的 `CHAT_MODEL_API_KEY`）
- **输出**: `test_output_layout.json`

### 2. 从JSON生成PPT测试
- **功能**: 从JSON文件生成PPT（不依赖LLM）
- **输出**: `test_outputs/测试演示-*.pptx`

### 3. 图表生成测试
- **功能**: 使用matplotlib生成柱状图和饼图
- **输出**: 
  - `test_outputs/charts/bar_chart_月度销售数据.png`
  - `test_outputs/charts/pie_chart_产品占比分布.png`

### 4. 生成包含图表的PPT测试
- **功能**: 生成包含自动生成图表的PPT
- **输出**: `test_outputs/测试图表PPT-*.pptx`

### 5. PPT框架填充测试
- **功能**: 根据框架PPT文件填充内容
- **要求**: 需要在项目目录中放置一个 `.pptx` 文件作为框架
- **要求**: 需要配置LLM服务

## 测试结果示例

```
============================================================
测试总结
============================================================

通过: 3/5

详细结果:
  layout: ✗ 跳过/失败 (需要LLM配置)
  ppt_from_json: ✓ 通过
  charts: ✓ 通过
  ppt_with_charts: ✓ 通过
  framework: ✗ 跳过/失败 (需要框架文件)
```

## 单独测试各个功能

### 测试1: 从JSON生成PPT（不需要LLM）

```bash
python cli.py example_input.json -n "测试演示" -o test_outputs
```

### 测试2: 生成图表

```python
from chart_generator import ChartGenerator

generator = ChartGenerator()
data = [
    {"月份": "1月", "销售额": 1000},
    {"月份": "2月", "销售额": 1500}
]
chart_path = generator.generate_bar_chart(data, "月份", "销售额", "销售数据")
print(f"图表已生成: {chart_path}")
```

### 测试3: 使用LLM生成布局（需要配置LLM）

```bash
# 先配置 .env 文件
python cli.py --generate "制作一个关于AI技术的演示文稿" -n "AI介绍" --num-slides 3
```

### 测试4: 根据框架生成PPT（需要框架文件和LLM）

```bash
# 准备一个框架PPT文件 template.pptx
python cli.py --framework template.pptx --fill-prompt "制作一个产品介绍PPT" --output-ppt output.pptx
```

## 配置LLM服务（用于测试1和4）

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的API密钥：
```env
CHAT_MODEL_API_KEY="your-api-key"
CHAT_MODEL_NAME="deepseek-chat"
CHAT_MODEL_BASE_URL="https://api.deepseek.com/v1"
```

3. 重新运行测试：
```bash
python test_deck.py
```

## 生成的文件位置

- **PPT文件**: `./test_outputs/*.pptx`
- **图表文件**: `./test_outputs/charts/*.png`
- **布局JSON**: `test_output_layout.json`

## 验证输出

1. **检查PPT文件**: 打开生成的 `.pptx` 文件，验证内容是否正确
2. **检查图表**: 查看 `test_outputs/charts/` 目录中的图表文件
3. **检查日志**: 查看测试输出中的日志信息

## 常见问题

### Q: LLM测试失败
**A**: 需要配置 `.env` 文件中的 `CHAT_MODEL_API_KEY`

### Q: 框架填充测试跳过
**A**: 需要在项目目录中放置一个 `.pptx` 文件作为框架

### Q: 图表没有显示在PPT中
**A**: 检查 `chart_insights` 中的 `insightId` 是否与 `content_map` 中的引用一致

### Q: 依赖安装失败
**A**: 运行 `pip install -r requirements.txt` 安装所有依赖

