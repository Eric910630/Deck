"""
调试：查看content_map的结构
"""

import asyncio
from ppt_filler import PPTFiller
from loguru import logger

logger.remove()
logger.add(lambda msg: print(msg, end=""), level="DEBUG")


async def debug_content_map():
    """调试content_map"""
    filler = PPTFiller('demo_filled.pptx', use_browser_rendering=True)
    
    prompt = '制作一个关于人工智能技术的演示文稿，包含技术介绍、应用场景和未来展望'
    
    # 获取content_map
    enhanced_parser = filler.parser.__class__('demo_filled.pptx')
    enhanced_structure = enhanced_parser.__class__('demo_filled.pptx').extract_structure_enhanced()
    
    from enhanced_ppt_parser import EnhancedPPTParser
    from human_centered_analyzer import HumanCenteredAnalyzer
    from content_strategy_generator import ContentStrategyGenerator
    
    enhanced_parser = EnhancedPPTParser('demo_filled.pptx')
    enhanced_structure = enhanced_parser.extract_structure_enhanced()
    
    analyzer = HumanCenteredAnalyzer(enhanced_structure)
    human_analysis = analyzer.analyze_all()
    
    strategy_gen = ContentStrategyGenerator(human_analysis)
    content_strategy = strategy_gen.generate_strategy()
    
    content_map = await filler._generate_content_by_sections(
        human_analysis, content_strategy, prompt
    )
    
    print("="*80)
    print("Content Map 结构分析")
    print("="*80)
    print()
    
    for key, value in content_map.items():
        print(f"Key: {key}")
        print(f"Content (前100字符): {value[:100]}...")
        print(f"Content 长度: {len(value)} 字符")
        print("-" * 80)
    
    print()
    print(f"总计: {len(content_map)} 个内容项")


if __name__ == "__main__":
    asyncio.run(debug_content_map())

