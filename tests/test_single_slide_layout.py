"""
简单测试：只生成一页HTML，验证布局修复
"""
import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.rendering.html_generator import HTMLGenerator
from src.rendering.html_canvas_generator import HTMLCanvasGenerator
from loguru import logger
from datetime import datetime


def create_test_data():
    """创建测试数据（支持CSS-First新架构）"""
    
    # 【CSS-First 新架构】LLM 生成的 HTML 代码
    # 【颜色修复】：大标题使用深黑色（--ant-text-color-heading），卡片标题使用彩色（与顶部装饰条呼应）
    llm_html_code = """
    <div class="slide-container" style="display: flex; flex-direction: column; height: 100vh; padding: 40px; background: var(--ant-bg-color-layout);">
      <!-- 大标题：保持深黑色 -->
      <header style="margin-bottom: 60px; border-left: 12px solid var(--ant-color-primary); padding-left: 24px;">
        <h1 data-ppt-element="true" data-ppt-element-id="title_text_0" data-ppt-element-type="title"
            style="font-size: 48px; font-weight: 600; color: var(--ant-text-color-heading); text-align: left; margin: 0; line-height: 1;">
          核心价值主张
        </h1>
      </header>
      <main style="flex: 1; display: flex; gap: 24px; align-items: stretch;">
        <!-- 卡片1：恢复蓝色标题 -->
        <div class="ant-card" data-ppt-element="true" data-ppt-element-id="value_card_0" data-ppt-element-type="card"
             style="flex: 1; background: var(--ant-bg-color-container); padding: 40px 32px; border-radius: var(--ant-border-radius-base); box-shadow: var(--ant-box-shadow); border-top: 6px solid #1677FF; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <h3 data-ppt-element="true" data-ppt-element-id="value_card_0_title" data-ppt-element-type="text"
              style="margin: 0 0 24px 0; font-size: 32px; font-weight: 700; color: #1677FF; text-align: center;">成本降低</h3>
          <p data-ppt-element="true" data-ppt-element-id="value_card_0_content" data-ppt-element-type="text"
             style="margin: 0; font-size: 18px; color: var(--ant-text-color-body); line-height: 1.8; text-align: center;">降低运营成本40-60%</p>
        </div>
        <!-- 卡片2：恢复绿色标题 -->
        <div class="ant-card" data-ppt-element="true" data-ppt-element-id="value_card_1" data-ppt-element-type="card"
             style="flex: 1; background: var(--ant-bg-color-container); padding: 40px 32px; border-radius: var(--ant-border-radius-base); box-shadow: var(--ant-box-shadow); border-top: 6px solid #52C41A; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <h3 data-ppt-element="true" data-ppt-element-id="value_card_1_title" data-ppt-element-type="text"
              style="margin: 0 0 24px 0; font-size: 32px; font-weight: 700; color: #52C41A; text-align: center;">效率提升</h3>
          <p data-ppt-element="true" data-ppt-element-id="value_card_1_content" data-ppt-element-type="text"
             style="margin: 0; font-size: 18px; color: var(--ant-text-color-body); line-height: 1.8; text-align: center;">提升转化效率20-35%</p>
        </div>
        <!-- 卡片3：恢复橙色标题 -->
        <div class="ant-card" data-ppt-element="true" data-ppt-element-id="value_card_2" data-ppt-element-type="card"
             style="flex: 1; background: var(--ant-bg-color-container); padding: 40px 32px; border-radius: var(--ant-border-radius-base); box-shadow: var(--ant-box-shadow); border-top: 6px solid #FA8C16; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <h3 data-ppt-element="true" data-ppt-element-id="value_card_2_title" data-ppt-element-type="text"
              style="margin: 0 0 24px 0; font-size: 32px; font-weight: 700; color: #FA8C16; text-align: center;">智能转型</h3>
          <p data-ppt-element="true" data-ppt-element-id="value_card_2_content" data-ppt-element-type="text"
             style="margin: 0; font-size: 18px; color: var(--ant-text-color-body); line-height: 1.8; text-align: center;">加速业务智能化转型</p>
        </div>
      </main>
      <!-- 底部：保持浅灰色 -->
      <footer style="margin-top: 40px; text-align: center; padding: 8px; background: rgba(0,0,0,0.02); border-radius: 4px;">
        <p data-ppt-element="true" data-ppt-element-id="subtitle_text_0" data-ppt-element-type="text"
           style="margin: 0; font-size: 24px; color: var(--ant-text-color-secondary);">
          全链路AI赋能解决方案
        </p>
      </footer>
    </div>
    """
    
    # 【CSS-First 新架构】布局规划（包含 html_code）
    layout_plan_css_first = {
        'slide_index': 0,
        'layout_plan': {
            'html_code': llm_html_code,  # 【新架构】LLM 生成的 HTML 代码
            'layout_strategy': '述职汇报风格，左对齐标题+三列卡片+底部总结',
            'design_tokens_used': ['--ant-color-primary', '--ant-bg-color-container', '--ant-box-shadow', '--ant-border-radius-base']
        }
    }
    
    # 【向后兼容】旧架构布局规划（用于对比测试）
    layout_plan_legacy = {
        'slide_index': 0,
        'layout_plan': {
            'overall_structure': '三个价值卡片并排排列，居中分布',
            'element_positions': [
                {
                    'element_id': 'title_text_0',
                    'element_type': 'title_text',
                    'position_description': '位于页面顶部，距离上边距80px，水平居中',
                    'size_description': '宽度占页面70%，高度自适应',
                    'alignment': 'center',
                    'spacing': {
                        'margin_top': '80px',
                        'margin_bottom': '24px',
                        'margin_left': 'auto',
                        'margin_right': 'auto'
                    }
                },
                {
                    'element_id': 'subtitle_text_0',
                    'element_type': 'subtitle_text',
                    'position_description': '位于标题下方，距离标题40px，水平居中',
                    'size_description': '宽度占页面60%，高度自适应',
                    'alignment': 'center',
                    'spacing': {
                        'margin_top': '40px',
                        'margin_bottom': '24px',
                        'margin_left': 'auto',
                        'margin_right': 'auto'
                    }
                },
                {
                    'element_id': 'value_card_0',
                    'element_type': 'value_card',
                    'position_description': '位于页面中间区域，左侧第一个位置',
                    'size_description': '宽度占页面25%，高度200px',
                    'alignment': 'center',
                    'spacing': {
                        'margin_top': 'auto',
                        'margin_bottom': 'auto',
                        'margin_left': '100px',
                        'margin_right': '24px'
                    }
                },
                {
                    'element_id': 'value_card_1',
                    'element_type': 'value_card',
                    'position_description': '位于页面中间区域，中间位置',
                    'size_description': '宽度占页面25%，高度200px',
                    'alignment': 'center',
                    'spacing': {
                        'margin_top': 'auto',
                        'margin_bottom': 'auto',
                        'margin_left': '24px',
                        'margin_right': '24px'
                    }
                },
                {
                    'element_id': 'value_card_2',
                    'element_type': 'value_card',
                    'position_description': '位于页面中间区域，右侧第三个位置',
                    'size_description': '宽度占页面25%，高度200px',
                    'alignment': 'center',
                    'spacing': {
                        'margin_top': 'auto',
                        'margin_bottom': 'auto',
                        'margin_left': '24px',
                        'margin_right': '100px'
                    }
                }
            ]
        }
    }
    
    # 模拟润色内容
    polished_slide = {
        'slide_index': 0,
        'title': '核心价值主张',
        'content': '展示三大核心价值维度',
        'content_type': 'content_page',
        'visual_elements_detail': [
            {
                'element_id': 'title_text_0',
                'element_type': 'title_text',
                'title': '核心价值主张',
                'content': '三大价值维度',
                'description': '展示核心价值主张的标题'
            },
            {
                'element_id': 'subtitle_text_0',
                'element_type': 'subtitle_text',
                'title': '全链路AI赋能解决方案',
                'content': '驱动业务智能化转型',
                'description': '副标题说明'
            },
            {
                'element_id': 'value_card_0',
                'element_type': 'value_card',
                'title': '成本降低',
                'content': '降低运营成本40-60%',
                'description': '第一个价值卡片'
            },
            {
                'element_id': 'value_card_1',
                'element_type': 'value_card',
                'title': '效率提升',
                'content': '提升转化效率20-35%',
                'description': '第二个价值卡片'
            },
            {
                'element_id': 'value_card_2',
                'element_type': 'value_card',
                'title': '智能转型',
                'content': '加速业务智能化转型',
                'description': '第三个价值卡片'
            }
        ]
    }
    
    # 模拟颜色配置
    color_config = {
        'slide_index': 0,
        'color_config': {
            'element_colors': [
                {
                    'element_id': 'title_text_0',
                    'text_color': '#1890ff',
                    'background_color': '#ffffff',
                    'border_color': '#d9d9d9'
                },
                {
                    'element_id': 'subtitle_text_0',
                    'text_color': '#595959',
                    'background_color': '#ffffff',
                    'border_color': '#d9d9d9'
                },
                {
                    'element_id': 'value_card_0',
                    'text_color': '#262626',
                    'background_color': '#f0f5ff',
                    'border_color': '#1890ff'
                },
                {
                    'element_id': 'value_card_1',
                    'text_color': '#262626',
                    'background_color': '#f6ffed',
                    'border_color': '#52c41a'
                },
                {
                    'element_id': 'value_card_2',
                    'text_color': '#262626',
                    'background_color': '#fff7e6',
                    'border_color': '#faad14'
                }
            ]
        }
    }
    
    return layout_plan_css_first, layout_plan_legacy, polished_slide, color_config


