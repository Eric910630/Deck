"""
测试浏览器到PPT复刻器
"""

import asyncio
from pathlib import Path
from browser_to_ppt_replicator import BrowserToPPTReplicator


async def test_replicator():
    """测试复刻器"""
    print("=== 测试浏览器到PPT复刻器 ===\n")
    
    # 创建测试HTML（包含Ant Design样式）
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试页面</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            width: 1920px;
            height: 1080px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
            background: #f0f2f5;
            padding: 24px;
        }
        .container {
            display: grid;
            grid-template-columns: repeat(24, 1fr);
            grid-template-rows: repeat(13.5, 1fr);
            gap: 16px;
            width: 100%;
            height: 100%;
        }
        .card {
            background: #ffffff;
            border: 1px solid #d9d9d9;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            padding: 24px;
        }
        .title-card {
            grid-column: 1 / 25;
            grid-row: 1 / 3;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .title {
            font-size: 48px;
            font-weight: 600;
            color: #1890ff;
            text-align: center;
        }
        .content-card {
            grid-column: 1 / 13;
            grid-row: 4 / 10;
        }
        .content-card-2 {
            grid-column: 13 / 25;
            grid-row: 4 / 10;
        }
        .content-title {
            font-size: 24px;
            font-weight: 600;
            color: #262626;
            margin-bottom: 16px;
        }
        .content-text {
            font-size: 16px;
            color: #595959;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card title-card">
            <h1 class="title">人工智能技术概述</h1>
        </div>
        
        <div class="card content-card">
            <h2 class="content-title">核心技术</h2>
            <p class="content-text">
                机器学习作为基础技术，通过算法让计算机从数据中学习规律，实现智能决策。
                深度学习基于神经网络架构，能够进行复杂模式识别，在图像识别、语音处理等领域表现卓越。
            </p>
        </div>
        
        <div class="card content-card-2">
            <h2 class="content-title">应用场景</h2>
            <p class="content-text">
                自然语言处理技术让机器理解并生成人类语言，实现人机自然交互。
                这些核心技术相互支撑，共同构建了人工智能的技术底座。
            </p>
        </div>
    </div>
</body>
</html>
    """
    
    # 创建复刻器
    replicator = BrowserToPPTReplicator()
    
    # 执行复刻
    try:
        output_path = await replicator.replicate(
            html_content,
            output_ppt_path=Path("test_replicated.pptx")
        )
        print(f"\n✅ 复刻成功！")
        print(f"   PPT文件: {output_path}")
    except Exception as e:
        print(f"\n❌ 复刻失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_replicator())

