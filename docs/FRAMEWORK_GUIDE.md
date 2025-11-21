# PPT框架填充功能说明

## 什么是PPT框架填充？

PPT框架填充是指：**根据一个已有的PPT框架文档（包含布局和占位符），使用LLM自动生成内容并填充到占位符中，生成完整的PPT**。

### 工作流程

```
框架PPT文件 (包含占位符)
    ↓
解析框架结构 (提取占位符位置和类型)
    ↓
LLM生成内容 (根据用户提示和框架结构)
    ↓
填充内容到占位符
    ↓
生成完整PPT
```

## 使用场景

1. **已有PPT模板**：你有一个设计好的PPT模板，只需要填充内容
2. **保持统一风格**：需要生成多个PPT，但保持相同的布局和设计风格
3. **快速生成**：不想从头设计布局，只想快速生成内容

## 使用示例

### 方式1: 使用命令行

```bash
# 基本用法
python cli.py --framework framework_template.pptx \
              --fill-prompt "制作一个关于产品介绍的演示文稿" \
              --output-ppt output.pptx

# 自动生成输出文件名
python cli.py --framework framework_template.pptx \
              --fill-prompt "制作一个关于AI技术的演示文稿"
```

### 方式2: 使用Python代码

```python
from ppt_filler import PPTFiller
import asyncio

async def main():
    # 创建填充器
    filler = PPTFiller("framework_template.pptx")
    
    # 填充内容
    output_path = await filler.fill_from_prompt(
        prompt="制作一个关于产品介绍的演示文稿，包含产品特点、优势和应用场景",
        preserve_structure=True
    )
    
    print(f"PPT已生成: {output_path}")

asyncio.run(main())
```

## 框架PPT的要求

框架PPT应该包含**占位符（Placeholder）**，这些占位符会被LLM生成的内容替换。

### 占位符类型

- **标题占位符**：用于标题
- **内容占位符**：用于正文内容
- **自定义文本框**：也可以作为占位符使用

### 创建框架PPT

你可以：
1. 在PowerPoint中手动创建，添加占位符
2. 使用我们提供的脚本创建示例框架：
   ```bash
   python create_framework_ppt.py
   ```

## 实际演示

刚才的测试已经成功运行：

1. **创建了框架PPT**：`framework_template.pptx`
   - 包含3张幻灯片
   - 每张都有占位符

2. **填充了内容**：`framework_template-filled-20251119-162118.pptx`
   - LLM根据提示生成了产品介绍相关的内容
   - 内容已填充到所有占位符中

## 查看结果

打开生成的文件查看效果：

```bash
# 查看框架（填充前）
open framework_template.pptx

# 查看填充后的PPT（填充后）
open framework_template-filled-*.pptx
```

## 优势

✅ **保持设计**：框架的布局、颜色、字体等设计保持不变  
✅ **自动填充**：LLM自动理解框架结构并生成合适的内容  
✅ **批量生成**：可以用同一个框架生成多个不同主题的PPT  
✅ **专业布局**：框架可以由设计师预先设计好，确保专业外观

## 与LLM生成布局的区别

| 功能 | LLM生成布局 (`--generate`) | 框架填充 (`--framework`) |
|------|---------------------------|-------------------------|
| 布局来源 | LLM自动生成 | 使用现有框架 |
| 设计控制 | LLM决定 | 框架决定 |
| 适用场景 | 从零开始创建 | 已有模板需要填充 |
| 输出 | 全新的PPT | 基于框架的PPT |

## 注意事项

1. **框架文件**：框架PPT必须包含占位符，否则无法填充
2. **LLM配置**：需要配置LLM服务（`.env` 文件中的 `CHAT_MODEL_API_KEY`）
3. **内容质量**：LLM生成的内容质量取决于提示的详细程度
4. **占位符识别**：工具会自动识别所有占位符并填充

