# Deck 快速开始指南

## 1. 安装依赖

```bash
cd ~/Desktop/Deck
pip install -r requirements.txt
```

## 2. 基本使用

### 生成PPT（不包含图表）

```bash
python cli.py example_input.json -n "我的演示文稿"
```

### 生成PPT（包含图表）

项目会自动使用matplotlib生成图表，**不需要**BeeWise项目或LLM服务：

```bash
python cli.py example_input.json -n "我的演示文稿"
```

确保JSON文件中包含 `chart_insights` 字段，工具会自动生成图表并插入到PPT中。

## 3. 自定义输入

编辑 `example_input.json` 或创建新的JSON文件：

```json
{
  "vml_plan": [
    {
      "vml_code": "<Slide padding=\"1.5cm\"><VStack><TextBox style=\"title\" ref=\"title\" /></VStack></Slide>"
    }
  ],
  "content_map": {
    "title": "你的标题"
  }
}
```

然后运行：

```bash
python cli.py your_input.json -n "项目名称"
```

## 4. 输出位置

生成的PPT文件默认保存在 `./ppt_outputs/` 目录中。

## 5. 更多选项

```bash
python cli.py example_input.json --help
```

查看所有可用选项。

