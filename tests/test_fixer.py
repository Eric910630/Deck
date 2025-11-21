#!/usr/bin/env python3
"""
Deck 测试脚本
演示各种使用方式
"""

import asyncio
import json
from pathlib import Path
from loguru import logger
import sys

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from ppt_generator import PPTGenerator
from layout_generator import create_layout_generator
from ppt_filler import PPTFiller
from chart_generator import ChartGenerator
from vinci_integration import create_vinci_integration


async def test_layout_generation():
    """测试1: LLM生成布局"""
    print("\n" + "="*60)
    print("测试1: LLM生成布局")
    print("="*60)
    
    try:
        layout_generator = create_layout_generator()
        if not layout_generator:
            print("⚠ LLM服务不可用，跳过此测试")
            print("   提示: 请配置 .env 文件中的 CHAT_MODEL_API_KEY")
            return None
        
        print("✓ LLM服务已初始化")
        print("正在生成布局...")
        
        result = await layout_generator.generate_layout_from_prompt(
            prompt="制作一个关于人工智能技术的演示文稿，包含介绍、应用场景和未来展望",
            num_slides=3,
            include_charts=False
        )
        
        print(f"✓ 成功生成布局，包含 {len(result.get('vml_plan', []))} 张幻灯片")
        print(f"✓ 生成了 {len(result.get('content_map', {}))} 个内容项")
        
        # 保存到文件
        output_file = Path("test_output_layout.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✓ 布局已保存到: {output_file}")
        
        return result
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_ppt_generation_from_json():
    """测试2: 从JSON生成PPT"""
    print("\n" + "="*60)
    print("测试2: 从JSON生成PPT")
    print("="*60)
    
    try:
        # 创建测试数据
        test_data = {
            "vml_plan": [
                {
                    "vml_code": '<Slide padding="1.5cm" background="#f0f0f0"><VStack align="center" gap="1cm"><TextBox style="title" ref="title" align="center" /><TextBox style="subtitle" ref="subtitle" align="center" /></VStack></Slide>'
                },
                {
                    "vml_code": '<Slide padding="1.5cm"><VStack gap="1.2cm"><TextBox style="title" ref="page_title" /><TextBox style="body" ref="content_1" /></VStack></Slide>'
                }
            ],
            "content_map": {
                "title": "Deck 测试演示",
                "subtitle": "PPT生成工具测试",
                "page_title": "功能特点",
                "content_1": "这是一个测试PPT。\n\n展示了以下功能：\n- 文本生成\n- 布局控制\n- 样式支持"
            }
        }
        
        print("✓ 测试数据已准备")
        
        generator = PPTGenerator(output_dir="./test_outputs")
        print("✓ PPT生成器已初始化")
        
        result = await generator.generate_ppt(
            project_name="测试演示",
            vml_plan=test_data["vml_plan"],
            content_map=test_data["content_map"]
        )
        
        if 'error' in result:
            print(f"✗ 生成失败: {result['error']}")
            return None
        
        print(f"✓ PPT生成成功: {result['file_path']}")
        print(f"✓ 文件大小: {result.get('file_size', 0)} bytes")
        return result
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_chart_generation():
    """测试3: 图表生成"""
    print("\n" + "="*60)
    print("测试3: 图表生成")
    print("="*60)
    
    try:
        chart_generator = ChartGenerator(output_dir="./test_outputs/charts")
        print("✓ 图表生成器已初始化")
        
        # 测试柱状图
        test_data = [
            {"月份": "1月", "销售额": 1000},
            {"月份": "2月", "销售额": 1500},
            {"月份": "3月", "销售额": 1200},
            {"月份": "4月", "销售额": 1800}
        ]
        
        print("正在生成柱状图...")
        chart_path = chart_generator.generate_bar_chart(
            data=test_data,
            x_key="月份",
            y_key="销售额",
            title="月度销售数据"
        )
        print(f"✓ 柱状图已生成: {chart_path}")
        
        # 测试饼图
        print("正在生成饼图...")
        pie_data = [
            {"类别": "产品A", "占比": 35},
            {"类别": "产品B", "占比": 25},
            {"类别": "产品C", "占比": 40}
        ]
        pie_path = chart_generator.generate_pie_chart(
            data=pie_data,
            label_key="类别",
            value_key="占比",
            title="产品占比分布"
        )
        print(f"✓ 饼图已生成: {pie_path}")
        
        return {"bar_chart": chart_path, "pie_chart": pie_path}
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_ppt_with_charts():
    """测试4: 生成包含图表的PPT"""
    print("\n" + "="*60)
    print("测试4: 生成包含图表的PPT")
    print("="*60)
    
    try:
        # 创建图表生成集成
        vinci_integration = create_vinci_integration(output_dir=Path("./test_outputs/charts"))
        print("✓ 图表生成集成已初始化")
        
        # 准备数据
        test_data = {
            "vml_plan": [
                {
                    "vml_code": '<Slide padding="1.5cm"><VStack gap="1.2cm"><TextBox style="title" ref="chart_title" /><ImageBox ref="chart_1" width="80%" height="60%" /></VStack></Slide>'
                }
            ],
            "content_map": {
                "chart_title": "销售数据可视化"
            },
            "chart_insights": [
                {
                    "insightId": "chart_1",
                    "type": "bar_chart",
                    "title": "月度销售数据",
                    "data": [
                        {"月份": "1月", "销售额": 1000},
                        {"月份": "2月", "销售额": 1500},
                        {"月份": "3月", "销售额": 1200},
                        {"月份": "4月", "销售额": 1800}
                    ]
                }
            ]
        }
        
        generator = PPTGenerator(
            output_dir="./test_outputs",
            vinci_integration=vinci_integration
        )
        print("✓ PPT生成器已初始化（包含图表生成）")
        
        result = await generator.generate_ppt(
            project_name="测试图表PPT",
            vml_plan=test_data["vml_plan"],
            content_map=test_data["content_map"],
            chart_insights=test_data["chart_insights"]
        )
        
        if 'error' in result:
            print(f"✗ 生成失败: {result['error']}")
            return None
        
        print(f"✓ PPT生成成功: {result['file_path']}")
        print(f"✓ 文件大小: {result.get('file_size', 0)} bytes")
        return result
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None


