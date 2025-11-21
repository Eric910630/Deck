"""
测试浏览器渲染输出 - 生成PPT并查看效果
"""

import asyncio
from pathlib import Path
from ppt_filler import PPTFiller
from loguru import logger

# 配置日志级别
logger.remove()
logger.add(lambda msg: print(msg, end=""), level="INFO")


async def test_browser_rendering():
    """测试浏览器渲染输出"""
    print("="*80)
    print("测试浏览器渲染PPT生成")
    print("="*80)
    print()
    
    # 检查框架文件
    framework_file = "demo_filled.pptx"
    if not Path(framework_file).exists():
        print(f"❌ 框架文件不存在: {framework_file}")
        return
    
    print(f"📄 框架文件: {framework_file}")
    print()
    
    # 创建填充器（启用浏览器渲染）
    print("🔧 初始化PPT填充器（浏览器渲染模式）...")
    filler = PPTFiller(
        framework_file,
        use_browser_rendering=True
    )
    print("✅ 初始化完成")
    print()
    
    # 用户提示
    prompt = """
    制作一个关于人工智能技术的演示文稿，包含以下内容：
    1. 人工智能技术概述
    2. 核心技术介绍（机器学习、深度学习、自然语言处理）
    3. 应用场景（图像识别、语音处理、智能推荐）
    4. 未来展望
    """
    
    print("📝 用户提示:")
    print(prompt.strip())
    print()
    
    # 生成PPT
    print("🚀 开始生成PPT（浏览器渲染 + Ant Design规范）...")
    print()
    
    try:
        output_path = await filler.fill_from_prompt(
            prompt=prompt.strip(),
            output_path="test_browser_rendering_output.pptx",
            use_enhanced_analysis=True,
            use_browser_rendering=True
        )
        
        print()
        print("="*80)
        print("✅ PPT生成成功！")
        print("="*80)
        print()
        print(f"📁 输出文件: {output_path}")
        print()
        print("📊 生成统计:")
        print(f"   - 文件大小: {Path(output_path).stat().st_size / 1024:.2f} KB")
        print()
        print("🎨 设计特点:")
        print("   ✅ 16:9横版布局")
        print("   ✅ Ant Design设计规范")
        print("   ✅ 24栅格系统布局")
        print("   ✅ 容器卡片样式（圆角、阴影）")
        print("   ✅ 精确的文本样式复刻")
        print()
        print("💡 提示: 请打开生成的PPT文件查看效果")
        print()
        
    except Exception as e:
        print()
        print("="*80)
        print("❌ PPT生成失败")
        print("="*80)
        print()
        print(f"错误信息: {e}")
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_browser_rendering())

