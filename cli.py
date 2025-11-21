#!/usr/bin/env python3
"""
Deck CLI - PPT生成工具命令行接口
从JSON文件读取架构内容（VML计划和内容映射），生成PPT文件
支持可选的Vinci图表生成集成
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path

from loguru import logger

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from src.core.ppt_generator import PPTGenerator
from scripts.vinci_integration import create_vinci_integration
from src.core.llm_service import create_llm_service
from scripts.layout_generator import create_layout_generator
from src.core.ppt_filler import PPTFiller


def load_input_file(input_path: str) -> dict:
    """从JSON文件加载输入数据"""
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data


def validate_input_data(data: dict) -> tuple[list, dict]:
    """验证并提取VML计划和内容映射"""
    if 'vml_plan' not in data:
        raise ValueError("Input data must contain 'vml_plan' field")
    
    if 'content_map' not in data:
        raise ValueError("Input data must contain 'content_map' field")
    
    vml_plan = data['vml_plan']
    content_map = data['content_map']
    
    if not isinstance(vml_plan, list):
        raise ValueError("'vml_plan' must be a list")
    
    if not isinstance(content_map, dict):
        raise ValueError("'content_map' must be a dict")
    
    # 验证每个VML计划项都有vml_code
    for i, slide_data in enumerate(vml_plan):
        if not isinstance(slide_data, dict):
            raise ValueError(f"VML plan item {i} must be a dict")
        if 'vml_code' not in slide_data:
            raise ValueError(f"VML plan item {i} must contain 'vml_code' field")
    
    return vml_plan, content_map


async def async_main(args):
    """异步主函数"""
    try:
        # 如果提供了框架文件，使用框架填充模式
        if args.framework:
            logger.info("Using framework-based PPT generation...")
            filler = PPTFiller(args.framework)
            
            if not args.fill_prompt:
                logger.error("--fill-prompt is required when using --framework")
                sys.exit(1)
            
            try:
                output_path = await filler.fill_from_prompt(
                    prompt=args.fill_prompt,
                    output_path=args.output_ppt,
                    preserve_structure=args.preserve_structure
                )
                logger.success(f"✓ PPT filled successfully: {output_path}")
                print(f"\n✓ Success! Filled PPT saved to: {output_path}")
                return
            except Exception as e:
                logger.error(f"Failed to fill PPT: {e}", exc_info=True)
                sys.exit(1)
        
        # 如果提供了生成提示，使用LLM生成布局
        if args.generate:
            logger.info("Using LLM to generate layout from prompt...")
            layout_generator = create_layout_generator()
            if not layout_generator:
                logger.error("LLM service is not available. Please configure CHAT_MODEL_API_KEY in .env file")
                sys.exit(1)
            
            try:
                generated_data = await layout_generator.generate_layout_from_prompt(
                    prompt=args.generate,
                    num_slides=args.num_slides,
                    include_charts=args.include_charts
                )
                logger.success(f"✓ Generated layout with {len(generated_data.get('vml_plan', []))} slides")
                
                # 如果指定了输出文件，保存生成的布局
                if args.output_json:
                    output_path = Path(args.output_json)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(generated_data, f, ensure_ascii=False, indent=2)
                    logger.info(f"✓ Saved generated layout to {output_path}")
                
                data = generated_data
            except Exception as e:
                logger.error(f"Failed to generate layout: {e}", exc_info=True)
                sys.exit(1)
        else:
            # 加载输入文件
            logger.info(f"Loading input file: {args.input_file}")
            data = load_input_file(args.input_file)
        
        # 验证数据
        logger.info("Validating input data...")
        vml_plan, content_map = validate_input_data(data)
        logger.info(f"✓ Found {len(vml_plan)} slides in VML plan")
        logger.info(f"✓ Found {len(content_map)} items in content map")
        
        # 检查是否有图表洞察
        chart_insights = data.get('chart_insights', None)
        if chart_insights:
            logger.info(f"✓ Found {len(chart_insights)} chart insights")
        
        # 创建图表生成集成（如果需要）
        vinci_integration = None
        if chart_insights:
            try:
                # 创建独立的图表生成器（不依赖LLM服务，直接使用matplotlib）
                vinci_integration = create_vinci_integration()
                if vinci_integration:
                    logger.info("✓ Chart generation enabled (using standalone ChartGenerator)")
                else:
                    logger.warning("⚠ Chart generation not available")
            except Exception as e:
                logger.warning(f"⚠ Failed to initialize chart generation: {e}")
                logger.warning("⚠ Chart generation will be disabled")
        
        # 创建生成器
        generator = PPTGenerator(
            output_dir=args.output_dir,
            vinci_integration=vinci_integration
        )
        
        # 生成PPT
        logger.info(f"Generating PPT: {args.project_name}")
        result = await generator.generate_ppt(
            project_name=args.project_name,
            vml_plan=vml_plan,
            content_map=content_map,
            template_path=args.template,
            chart_insights=chart_insights
        )
        
        if 'error' in result:
            logger.error(f"Failed to generate PPT: {result['error']}")
            sys.exit(1)
        
        logger.success(f"✓ PPT generated successfully: {result['file_path']}")
        logger.info(f"  File size: {result.get('file_size', 0)} bytes")
        print(f"\n✓ Success! PPT file saved to: {result['file_path']}")
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Deck - PPT生成工具，根据架构内容（VML计划）生成PPT文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从JSON文件生成PPT
  python cli.py example_input.json -o output_dir -n "我的演示文稿"
  
  # 使用LLM生成布局（需要配置LLM服务）
  python cli.py --generate "制作一个关于AI技术的演示文稿，包含3页" -n "AI技术介绍" --num-slides 3
  
  # 根据框架PPT生成完整PPT（推荐）
  python cli.py --framework template.pptx --fill-prompt "制作一个关于产品介绍的演示文稿" --output-ppt output.pptx
  
  # 使用模板文件
  python cli.py example_input.json -t template.pptx -n "我的演示文稿"
  
  # 包含图表生成（自动使用matplotlib生成）
  python cli.py example_input.json -n "我的演示文稿"
  
输入JSON格式:
  {
    "vml_plan": [
      {
        "vml_code": "<Slide padding=\"1.5cm\"><VStack><TextBox style=\"title\" ref=\"title_1\" /></VStack></Slide>"
      }
    ],
    "content_map": {
      "title_1": "这是标题文本"
    },
    "chart_insights": [
      {
        "insightId": "chart_1",
        "type": "bar_chart",
        "title": "销售数据",
        "data": [...]
      }
    ]
  }
        """
    )
    
    parser.add_argument(
        'input_file',
        type=str,
        nargs='?',
        help='输入JSON文件路径（包含vml_plan和content_map），如果使用--generate则不需要'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        default=None,
        help='PPT输出目录（默认：当前目录下的ppt_outputs）'
    )
    
    parser.add_argument(
        '-n', '--project-name',
        type=str,
        default='presentation',
        help='项目名称（用于生成文件名，默认：presentation）'
    )
    
    parser.add_argument(
        '-t', '--template',
        type=str,
        default=None,
        help='可选的PPT模板文件路径'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细日志'
    )
    
    parser.add_argument(
        '--generate',
        type=str,
        default=None,
        help='使用LLM根据自然语言提示生成布局（需要配置LLM服务）'
    )
    
    parser.add_argument(
        '--num-slides',
        type=int,
        default=3,
        help='生成布局时的幻灯片数量（默认：3）'
    )
    
    parser.add_argument(
        '--include-charts',
        action='store_true',
        help='生成布局时包含图表'
    )
    
    parser.add_argument(
        '--output-json',
        type=str,
        default=None,
        help='将生成的布局保存到JSON文件'
    )
    
    parser.add_argument(
        '--framework',
        type=str,
        default=None,
        help='PPT框架文件路径（根据框架生成完整PPT）'
    )
    
    parser.add_argument(
        '--fill-prompt',
        type=str,
        default=None,
        help='内容填充提示（与--framework一起使用）'
    )
    
    parser.add_argument(
        '--output-ppt',
        type=str,
        default=None,
        help='输出PPT文件路径（与--framework一起使用）'
    )
    
    parser.add_argument(
        '--preserve-structure',
        action='store_true',
        default=True,
        help='保持框架原有结构（默认：True）'
    )
    
    args = parser.parse_args()
    
    # 验证参数
    if args.framework:
        if not args.fill_prompt:
            parser.error("--fill-prompt is required when using --framework")
    elif args.generate and args.input_file:
        logger.warning("Both --generate and input_file provided, --generate will be used")
    elif not args.generate and not args.input_file and not args.framework:
        parser.error("Either input_file, --generate, or --framework must be provided")
    
    # 配置日志
    if args.verbose:
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.remove()
        logger.add(sys.stderr, level="INFO")
    
    # 运行异步主函数
    asyncio.run(async_main(args))


if __name__ == '__main__':
    main()