async def test_framework_filling():
    """测试5: 框架填充（需要框架PPT文件）"""
    print("\n" + "="*60)
    print("测试5: PPT框架填充")
    print("="*60)
    
    # 检查是否有框架文件
    framework_files = list(Path(".").glob("*.pptx"))
    if not framework_files:
        print("⚠ 未找到框架PPT文件，跳过此测试")
        print("   提示: 在项目目录中放置一个 .pptx 文件作为框架")
        print("   或者使用: python cli.py --framework your_template.pptx --fill-prompt '你的提示'")
        return None
    
    framework_file = framework_files[0]
    print(f"找到框架文件: {framework_file}")
    
    try:
        filler = PPTFiller(str(framework_file))
        print("✓ PPT填充器已初始化")
        
        print("正在使用LLM填充内容...")
        output_path = await filler.fill_from_prompt(
            prompt="制作一个关于产品介绍的演示文稿，包含产品特点、优势和应用场景",
            preserve_structure=True
        )
        
        print(f"✓ PPT填充成功: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        if "LLM service is required" in str(e):
            print("   提示: 请配置 .env 文件中的 CHAT_MODEL_API_KEY")
        import traceback
        traceback.print_exc()
        return None


async def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("Deck 测试套件")
    print("="*60)
    print("\n将运行以下测试：")
    print("1. LLM生成布局")
    print("2. 从JSON生成PPT")
    print("3. 图表生成")
    print("4. 生成包含图表的PPT")
    print("5. PPT框架填充（如果找到框架文件）")
    print("\n开始测试...\n")
    
    results = {}
    
    # 测试1: LLM生成布局
    results['layout'] = await test_layout_generation()
    
    # 测试2: 从JSON生成PPT
    results['ppt_from_json'] = await test_ppt_generation_from_json()
    
    # 测试3: 图表生成
    results['charts'] = await test_chart_generation()
    
    # 测试4: 生成包含图表的PPT
    results['ppt_with_charts'] = await test_ppt_with_charts()
    
    # 测试5: 框架填充
    results['framework'] = await test_framework_filling()
    
    # 总结
    print("\n" + "="*60)
    print("测试总结")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v is not None)
    total = len(results)
    
    print(f"\n通过: {passed}/{total}")
    print("\n详细结果:")
    for name, result in results.items():
        status = "✓ 通过" if result is not None else "✗ 跳过/失败"
        print(f"  {name}: {status}")
    
    print("\n生成的文件位置:")
    print("  - PPT文件: ./test_outputs/")
    print("  - 图表文件: ./test_outputs/charts/")
    print("  - 布局JSON: test_output_layout.json")
    
    print("\n测试完成！")


if __name__ == "__main__":
    # 配置日志
    logger.remove()
    logger.add(sys.stderr, level="INFO")
    
    asyncio.run(main())

