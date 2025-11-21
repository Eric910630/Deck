#!/usr/bin/env python3
"""
使用Demo文档作为框架的测试脚本
"""

import asyncio
from pathlib import Path
from ppt_filler import PPTFiller
from loguru import logger

async def test_demo_framework():
    """使用Demo文档作为框架进行测试"""
    print("\n" + "="*60)
    print("Demo文档框架填充测试")
    print("="*60)
    
    # 查找Demo文档
    demo_files = [
        "demo_filled.pptx",
        "Demo文档.pptx",
        "Demo文档.docx"
    ]
    
    framework_file = None
    for f in demo_files:
        if Path(f).exists():
            framework_file = f
            break
    
    if not framework_file:
        print("✗ 未找到Demo文档")
        print("   请确保以下文件之一存在：")
        for f in demo_files:
            print(f"   - {f}")
        return None
    
    # 如果是docx，需要先转换（这里先提示）
    if framework_file.endswith('.docx'):
        print("⚠ 检测到.docx文件，PPT框架填充需要.pptx文件")
        print("   请先将Demo文档.docx转换为.pptx格式")
        return None
    
    print(f"✓ 找到框架文件: {framework_file}")
    
    try:
        # 初始化填充器
        filler = PPTFiller(framework_file)
        print("✓ PPT填充器已初始化")
        
        # 测试提示词
        test_prompts = [
            "制作一个关于人工智能技术的演示文稿，包含技术介绍、应用场景和未来展望",
            "制作一个产品发布会的演示文稿，包含产品特点、市场定位和竞争优势",
            "制作一个项目总结报告，包含项目背景、完成情况和成果展示"
        ]
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n--- 测试 {i}/{len(test_prompts)} ---")
            print(f"提示词: {prompt}")
            print("正在使用LLM填充内容...")
            
            try:
                output_path = await filler.fill_from_prompt(
                    prompt=prompt,
                    preserve_structure=True
                )
                print(f"✓ PPT填充成功: {output_path}")
                
                # 检查文件大小
                file_size = Path(output_path).stat().st_size
                print(f"✓ 文件大小: {file_size:,} bytes ({file_size/1024:.2f} KB)")
                
            except Exception as e:
                print(f"✗ 填充失败: {e}")
                import traceback
                traceback.print_exc()
        
        print("\n" + "="*60)
        print("测试完成！")
        print("="*60)
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        if "LLM service is required" in str(e):
            print("   提示: 请配置环境变量 CHAT_MODEL_API_KEY")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(test_demo_framework())

