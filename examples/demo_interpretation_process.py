#!/usr/bin/env python3
"""
Demo文档解读过程演示脚本
展示完整的解读流程和产出物
"""

import json
import asyncio
from pathlib import Path
from ppt_parser import PPTParser
from ppt_filler import PPTFiller
from loguru import logger

# 配置日志输出到文件
logger.add("demo_interpretation.log", rotation="10 MB", level="DEBUG")

async def demonstrate_interpretation_process():
    """演示完整的解读过程"""
    
    framework_file = "demo_filled.pptx"
    
    print("="*80)
    print("Demo文档解读过程完整演示")
    print("="*80)
    print(f"\n输入文件: {framework_file}\n")
    
    # ========== 阶段1: 初始化解析器 ==========
    print("\n" + "="*80)
    print("阶段1: 初始化PPT解析器")
    print("="*80)
    
    parser = PPTParser(framework_file)
    print(f"✅ PPT解析器已初始化")
    print(f"   文件路径: {parser.ppt_path}")
    print(f"   文件大小: {parser.ppt_path.stat().st_size:,} bytes")
    
    # ========== 阶段2: 提取结构信息 ==========
    print("\n" + "="*80)
    print("阶段2: 提取PPT结构信息")
    print("="*80)
    
    structure = parser.extract_structure()
    
    print(f"\n【产出物2.1】PPT基本信息:")
    print(json.dumps({
        "slide_count": structure["slide_count"],
        "dimensions": {
            "width_cm": round(structure["slide_width"], 2),
            "height_cm": round(structure["slide_height"], 2),
            "ratio": round(structure["slide_width"] / structure["slide_height"], 2),
            "is_16_9": abs(structure["slide_width"] / structure["slide_height"] - 16/9) < 0.1,
            "is_4_3": abs(structure["slide_width"] / structure["slide_height"] - 4/3) < 0.1
        }
    }, indent=2, ensure_ascii=False))
    
    print(f"\n【产出物2.2】每张幻灯片的详细结构:")
    for slide_info in structure["slides"]:
        print(f"\n幻灯片 {slide_info['slide_index'] + 1}:")
        print(f"  布局名称: {slide_info['layout_name']}")
        print(f"  形状总数: {len(slide_info['shapes'])}")
        print(f"  占位符数量: {len(slide_info['placeholders'])}")
        print(f"  文本内容数量: {len(slide_info['text_content'])}")
        
        if slide_info['placeholders']:
            print(f"  占位符详情:")
            for p in slide_info['placeholders']:
                print(f"    - ID: {p.get('placeholder_id')}, 类型: {p.get('placeholder_type')}")
                print(f"      位置: ({p.get('left', 0):.2f}cm, {p.get('top', 0):.2f}cm)")
                print(f"      尺寸: {p.get('width', 0):.2f}cm x {p.get('height', 0):.2f}cm")
                print(f"      有文本: {p.get('has_text', False)}")
                if p.get('text'):
                    text_preview = p['text'][:50] + "..." if len(p['text']) > 50 else p['text']
                    print(f"      文本预览: {text_preview}")
    
    # ========== 阶段3: 提取文本摘要 ==========
    print("\n" + "="*80)
    print("阶段3: 提取文本摘要（用于LLM理解）")
    print("="*80)
    
    text_summary = parser.extract_text_summary()
    
    print(f"\n【产出物3】文本摘要:")
    print(text_summary)
    
    # ========== 阶段4: 获取占位符映射 ==========
    print("\n" + "="*80)
    print("阶段4: 获取占位符映射")
    print("="*80)
    
    placeholder_mapping = parser.get_placeholder_mapping()
    
    print(f"\n【产出物4】占位符映射:")
    print(json.dumps(placeholder_mapping, indent=2, ensure_ascii=False))
    
    # ========== 阶段5: LLM生成内容 ==========
    print("\n" + "="*80)
    print("阶段5: 使用LLM生成内容")
    print("="*80)
    
    test_prompt = "制作一个关于人工智能技术的演示文稿，包含技术介绍、应用场景和未来展望"
    print(f"\n用户提示词: {test_prompt}")
    
    filler = PPTFiller(framework_file)
    
    print("\n【产出物5.1】发送给LLM的系统提示词:")
    system_prompt = """你是一个专业的PPT内容创作助手。你的任务是根据用户需求和PPT框架结构，为每张幻灯片的占位符生成合适的内容。

要求：
1. 理解PPT框架的结构和现有内容（如果有）
2. 根据用户需求生成专业、相关的内容
3. 为每个占位符生成合适的内容
4. 保持内容的逻辑连贯性和专业性
5. 标题要简洁有力，正文要详细但不过长

输出格式（JSON）：
{
  "slide_0_placeholder_0": "标题内容",
  "slide_0_placeholder_1": "正文内容",
  "slide_1_placeholder_0": "标题内容",
  ...
}

占位符标识格式：slide_{幻灯片索引}_placeholder_{占位符ID}"""
    print(system_prompt)
    
    print(f"\n【产出物5.2】发送给LLM的用户提示词:")
    user_prompt = f"""PPT框架信息：
{text_summary}

用户需求：{test_prompt}

请为每张幻灯片的占位符生成合适的内容。如果占位符已有内容，可以基于现有内容进行扩展或优化。"""
    print(user_prompt)
    
    print("\n正在调用LLM生成内容...")
    content_map = await filler._generate_content_for_framework(
        prompt=test_prompt,
        structure=structure,
        text_summary=text_summary,
        placeholder_mapping=placeholder_mapping
    )
    
    print(f"\n【产出物5.3】LLM生成的内容映射:")
    print(json.dumps(content_map, indent=2, ensure_ascii=False))
    
    # ========== 阶段6: 填充PPT ==========
    print("\n" + "="*80)
    print("阶段6: 填充PPT内容")
    print("="*80)
    
    output_path = "demo_interpretation_output.pptx"
    print(f"\n输出文件: {output_path}")
    print("\n开始填充...")
    
    filler._fill_ppt(content_map, output_path, preserve_structure=True)
    
    print(f"\n【产出物6】最终生成的PPT文件:")
    print(f"  文件路径: {output_path}")
    print(f"  文件大小: {Path(output_path).stat().st_size:,} bytes")
    
    # ========== 总结 ==========
    print("\n" + "="*80)
    print("解读过程总结")
    print("="*80)
    
    print("""
完整流程：
1. 初始化解析器 → 加载PPT文件
2. 提取结构信息 → 获取幻灯片、形状、占位符信息
3. 提取文本摘要 → 生成LLM可理解的文本描述
4. 获取占位符映射 → 建立占位符ID到内容的映射关系
5. LLM生成内容 → 根据框架和用户需求生成内容
6. 填充PPT → 将生成的内容填充到占位符中

关键产出物：
- 结构信息 (structure): 完整的PPT结构数据
- 文本摘要 (text_summary): 用于LLM理解的文本描述
- 占位符映射 (placeholder_mapping): 占位符ID和类型映射
- 内容映射 (content_map): LLM生成的内容
- 最终PPT文件: 填充完成的PPT
    """)
    
    # 保存所有产出物到JSON文件
    output_data = {
        "input_file": framework_file,
        "stage_2_structure": structure,
        "stage_3_text_summary": text_summary,
        "stage_4_placeholder_mapping": placeholder_mapping,
        "stage_5_content_map": content_map,
        "stage_6_output_file": output_path
    }
    
    with open("demo_interpretation_output.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 所有产出物已保存到: demo_interpretation_output.json")
    print(f"✅ 详细日志已保存到: demo_interpretation.log")


if __name__ == "__main__":
    asyncio.run(demonstrate_interpretation_process())