async def test_single_slide():
    """测试单页HTML生成（支持CSS-First新架构）"""
    logger.info("="*80)
    logger.info("简单测试：单页HTML生成（验证CSS-First架构）")
    logger.info("="*80)
    
    # 创建测试数据
    layout_plan_css_first, layout_plan_legacy, polished_slide, color_config = create_test_data()
    
    # 初始化HTML生成器
    html_generator = HTMLGenerator()
    
    # 构建polished_content_map（使用(slide_index, element_id)作为键）
    polished_content_map = {}
    slide_idx = polished_slide.get('slide_index', 0)
    for elem in polished_slide.get('visual_elements_detail', []):
        elem_id = elem.get('element_id', '')
        if elem_id:
            key = (slide_idx, elem_id)
            polished_content_map[key] = {
                'slide_index': slide_idx,
                'element': elem,
                'polished_slide': polished_slide
            }
    
    # 构建color_map（使用(slide_index, element_id)作为键）
    color_map = {}
    for elem_color in color_config.get('color_config', {}).get('element_colors', []):
        elem_id = elem_color.get('element_id', '')
        if elem_id:
            key = (slide_idx, elem_id)
            color_map[key] = elem_color
    
    # 【测试1】CSS-First 新架构
    logger.info("--- [测试1] CSS-First 新架构：使用 LLM 生成的 HTML...")
    html_content_css_first = html_generator._generate_html_from_layout_plan(
        layout_plan=layout_plan_css_first.get('layout_plan', {}),
        polished_slide=polished_slide,
        polished_content_map=polished_content_map,
        color_map=color_map
    )
    
    # 保存CSS-First HTML文件
    output_dir = Path("html_output")
    output_dir.mkdir(exist_ok=True)
    output_file_css_first = output_dir / "test_single_slide_css_first.html"
    
    with open(output_file_css_first, 'w', encoding='utf-8') as f:
        f.write(html_content_css_first)
    
    logger.info(f"--- [测试1] ✅ CSS-First HTML生成完成，保存到: {output_file_css_first}")
    logger.info(f"--- [测试1] 文件大小: {output_file_css_first.stat().st_size} bytes")
    
    # 【测试2】向后兼容：旧架构（用于对比）
    logger.info("\n--- [测试2] 向后兼容：旧架构（Python坐标计算）...")
    html_content_legacy = html_generator._generate_html_from_layout_plan(
        layout_plan=layout_plan_legacy.get('layout_plan', {}),
        polished_slide=polished_slide,
        polished_content_map=polished_content_map,
        color_map=color_map
    )
    
    # 保存旧架构HTML文件
    output_file_legacy = output_dir / "test_single_slide_legacy.html"
    
    with open(output_file_legacy, 'w', encoding='utf-8') as f:
        f.write(html_content_legacy)
    
    logger.info(f"--- [测试2] ✅ 旧架构HTML生成完成，保存到: {output_file_legacy}")
    logger.info(f"--- [测试2] 文件大小: {output_file_legacy.stat().st_size} bytes")
    
    logger.info("="*80)
    logger.info("💡 提示: 请在浏览器中打开HTML文件查看效果")
    logger.info(f"   - CSS-First: {output_file_css_first}")
    logger.info(f"   - 旧架构: {output_file_legacy}")
    logger.info("="*80)
    
    return str(output_file_css_first), str(output_file_legacy)


if __name__ == "__main__":
    asyncio.run(test_single_slide())

