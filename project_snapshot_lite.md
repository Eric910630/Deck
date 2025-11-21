# Project Snapshot (Lite): Fixer
> Optimized for LLM Context Context

## 1. File List
- `__init__.py`
- `analyze_demo_docx.py`
- `ant_design_theme.py`
- `antv_chart_theme.py`
- `chart_generator.py`
- `chart_integrator.py`
- `chinese_ppt_theme.py`
- `cli.py`
- `color_configurator.py`
- `content_polisher.py`
- `content_strategy_generator.py`
- `create_framework_ppt.py`
- `deep_analyze_demo_docx.py`
- `deep_parser.py`
- `enhanced_ppt_parser.py`
- `html_canvas_generator.py`
- `html_flow_layout_generator.py`
- `html_generator.py`
- `human_centered_analyzer.py`
- `layout_generator.py`
- `layout_planner.py`
- `llm_service.py`
- `ppt_filler.py`
- `ppt_generator.py`
- `ppt_parser.py`
- `presentation_planner.py`
- `presentation_schema.py`
- `semantic_analyzer.py`
- `supporting_materials_analyzer.py`
- `test_canvas_generator.py`
- `verify_fixes.py`
- `vinci_integration.py`
- `web_chart_generator.py`
- `tests/test_browser_rendering_output.py`
- `tests/test_browser_to_ppt_replicator.py`
- `tests/test_demo_framework.py`
- `tests/test_docx_to_ppt_full_flow.py`
- `tests/test_fixer.py`
- `tests/test_llm_understand_demo_docx.py`
- `tests/test_single_slide_layout.py`
- `browser_to_ppt_replicator/__init__.py`
- `browser_to_ppt_replicator/browser_renderer.py`
- `browser_to_ppt_replicator/container_extractor.py`
- `browser_to_ppt_replicator/coordinate_mapper.py`
- `browser_to_ppt_replicator/element_analyzer.py`
- `browser_to_ppt_replicator/hybrid_renderer.py`
- `browser_to_ppt_replicator/ppt_replicator.py`
- `browser_to_ppt_replicator/replicator.py`
- `browser_to_ppt_replicator/text_extractor.py`

---

## 2. Code Contents

## File: __init__.py

```python
"""
Fixer - PPT生成工具
独立的PPT组装工具，可以根据指定的架构内容（VML计划）生成PPT文件
支持可选的Vinci图表生成集成
"""

from .ppt_generator import PPTGenerator

try:
    from .vinci_integration import VinciIntegration, create_vinci_integration
    __all__ = ["PPTGenerator", "VinciIntegration", "create_vinci_integration"]
except ImportError:
    __all__ = ["PPTGenerator"]

```


## File: analyze_demo_docx.py

```python
#!/usr/bin/env python3
"""
手动分析Demo文档.docx的结构和层次
不使用系统，直接由AI进行深度解读
"""

import json
from docx import Document
from pathlib import Path

def analyze_docx_structure(docx_path: str):
    """深度分析docx文档的结构和层次"""
    
    doc = Document(docx_path)
    
    analysis = {
        "file_info": {
            "path": docx_path,
            "size_bytes": Path(docx_path).stat().st_size,
            "paragraph_count": len(doc.paragraphs),
            "tables_count": len(doc.tables),
            "sections_count": len(doc.sections)
        },
        "document_structure": {
            "sections": [],
            "paragraphs": [],
            "tables": [],
            "styles_used": set(),
            "hierarchical_structure": []
        },
        "content_analysis": {
            "headings": [],
            "body_text": [],
            "lists": [],
            "tables": [],
            "metadata": {}
        },
        "semantic_layers": []
    }
    
    # 分析段落
    current_heading_level = 0
    current_section = None
    paragraph_stack = []
    
    for i, para in enumerate(doc.paragraphs):
        para_info = {
            "index": i,
            "text": para.text.strip(),
            "style": para.style.name if para.style else "Normal",
            "runs": [],
            "level": None,
            "is_heading": False,
            "is_list": False,
            "is_empty": not para.text.strip()
        }
        
        # 分析样式
        if para.style:
            analysis["document_structure"]["styles_used"].add(para.style.name)
        
        # 判断是否为标题
        if para.style and para.style.name.startswith('Heading'):
            para_info["is_heading"] = True
            try:
                para_info["level"] = int(para.style.name.replace('Heading ', ''))
            except:
                para_info["level"] = 1
        
        # 分析文本运行（runs）
        for run in para.runs:
            run_info = {
                "text": run.text,
                "bold": run.bold,
                "italic": run.italic,
                "underline": run.underline,
                "font_name": run.font.name if run.font.name else None,
                "font_size": run.font.size.pt if run.font.size else None,
                "font_color": str(run.font.color.rgb) if run.font.color and run.font.color.rgb else None
            }
            para_info["runs"].append(run_info)
        
        # 判断是否为列表
        if para.style and ('List' in para.style.name or para.style.name.startswith('List')):
            para_info["is_list"] = True
        
        # 检查段落格式中的列表信息
        if para.paragraph_format.left_indent or para.paragraph_format.first_line_indent:
            para_info["is_list"] = True
        
        analysis["document_structure"]["paragraphs"].append(para_info)
        
        # 构建层次结构
        if para_info["is_heading"]:
            # 遇到新标题，处理之前的段落栈
            if paragraph_stack:
                analysis["document_structure"]["hierarchical_structure"].append({
                    "heading": paragraph_stack[0] if paragraph_stack else None,
                    "content": paragraph_stack[1:] if len(paragraph_stack) > 1 else []
                })
                paragraph_stack = []
            
            paragraph_stack.append(para_info)
            analysis["content_analysis"]["headings"].append(para_info)
        elif para_info["text"]:
            paragraph_stack.append(para_info)
            if not para_info["is_heading"]:
                analysis["content_analysis"]["body_text"].append(para_info)
    
    # 处理最后一个段落栈
    if paragraph_stack:
        analysis["document_structure"]["hierarchical_structure"].append({
            "heading": paragraph_stack[0] if paragraph_stack and paragraph_stack[0]["is_heading"] else None,
            "content": paragraph_stack[1:] if len(paragraph_stack) > 1 else paragraph_stack
        })
    
    # 分析表格
    for i, table in enumerate(doc.tables):
        table_info = {
            "index": i,
            "rows": len(table.rows),
            "columns": len(table.columns) if table.rows else 0,
            "cells": [],
            "structure": []
        }
        
        for row_idx, row in enumerate(table.rows):
            row_data = []
            for cell_idx, cell in enumerate(row.cells):
                cell_text = cell.text.strip()
                row_data.append(cell_text)
                table_info["cells"].append({
                    "row": row_idx,
                    "column": cell_idx,
                    "text": cell_text
                })
            table_info["structure"].append(row_data)
        
        analysis["document_structure"]["tables"].append(table_info)
        analysis["content_analysis"]["tables"].append(table_info)
    
    # 分析章节
    for i, section in enumerate(doc.sections):
        section_info = {
            "index": i,
            "page_width": section.page_width.inches if section.page_width else None,
            "page_height": section.page_height.inches if section.page_height else None,
            "margin_left": section.left_margin.inches if section.left_margin else None,
            "margin_right": section.right_margin.inches if section.right_margin else None,
            "margin_top": section.top_margin.inches if section.top_margin else None,
            "margin_bottom": section.bottom_margin.inches if section.bottom_margin else None
        }
        analysis["document_structure"]["sections"].append(section_info)
    
    # 转换为可序列化的格式
    analysis["document_structure"]["styles_used"] = list(analysis["document_structure"]["styles_used"])
    
    return analysis

def identify_semantic_layers(analysis):
    """识别语义层次"""
    
    layers = []
    
    # 层次1: 文档元信息层
    layers.append({
        "layer_name": "文档元信息层",
        "level": 1,
        "description": "文档的基础信息和格式设置",
        "content": {
            "file_size": analysis["file_info"]["size_bytes"],
            "paragraph_count": analysis["file_info"]["paragraph_count"],
            "tables_count": analysis["file_info"]["tables_count"],
            "sections_count": analysis["file_info"]["sections_count"],
            "styles_used": analysis["document_structure"]["styles_used"]
        }
    })
    
    # 层次2: 结构层次（标题层级）
    heading_hierarchy = {}
    for heading in analysis["content_analysis"]["headings"]:
        level = heading.get("level", 1)
        if level not in heading_hierarchy:
            heading_hierarchy[level] = []
        heading_hierarchy[level].append({
            "text": heading["text"],
            "style": heading["style"],
            "index": heading["index"]
        })
    
    layers.append({
        "layer_name": "结构层次（标题层级）",
        "level": 2,
        "description": "文档的标题层级结构，反映内容的组织方式",
        "content": heading_hierarchy
    })
    
    # 层次3: 内容语义层
    semantic_blocks = []
    for block in analysis["document_structure"]["hierarchical_structure"]:
        if block["heading"]:
            semantic_blocks.append({
                "heading": block["heading"]["text"],
                "heading_level": block["heading"].get("level", 1),
                "content_paragraphs": len(block["content"]),
                "content_preview": [p["text"][:50] for p in block["content"][:3] if p["text"]]
            })
    
    layers.append({
        "layer_name": "内容语义层",
        "level": 3,
        "description": "基于标题-内容块的内容组织",
        "content": semantic_blocks
    })
    
    # 层次4: 文本格式层
    format_analysis = {
        "bold_text": [],
        "italic_text": [],
        "colored_text": [],
        "different_fonts": set(),
        "different_sizes": set()
    }
    
    for para in analysis["document_structure"]["paragraphs"]:
        for run in para["runs"]:
            if run["bold"]:
                format_analysis["bold_text"].append(run["text"][:30])
            if run["italic"]:
                format_analysis["italic_text"].append(run["text"][:30])
            if run["font_color"]:
                format_analysis["colored_text"].append(run["text"][:30])
            if run["font_name"]:
                format_analysis["different_fonts"].add(run["font_name"])
            if run["font_size"]:
                format_analysis["different_sizes"].add(run["font_size"])
    
    format_analysis["different_fonts"] = list(format_analysis["different_fonts"])
    format_analysis["different_sizes"] = list(format_analysis["different_sizes"])
    
    layers.append({
        "layer_name": "文本格式层",
        "level": 4,
        "description": "文本的格式信息（加粗、斜体、颜色、字体等）",
        "content": format_analysis
    })
    
    # 层次5: 列表结构层
    list_structure = []
    for para in analysis["document_structure"]["paragraphs"]:
        if para["is_list"]:
            list_structure.append({
                "text": para["text"][:100],
                "style": para["style"],
                "index": para["index"]
            })
    
    layers.append({
        "layer_name": "列表结构层",
        "level": 5,
        "description": "文档中的列表项和项目符号",
        "content": list_structure
    })
    
    # 层次6: 表格数据层
    if analysis["content_analysis"]["tables"]:
        layers.append({
            "layer_name": "表格数据层",
            "level": 6,
            "description": "文档中的表格结构和数据",
            "content": analysis["content_analysis"]["tables"]
        })
    
    return layers

if __name__ == "__main__":
    docx_path = "Demo文档.docx"
    
    print("="*80)
    print("Demo文档.docx 深度拆解分析")
    print("="*80)
    print(f"\n正在分析: {docx_path}\n")
    
    # 分析文档结构
    analysis = analyze_docx_structure(docx_path)
    
    # 识别语义层次
    semantic_layers = identify_semantic_layers(analysis)
    analysis["semantic_layers"] = semantic_layers
    
    # 输出分析结果
    print("\n" + "="*80)
    print("【层次1】文档元信息层")
    print("="*80)
    print(json.dumps(analysis["semantic_layers"][0]["content"], indent=2, ensure_ascii=False))
    
    print("\n" + "="*80)
    print("【层次2】结构层次（标题层级）")
    print("="*80)
    print(json.dumps(analysis["semantic_layers"][1]["content"], indent=2, ensure_ascii=False))
    
    print("\n" + "="*80)
    print("【层次3】内容语义层")
    print("="*80)
    for i, block in enumerate(analysis["semantic_layers"][2]["content"], 1):
        print(f"\n块 {i}: {block['heading']} (级别{block['heading_level']})")
        print(f"  内容段落数: {block['content_paragraphs']}")
        if block['content_preview']:
            print(f"  内容预览:")
            for preview in block['content_preview']:
                print(f"    - {preview}...")
    
    print("\n" + "="*80)
    print("【层次4】文本格式层")
    print("="*80)
    format_info = analysis["semantic_layers"][3]["content"]
    print(f"使用的字体: {format_info['different_fonts']}")
    print(f"使用的字号: {format_info['different_sizes']}")
    print(f"加粗文本数量: {len(format_info['bold_text'])}")
    print(f"斜体文本数量: {len(format_info['italic_text'])}")
    print(f"彩色文本数量: {len(format_info['colored_text'])}")
    
    if analysis["semantic_layers"][4]["content"]:
        print("\n" + "="*80)
        print("【层次5】列表结构层")
        print("="*80)
        print(f"列表项数量: {len(analysis['semantic_layers'][4]['content'])}")
        for i, item in enumerate(analysis["semantic_layers"][4]["content"][:5], 1):
            print(f"  {i}. {item['text']}...")
    
    if len(analysis["semantic_layers"]) > 5:
        print("\n" + "="*80)
        print("【层次6】表格数据层")
        print("="*80)
        for i, table in enumerate(analysis["semantic_layers"][5]["content"], 1):
            print(f"\n表格 {i}:")
            print(f"  行数: {table['rows']}, 列数: {table['columns']}")
            if table['structure']:
                print(f"  表格内容预览:")
                for row in table['structure'][:3]:
                    print(f"    {row}")
    
    # 保存完整分析结果
    output_file = "demo_docx_analysis.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n✅ 完整分析结果已保存到: {output_file}")
    print(f"   总层次数: {len(semantic_layers)}")
    print(f"   总段落数: {analysis['file_info']['paragraph_count']}")
    print(f"   总表格数: {analysis['file_info']['tables_count']}")


```


## File: ant_design_theme.py

```python
"""
Ant Design 设计规范集成
提供Ant Design的颜色、间距、字体等设计Token
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class AntDesignColors:
    """Ant Design 颜色系统"""
    # 主色调
    colorPrimary: str = "#1890ff"  # 蓝色
    colorSuccess: str = "#52c41a"  # 绿色
    colorWarning: str = "#faad14"  # 橙色
    colorError: str = "#f5222d"    # 红色
    colorInfo: str = "#1890ff"     # 信息色
    
    # 中性色（matplotlib兼容格式）
    colorText: str = "#262626"  # 主文本 rgba(0,0,0,0.85) ≈ #262626
    colorTextSecondary: str = "#595959"  # 次文本 rgba(0,0,0,0.65) ≈ #595959
    colorTextTertiary: str = "#8c8c8c"  # 辅助文本 rgba(0,0,0,0.45) ≈ #8c8c8c
    colorTextDisabled: str = "#bfbfbf"  # 禁用文本 rgba(0,0,0,0.25) ≈ #bfbfbf
    
    # 背景色
    colorBgBase: str = "#ffffff"  # 基础背景
    colorBgContainer: str = "#ffffff"  # 容器背景
    colorBgElevated: str = "#ffffff"  # 悬浮背景
    colorBgLayout: str = "#f0f2f5"  # 布局背景
    
    # 边框色
    colorBorder: str = "#d9d9d9"  # 基础边框
    colorBorderSecondary: str = "#f0f0f0"  # 次要边框
    
    # 分类色（用于图表）
    category10: List[str] = None
    
    def __post_init__(self):
        if self.category10 is None:
            # Ant Design 默认分类色
            self.category10 = [
                "#1890ff",  # 蓝色
                "#52c41a",  # 绿色
                "#faad14",  # 橙色
                "#f5222d",  # 红色
                "#722ed1",  # 紫色
                "#13c2c2",  # 青色
                "#eb2f96",  # 粉色
                "#fa8c16",  # 橙红
                "#a0d911",  # 黄绿
                "#2f54eb",  # 深蓝
            ]


@dataclass
class AntDesignSpacing:
    """Ant Design 间距系统（基于8px基础单位）"""
    # 基础间距
    paddingXXS: int = 4   # 4px
    paddingXS: int = 8    # 8px
    paddingSM: int = 12   # 12px
    padding: int = 16     # 16px
    paddingMD: int = 20   # 20px
    paddingLG: int = 24   # 24px
    paddingXL: int = 32   # 32px
    paddingXXL: int = 48  # 48px
    
    # 边距
    marginXXS: int = 4
    marginXS: int = 8
    marginSM: int = 12
    margin: int = 16
    marginMD: int = 20
    marginLG: int = 24
    marginXL: int = 32
    marginXXL: int = 48


@dataclass
class AntDesignTypography:
    """Ant Design 字体系统"""
    # 字体族
    fontFamily: str = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    fontFamilyCode: str = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace"
    
    # 字号（针对PPT显示优化，放大2倍以确保在PPT中清晰可见）
    fontSizeSM: int = 24   # 24px (原12px × 2)
    fontSize: int = 28     # 28px (原14px × 2)
    fontSizeLG: int = 32   # 32px (原16px × 2)
    fontSizeXL: int = 40   # 40px (原20px × 2)
    fontSizeXXL: int = 48  # 48px (原24px × 2)
    fontSizeHeading1: int = 76  # 76px (原38px × 2)
    fontSizeHeading2: int = 60  # 60px (原30px × 2)
    fontSizeHeading3: int = 48  # 48px (原24px × 2)
    fontSizeHeading4: int = 40  # 40px (原20px × 2)
    fontSizeHeading5: int = 32  # 32px (原16px × 2)
    
    # 字重
    fontWeightStrong: int = 600
    fontWeight: int = 400
    
    # 行高
    lineHeight: float = 1.5715
    lineHeightLG: float = 1.5
    lineHeightSM: float = 1.66


@dataclass
class AntDesignBorderRadius:
    """Ant Design 圆角系统"""
    borderRadius: int = 6      # 基础圆角 6px
    borderRadiusSM: int = 2    # 小圆角 2px
    borderRadiusLG: int = 8    # 大圆角 8px
    borderRadiusOuter: int = 4 # 外圆角 4px


class AntDesignTheme:
    """Ant Design 完整主题"""
    
    def __init__(self):
        self.colors = AntDesignColors()
        self.spacing = AntDesignSpacing()
        self.typography = AntDesignTypography()
        self.borderRadius = AntDesignBorderRadius()
    
    def get_color_palette(self, count: int = 10) -> List[str]:
        """获取颜色调色板"""
        if count <= len(self.colors.category10):
            return self.colors.category10[:count]
        # 如果需要更多颜色，可以扩展
        return self.colors.category10 * ((count // len(self.colors.category10)) + 1)[:count]
    
    def get_spacing_cm(self, spacing_key: str) -> float:
        """将间距转换为厘米（用于PPT）"""
        spacing_map = {
            'xxs': self.spacing.paddingXXS,
            'xs': self.spacing.paddingXS,
            'sm': self.spacing.paddingSM,
            'md': self.spacing.padding,
            'lg': self.spacing.paddingLG,
            'xl': self.spacing.paddingXL,
            'xxl': self.spacing.paddingXXL,
        }
        px = spacing_map.get(spacing_key.lower(), self.spacing.padding)
        # 转换为厘米 (1px ≈ 0.0264cm at 96dpi)
        return px * 0.0264
    
    def get_font_size_pt(self, size_key: str) -> int:
        """获取字号（转换为pt）
        
        注意：PPT中直接使用pt，不需要从px转换
        Ant Design的px值可以直接作为pt使用（在PPT中）
        """
        size_map = {
            'sm': self.typography.fontSizeSM,
            'base': self.typography.fontSize,
            'lg': self.typography.fontSizeLG,
            'xl': self.typography.fontSizeXL,
            'xxl': self.typography.fontSizeXXL,
            'h1': self.typography.fontSizeHeading1,
            'h2': self.typography.fontSizeHeading2,
            'h3': self.typography.fontSizeHeading3,
            'h4': self.typography.fontSizeHeading4,
            'h5': self.typography.fontSizeHeading5,
        }
        px = size_map.get(size_key.lower(), self.typography.fontSize)
        # PPT中直接使用px值作为pt（在屏幕显示中，1px ≈ 0.75pt，但PPT中通常直接使用）
        # 为了保持Ant Design的视觉效果，我们直接使用px值
        return int(px)


# 全局主题实例
ant_design_theme = AntDesignTheme()


```


## File: antv_chart_theme.py

```python
"""
AntV 图表设计规范集成
提供AntV/G2/G2Plot的图表配色和样式规范
"""

from typing import List, Dict, Any
from ant_design_theme import AntDesignTheme


class AntVChartTheme:
    """AntV 图表主题配置"""
    
    def __init__(self):
        self.ant_design = AntDesignTheme()
    
    def get_default_colors(self) -> List[str]:
        """获取AntV默认分类色（基于Ant Design）"""
        return self.ant_design.colors.category10
    
    def get_chart_style_config(self) -> Dict[str, Any]:
        """获取AntV图表样式配置"""
        return {
            # 基础样式
            "fontFamily": self.ant_design.typography.fontFamily,
            "fontSize": self.ant_design.typography.fontSize,
            
            # 颜色配置
            "defaultColor": self.ant_design.colors.colorPrimary,
            "category10": self.ant_design.colors.category10,
            
            # 背景色
            "backgroundColor": self.ant_design.colors.colorBgBase,
            
            # 网格线
            "gridLineStyle": {
                "stroke": self.ant_design.colors.colorBorderSecondary,
                "lineWidth": 1,
            },
            
            # 坐标轴
            "axisLabelStyle": {
                "fill": self.ant_design.colors.colorTextSecondary,
                "fontSize": self.ant_design.typography.fontSizeSM,
            },
            
            # 图例
            "legendStyle": {
                "fill": self.ant_design.colors.colorText,
                "fontSize": self.ant_design.typography.fontSizeSM,
            },
        }
    
    def get_bar_chart_colors(self, count: int = 1) -> List[str]:
        """获取柱状图颜色（使用Ant Design主色系）"""
        colors = self.ant_design.get_color_palette(count)
        return colors
    
    def get_pie_chart_colors(self, count: int = 1) -> List[str]:
        """获取饼图颜色"""
        return self.ant_design.get_color_palette(count)
    
    def get_line_chart_color(self) -> str:
        """获取折线图主色"""
        return self.ant_design.colors.colorPrimary


# 全局AntV主题实例
antv_chart_theme = AntVChartTheme()


```


## File: chart_generator.py

```python
"""
独立的图表生成模块
使用matplotlib生成各种类型的图表
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from loguru import logger

# 导入Ant Design和AntV主题
from ant_design_theme import ant_design_theme
from antv_chart_theme import antv_chart_theme

# 配置matplotlib使用Ant Design字体和样式
try:
    # Ant Design字体系统（优先中文字体，确保中文显示正常）
    plt.rcParams['font.sans-serif'] = [
        'Microsoft YaHei', 'SimHei',  # 中文字体优先
        '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 
        'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif'
    ]
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    plt.rcParams['font.size'] = ant_design_theme.typography.fontSize
except Exception:
    logger.warning("Failed to set Ant Design font, using default")


class ChartGenerator:
    """
    独立的图表生成器
    优先使用WebChartGenerator（无头浏览器+AntV），fallback到matplotlib
    """
    
    def __init__(self, output_dir: Optional[Path] = None, use_web: bool = True):
        """
        初始化图表生成器
        
        Args:
            output_dir: 图表输出目录
            use_web: 是否优先使用web渲染（Playwright + AntV），如果失败则fallback到matplotlib
        """
        if output_dir is None:
            output_dir = Path.cwd() / "charts"
        elif isinstance(output_dir, str):
            output_dir = Path(output_dir)
        
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.use_web = use_web
        
        # 尝试初始化WebChartGenerator
        self.web_generator = None
        if use_web:
            try:
                from web_chart_generator import WebChartGenerator
                self.web_generator = WebChartGenerator(output_dir=output_dir)
                logger.info("--- [ChartGenerator]: Using WebChartGenerator (Playwright + AntV)")
            except Exception as e:
                logger.warning(f"--- [ChartGenerator]: WebChartGenerator not available: {e}. Falling back to matplotlib")
                self.web_generator = None
        
        logger.info(f"--- [ChartGenerator]: Output directory: {self.output_dir}")
    
    def _prepare_data(self, data: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        准备数据，转换为DataFrame
        
        Args:
            data: 数据列表，每个元素是一个字典
            
        Returns:
            pandas DataFrame
        """
        if not data:
            raise ValueError("Data list is empty")
        
        return pd.DataFrame(data)
    
    def _save_chart(self, fig, filename: str, dpi: int = 300) -> str:
        """
        保存图表到文件
        
        Args:
            fig: matplotlib figure对象
            filename: 文件名
            dpi: 分辨率
            
        Returns:
            保存的文件路径
        """
        file_path = self.output_dir / filename
        fig.savefig(
            str(file_path),
            dpi=dpi,
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none'
        )
        plt.close(fig)  # 关闭图形以释放内存
        logger.info(f"--- [ChartGenerator]: Chart saved to {file_path}")
        return str(file_path)
    
    def generate_bar_chart(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Bar Chart",
        width: float = 10,
        height: float = 6,
        color: Optional[str] = None
    ) -> str:
        """
        生成柱状图
        优先使用WebChartGenerator（AntV），失败则使用matplotlib
        """
        # 尝试使用web渲染
        if self.web_generator:
            try:
                # 转换尺寸（matplotlib使用英寸，web使用像素）
                width_px = int(width * 96)  # 1英寸 = 96像素
                height_px = int(height * 96)
                return self.web_generator.generate_bar_chart(
                    data, x_key, y_key, title, width_px, height_px
                )
            except Exception as e:
                logger.warning(f"--- [ChartGenerator]: Web rendering failed: {e}. Using matplotlib fallback")
        
        # Fallback到matplotlib
        return self._generate_bar_chart_matplotlib(data, x_key, y_key, title, width, height, color)
    
    def _generate_bar_chart_matplotlib(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Bar Chart",
        width: float = 10,
        height: float = 6,
        color: Optional[str] = None
    ) -> str:
        """
        生成柱状图
        
        Args:
            data: 数据列表
            x_key: X轴数据键名
            y_key: Y轴数据键名
            title: 图表标题
            width: 图表宽度（英寸）
            height: 图表高度（英寸）
            color: 柱状图颜色
            
        Returns:
            保存的图表文件路径
        """
        # matplotlib实现
        df = self._prepare_data(data)
        
        # 使用AntV/Ant Design配色
        if color is None:
            color = antv_chart_theme.get_line_chart_color()
        
        # 如果是多系列，使用AntV分类色
        colors = antv_chart_theme.get_bar_chart_colors(len(df))
        
        fig, ax = plt.subplots(figsize=(width, height))
        
        # 应用Ant Design样式
        fig.patch.set_facecolor(ant_design_theme.colors.colorBgBase)
        ax.set_facecolor(ant_design_theme.colors.colorBgContainer)
        
        # 使用AntV配色方案
        if len(df) > 1:
            bars = ax.bar(df[x_key], df[y_key], color=colors[:len(df)], 
                         edgecolor=ant_design_theme.colors.colorBorder, linewidth=1)
        else:
            bars = ax.bar(df[x_key], df[y_key], color=color,
                         edgecolor=ant_design_theme.colors.colorBorder, linewidth=1)
        
        # 添加数值标签
        ax.bar_label(bars, padding=3)
        
        # 使用Ant Design字体和颜色
        ax.set_xlabel(x_key, fontsize=ant_design_theme.typography.fontSize, 
                     color=ant_design_theme.colors.colorText)
        ax.set_ylabel(y_key, fontsize=ant_design_theme.typography.fontSize,
                     color=ant_design_theme.colors.colorText)
        ax.set_title(title, fontsize=ant_design_theme.typography.fontSizeLG, 
                    fontweight='bold',
                    color=ant_design_theme.colors.colorText)
        
        # Ant Design网格样式
        ax.grid(axis='y', color=ant_design_theme.colors.colorBorderSecondary, 
               linestyle='-', linewidth=1, alpha=0.5)
        
        # 坐标轴颜色
        ax.spines['top'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['right'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['bottom'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['left'].set_color(ant_design_theme.colors.colorBorder)
        
        # 标签颜色
        ax.tick_params(colors=ant_design_theme.colors.colorTextSecondary)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        filename = f"bar_chart_{title.replace(' ', '_')}.png"
        return self._save_chart(fig, filename)
    
    def generate_line_chart(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Line Chart",
        width: float = 10,
        height: float = 6,
        color: Optional[str] = None
    ) -> str:
        """
        生成折线图
        优先使用WebChartGenerator（AntV），失败则使用matplotlib
        """
        if self.web_generator:
            try:
                width_px = int(width * 96)
                height_px = int(height * 96)
                return self.web_generator.generate_line_chart(
                    data, x_key, y_key, title, width_px, height_px
                )
            except Exception as e:
                logger.warning(f"--- [ChartGenerator]: Web rendering failed: {e}. Using matplotlib fallback")
        
        return self._generate_line_chart_matplotlib(data, x_key, y_key, title, width, height, color)
    
    def _generate_line_chart_matplotlib(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Line Chart",
        width: float = 10,
        height: float = 6,
        color: Optional[str] = None
    ) -> str:
        """
        生成折线图
        
        Args:
            data: 数据列表
            x_key: X轴数据键名
            y_key: Y轴数据键名
            title: 图表标题
            width: 图表宽度
            height: 图表高度
            color: 折线颜色
            
        Returns:
            保存的图表文件路径
        """
        # matplotlib实现
        df = self._prepare_data(data)
        df = df.sort_values(by=x_key)  # 按X轴排序
        
        # 使用AntV配色
        if color is None:
            color = antv_chart_theme.get_line_chart_color()
        
        fig, ax = plt.subplots(figsize=(width, height))
        
        # 应用Ant Design样式
        fig.patch.set_facecolor(ant_design_theme.colors.colorBgBase)
        ax.set_facecolor(ant_design_theme.colors.colorBgContainer)
        
        ax.plot(df[x_key], df[y_key], color=color, linewidth=2.5, 
               marker='o', markersize=6, markerfacecolor=color, 
               markeredgecolor=ant_design_theme.colors.colorBgBase,
               markeredgewidth=1)
        
        # 使用Ant Design字体和颜色
        ax.set_xlabel(x_key, fontsize=ant_design_theme.typography.fontSize,
                     color=ant_design_theme.colors.colorText)
        ax.set_ylabel(y_key, fontsize=ant_design_theme.typography.fontSize,
                     color=ant_design_theme.colors.colorText)
        ax.set_title(title, fontsize=ant_design_theme.typography.fontSizeLG,
                    fontweight='bold',
                    color=ant_design_theme.colors.colorText)
        
        # Ant Design网格样式
        ax.grid(True, color=ant_design_theme.colors.colorBorderSecondary,
               linestyle='-', linewidth=1, alpha=0.5)
        
        # 坐标轴样式
        ax.spines['top'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['right'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['bottom'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['left'].set_color(ant_design_theme.colors.colorBorder)
        ax.tick_params(colors=ant_design_theme.colors.colorTextSecondary)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        filename = f"line_chart_{title.replace(' ', '_')}.png"
        return self._save_chart(fig, filename)
    
    def generate_pie_chart(
        self,
        data: List[Dict[str, Any]],
        label_key: str,
        value_key: str,
        title: str = "Pie Chart",
        width: float = 10,
        height: float = 8
    ) -> str:
        """
        生成饼图
        
        Args:
            data: 数据列表
            label_key: 标签键名
            value_key: 数值键名
            title: 图表标题
            width: 图表宽度
            height: 图表高度
            
        Returns:
            保存的图表文件路径
        """
        # matplotlib实现
        df = self._prepare_data(data)
        
        # 使用AntV/Ant Design配色方案
        colors = antv_chart_theme.get_pie_chart_colors(len(df))
        
        fig, ax = plt.subplots(figsize=(width, height))
        
        # 应用Ant Design样式
        fig.patch.set_facecolor(ant_design_theme.colors.colorBgBase)
        
        wedges, texts, autotexts = ax.pie(
            df[value_key],
            labels=df[label_key],
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={
                'fontsize': ant_design_theme.typography.fontSizeSM,
                'color': ant_design_theme.colors.colorText
            },
            wedgeprops={'edgecolor': ant_design_theme.colors.colorBgBase, 'linewidth': 2}
        )
        
        # 设置百分比文本样式（Ant Design风格）
        for autotext in autotexts:
            autotext.set_color(ant_design_theme.colors.colorText)
            autotext.set_fontweight('bold')
        
        # 设置标签颜色
        for text in texts:
            text.set_color(ant_design_theme.colors.colorText)
            text.set_fontsize(ant_design_theme.typography.fontSizeSM)
        
        ax.set_title(title, fontsize=ant_design_theme.typography.fontSizeLG,
                    fontweight='bold',
                    color=ant_design_theme.colors.colorText, pad=20)
        plt.tight_layout()
        
        filename = f"pie_chart_{title.replace(' ', '_')}.png"
        return self._save_chart(fig, filename)
    
    def generate_grouped_bar_chart(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_keys: List[str],
        title: str = "Grouped Bar Chart",
        width: float = 12,
        height: float = 6
    ) -> str:
        """
        生成分组柱状图
        
        Args:
            data: 数据列表
            x_key: X轴数据键名
            y_keys: Y轴数据键名列表（多个系列）
            title: 图表标题
            width: 图表宽度
            height: 图表高度
            
        Returns:
            保存的图表文件路径
        """
        # matplotlib实现
        df = self._prepare_data(data)
        
        x = range(len(df))
        bar_width = 0.8 / len(y_keys)
        
        # 使用AntV/Ant Design配色方案
        colors = antv_chart_theme.get_bar_chart_colors(len(y_keys))
        
        fig, ax = plt.subplots(figsize=(width, height))
        
        # 应用Ant Design样式
        fig.patch.set_facecolor(ant_design_theme.colors.colorBgBase)
        ax.set_facecolor(ant_design_theme.colors.colorBgContainer)
        
        for i, y_key in enumerate(y_keys):
            offset = (i - len(y_keys) / 2 + 0.5) * bar_width
            bars = ax.bar(
                [xi + offset for xi in x],
                df[y_key],
                bar_width,
                label=y_key,
                color=colors[i % len(colors)],
                edgecolor=ant_design_theme.colors.colorBorder,
                linewidth=1
            )
            ax.bar_label(bars, padding=3, fontsize=ant_design_theme.typography.fontSizeSM,
                        color=ant_design_theme.colors.colorText)
        
        # 使用Ant Design样式
        ax.set_xlabel(x_key, fontsize=ant_design_theme.typography.fontSize,
                     color=ant_design_theme.colors.colorText)
        ax.set_ylabel('Value', fontsize=ant_design_theme.typography.fontSize,
                     color=ant_design_theme.colors.colorText)
        ax.set_title(title, fontsize=ant_design_theme.typography.fontSizeLG,
                    fontweight='bold',
                    color=ant_design_theme.colors.colorText)
        ax.set_xticks(x)
        ax.set_xticklabels(df[x_key], rotation=45, ha='right',
                          fontsize=ant_design_theme.typography.fontSizeSM,
                          color=ant_design_theme.colors.colorTextSecondary)
        ax.legend(loc='upper left', fontsize=ant_design_theme.typography.fontSizeSM,
                 frameon=True, fancybox=True, shadow=False,
                 framealpha=0.9, facecolor=ant_design_theme.colors.colorBgContainer,
                 edgecolor=ant_design_theme.colors.colorBorder)
        ax.grid(axis='y', color=ant_design_theme.colors.colorBorderSecondary,
               linestyle='-', linewidth=1, alpha=0.5)
        
        # 坐标轴样式
        ax.spines['top'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['right'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['bottom'].set_color(ant_design_theme.colors.colorBorder)
        ax.spines['left'].set_color(ant_design_theme.colors.colorBorder)
        ax.tick_params(colors=ant_design_theme.colors.colorTextSecondary)
        
        plt.tight_layout()
        
        filename = f"grouped_bar_chart_{title.replace(' ', '_')}.png"
        return self._save_chart(fig, filename)
    
    def generate_chart_from_insight(
        self,
        insight_details: Dict[str, Any],
        project_id: str = "fixer"
    ) -> Dict[str, Any]:
        """
        从数据洞察生成图表
        
        Args:
            insight_details: 数据洞察字典，包含：
                - insightId 或 insight_id: 洞察ID
                - type: 图表类型（bar_chart, line_chart, pie_chart, grouped_bar_chart）
                - title: 图表标题
                - data: 数据列表
                - x_key: X轴数据键名（可选，自动推断）
                - y_key: Y轴数据键名（可选，自动推断）
            project_id: 项目ID，用于组织输出目录
            
        Returns:
            包含 'chart_image_path' 和 'insight_id' 的字典，失败时包含 'error'
        """
        try:
            insight_id = insight_details.get("insightId") or insight_details.get("insight_id", "unknown")
            chart_type = insight_details.get("type", "bar_chart")
            title = insight_details.get("title", "Chart")
            data = insight_details.get("data", [])
            
            if not data:
                raise ValueError("Data is empty")
            
            # 自动推断键名（如果未提供）
            if isinstance(data[0], dict):
                keys = list(data[0].keys())
                x_key = insight_details.get("x_key", keys[0])
                y_key = insight_details.get("y_key", keys[1] if len(keys) > 1 else keys[0])
                y_keys = insight_details.get("y_keys", None)
            else:
                raise ValueError("Data must be a list of dictionaries")
            
            # 根据类型生成图表
            if chart_type == "bar_chart":
                chart_path = self.generate_bar_chart(data, x_key, y_key, title)
            elif chart_type == "line_chart":
                chart_path = self.generate_line_chart(data, x_key, y_key, title)
            elif chart_type == "pie_chart":
                chart_path = self.generate_pie_chart(data, x_key, y_key, title)
            elif chart_type == "grouped_bar_chart":
                if not y_keys:
                    # 如果没有指定y_keys，尝试从数据中推断
                    df = pd.DataFrame(data)
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    if x_key in numeric_cols:
                        numeric_cols.remove(x_key)
                    y_keys = numeric_cols[:3]  # 最多3个系列
                chart_path = self.generate_grouped_bar_chart(data, x_key, y_keys, title)
            else:
                # 默认使用柱状图
                logger.warning(f"Unknown chart type '{chart_type}', using bar_chart")
                chart_path = self.generate_bar_chart(data, x_key, y_key, title)
            
            return {
                "chart_image_path": chart_path,
                "insight_id": insight_id
            }
            
        except Exception as e:
            logger.error(f"--- [ChartGenerator]: Failed to generate chart: {e}", exc_info=True)
            return {
                "error": str(e),
                "insight_id": insight_details.get("insightId") or insight_details.get("insight_id", "unknown")
            }
    
    async def generate_charts_from_insights(
        self,
        insights: List[Dict[str, Any]],
        project_id: str = "fixer"
    ) -> Dict[str, str]:
        """
        批量生成图表
        
        Args:
            insights: 数据洞察列表
            project_id: 项目ID
            
        Returns:
            图表路径映射字典，键是insight_id，值是图表路径
        """
        chart_paths = {}
        
        for insight in insights:
            insight_id = insight.get("insightId") or insight.get("insight_id", "unknown")
            logger.info(f"--- [ChartGenerator]: Generating chart for insight: {insight_id}")
            
            result = self.generate_chart_from_insight(insight, project_id)
            
            if "error" in result:
                logger.error(f"--- [ChartGenerator]: Failed to generate chart for {insight_id}: {result['error']}")
            else:
                chart_paths[insight_id] = result["chart_image_path"]
                logger.success(f"--- [ChartGenerator]: Chart generated: {result['chart_image_path']}")
        
        return chart_paths


```


## File: chart_integrator.py

```python
"""
图表整合器
识别可可视化数据，生成图表，并插入到PPT
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from loguru import logger
from pptx import Presentation
from pptx.util import Cm

from chart_generator import ChartGenerator
from supporting_materials_analyzer import SupportingMaterialsAnalyzer


class ChartIntegrator:
    """
    图表整合器
    识别可可视化数据，生成图表，并插入到PPT
    """
    
    def __init__(
        self,
        chart_generator: Optional[ChartGenerator] = None,
        materials_analyzer: Optional[SupportingMaterialsAnalyzer] = None
    ):
        """
        初始化图表整合器
        
        Args:
            chart_generator: 图表生成器
            materials_analyzer: 支撑材料分析器
        """
        self.chart_generator = chart_generator or ChartGenerator()
        self.materials_analyzer = materials_analyzer
        logger.info("--- [ChartIntegrator]: 初始化图表整合器")
    
    async def integrate_charts(
        self,
        prs: Presentation,
        data_points: List[Dict[str, Any]],
        output_dir: Optional[Path] = None
    ) -> int:
        """
        整合图表到PPT
        
        Args:
            prs: PPT演示文稿对象
            data_points: 智能识别的数据点列表
            output_dir: 图表输出目录
            
        Returns:
            生成的图表数量
        """
        if not data_points:
            logger.info("--- [ChartIntegrator]: 无数据点，跳过图表生成")
            return 0
        
        logger.info(f"--- [ChartIntegrator]: 开始整合图表，数据点数量: {len(data_points)}")
        
        # 1. 识别可可视化数据
        if self.materials_analyzer:
            chartable_data = await self.materials_analyzer.identify_chartable_data(data_points)
        else:
            # Fallback: 简单判断
            chartable_data = self._simple_identify_chartable_data(data_points)
        
        if not chartable_data:
            logger.info("--- [ChartIntegrator]: 无适合可视化的数据")
            return 0
        
        logger.info(f"--- [ChartIntegrator]: 识别出{len(chartable_data)}个可可视化数据")
        
        # 2. 生成图表并插入到PPT
        chart_count = 0
        for chart_data in chartable_data:
            try:
                chart_path = self._generate_chart(chart_data, output_dir)
                if chart_path and chart_path.exists():
                    self._insert_chart_to_ppt(prs, chart_path, chart_data)
                    chart_count += 1
                    logger.info(f"--- [ChartIntegrator]: 成功插入图表到幻灯片{chart_data.get('slide_index', 0)}")
            except Exception as e:
                logger.warning(f"--- [ChartIntegrator]: 生成/插入图表失败: {e}")
        
        logger.info(f"--- [ChartIntegrator]: 共生成并插入{chart_count}个图表")
        return chart_count
    
    def _generate_chart(
        self,
        chart_data: Dict[str, Any],
        output_dir: Optional[Path] = None
    ) -> Optional[Path]:
        """
        生成图表
        
        Args:
            chart_data: 图表数据
            output_dir: 输出目录
            
        Returns:
            图表文件路径
        """
        chart_type = chart_data.get("chart_type", "bar")
        data = chart_data.get("data", [])
        title = chart_data.get("title", "图表")
        
        if not data:
            return None
        
        try:
            # 转换为图表生成器需要的格式
            chart_config = {
                "type": chart_type,
                "title": title,
                "data": data,
                "x_axis": chart_data.get("x_axis", ""),
                "y_axis": chart_data.get("y_axis", "")
            }
            
            # 生成图表（使用现有的方法）
            # 确保数据格式正确
            chart_data_list = []
            for item in data:
                if isinstance(item, dict):
                    chart_data_list.append(item)
                else:
                    # 如果是简单格式，转换为字典
                    chart_data_list.append({"label": str(item.get("label", "")), "value": float(item.get("value", 0))})
            
            if chart_type == "bar":
                chart_path = self.chart_generator.generate_bar_chart(
                    data=chart_data_list,
                    x_key="label",
                    y_key="value",
                    title=title
                )
            elif chart_type == "line":
                chart_path = self.chart_generator.generate_line_chart(
                    data=chart_data_list,
                    x_key="label",
                    y_key="value",
                    title=title
                )
            elif chart_type == "pie":
                chart_path = self.chart_generator.generate_pie_chart(
                    data=chart_data_list,
                    label_key="label",
                    value_key="value",
                    title=title
                )
            else:
                # 默认使用柱状图
                chart_path = self.chart_generator.generate_bar_chart(
                    data=chart_data_list,
                    x_key="label",
                    y_key="value",
                    title=title
                )
            
            if chart_path:
                chart_path_obj = Path(chart_path) if isinstance(chart_path, str) else chart_path
                return chart_path_obj
            return None
            
        except Exception as e:
            logger.error(f"--- [ChartIntegrator]: 生成图表失败: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return None
    
    def _insert_chart_to_ppt(
        self,
        prs: Presentation,
        chart_path: Path,
        chart_data: Dict[str, Any]
    ):
        """
        将图表插入到PPT
        
        Args:
            prs: PPT演示文稿对象
            chart_path: 图表文件路径
            chart_data: 图表数据（包含位置信息）
        """
        slide_index = chart_data.get("slide_index", 0)
        position = chart_data.get("recommended_position", {})
        
        # 确保幻灯片存在
        if slide_index >= len(prs.slides):
            logger.warning(f"--- [ChartIntegrator]: 幻灯片{slide_index}不存在，跳过")
            return
        
        slide = prs.slides[slide_index]
        
        # 获取位置信息（默认值）
        x = Cm(position.get("x", 10))
        y = Cm(position.get("y", 5))
        width = Cm(position.get("width", 15))
        height = Cm(position.get("height", 8))
        
        # 插入图表图片
        slide.shapes.add_picture(
            str(chart_path),
            x,
            y,
            width,
            height
        )
        
        logger.info(f"--- [ChartIntegrator]: 图表插入到幻灯片{slide_index}，位置: ({x}, {y}), 尺寸: {width} × {height}")
    
    def _simple_identify_chartable_data(
        self,
        data_points: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        简单识别可可视化数据（Fallback方法）
        
        Args:
            data_points: 数据点列表
            
        Returns:
            可可视化数据列表
        """
        # 简单策略：如果有3个或以上数据点，生成柱状图
        if len(data_points) >= 3:
            chart_data = {
                "chart_type": "bar",
                "data": [
                    {
                        "label": dp.get("label", dp.get("value", "")),
                        "value": self._extract_numeric_value(dp.get("value", ""))
                    }
                    for dp in data_points[:5]  # 最多5个数据点
                ],
                "title": "数据对比",
                "x_axis": "指标",
                "y_axis": "数值",
                "slide_index": data_points[0].get("slide_index", 0),
                "recommended_position": {
                    "x": 10,
                    "y": 5,
                    "width": 15,
                    "height": 8
                }
            }
            return [chart_data]
        
        return []
    
    def _extract_numeric_value(self, value_str: str) -> float:
        """
        从字符串中提取数值
        
        Args:
            value_str: 数值字符串（如"40-60%"、"50%"等）
            
        Returns:
            提取的数值
        """
        import re
        
        # 提取数字
        numbers = re.findall(r'\d+\.?\d*', value_str)
        if numbers:
            # 如果有范围，取平均值
            if len(numbers) >= 2:
                return (float(numbers[0]) + float(numbers[1])) / 2
            else:
                return float(numbers[0])
        
        return 0.0


```


## File: chinese_ppt_theme.py

```python
"""
中国述职PPT主题
融合Ant Design设计原则与中国述职PPT风格
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ChinesePPTColors:
    """中国述职PPT颜色系统（融合Ant Design间距原则）"""
    # 主色调（中国述职PPT常用）
    colorPrimary: str = "#d32f2f"  # 红色（权威、正式）
    colorAccent: str = "#ffb300"   # 金色（喜庆、重要）
    colorSecondary: str = "#1976d2"  # 深蓝（辅助、专业）
    
    # 文本色（基于Ant Design原则，但调整为中式风格）
    colorText: str = "#212121"      # 主文本（深灰，正式）
    colorTextSecondary: str = "#616161"  # 次文本（中灰）
    colorTextTertiary: str = "#9e9e9e"  # 辅助文本（浅灰）
    
    # 背景色（保持Ant Design的简洁原则）
    colorBgBase: str = "#ffffff"    # 基础背景（白色）
    colorBgContainer: str = "#fafafa"  # 容器背景（浅灰）
    colorBgLayout: str = "#f5f5f5"  # 布局背景（浅灰）
    
    # 边框色（保持Ant Design的简洁原则）
    colorBorder: str = "#e0e0e0"    # 基础边框（浅灰）
    colorBorderSecondary: str = "#f5f5f5"  # 次要边框（更浅）
    
    # 强调色（中国述职PPT常用）
    colorHighlight: str = "#ffb300"  # 高亮色（金色）
    colorWarning: str = "#ff9800"    # 警告色（橙色）
    colorSuccess: str = "#4caf50"   # 成功色（绿色）


@dataclass
class ChinesePPTTypography:
    """中国述职PPT字体系统"""
    # 标题字体（黑体、微软雅黑）
    fontFamilyHeading: str = "'Microsoft YaHei', 'SimHei', '黑体', 'Arial', sans-serif"
    
    # 正文字体（宋体、微软雅黑）
    fontFamilyBody: str = "'SimSun', '宋体', 'Microsoft YaHei', 'Arial', sans-serif"
    
    # 强调字体（楷体）
    fontFamilyEmphasis: str = "'KaiTi', '楷体', 'SimSun', serif"
    
    # 字号（基于Ant Design，但针对PPT优化）
    fontSizeHeading1: int = 76   # 主标题（PPT中约38pt）
    fontSizeHeading2: int = 60   # 副标题（PPT中约30pt）
    fontSizeHeading3: int = 48   # 三级标题（PPT中约24pt）
    fontSizeHeading4: int = 40   # 四级标题（PPT中约20pt）
    fontSizeHeading5: int = 32   # 五级标题（PPT中约16pt）
    fontSizeBody: int = 28       # 正文（PPT中约14pt）
    fontSizeSmall: int = 24      # 小号（PPT中约12pt）
    
    # 字重
    fontWeightStrong: int = 700  # 加粗（标题）
    fontWeight: int = 400        # 常规（正文）
    
    # 行高（基于Ant Design原则）
    lineHeight: float = 1.6      # 正文行高
    lineHeightHeading: float = 1.4  # 标题行高


@dataclass
class ChinesePPTSpacing:
    """中国述职PPT间距系统（基于Ant Design 8px原则）"""
    # 基础间距（基于8px）
    spacingXXS: int = 4   # 4px
    spacingXS: int = 8    # 8px
    spacingSM: int = 12   # 12px
    spacing: int = 16     # 16px
    spacingMD: int = 20   # 20px
    spacingLG: int = 24   # 24px
    spacingXL: int = 32   # 32px
    spacingXXL: int = 48  # 48px
    
    # 区块间距（中国述职PPT常用）
    sectionSpacing: int = 32  # 区块间距（32px）
    blockSpacing: int = 24    # 内容块间距（24px）


@dataclass
class ChinesePPTBorderRadius:
    """中国述职PPT圆角系统（保持Ant Design原则）"""
    borderRadius: int = 4      # 基础圆角（4px，比Ant Design稍小，更正式）
    borderRadiusSM: int = 2    # 小圆角（2px）
    borderRadiusLG: int = 6     # 大圆角（6px）


class ChinesePPTTheme:
    """中国述职PPT完整主题（融合Ant Design原则）"""
    
    def __init__(self):
        self.colors = ChinesePPTColors()
        self.typography = ChinesePPTTypography()
        self.spacing = ChinesePPTSpacing()
        self.borderRadius = ChinesePPTBorderRadius()
    
    def get_layout_mode(self, content_type: str) -> str:
        """
        根据内容类型获取布局模式
        
        Args:
            content_type: 内容类型（'title', 'content', 'summary'等）
            
        Returns:
            布局模式（'symmetric', 'hierarchical', 'centered'等）
        """
        layout_modes = {
            'title': 'centered',      # 标题页：居中
            'content': 'symmetric',   # 内容页：对称
            'summary': 'hierarchical', # 总结页：层次
            'default': 'symmetric'    # 默认：对称
        }
        return layout_modes.get(content_type, 'symmetric')
    
    def get_color_scheme(self, scheme_type: str = 'default') -> Dict[str, str]:
        """
        获取配色方案
        
        Args:
            scheme_type: 方案类型（'default', 'formal', 'warm'等）
            
        Returns:
            配色方案字典
        """
        schemes = {
            'default': {
                'primary': self.colors.colorPrimary,  # 红色
                'accent': self.colors.colorAccent,    # 金色
                'text': self.colors.colorText,        # 深灰
                'bg': self.colors.colorBgBase         # 白色
            },
            'formal': {
                'primary': '#1976d2',  # 深蓝（正式）
                'accent': '#424242',   # 深灰
                'text': '#212121',
                'bg': '#ffffff'
            },
            'warm': {
                'primary': '#ff6f00',  # 暖橙
                'accent': '#ffb300',   # 金色
                'text': '#212121',
                'bg': '#fff8e1'        # 浅黄
            }
        }
        return schemes.get(scheme_type, schemes['default'])


# 全局主题实例
chinese_ppt_theme = ChinesePPTTheme()


```


## File: cli.py

```python
#!/usr/bin/env python3
"""
Fixer CLI - PPT生成工具命令行接口
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

from ppt_generator import PPTGenerator
from vinci_integration import create_vinci_integration
from llm_service import create_llm_service
from layout_generator import create_layout_generator
from ppt_filler import PPTFiller


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
        description="Fixer - PPT生成工具，根据架构内容（VML计划）生成PPT文件",
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

```


## File: color_configurator.py

```python
"""
颜色配置器
为PPT内容配置符合Ant Design规范的颜色方案
"""

from typing import Dict, Any, List, Optional
from loguru import logger
from llm_service import LLMService, create_llm_service


class ColorConfigurator:
    """
    颜色配置器
    为润色后的内容和布局规划配置颜色方案
    """
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        初始化颜色配置器
        
        Args:
            llm_service: LLM服务实例
        """
        self.llm_service = llm_service or create_llm_service()
        logger.info("--- [ColorConfigurator]: 初始化颜色配置器")
    
    async def configure_colors(
        self,
        polished_slides: List[Dict[str, Any]],
        presentation_plans: List[Dict[str, Any]],
        layout_plans: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """
        为幻灯片配置颜色方案
        
        Args:
            polished_slides: 润色后的幻灯片列表
            presentation_plans: 展示策划结果列表
            layout_plans: 布局规划结果列表（可选）
            
        Returns:
            颜色配置结果列表，每个元素包含：
            - slide_index: 幻灯片索引
            - color_config: 颜色配置详情
                - overall_scheme: 整体配色方案描述
                - element_colors: 每个元素的颜色配置
                    - element_id: 元素ID
                    - text_color: 文本颜色（hex或rgba）
                    - background_color: 背景颜色（hex或rgba）
                    - border_color: 边框颜色（hex或rgba）
                    - accent_color: 强调色（hex或rgba，如有）
        """
        if not self.llm_service:
            logger.warning("   ⚠️ LLM服务不可用，使用默认颜色配置")
            return self._default_color_config(polished_slides)
        
        logger.info(f"--- [ColorConfigurator]: 开始颜色配置，共{len(polished_slides)}张幻灯片")
        
        # 读取设计规范中的颜色系统
        color_specs = self._load_color_specifications()
        
        color_configs = []
        
        for idx, (polished_slide, plan) in enumerate(zip(polished_slides, presentation_plans)):
            logger.info(f"--- [ColorConfigurator]: 配置幻灯片{idx + 1}的颜色...")
            
            try:
                color_config = await self._configure_single_slide(
                    polished_slide=polished_slide,
                    presentation_plan=plan,
                    layout_plan=layout_plans[idx] if layout_plans and idx < len(layout_plans) else None,
                    color_specs=color_specs
                )
                color_configs.append(color_config)
                logger.info(f"   ✅ 幻灯片{idx + 1}颜色配置完成")
            except Exception as e:
                logger.error(f"   ❌ 幻灯片{idx + 1}颜色配置失败: {e}", exc_info=True)
                # 使用默认配置
                default_config = self._default_single_slide_color(polished_slide, plan)
                color_configs.append(default_config)
        
        logger.info(f"--- [ColorConfigurator]: ✅ 颜色配置完成，共配置{len(color_configs)}张幻灯片")
        return color_configs
    
    async def _configure_single_slide(
        self,
        polished_slide: Dict[str, Any],
        presentation_plan: Dict[str, Any],
        layout_plan: Optional[Dict[str, Any]],
        color_specs: str
    ) -> Dict[str, Any]:
        """
        配置单张幻灯片的颜色
        
        Args:
            polished_slide: 润色后的幻灯片
            presentation_plan: 展示策划结果
            layout_plan: 布局规划结果（可选）
            color_specs: 颜色规范说明
            
        Returns:
            颜色配置结果
        """
        system_prompt = f"""你是一个专业的UI/UX设计师，精通Ant Design颜色系统。

你的任务是为PPT幻灯片配置符合Ant Design规范的颜色方案。

【Ant Design颜色系统】：
{color_specs}

【颜色配置要求】：
1. **遵循Ant Design颜色系统**：使用Ant Design定义的颜色值，不要使用自定义颜色
2. **建立视觉层次**：通过颜色建立清晰的视觉层次（标题、内容、数据等）
3. **保持一致性**：同一类型的元素使用相同的颜色方案
4. **避免红色**：根据用户要求，避免使用大红色（#F5222D），除非是错误提示
5. **高管汇报风格**：配色要专业、简洁、优雅，适合副总裁级别的汇报

【输出格式（JSON）】：
{{
  "slide_index": 幻灯片索引,
  "color_config": {{
    "overall_scheme": "整体配色方案描述（如：蓝色主色调，白色背景，深灰色文本）",
    "element_colors": [
      {{
        "element_id": "元素ID（如title_text_0）",
        "element_type": "元素类型（如title_text）",
        "text_color": "文本颜色（hex格式，如#1677FF或rgba格式）",
        "background_color": "背景颜色（hex格式，如#FFFFFF，如果是透明则用null）",
        "border_color": "边框颜色（hex格式，如#D9D9D9，如果没有边框则用null）",
        "accent_color": "强调色（hex格式，用于数据、图标等，可选）",
        "color_rationale": "颜色选择理由（简要说明为什么选择这些颜色）"
      }}
    ]
  }}
}}"""
        
        # 构建用户提示词
        slide_title = polished_slide.get('title', '')
        slide_content = polished_slide.get('content', '')
        slide_content_type = polished_slide.get('content_type', '')
        visual_elements = polished_slide.get('visual_elements_detail', [])
        layout_type = presentation_plan.get('layout_type', '')
        existing_color_scheme = presentation_plan.get('visual_guidance', {}).get('color_scheme', '')
        
        elements_info = []
        for elem in visual_elements:
            elem_id = elem.get('element_id', '')
            elem_type = elem.get('element_type', '')
            elem_title = elem.get('title', '')
            elem_data = elem.get('data', '')
            elements_info.append(f"- {elem_id} ({elem_type}): {elem_title}, 数据: {elem_data}")
        
        user_prompt = f"""请为以下幻灯片配置颜色方案。

幻灯片信息：
- 标题: {slide_title}
- 内容: {slide_content}
- 内容类型: {slide_content_type}
- 布局类型: {layout_type}
- 现有配色描述: {existing_color_scheme if existing_color_scheme else '无'}

视觉元素（共{len(visual_elements)}个）：
{chr(10).join(elements_info)}

请为每个视觉元素配置颜色，要求：
1. 标题元素：使用Ant Design主色（#1677FF）或深灰色（#262626），背景白色或透明
2. 内容文本：使用Ant Design主文本色（rgba(0,0,0,0.85)或#262626）
3. 卡片元素：背景白色（#FFFFFF），边框浅灰（#D9D9D9），文本深灰（#262626）
4. 数据元素：使用Ant Design主色（#1677FF）或成功色（#52C41A）突出显示
5. 图表元素：使用Ant Design分类色（colors10）
6. 避免使用大红色（#F5222D），除非是错误提示

请输出JSON格式的颜色配置。"""
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # 解析JSON响应
            import json
            import re
            
            if isinstance(response, str):
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    color_config = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用默认颜色配置")
                    return self._default_single_slide_color(polished_slide, presentation_plan)
            else:
                color_config = response
            
            # 确保包含slide_index
            color_config['slide_index'] = polished_slide.get('slide_index', 0)
            
            return color_config
            
        except Exception as e:
            logger.error(f"   颜色配置失败: {e}", exc_info=True)
            return self._default_single_slide_color(polished_slide, presentation_plan)
    
    def _default_single_slide_color(
        self,
        polished_slide: Dict[str, Any],
        presentation_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """默认单张幻灯片颜色配置"""
        visual_elements = polished_slide.get('visual_elements_detail', [])
        
        element_colors = []
        for elem in visual_elements:
            elem_id = elem.get('element_id', '')
            elem_type = elem.get('element_type', '')
            
            # 根据元素类型设置默认颜色
            if 'title' in elem_type:
                text_color = "#1677FF"  # Ant Design主色
                background_color = None  # 透明
                border_color = None
            elif 'content' in elem_type or 'subtitle' in elem_type:
                text_color = "rgba(0,0,0,0.85)"  # Ant Design主文本色
                background_color = None
                border_color = None
            elif 'card' in elem_type:
                text_color = "#262626"  # Ant Design主文本色
                background_color = "#FFFFFF"  # 白色
                border_color = "#D9D9D9"  # Ant Design边框色
            elif 'data' in elem_type or 'value' in elem_type:
                text_color = "#1677FF"  # Ant Design主色
                background_color = "#FFFFFF"
                border_color = "#D9D9D9"
            else:
                text_color = "rgba(0,0,0,0.85)"
                background_color = None
                border_color = None
            
            element_colors.append({
                "element_id": elem_id,
                "element_type": elem_type,
                "text_color": text_color,
                "background_color": background_color,
                "border_color": border_color,
                "accent_color": None,
                "color_rationale": "默认Ant Design配色"
            })
        
        return {
            "slide_index": polished_slide.get('slide_index', 0),
            "color_config": {
                "overall_scheme": "Ant Design标准配色：蓝色主色，白色背景，深灰色文本",
                "element_colors": element_colors
            }
        }
    
    def _default_color_config(
        self,
        polished_slides: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """默认颜色配置（回退方案）"""
        return [
            self._default_single_slide_color(slide, {})
            for slide in polished_slides
        ]
    
    def _load_color_specifications(self) -> str:
        """加载颜色规范说明"""
        try:
            from pathlib import Path
            design_file = Path(__file__).parent / "DESIGN_SYSTEM.md"
            if design_file.exists():
                content = design_file.read_text(encoding='utf-8')
                # 提取颜色系统部分（前200行左右）
                lines = content.split('\n')
                color_section = []
                in_color_section = False
                for i, line in enumerate(lines):
                    if '颜色系统' in line or 'Color' in line:
                        in_color_section = True
                    if in_color_section:
                        color_section.append(line)
                        if len(color_section) > 150:  # 提取前150行
                            break
                return '\n'.join(color_section)
        except Exception as e:
            logger.warning(f"   无法加载颜色规范文档: {e}")
        
        # 返回基础颜色规范
        return """【Ant Design颜色系统】：
- 主色调（Primary）：#1677FF（蓝色）
- 成功色（Success）：#52C41A（绿色）
- 警告色（Warning）：#FA8C16（橙色）
- 错误色（Error）：#F5222D（红色，避免使用）
- 文本主色：rgba(0,0,0,0.85) 或 #262626
- 文本次色：rgba(0,0,0,0.65) 或 #595959
- 背景色：#FFFFFF（白色），#F0F2F5（浅灰）
- 边框色：#D9D9D9（基础），#F0F0F0（次要）
- 分类色（用于图表）：['#1677FF', '#52C41A', '#FA8C16', '#F5222D', '#722ED1', '#13C2C2', '#EB2F96', '#FA541C', '#A0D911', '#2F54EB']"""


```


## File: content_polisher.py

```python
"""
内容润色模块
将文档内容润色成适合PPT展示的文案
"""

from typing import Dict, Any, List
from loguru import logger
from llm_service import LLMService
from presentation_schema import (
    PresentationProtocol,
    PolishedSlideSchema,
    ContentType
)
import json
import re


class ContentPolisher:
    """
    内容润色器
    将文档内容润色成适合PPT展示的文案
    """
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        logger.info("--- [ContentPolisher]: 初始化内容润色器")
    
    async def polish_section(
        self,
        section_analysis: Dict[str, Any],
        section_index: int
    ) -> List[Dict[str, Any]]:
        """
        润色板块内容，生成适合PPT展示的文案
        
        Args:
            section_analysis: 板块分析结果（包含主题、核心思想、内容摘要等）
            section_index: 板块索引
            
        Returns:
            润色后的幻灯片列表，每个元素包含：
            - slide_index: 幻灯片索引（在该板块内的索引）
            - title: 幻灯片标题
            - content: 幻灯片内容
            - content_type: 内容类型（title_page, content_page, data_page等）
            - notes: 备注（如需要表格、图表等）
        """
        logger.info(f"--- [ContentPolisher]: 润色板块{section_index}: {section_analysis.get('theme', '')}")
        
        # 获取Schema描述
        schema_desc = PresentationProtocol.get_schema_description()
        schema_json = json.dumps(schema_desc, ensure_ascii=False, indent=2)
        
        system_prompt = f"""你是中国职场的述职汇报专家，专门为副总裁级别的职场高管筹备述职内容，最擅长将高管整理的文稿大纲转换成适合呈现在ppt上的语言内容。

你具备强大的内容润色能力，能够将文档内容润色成适合PPT展示的文案。

【重要】PPT不是文字堆砌的展示平台，润色要求：
1. **简洁有力**：每张幻灯片只表达一个核心观点
2. **标题化**：将内容提炼成简洁的标题和副标题
3. **视觉化**：考虑如何用视觉元素（表格、图表、卡片等）展示内容
4. **层次化**：将复杂内容拆分成多张幻灯片，每张聚焦一个要点
5. **数据化**：识别需要数据支持的内容，标注需要表格/图表的位置
6. **详细展开**：当有多个视觉元素（如多个卡片、多个图表）时，必须详细展开每个元素的具体内容，不能只说"需要3个卡片"，而要说明每个卡片的具体标题、内容、数据等

【输出Schema规范】：
请严格按照以下Schema规范输出JSON格式的结果。核心字段必须包含，扩展字段可放在metadata中。

{schema_json}

【关键说明】：
- 必须使用JSON格式输出，包含"polished_slides"数组
- 每个slide必须包含：slide_index, title, content, content_type
- content_type必须是以下之一：{', '.join([e.value for e in ContentType])}
- visual_elements可以包含needs_table, needs_chart, needs_cards等标准字段，也可以添加自定义字段
- 如果需要扩展信息，请放在metadata字段中，使用snake_case命名"""
        
        user_prompt = f"""请对以下板块内容进行PPT展示层面的润色，生成适合PPT展示的文案。

板块信息：
- 板块主题：{section_analysis.get('theme', '')}
- 核心思想：{section_analysis.get('core_idea', '')}
- 内容摘要：{section_analysis.get('content_summary', '')}

请按照以下要求进行润色：
1. 将板块内容拆分成多张幻灯片（根据内容复杂度，通常2-4张）
2. 为每张幻灯片生成：
   - 简洁有力的标题（不超过15字）
   - 核心内容描述（1-2句话）
   - 内容类型（title_page标题页、content_page内容页、data_page数据页等）
   - 视觉元素需求（如需要表格、图表、卡片等，用占位符标注）

【润色示例】：
板块：技术产品概览与价值主张
内容摘要：介绍全链路AI赋能解决方案，核心价值主张包括降低运营成本40-60%、提升转化效率20-35%、加速业务智能化转型。包含25年技术回顾，涵盖朋友云、AI平台和数据中心的成果展示

润色结果：
幻灯片1：
- 标题：技术产品概述与价值主张
- 内容类型：title_page（标题页，空白模板，页面正中间加粗、放大显示）
- 视觉元素：无

幻灯片2：
- 标题：产品核心价值 —— 全链路AI赋能解决方案
- 内容类型：content_page（内容页，页面正中间加粗、放大显示）
- 视觉元素：无

幻灯片3：
- 标题：技术成果展示
- 内容：25年技术回顾，涵盖朋友云、AI平台和数据中心的成果展示
- 内容类型：data_page（数据页，需要表格/图表展示）
- 视觉元素：需要表格数据，但检索当前文档无相关数据，使用占位符保留位置

幻灯片4：
- 标题：技术产品落地效果
- 内容：降低运营成本40-60%、提升转化效率20-35%、加速业务智能化转型
- 内容类型：content_page（内容页，用圆角矩形卡片展示）
- 视觉元素：三个圆角矩形分别包裹三个系统内容，下方用居中的数字/文字展示提升数据
- 视觉元素详细展开（必须包含所有元素，包括标题和内容）：
  * 元素0 (ID: title_text_0, 类型: title_text)：技术产品落地效果
    - 内容: 幻灯片标题
    - 说明: 标题文本，用于标识幻灯片主题
  * 元素1 (ID: content_text_0, 类型: content_text)：降低运营成本40-60%、提升转化效率20-35%、加速业务智能化转型
    - 内容: 幻灯片内容描述
    - 说明: 内容文本，概述幻灯片核心信息
  * 元素2 (ID: value_card_0, 类型: value_card)：降本
    - 内容: 运营成本降低40-60%
    - 数据: 40-60%
    - 说明: 通过自动化流程和智能优化实现运营成本大幅降低
  * 元素3 (ID: value_card_1, 类型: value_card)：增效
    - 内容: 转化效率提升20-35%
    - 数据: 20-35%
    - 说明: 通过AI技术提升转化效率
  * 元素4 (ID: value_card_2, 类型: value_card)：转型
    - 内容: 加速业务智能化转型
    - 数据: 智能化
    - 说明: 推动业务向智能化方向转型

请以JSON格式输出润色结果：
{{
  "polished_slides": [
    {{
      "slide_index": 在该板块内的索引（从0开始）,
      "title": "幻灯片标题",
      "content": "幻灯片核心内容（1-2句话）",
      "content_type": "title_page|content_page|data_page|effect_page",
      "visual_elements": {{
        "needs_table": true/false,
        "needs_chart": true/false,
        "needs_cards": true/false,
        "needs_placeholder": true/false,
        "notes": "视觉元素说明（如：需要三个圆角矩形卡片）"
      }},
      "visual_elements_detail": [
        {{
          "element_index": 元素索引（从0开始）,
          "element_id": "元素唯一标识（格式：element_type_element_index，如value_card_0、product_card_1等，用于唯一标识每个元素，避免传参混淆）",
          "element_type": "元素类型（必须根据元素的具体用途命名，不能都用'card'，应该用：value_card|product_card|advantage_card|data_card|feature_card|trend_card|strategy_card|chart|table|text|icon等）",
          "title": "元素标题（如卡片标题）",
          "content": "元素内容描述",
          "data": "元素数据（如有）",
          "description": "元素详细说明"
        }},
        ...
      ]
    }},
    ...
  ]
}}

【关键要求】：
- **重要**：每张幻灯片的所有内容元素都必须展开，包括：
  * 标题文本（title_text）：幻灯片的标题，必须作为独立元素
  * 内容文本（content_text）：幻灯片的内容描述，必须作为独立元素
  * 视觉元素（cards、charts等）：所有视觉元素都必须展开
- visual_elements_detail必须包含幻灯片上的所有元素，不能遗漏：
  * 元素0通常是title_text（标题文本）
  * 元素1通常是content_text（内容文本）
  * 元素2+是各种视觉元素（cards、charts等）
- 每个元素都要有element_index、element_id、element_type、title、content
- element_id格式：element_type_element_index（如title_text_0、content_text_0、value_card_0、product_card_1），用于唯一标识，避免传参混淆
- element_type必须根据元素的具体用途命名：
    - title_text：标题文本（幻灯片的标题）
    - content_text：内容文本（幻灯片的内容描述）
    - subtitle_text：副标题文本（如有）
    - value_card：价值卡片（展示价值主张、效益等）
    - product_card：产品卡片（展示产品、系统等）
    - advantage_card：优势卡片（展示竞争优势、特点等）
    - data_card：数据卡片（展示数据指标、统计等）
    - feature_card：功能卡片（展示功能特性等）
    - trend_card：趋势卡片（展示趋势、方向等）
    - strategy_card：策略卡片（展示策略、方案等）
    - chart：图表
    - table：表格
    - icon：图标
- 如果有数据，必须包含data字段
- 每个元素都要有清晰的description说明其具体作用
- 示例：一张包含标题、内容和3个卡片的幻灯片，visual_elements_detail应该包含5个元素：
  * 元素0 (title_text_0)：标题文本
  * 元素1 (content_text_0)：内容文本
  * 元素2 (value_card_0)：第一个卡片
  * 元素3 (value_card_1)：第二个卡片
  * 元素4 (value_card_2)：第三个卡片"""
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # 解析JSON响应
            if isinstance(response, str):
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    raw_result = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用默认润色")
                    return self._default_polish(section_analysis)
            else:
                raw_result = response
            
            # 规范化LLM输出
            normalized_result = PresentationProtocol.normalize_llm_output(raw_result)
            polished_slides = normalized_result.get("polished_slides", [])
            
            # 验证每个slide
            validated_slides = []
            for slide in polished_slides:
                if PresentationProtocol.validate_polished_slide(slide):
                    validated_slides.append(slide)
                else:
                    logger.warning(f"   幻灯片数据不符合Schema，跳过: {slide}")
            
            if not validated_slides:
                logger.warning("   没有有效的润色结果，使用默认润色")
                return self._default_polish(section_analysis)
            
            logger.info(f"   ✅ 润色完成，生成{len(validated_slides)}张幻灯片")
            for slide in validated_slides:
                logger.info(f"      幻灯片{slide.get('slide_index', 0)}: {slide.get('title', '')} ({slide.get('content_type', '')})")
            
            return validated_slides
        except Exception as e:
            logger.error(f"   ❌ 润色失败: {e}，使用默认润色", exc_info=True)
            return self._default_polish(section_analysis)
    
    def _default_polish(self, section_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """默认润色（回退方案）"""
        return [{
            "slide_index": 0,
            "title": section_analysis.get("theme", "未命名板块"),
            "content": section_analysis.get("content_summary", ""),
            "content_type": "content_page",
            "visual_elements": {
                "needs_table": False,
                "needs_chart": False,
                "needs_cards": False,
                "needs_placeholder": False,
                "notes": ""
            }
        }]


```


## File: content_strategy_generator.py

```python
"""
内容生成策略制定器
根据人类中心化分析结果，制定内容生成策略
"""

from typing import Dict, Any, List
from loguru import logger


class ContentStrategyGenerator:
    """
    内容生成策略制定器
    根据人类中心化分析结果，制定整体策略和板块策略
    """
    
    def __init__(self, human_analysis: Dict[str, Any]):
        """
        初始化策略生成器
        
        Args:
            human_analysis: 人类中心化分析结果
        """
        self.analysis = human_analysis
        logger.info("--- [ContentStrategyGenerator]: 初始化内容生成策略制定器")
    
    def generate_strategy(self) -> Dict[str, Any]:
        """
        生成完整的内容生成策略
        
        Returns:
            包含整体策略和板块策略的字典
        """
        logger.info("--- [ContentStrategyGenerator]: 开始生成内容生成策略")
        
        # 1. 生成整体策略
        overall_strategy = self._generate_overall_strategy()
        
        # 2. 生成板块策略
        section_strategies = self._generate_section_strategies()
        
        # 3. 生成表达风格策略
        expression_strategy = self._generate_expression_strategy()
        
        strategy = {
            "overall_strategy": overall_strategy,
            "section_strategies": section_strategies,
            "expression_strategy": expression_strategy
        }
        
        logger.info(f"--- [ContentStrategyGenerator]: 策略生成完成")
        logger.info(f"   整体策略: {overall_strategy.get('core_theme', '')}")
        logger.info(f"   板块策略数: {len(section_strategies)}")
        
        return strategy
    
    def _generate_overall_strategy(self) -> Dict[str, Any]:
        """生成整体策略"""
        layer_1 = self.analysis.get("layer_1_overall_understanding", {}).get("data", {})
        layer_5 = self.analysis.get("layer_5_expression_style", {}).get("data", {})
        
        return {
            "core_theme": layer_1.get("core_theme", ""),
            "value_propositions": layer_1.get("value_propositions", []),
            "purpose": layer_1.get("purpose", "通用文档"),
            "target_audience": layer_1.get("target_audience", "通用受众"),
            "tone": layer_5.get("tone", "中性"),
            "formality_level": layer_5.get("formality_level", "中性"),
            "key_phrases": layer_1.get("key_phrases", [])
        }
    
    def _generate_section_strategies(self) -> List[Dict[str, Any]]:
        """生成板块策略（详细探针）"""
        logger.info("--- [ContentStrategyGenerator]: 【详细探针】生成板块策略")
        
        sections = self.analysis.get("layer_2_sections", {}).get("data", {}).get("sections", [])
        arguments = self.analysis.get("layer_3_arguments", {}).get("data", {}).get("arguments", [])
        
        logger.info(f"   识别到{len(sections)}个板块")
        logger.info(f"   识别到{len(arguments)}个论证逻辑")
        
        section_strategies = []
        
        for section in sections:
            section_idx = section.get("section_index", 0)
            logger.info(f"\n   处理板块{section_idx}:")
            logger.info(f"     主题: {section.get('theme', '')}")
            logger.info(f"     核心思想: {section.get('core_idea', '')[:100]}...")
            logger.info(f"     分配的幻灯片: {section.get('slides', [])}")
            
            # 找到对应的论证逻辑
            section_args = next(
                (arg for arg in arguments if arg.get("section_index") == section_idx),
                {}
            )
            
            if section_args:
                logger.info(f"     论证类型: {section_args.get('argument_types', [])}")
                logger.info(f"     证据点数量: {len(section_args.get('evidence_points', []))}")
            else:
                logger.warning(f"     ⚠️ 未找到对应的论证逻辑")
            
            # 生成板块策略
            strategy = {
                "section_index": section_idx,
                "theme": section.get("theme", ""),
                "core_idea": section.get("core_idea", ""),
                "slides": section.get("slides", []),
                "argument_types": section_args.get("argument_types", []),
                "evidence_points": section_args.get("evidence_points", []),
                "content_generation_approach": self._determine_content_approach(
                    section, section_args
                )
            }
            
            logger.info(f"     内容生成方式: {strategy['content_generation_approach']}")
            
            section_strategies.append(strategy)
        
        logger.info(f"\n   生成完成，共{len(section_strategies)}个板块策略")
        
        return section_strategies
    
    def _determine_content_approach(self, section: Dict, arguments: Dict) -> Dict[str, Any]:
        """确定内容生成方法"""
        argument_types = arguments.get("argument_types", [])
        evidence_points = arguments.get("evidence_points", [])
        
        # 根据论证类型确定重点
        if "数据论证" in argument_types:
            emphasis = "数据支撑"
            evidence_priority = ["数据", "图表"]
        elif "案例论证" in argument_types:
            emphasis = "案例说明"
            evidence_priority = ["案例", "客户反馈"]
        elif "对比论证" in argument_types:
            emphasis = "对比分析"
            evidence_priority = ["对比数据", "优势说明"]
        else:
            emphasis = "核心观点"
            evidence_priority = ["论据", "说明"]
        
        # 根据内容长度确定生成长度
        content_summary = section.get("content_summary", "")
        if len(content_summary) > 200:
            length = "long"
        elif len(content_summary) > 100:
            length = "medium"
        else:
            length = "short"
        
        return {
            "emphasis": emphasis,
            "evidence_priority": evidence_priority,
            "length": length
        }
    
    def _generate_expression_strategy(self) -> Dict[str, Any]:
        """生成表达风格策略"""
        layer_5 = self.analysis.get("layer_5_expression_style", {}).get("data", {})
        layer_6 = self.analysis.get("layer_6_presentation_form", {}).get("data", {})
        
        formality = layer_5.get("formality_level", "中性")
        tone = layer_5.get("tone", "中性")
        cultural_features = layer_5.get("cultural_features", [])
        
        # 根据正式程度确定字体大小
        if formality == "正式":
            title_font_size = 40
            body_font_size = 15
        elif formality == "非正式":
            title_font_size = 36
            body_font_size = 14
        else:
            title_font_size = 38
            body_font_size = 14
        
        # 根据语调确定颜色
        if tone == "积极":
            primary_color = "primary"  # Ant Design蓝色
            accent_color = "success"   # 绿色
        elif tone == "谨慎":
            primary_color = "warning"  # 橙色
            accent_color = "error"     # 红色
        else:
            primary_color = "text_primary"  # 黑色
            accent_color = "primary"        # 蓝色
        
        return {
            "language_style": {
                "formality": formality,
                "tone": tone,
                "cultural_features": cultural_features
            },
            "visual_style": {
                "layout": layer_6.get("layout_style", {}).get("aspect_ratio", "16:9"),
                "typography": {
                    "title_font_size": title_font_size,
                    "body_font_size": body_font_size,
                    "font_family": "Segoe UI, 微软雅黑, Arial"
                },
                "color_scheme": {
                    "primary": primary_color,
                    "accent": accent_color
                }
            }
        }
    
    def build_generation_prompt(self, section_strategy: Dict[str, Any], strategy: Dict[str, Any]) -> str:
        """
        构建内容生成提示词
        
        Args:
            section_strategy: 板块策略
            
        Returns:
            生成提示词字符串
        """
        overall = strategy.get("overall_strategy", {})
        expression = strategy.get("expression_strategy", {})
        approach = section_strategy.get("content_generation_approach", {})
        
        prompt = f"""
根据以下信息，生成符合中国商业汇报习惯的PPT内容：

【整体背景】
核心主题：{overall.get("core_theme", "")}
目标受众：{overall.get("target_audience", "")}
文档目的：{overall.get("purpose", "")}

【板块信息】
板块主题：{section_strategy.get("theme", "")}
核心思想：{section_strategy.get("core_idea", "")}

【论证方式】
{", ".join(section_strategy.get("argument_types", []))}

【证据点】
{self._format_evidence_points(section_strategy.get("evidence_points", []))}

【生成要求】
1. 语言风格：{expression.get("language_style", {}).get("formality", "中性")}，语调：{expression.get("language_style", {}).get("tone", "中性")}
2. 强调重点：{approach.get("emphasis", "")}
3. 优先使用：{", ".join(approach.get("evidence_priority", []))}
4. 内容长度：{approach.get("length", "medium")}
5. 符合中国商业文化：{", ".join(expression.get("language_style", {}).get("cultural_features", []))}

【价值主张】
{", ".join(overall.get("value_propositions", []))}

请生成：
- 标题（简洁有力，体现核心思想，不超过20字）
- 正文内容（包含论据和证据点，{approach.get("length", "medium")}长度）
- 数据支撑（如果有，突出显示）
- 案例说明（如果有，简洁明了）

要求：
- 语言符合中国商业汇报习惯
- 逻辑清晰，有说服力
- 突出价值主张
- 使用数据支撑观点
"""
        return prompt
    
    def _format_evidence_points(self, evidence_points: List[str]) -> str:
        """格式化证据点"""
        if not evidence_points:
            return "无"
        
        formatted = []
        for i, point in enumerate(evidence_points[:5], 1):  # 最多5个
            formatted.append(f"{i}. {point}")
        
        return "\n".join(formatted)


```


## File: create_framework_ppt.py

```python
#!/usr/bin/env python3
"""
创建示例PPT框架文件
用于演示框架填充功能
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_framework_ppt():
    """创建一个包含占位符的PPT框架（16:9横版）"""
    from pptx.util import Cm
    
    prs = Presentation()
    # 16:9 横版尺寸 (33.867cm x 19.05cm)
    prs.slide_width = Cm(33.867)
    prs.slide_height = Cm(19.05)
    
    # 第1张幻灯片 - 标题页
    slide1 = prs.slides.add_slide(prs.slide_layouts[0])  # Title slide layout
    
    # 获取标题和副标题占位符
    title_shape = slide1.shapes.title
    subtitle_shape = slide1.placeholders[1]
    
    # 设置占位符提示文本（这些会被LLM生成的内容替换）
    title_shape.text = "[标题占位符]"
    subtitle_shape.text = "[副标题占位符]"
    
    # 第2张幻灯片 - 内容页
    slide2 = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content layout
    
    title_shape2 = slide2.shapes.title
    content_shape2 = slide2.placeholders[1]
    
    title_shape2.text = "[内容页标题]"
    content_shape2.text = "[内容占位符]\n\n这里可以添加详细内容..."
    
    # 第3张幻灯片 - 空白页（用于自定义布局）
    slide3 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    
    # 添加标题文本框
    title_box = slide3.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1))
    title_frame = title_box.text_frame
    title_frame.text = "[自定义标题]"
    title_frame.paragraphs[0].font.size = Pt(32)
    title_frame.paragraphs[0].font.bold = True
    
    # 添加内容文本框
    content_box = slide3.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(4))
    content_frame = content_box.text_frame
    content_frame.text = "[自定义内容占位符]\n\n可以在这里添加更多内容..."
    content_frame.paragraphs[0].font.size = Pt(18)
    
    # 保存文件
    output_path = "framework_template.pptx"
    prs.save(output_path)
    print(f"✓ 框架PPT已创建: {output_path}")
    print(f"  - 包含 {len(prs.slides)} 张幻灯片")
    print(f"  - 包含多个占位符，等待填充")
    
    return output_path

if __name__ == "__main__":
    create_framework_ppt()


```


## File: deep_analyze_demo_docx.py

```python
#!/usr/bin/env python3
"""
深度分析Demo文档.docx - 通过内容语义和格式识别层次结构
"""

import json
from docx import Document
from pathlib import Path
import re

def deep_analyze_docx(docx_path: str):
    """深度分析docx文档，识别所有可能的层次"""
    
    doc = Document(docx_path)
    
    analysis = {
        "file_info": {
            "path": docx_path,
            "size_bytes": Path(docx_path).stat().st_size
        },
        "layers": {}
    }
    
    # ========== 层次1: 物理结构层 ==========
    physical_structure = {
        "total_paragraphs": len(doc.paragraphs),
        "total_tables": len(doc.tables),
        "total_sections": len(doc.sections),
        "paragraphs_by_style": {},
        "paragraphs_by_format": {
            "bold_paragraphs": [],
            "large_font_paragraphs": [],
            "indented_paragraphs": []
        }
    }
    
    for para_idx, para in enumerate(doc.paragraphs):
        style_name = para.style.name if para.style else "Unknown"
        if style_name not in physical_structure["paragraphs_by_style"]:
            physical_structure["paragraphs_by_style"][style_name] = []
        physical_structure["paragraphs_by_style"][style_name].append({
            "text": para.text[:100],
            "index": para_idx
        })
        
        # 检查格式特征
        max_font_size = 0
        has_bold = False
        for run in para.runs:
            if run.font.size and run.font.size.pt:
                max_font_size = max(max_font_size, run.font.size.pt)
            if run.bold:
                has_bold = True
        
        if has_bold:
            physical_structure["paragraphs_by_format"]["bold_paragraphs"].append({
                "text": para.text[:100],
                "index": para_idx
            })
        
        if max_font_size >= 20:
            physical_structure["paragraphs_by_format"]["large_font_paragraphs"].append({
                "text": para.text[:100],
                "font_size": max_font_size,
                "index": para_idx
            })
    
    analysis["layers"]["layer_1_physical"] = {
        "name": "物理结构层",
        "description": "文档的物理结构：段落、表格、章节等",
        "data": physical_structure
    }
    
    # ========== 层次2: 格式特征层 ==========
    format_features = {
        "font_sizes": set(),
        "font_names": set(),
        "bold_runs": [],
        "italic_runs": [],
        "colored_runs": [],
        "paragraph_formats": []
    }
    
    for para in doc.paragraphs:
        para_format = {
            "text": para.text[:50],
            "alignment": str(para.alignment) if para.alignment else None,
            "left_indent": para.paragraph_format.left_indent.pt if para.paragraph_format.left_indent else 0,
            "first_line_indent": para.paragraph_format.first_line_indent.pt if para.paragraph_format.first_line_indent else 0,
            "space_before": para.paragraph_format.space_before.pt if para.paragraph_format.space_before else 0,
            "space_after": para.paragraph_format.space_after.pt if para.paragraph_format.space_after else 0
        }
        format_features["paragraph_formats"].append(para_format)
        
        for run in para.runs:
            if run.font.size and run.font.size.pt:
                format_features["font_sizes"].add(run.font.size.pt)
            if run.font.name:
                format_features["font_names"].add(run.font.name)
            if run.bold and run.text.strip():
                format_features["bold_runs"].append({
                    "text": run.text[:50],
                    "font_size": run.font.size.pt if run.font.size and run.font.size.pt else None
                })
            if run.italic and run.text.strip():
                format_features["italic_runs"].append(run.text[:50])
            if run.font.color and run.font.color.rgb:
                format_features["colored_runs"].append(run.text[:50])
    
    format_features["font_sizes"] = sorted(list(format_features["font_sizes"]))
    format_features["font_names"] = list(format_features["font_names"])
    
    analysis["layers"]["layer_2_format"] = {
        "name": "格式特征层",
        "description": "文本格式特征：字体、字号、加粗、颜色、缩进等",
        "data": format_features
    }
    
    # ========== 层次3: 内容语义层 ==========
    semantic_blocks = []
    current_block = None
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        # 判断是否为标题（通过格式特征）
        is_heading = False
        heading_level = 0
        
        # 检查1: 字体大小（大字体可能是标题）
        max_font_size = 0
        has_bold = False
        for run in para.runs:
            if run.font.size and run.font.size.pt:
                max_font_size = max(max_font_size, run.font.size.pt)
            if run.bold:
                has_bold = True
        
        # 检查2: 文本长度（短文本可能是标题）
        is_short = len(text) < 50
        
        # 检查3: 是否包含数字编号（如"1. "、"一、"等）
        has_numbering = bool(re.match(r'^[\d一二三四五六七八九十]+[\.、]', text))
        
        # 检查4: 是否全为加粗
        all_bold = all(run.bold for run in para.runs if run.text.strip())
        
        # 综合判断
        if (max_font_size >= 20 and has_bold) or (is_short and all_bold) or has_numbering:
            is_heading = True
            if max_font_size >= 24:
                heading_level = 1
            elif max_font_size >= 18:
                heading_level = 2
            else:
                heading_level = 3
            
            # 保存之前的块
            if current_block:
                semantic_blocks.append(current_block)
            
            # 开始新块
            current_block = {
                "heading": text,
                "heading_level": heading_level,
                "heading_format": {
                    "font_size": max_font_size,
                    "is_bold": has_bold,
                    "has_numbering": has_numbering
                },
                "content": []
            }
        else:
            # 添加到当前块的内容
            if current_block:
                current_block["content"].append({
                    "text": text,
                    "font_size": max_font_size,
                    "is_bold": has_bold
                })
            else:
                # 如果没有标题，创建一个匿名块
                current_block = {
                    "heading": None,
                    "heading_level": 0,
                    "content": [{
                        "text": text,
                        "font_size": max_font_size,
                        "is_bold": has_bold
                    }]
                }
    
    # 保存最后一个块
    if current_block:
        semantic_blocks.append(current_block)
    
    analysis["layers"]["layer_3_semantic"] = {
        "name": "内容语义层",
        "description": "基于内容语义和格式特征识别的标题-内容块结构",
        "data": {
            "total_blocks": len(semantic_blocks),
            "blocks": semantic_blocks
        }
    }
    
    # ========== 层次4: 列表结构层 ==========
    list_structure = {
        "numbered_lists": [],
        "bullet_lists": [],
        "indented_items": []
    }
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        
        # 检查编号列表
        numbered_match = re.match(r'^[\d一二三四五六七八九十]+[\.、]\s*(.+)', text)
        if numbered_match:
            list_structure["numbered_lists"].append({
                "number": numbered_match.group(1) if numbered_match.group(1) else text[0],
                "content": numbered_match.group(2) if len(numbered_match.groups()) > 1 else text,
                "full_text": text
            })
        
        # 检查项目符号
        bullet_match = re.match(r'^[•·▪▫○●■□]\s*(.+)', text)
        if bullet_match:
            list_structure["bullet_lists"].append({
                "bullet": text[0],
                "content": bullet_match.group(1),
                "full_text": text
            })
        
        # 检查缩进（可能是列表）
        if para.paragraph_format.left_indent and para.paragraph_format.left_indent.pt > 0:
            list_structure["indented_items"].append({
                "text": text[:100],
                "indent_pt": para.paragraph_format.left_indent.pt
            })
    
    analysis["layers"]["layer_4_lists"] = {
        "name": "列表结构层",
        "description": "文档中的列表结构：编号列表、项目符号、缩进列表",
        "data": list_structure
    }
    
    # ========== 层次5: 表格数据层 ==========
    table_analysis = []
    for i, table in enumerate(doc.tables):
        table_info = {
            "index": i,
            "rows": len(table.rows),
            "columns": len(table.columns) if table.rows else 0,
            "structure": [],
            "header_row": None,
            "data_rows": []
        }
        
        for row_idx, row in enumerate(table.rows):
            row_data = [cell.text.strip() for cell in row.cells]
            table_info["structure"].append(row_data)
            
            # 第一行通常是表头
            if row_idx == 0:
                table_info["header_row"] = row_data
            else:
                table_info["data_rows"].append({
                    "row_index": row_idx,
                    "data": row_data
                })
        
        table_analysis.append(table_info)
    
    analysis["layers"]["layer_5_tables"] = {
        "name": "表格数据层",
        "description": "文档中的表格结构和数据",
        "data": table_analysis
    }
    
    # ========== 层次6: 主题/话题层 ==========
    # 通过关键词和内容聚类识别主题
    topics = {}
    keywords_patterns = {
        "业务相关": ["业务", "销售", "客户", "市场", "产品"],
        "技术相关": ["技术", "系统", "平台", "开发", "实现"],
        "管理相关": ["管理", "流程", "规范", "制度", "标准"],
        "数据相关": ["数据", "分析", "统计", "报表", "指标"]
    }
    
    for block in semantic_blocks:
        block_text = block["heading"] or ""
        if block["content"]:
            block_text += " " + " ".join([c["text"] for c in block["content"][:3]])
        
        for topic, keywords in keywords_patterns.items():
            if any(keyword in block_text for keyword in keywords):
                if topic not in topics:
                    topics[topic] = []
                topics[topic].append({
                    "heading": block["heading"],
                    "content_preview": [c["text"][:50] for c in block["content"][:2]]
                })
                break
    
    analysis["layers"]["layer_6_topics"] = {
        "name": "主题/话题层",
        "description": "基于关键词识别的内容主题分类",
        "data": topics
    }
    
    # ========== 层次7: 逻辑关系层 ==========
    # 识别内容之间的逻辑关系
    logical_relations = {
        "sequential": [],  # 顺序关系
        "hierarchical": [],  # 层级关系
        "comparative": []  # 对比关系
    }
    
    for i, block in enumerate(semantic_blocks):
        if i > 0:
            prev_block = semantic_blocks[i-1]
            # 顺序关系：连续的块
            logical_relations["sequential"].append({
                "from": prev_block["heading"] or f"块{i}",
                "to": block["heading"] or f"块{i+1}"
            })
        
        # 层级关系：标题级别
        if block["heading_level"] > 0:
            logical_relations["hierarchical"].append({
                "heading": block["heading"],
                "level": block["heading_level"],
                "sub_items": len(block["content"])
            })
    
    # 检查表格中的对比关系
    for table_info in table_analysis:
        if table_info["header_row"] and len(table_info["header_row"]) >= 2:
            logical_relations["comparative"].append({
                "type": "table_comparison",
                "table_index": table_info["index"],
                "comparison_dimensions": table_info["header_row"]
            })
    
    analysis["layers"]["layer_7_logic"] = {
        "name": "逻辑关系层",
        "description": "内容之间的逻辑关系：顺序、层级、对比等",
        "data": logical_relations
    }
    
    return analysis

if __name__ == "__main__":
    docx_path = "Demo文档.docx"
    
    print("="*80)
    print("Demo文档.docx 深度层次拆解")
    print("="*80)
    print(f"\n正在深度分析: {docx_path}\n")
    
    analysis = deep_analyze_docx(docx_path)
    
    # 输出每个层次
    for layer_key, layer_data in analysis["layers"].items():
        print("\n" + "="*80)
        print(f"【{layer_data['name']}】")
        print("="*80)
        print(f"描述: {layer_data['description']}\n")
        
        if layer_key == "layer_1_physical":
            data = layer_data["data"]
            print(f"总段落数: {data['total_paragraphs']}")
            print(f"总表格数: {data['total_tables']}")
            print(f"使用的样式: {list(data['paragraphs_by_style'].keys())}")
            print(f"大字体段落数: {len(data['paragraphs_by_format']['large_font_paragraphs'])}")
            print(f"加粗段落数: {len(data['paragraphs_by_format']['bold_paragraphs'])}")
        
        elif layer_key == "layer_2_format":
            data = layer_data["data"]
            print(f"使用的字体: {data['font_names']}")
            print(f"使用的字号: {sorted(data['font_sizes'])}")
            print(f"加粗文本段数: {len(data['bold_runs'])}")
            print(f"缩进段落数: {len([p for p in data['paragraph_formats'] if p['left_indent'] > 0])}")
        
        elif layer_key == "layer_3_semantic":
            data = layer_data["data"]
            print(f"识别的内容块数: {data['total_blocks']}")
            print(f"\n内容块详情:")
            for i, block in enumerate(data["blocks"][:10], 1):
                heading = block["heading"] or "(无标题)"
                print(f"\n  块 {i}: {heading}")
                print(f"    级别: {block['heading_level']}")
                print(f"    内容段落数: {len(block['content'])}")
                if block["content"]:
                    preview = block["content"][0]["text"][:60]
                    print(f"    内容预览: {preview}...")
        
        elif layer_key == "layer_4_lists":
            data = layer_data["data"]
            print(f"编号列表项: {len(data['numbered_lists'])}")
            print(f"项目符号项: {len(data['bullet_lists'])}")
            print(f"缩进项: {len(data['indented_items'])}")
            if data['numbered_lists']:
                print(f"\n编号列表示例:")
                for item in data['numbered_lists'][:3]:
                    print(f"  {item['full_text'][:60]}...")
        
        elif layer_key == "layer_5_tables":
            data = layer_data["data"]
            print(f"表格数量: {len(data)}")
            for table in data:
                print(f"\n表格 {table['index'] + 1}:")
                print(f"  行数: {table['rows']}, 列数: {table['columns']}")
                if table['header_row']:
                    print(f"  表头: {table['header_row']}")
                if table['data_rows']:
                    print(f"  数据行示例:")
                    for row in table['data_rows'][:2]:
                        print(f"    {row['data']}")
        
        elif layer_key == "layer_6_topics":
            data = layer_data["data"]
            print(f"识别的话题数: {len(data)}")
            for topic, blocks in data.items():
                print(f"\n话题: {topic}")
                print(f"  相关块数: {len(blocks)}")
                for block in blocks[:2]:
                    print(f"    - {block['heading']}")
        
        elif layer_key == "layer_7_logic":
            data = layer_data["data"]
            print(f"顺序关系: {len(data['sequential'])}")
            print(f"层级关系: {len(data['hierarchical'])}")
            print(f"对比关系: {len(data['comparative'])}")
            if data['hierarchical']:
                print(f"\n层级结构:")
                for rel in data['hierarchical'][:5]:
                    print(f"  {rel['heading']} (级别{rel['level']}, {rel['sub_items']}个子项)")
    
    # 保存完整分析
    output_file = "demo_docx_deep_analysis.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print("\n\n" + "="*80)
    print("分析完成")
    print("="*80)
    print(f"✅ 完整分析结果已保存到: {output_file}")
    print(f"   识别层次数: {len(analysis['layers'])}")
    print(f"   内容块数: {analysis['layers']['layer_3_semantic']['data']['total_blocks']}")


```


## File: deep_parser.py

```python
"""
深度解析器
整合所有分析模块，提供统一的深度解析接口
"""

from pathlib import Path
from typing import Dict, Any
from loguru import logger

from enhanced_ppt_parser import EnhancedPPTParser
from semantic_analyzer import SemanticAnalyzer


class DeepParser:
    """
    深度解析器
    整合格式分析、语义分析、主题识别、逻辑关系等所有能力
    """
    
    def __init__(self, ppt_path: str):
        """
        初始化深度解析器
        
        Args:
            ppt_path: PPT文件路径
        """
        self.ppt_path = Path(ppt_path)
        self.parser = EnhancedPPTParser(ppt_path)
        logger.info("--- [DeepParser]: Initialized")
    
    def parse_all(self) -> Dict[str, Any]:
        """
        执行完整的深度解析
        
        Returns:
            包含7个层次的完整分析结果
        """
        logger.info("="*80)
        logger.info("--- [DeepParser]: 开始深度解析")
        logger.info("="*80)
        
        # 1. 增强结构提取（包含格式信息）
        logger.info("--- [DeepParser]: 阶段1 - 提取增强结构...")
        enhanced_structure = self.parser.extract_structure_enhanced()
        
        # 2. 段落级别分析
        logger.info("--- [DeepParser]: 阶段2 - 提取段落结构...")
        paragraph_structure = self.parser.extract_paragraph_structure()
        
        # 3. 列表识别
        logger.info("--- [DeepParser]: 阶段3 - 识别列表结构...")
        list_structure = self.parser.extract_list_structure()
        
        # 4. 表格识别
        logger.info("--- [DeepParser]: 阶段4 - 识别表格结构...")
        table_structure = self.parser.extract_table_structure()
        
        # 5. 语义分析
        logger.info("--- [DeepParser]: 阶段5 - 语义分析...")
        semantic_analyzer = SemanticAnalyzer(enhanced_structure)
        semantic_blocks = semantic_analyzer.identify_semantic_blocks()
        
        # 6. 主题识别
        logger.info("--- [DeepParser]: 阶段6 - 主题识别...")
        topics = semantic_analyzer.identify_topics(semantic_blocks)
        
        # 7. 逻辑关系
        logger.info("--- [DeepParser]: 阶段7 - 逻辑关系识别...")
        logical_relations = semantic_analyzer.identify_logical_relations(semantic_blocks)
        
        # 8. 格式特征分析
        logger.info("--- [DeepParser]: 阶段8 - 格式特征分析...")
        format_features = self._analyze_format_features(enhanced_structure)
        
        # 构建7层结构
        result = {
            "file_info": {
                "path": str(self.ppt_path),
                "size_bytes": self.ppt_path.stat().st_size
            },
            "layers": {
                "layer_1_physical": {
                    "name": "物理结构层",
                    "description": "文档的物理结构：段落、表格、章节等",
                    "data": {
                        "slide_count": enhanced_structure["slide_count"],
                        "total_shapes": sum(len(s["shapes"]) for s in enhanced_structure["slides"]),
                        "total_placeholders": sum(len(s["placeholders"]) for s in enhanced_structure["slides"]),
                        "total_paragraphs": len(paragraph_structure),
                        "total_tables": len(table_structure),
                        "dimensions": {
                            "width_cm": enhanced_structure["slide_width"],
                            "height_cm": enhanced_structure["slide_height"],
                            "ratio": enhanced_structure["slide_width"] / enhanced_structure["slide_height"]
                        }
                    }
                },
                "layer_2_format": {
                    "name": "格式特征层",
                    "description": "文本格式特征：字体、字号、加粗、颜色、缩进等",
                    "data": format_features
                },
                "layer_3_semantic": {
                    "name": "内容语义层",
                    "description": "基于内容语义和格式特征识别的标题-内容块结构",
                    "data": {
                        "total_blocks": len(semantic_blocks),
                        "blocks": semantic_blocks
                    }
                },
                "layer_4_lists": {
                    "name": "列表结构层",
                    "description": "文档中的列表结构：编号列表、项目符号、缩进列表",
                    "data": list_structure
                },
                "layer_5_tables": {
                    "name": "表格数据层",
                    "description": "文档中的表格结构和数据",
                    "data": table_structure
                },
                "layer_6_topics": {
                    "name": "主题/话题层",
                    "description": "基于关键词识别的内容主题分类",
                    "data": topics
                },
                "layer_7_logic": {
                    "name": "逻辑关系层",
                    "description": "内容之间的逻辑关系：顺序、层级、对比等",
                    "data": logical_relations
                }
            }
        }
        
        logger.info("="*80)
        logger.info("--- [DeepParser]: 深度解析完成")
        logger.info(f"   识别层次: 7个")
        logger.info(f"   内容块数: {len(semantic_blocks)}")
        logger.info(f"   主题数: {len(topics)}")
        logger.info("="*80)
        
        return result
    
    def _analyze_format_features(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """分析格式特征"""
        features = {
            "font_sizes": set(),
            "font_names": set(),
            "font_colors": set(),
            "bold_count": 0,
            "italic_count": 0,
            "colored_count": 0,
            "format_statistics": {}
        }
        
        for slide in structure["slides"]:
            for shape in slide["shapes"]:
                format_info = shape.get("format", {})
                
                if format_info.get("font_size_pt"):
                    features["font_sizes"].add(format_info["font_size_pt"])
                if format_info.get("font_name"):
                    features["font_names"].add(format_info["font_name"])
                if format_info.get("font_color"):
                    features["font_colors"].add(format_info["font_color"])
                
                if format_info.get("is_bold"):
                    features["bold_count"] += 1
                if format_info.get("is_italic"):
                    features["italic_count"] += 1
                if format_info.get("font_color"):
                    features["colored_count"] += 1
        
        # 转换set为list
        features["font_sizes"] = sorted(list(features["font_sizes"]))
        features["font_names"] = list(features["font_names"])
        features["font_colors"] = list(features["font_colors"])
        
        # 统计信息
        total_shapes = sum(len(s["shapes"]) for s in structure["slides"])
        features["format_statistics"] = {
            "total_shapes": total_shapes,
            "bold_percentage": (features["bold_count"] / total_shapes * 100) if total_shapes > 0 else 0,
            "unique_font_sizes": len(features["font_sizes"]),
            "unique_font_names": len(features["font_names"])
        }
        
        return features


```


## File: enhanced_ppt_parser.py

```python
"""
增强版PPT解析器
添加格式提取、段落分析、列表识别等功能
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Pt
from loguru import logger
import re


class EnhancedPPTParser:
    """
    增强版PPT解析器
    在基础解析的基础上，增加格式提取、段落分析、列表识别等功能
    """
    
    def __init__(self, ppt_path: str):
        """初始化增强解析器"""
        self.ppt_path = Path(ppt_path)
        if not self.ppt_path.exists():
            raise FileNotFoundError(f"PPT file not found: {ppt_path}")
        
        self.prs = Presentation(str(self.ppt_path))
        logger.info(f"--- [EnhancedPPTParser]: Loaded PPT: {self.ppt_path}")
    
    def _extract_format_info(self, shape) -> Dict[str, Any]:
        """
        提取形状的格式信息
        
        Args:
            shape: PPT形状对象
            
        Returns:
            格式信息字典
        """
        format_info = {
            "font_name": None,
            "font_size_pt": None,
            "font_color": None,
            "is_bold": False,
            "is_italic": False,
            "is_underline": False,
            "alignment": None,
            "line_spacing": None,
            "left_indent_pt": None,
            "first_line_indent_pt": None
        }
        
        if hasattr(shape, "text_frame"):
            # 收集所有运行（runs）的格式信息
            font_sizes = []
            font_names = []
            font_colors = []
            has_bold = False
            has_italic = False
            has_underline = False
            
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if run.font.name:
                        font_names.append(run.font.name)
                    if run.font.size:
                        font_sizes.append(run.font.size.pt)
                    try:
                        if run.font.color and hasattr(run.font.color, 'rgb') and run.font.color.rgb:
                            font_colors.append(str(run.font.color.rgb))
                    except:
                        pass
                    if hasattr(run, 'bold') and run.bold:
                        has_bold = True
                    if hasattr(run, 'italic') and run.italic:
                        has_italic = True
                    if hasattr(run, 'underline') and run.underline:
                        has_underline = True
                
                # 段落格式
                try:
                    pf = para.paragraph_format
                    if para.alignment:
                        format_info["alignment"] = str(para.alignment)
                    if pf.line_spacing:
                        format_info["line_spacing"] = pf.line_spacing
                    if pf.left_indent:
                        format_info["left_indent_pt"] = pf.left_indent.pt
                    if pf.first_line_indent:
                        format_info["first_line_indent_pt"] = pf.first_line_indent.pt
                except:
                    pass
            
            # 取最常见的值
            if font_names:
                format_info["font_name"] = max(set(font_names), key=font_names.count)
            if font_sizes:
                format_info["font_size_pt"] = max(font_sizes)  # 取最大字号
            if font_colors:
                format_info["font_color"] = max(set(font_colors), key=font_colors.count)
            
            format_info["is_bold"] = has_bold
            format_info["is_italic"] = has_italic
            format_info["is_underline"] = has_underline
        
        return format_info
    
    def extract_structure_enhanced(self) -> Dict[str, Any]:
        """
        提取增强的结构信息（包含格式信息）
        
        Returns:
            增强的结构信息字典
        """
        structure = {
            "slides": [],
            "slide_count": len(self.prs.slides),
            "slide_width": float(self.prs.slide_width) / 360000,
            "slide_height": float(self.prs.slide_height) / 360000
        }
        
        for idx, slide in enumerate(self.prs.slides):
            slide_info = {
                "slide_index": idx,
                "layout_name": slide.slide_layout.name if hasattr(slide.slide_layout, 'name') else "Unknown",
                "shapes": [],
                "placeholders": [],
                "format_statistics": {
                    "font_sizes": set(),
                    "font_names": set(),
                    "bold_count": 0,
                    "total_shapes": 0
                }
            }
            
            for shape in slide.shapes:
                shape_info = self._extract_shape_info_enhanced(shape, idx)
                if shape_info:
                    slide_info["shapes"].append(shape_info)
                    
                    # 统计格式信息
                    format_info = shape_info.get("format", {})
                    if format_info.get("font_size_pt"):
                        slide_info["format_statistics"]["font_sizes"].add(format_info["font_size_pt"])
                    if format_info.get("font_name"):
                        slide_info["format_statistics"]["font_names"].add(format_info["font_name"])
                    if format_info.get("is_bold"):
                        slide_info["format_statistics"]["bold_count"] += 1
                    
                    slide_info["format_statistics"]["total_shapes"] += 1
                    
                    if shape.is_placeholder:
                        slide_info["placeholders"].append(shape_info)
            
            # 转换set为list
            slide_info["format_statistics"]["font_sizes"] = sorted(list(slide_info["format_statistics"]["font_sizes"]))
            slide_info["format_statistics"]["font_names"] = list(slide_info["format_statistics"]["font_names"])
            
            structure["slides"].append(slide_info)
        
        logger.info(f"--- [EnhancedPPTParser]: Extracted enhanced structure from {len(structure['slides'])} slides")
        return structure
    
    def _extract_shape_info_enhanced(self, shape, slide_index: int) -> Optional[Dict[str, Any]]:
        """提取增强的形状信息（包含格式）"""
        try:
            shape_info = {
                "type": self._get_shape_type(shape),
                "shape_id": shape.shape_id,
                "left": float(shape.left) / 360000,
                "top": float(shape.top) / 360000,
                "width": float(shape.width) / 360000,
                "height": float(shape.height) / 360000,
                "is_placeholder": shape.is_placeholder,
                "format": self._extract_format_info(shape)  # 新增：格式信息
            }
            
            if shape.is_placeholder:
                try:
                    shape_info["placeholder_id"] = shape.placeholder_format.idx
                    shape_info["placeholder_type"] = str(shape.placeholder_format.type)
                except:
                    pass
            
            if hasattr(shape, "text_frame"):
                text = shape.text_frame.text.strip()
                if text:
                    shape_info["text"] = text
                    shape_info["has_text"] = True
                else:
                    shape_info["has_text"] = False
                    shape_info["text"] = ""
            else:
                shape_info["has_text"] = False
                shape_info["text"] = ""
            
            return shape_info
            
        except Exception as e:
            logger.warning(f"--- [EnhancedPPTParser]: Failed to extract shape info: {e}")
            return None
    
    def _get_shape_type(self, shape) -> str:
        """获取形状类型名称"""
        try:
            shape_type = shape.shape_type
            type_names = {
                MSO_SHAPE_TYPE.AUTO_SHAPE: "auto_shape",
                MSO_SHAPE_TYPE.PLACEHOLDER: "placeholder",
                MSO_SHAPE_TYPE.PICTURE: "picture",
                MSO_SHAPE_TYPE.TEXT_BOX: "text_box",
                MSO_SHAPE_TYPE.GROUP: "group",
                MSO_SHAPE_TYPE.TABLE: "table",
                MSO_SHAPE_TYPE.MEDIA: "media"
            }
            return type_names.get(shape_type, "unknown")
        except:
            return "unknown"
    
    def extract_paragraph_structure(self) -> List[Dict[str, Any]]:
        """
        提取段落级别的结构
        
        Returns:
            段落结构列表
        """
        paragraph_structure = []
        
        for slide_idx, slide in enumerate(self.prs.slides):
            for shape_idx, shape in enumerate(slide.shapes):
                if hasattr(shape, "text_frame"):
                    for para_idx, para in enumerate(shape.text_frame.paragraphs):
                        para_info = {
                            "slide_index": slide_idx,
                            "shape_index": shape_idx,
                            "paragraph_index": para_idx,
                            "text": para.text.strip(),
                            "format": self._extract_paragraph_format(para),
                            "runs": []
                        }
                        
                        # 分析文本运行
                        for run in para.runs:
                            run_info = {
                                "text": run.text,
                                "format": self._extract_run_format(run)
                            }
                            para_info["runs"].append(run_info)
                        
                        paragraph_structure.append(para_info)
        
        logger.info(f"--- [EnhancedPPTParser]: Extracted {len(paragraph_structure)} paragraphs")
        return paragraph_structure
    
    def _extract_paragraph_format(self, para) -> Dict[str, Any]:
        """提取段落格式"""
        try:
            pf = para.paragraph_format
            return {
                "alignment": str(para.alignment) if para.alignment else None,
                "left_indent_pt": pf.left_indent.pt if pf.left_indent else 0,
                "first_line_indent_pt": pf.first_line_indent.pt if pf.first_line_indent else 0,
                "space_before_pt": pf.space_before.pt if pf.space_before else 0,
                "space_after_pt": pf.space_after.pt if pf.space_after else 0,
                "line_spacing": str(pf.line_spacing) if pf.line_spacing else None
            }
        except Exception as e:
            logger.warning(f"--- [EnhancedPPTParser]: Failed to extract paragraph format: {e}")
            return {
                "alignment": None,
                "left_indent_pt": 0,
                "first_line_indent_pt": 0,
                "space_before_pt": 0,
                "space_after_pt": 0,
                "line_spacing": None
            }
    
    def _extract_run_format(self, run) -> Dict[str, Any]:
        """提取文本运行格式"""
        font_color = None
        try:
            if run.font.color and hasattr(run.font.color, 'rgb') and run.font.color.rgb:
                font_color = str(run.font.color.rgb)
        except:
            pass
        
        return {
            "font_name": run.font.name if run.font.name else None,
            "font_size_pt": run.font.size.pt if run.font.size else None,
            "font_color": font_color,
            "is_bold": run.bold if hasattr(run, 'bold') and run.bold is not None else False,
            "is_italic": run.italic if hasattr(run, 'italic') and run.italic is not None else False,
            "is_underline": run.underline if hasattr(run, 'underline') and run.underline is not None else False
        }
    
    def extract_list_structure(self) -> Dict[str, Any]:
        """
        提取列表结构
        
        Returns:
            列表结构字典
        """
        lists = {
            "numbered_lists": [],
            "bullet_lists": [],
            "indented_items": []
        }
        
        for slide_idx, slide in enumerate(self.prs.slides):
            for shape in slide.shapes:
                if hasattr(shape, "text_frame"):
                    for para in shape.text_frame.paragraphs:
                        text = para.text.strip()
                        if not text:
                            continue
                        
                        # 检查编号列表
                        numbered_match = re.match(r'^[\d一二三四五六七八九十]+[\.、]\s*(.+)', text)
                        if numbered_match:
                            lists["numbered_lists"].append({
                                "slide_index": slide_idx,
                                "text": text,
                                "number": text[0] if text else "",
                                "content": numbered_match.group(1) if len(numbered_match.groups()) > 0 else text,
                                "format": self._extract_paragraph_format(para)
                            })
                        
                        # 检查项目符号
                        bullet_match = re.match(r'^[•·▪▫○●■□]\s*(.+)', text)
                        if bullet_match:
                            lists["bullet_lists"].append({
                                "slide_index": slide_idx,
                                "text": text,
                                "bullet": text[0],
                                "content": bullet_match.group(1),
                                "format": self._extract_paragraph_format(para)
                            })
                        
                        # 检查缩进
                        try:
                            pf = para.paragraph_format
                            if pf.left_indent and pf.left_indent.pt > 0:
                                lists["indented_items"].append({
                                    "slide_index": slide_idx,
                                    "text": text[:100],
                                    "indent_pt": pf.left_indent.pt,
                                    "format": self._extract_paragraph_format(para)
                                })
                        except:
                            pass
        
        logger.info(f"--- [EnhancedPPTParser]: Extracted {len(lists['numbered_lists'])} numbered lists, {len(lists['bullet_lists'])} bullet lists, {len(lists['indented_items'])} indented items")
        return lists
    
    def extract_table_structure(self) -> List[Dict[str, Any]]:
        """
        提取表格结构
        
        Returns:
            表格结构列表
        """
        tables = []
        
        for slide_idx, slide in enumerate(self.prs.slides):
            for shape in slide.shapes:
                if shape.shape_type == MSO_SHAPE_TYPE.TABLE:
                    table_info = {
                        "slide_index": slide_idx,
                        "rows": len(shape.table.rows),
                        "columns": len(shape.table.columns) if shape.table.rows else 0,
                        "cells": [],
                        "structure": []
                    }
                    
                    for row_idx, row in enumerate(shape.table.rows):
                        row_data = []
                        for cell in row.cells:
                            cell_text = cell.text.strip()
                            row_data.append(cell_text)
                            table_info["cells"].append({
                                "row": row_idx,
                                "column": row.cells.index(cell),
                                "text": cell_text
                            })
                        table_info["structure"].append(row_data)
                    
                    # 识别表头
                    if table_info["structure"]:
                        table_info["header_row"] = table_info["structure"][0]
                        table_info["data_rows"] = table_info["structure"][1:]
                    
                    tables.append(table_info)
        
        logger.info(f"--- [EnhancedPPTParser]: Extracted {len(tables)} tables")
        return tables


```


## File: html_canvas_generator.py

```python
"""
HTML画布生成器
先创建标准的16:9白色画布，建立坐标系，然后放置元素
"""

from typing import Dict, Any, List, Optional, Tuple
from loguru import logger


class HTMLCanvasGenerator:
    """
    HTML画布生成器
    按照正确的工作顺序：
    1. 先创建16:9白色画布
    2. 建立坐标系（左下角为原点）
    3. 绘制栅格标准尺
    4. 然后根据坐标放置元素
    """
    
    # 16:9画布尺寸（像素）
    CANVAS_WIDTH = 1920
    CANVAS_HEIGHT = 1080
    
    # 24栅格系统
    GRID_COLUMNS = 24
    GRID_ROWS = 13.5
    
    # 栅格单元尺寸（基于画布尺寸）
    CELL_WIDTH = CANVAS_WIDTH / GRID_COLUMNS  # 80px
    CELL_HEIGHT = CANVAS_HEIGHT / GRID_ROWS   # 80px
    
    def __init__(self):
        """初始化画布生成器"""
        logger.info("--- [HTMLCanvasGenerator]: Initialized")
    
    def create_canvas_html(
        self,
        elements: List[Dict[str, Any]],
        show_grid: bool = True
    ) -> str:
        """
        创建完整的HTML画布
        
        Args:
            elements: 元素列表，每个元素包含：
                - id: 元素ID
                - type: 元素类型（card, text, title等）
                - content: 内容
                - coordinates: 坐标信息
                    - left: 距离左边缘的像素
                    - right: 距离右边缘的像素（可选）
                    - top: 距离上边缘的像素
                    - bottom: 距离下边缘的像素（可选）
                    - width: 宽度（像素）
                    - height: 高度（像素）
            show_grid: 是否显示栅格标准尺
            
        Returns:
            完整的HTML字符串
        """
        # 1. 生成画布基础HTML结构
        canvas_html = self._generate_canvas_structure()
        
        # 2. 生成CSS样式（包含坐标系和栅格标准尺）
        css = self._generate_canvas_css(show_grid=show_grid)
        
        # 3. 生成栅格标准尺HTML（如果启用）
        grid_ruler_html = ""
        if show_grid:
            grid_ruler_html = self._generate_grid_ruler_html()
        
        # 4. 生成元素HTML（根据坐标放置）
        elements_html = self._generate_elements_html(elements)
        
        # 5. 组装完整HTML（栅格标准尺和元素都放在canvas内部）
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>16:9画布 - 坐标系演示</title>
    <style>
        {css}
    </style>
</head>
<body>
    {canvas_html.replace('<!-- 栅格标准尺和元素将放置在这里 -->', f'{grid_ruler_html}\n            {elements_html}')}
</body>
</html>"""
        
        return html
    
    def _generate_canvas_structure(self) -> str:
        """
        生成画布基础HTML结构
        创建一个16:9的白色画布容器
        """
        return f"""
    <!-- 16:9白色画布容器 -->
    <div id="canvas-container" class="canvas-container">
        <!-- 画布（左下角为坐标原点） -->
        <div id="canvas" class="canvas">
            <!-- 栅格标准尺和元素将放置在这里 -->
        </div>
    </div>"""
    
    def _generate_canvas_css(self, show_grid: bool = True) -> str:
        """
        生成画布CSS样式
        建立坐标系：左下角为原点
        应用 Ant Design Design Tokens
        """
        return f"""
        :root {{
            /* --- Ant Design Color Tokens --- */
            --ant-color-primary: #1677FF;
            --ant-color-success: #52C41A;
            --ant-color-warning: #FA8C16;
            --ant-color-error: #F5222D;
            
            /* --- Text Colors --- */
            --ant-text-color: rgba(0, 0, 0, 0.88);       /* 主文本 */
            --ant-text-color-secondary: rgba(0, 0, 0, 0.65); /* 次文本/副标题 */
            --ant-text-color-tertiary: rgba(0, 0, 0, 0.45);  /* 辅助文本 */
            
            /* --- Backgrounds --- */
            --ant-bg-color-layout: #F0F2F5;  /* 页面背景灰 */
            --ant-bg-color-container: #FFFFFF; /* 卡片背景白 */
            
            /* --- Borders & Shadows --- */
            --ant-border-color: #F0F0F0;
            --ant-border-radius-base: 8px;
            --ant-box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02);
            --ant-box-shadow-hover: 0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 9px 28px 8px rgba(0, 0, 0, 0.05);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            margin: 0;
            padding: 20px;
            background-color: #e6e6e6; /* 浏览器背景，非画布背景 */
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: flex-start; /* 改为顶部对齐，避免垂直居中导致的问题 */
            min-height: 100vh;
            /* 确保横版显示 */
            width: 100%;
            overflow-x: auto; /* 如果画布太宽，允许横向滚动 */
        }}
        
        /* 画布容器 */
        .canvas-container {{
            position: relative;
            width: {self.CANVAS_WIDTH}px;
            height: {self.CANVAS_HEIGHT}px;
            background: #ffffff; /* 白色画布 */
            border: 2px solid #d9d9d9;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        
        /* 画布（坐标系容器） */
        .canvas {{
            position: relative;
            width: 100%;
            height: 100%;
            /* 强制应用 Ant Design 页面背景色 */
            background-color: var(--ant-bg-color-layout) !important;
            /* 坐标系：左下角为原点 */
            /* CSS默认使用top-left原点，我们需要通过transform或计算来模拟左下角原点 */
        }}
        
        /* 栅格标准尺样式 */
        .grid-ruler {{
            position: absolute;
            pointer-events: none;
            z-index: 1;
        }}
        
        .grid-ruler-line {{
            stroke: #e8e8e8;
            stroke-width: 1;
            stroke-dasharray: 2, 2;
        }}
        
        .grid-ruler-label {{
            font-size: 10px;
            fill: #999;
            text-anchor: middle;
        }}
        
        /* 元素样式 */
        .element {{
            position: absolute;
            /* 坐标将通过style属性动态设置 */
        }}
        
        .element-card {{
            background: #ffffff;
            border: 1px solid #d9d9d9;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            padding: 16px;
            overflow: hidden;
        }}
        
        .element-text {{
            color: #262626;
            word-wrap: break-word;
            word-break: break-word;
            white-space: normal;
            font-size: 18px;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}
        
        .element-title {{
            font-size: 48px;
            font-weight: 700;
            color: #1890ff;
            margin: 0;
            padding: 0;
            line-height: 1.2;
        }}
        
        .element-body {{
            font-size: 16px;
            line-height: 1.6;
            color: #595959;
            margin: 0;
            padding: 0;
        }}
        
        /* 坐标原点标记 */
        .origin-marker {{
            position: absolute;
            left: 0;
            bottom: 0;
            width: 20px;
            height: 20px;
            background: #ff4d4f;
            border-radius: 50%;
            z-index: 1000;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        .origin-marker::after {{
            content: 'O';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 12px;
            font-weight: bold;
        }}"""
    
    def _generate_grid_ruler_html(self) -> str:
        """
        生成栅格标准尺HTML
        在画布四周绘制24列×13.5行的栅格线
        """
        svg_lines = []
        svg_labels = []
        
        # 绘制垂直栅格线（24列）
        for col in range(self.GRID_COLUMNS + 1):
            x = col * self.CELL_WIDTH
            # 垂直线
            svg_lines.append(f'<line class="grid-ruler-line" x1="{x}" y1="0" x2="{x}" y2="{self.CANVAS_HEIGHT}"/>')
            # 底部标签
            svg_labels.append(f'<text class="grid-ruler-label" x="{x}" y="{self.CANVAS_HEIGHT + 15}" fill="#999">{col}</text>')
            # 顶部标签
            svg_labels.append(f'<text class="grid-ruler-label" x="{x}" y="-5" fill="#999">{col}</text>')
        
        # 绘制水平栅格线（13.5行，向上从底部开始）
        for row in range(int(self.GRID_ROWS) + 1):
            # CSS使用top定位，所以需要从顶部计算
            y_from_top = self.CANVAS_HEIGHT - (row * self.CELL_HEIGHT)
            # 水平线
            svg_lines.append(f'<line class="grid-ruler-line" x1="0" y1="{y_from_top}" x2="{self.CANVAS_WIDTH}" y2="{y_from_top}"/>')
            # 左侧标签（从底部开始，row=0是底部）
            svg_labels.append(f'<text class="grid-ruler-label" x="-15" y="{y_from_top + 4}" fill="#999">{row}</text>')
            # 右侧标签
            svg_labels.append(f'<text class="grid-ruler-label" x="{self.CANVAS_WIDTH + 15}" y="{y_from_top + 4}" fill="#999">{row}</text>')
        
        return f"""
            <!-- 栅格标准尺 -->
            <svg class="grid-ruler" width="{self.CANVAS_WIDTH}" height="{self.CANVAS_HEIGHT}" style="position: absolute; top: 0; left: 0;">
                {''.join(svg_lines)}
                {''.join(svg_labels)}
            </svg>
            
            <!-- 坐标原点标记（左下角） -->
            <div class="origin-marker" title="坐标原点 (0, 0)"></div>"""
    
    def _generate_elements_html(self, elements: List[Dict[str, Any]]) -> str:
        """
        生成元素HTML
        根据坐标信息放置元素
        
        Args:
            elements: 元素列表，每个元素包含坐标信息
            
        Returns:
            元素HTML字符串
        """
        elements_html = []
        
        for elem in elements:
            elem_id = elem.get('id', '')
            elem_type = elem.get('type', 'card')
            content = elem.get('content', '')
            coordinates = elem.get('coordinates', {})
            
            # 解析坐标
            # 坐标系：左下角为原点
            # CSS使用top-left原点，需要转换
            left = coordinates.get('left', 0)
            right = coordinates.get('right')
            top = coordinates.get('top')
            bottom = coordinates.get('bottom', 0)
            width = coordinates.get('width', 200)
            height = coordinates.get('height', 100)
            
            # 计算CSS位置（从左下角原点转换为top-left原点）
            css_left = left
            if right is not None:
                css_left = self.CANVAS_WIDTH - right - width
            
            css_top = None
            if top is not None:
                css_top = top
            elif bottom is not None:
                # 从底部距离转换为顶部距离
                css_top = self.CANVAS_HEIGHT - bottom - height
            
            # 获取原始颜色配置（来自 ColorConfigurator）
            raw_style = elem.get('style_config', {})
            accent_color = raw_style.get('border_color', '#1677FF')  # 提取"特征色"，默认主色
            
            # 生成基础样式
            style_list = [
                f"left: {css_left}px;",
                f"top: {css_top}px;",
                f"width: {width}px;",
                f"height: {height}px;",
                "position: absolute;",
                "box-sizing: border-box;"
            ]
            
            # --- 针对不同类型的"设计感"处理 ---
            
            # 1. 标题 (Title)
            if 'title' in elem_type and 'subtitle' not in elem_type:
                # 使用主色或主文本色
                text_color = raw_style.get('text_color', 'var(--ant-color-primary)')
                style_list.append(f"color: {text_color};")
                style_list.append("font-size: 48px;")  # 加大字号
                style_list.append("font-weight: 600;")
                style_list.append("text-align: center;")
                style_list.append("line-height: 1.2;")
                # 移除背景色，标题通常是透明背景
                style_list.append("margin: 0;")
                
            # 2. 副标题 (Subtitle)
            elif 'subtitle' in elem_type or (elem_type == 'text' and 'subtitle' in elem_id):
                style_list.append("color: var(--ant-text-color-secondary);")
                style_list.append("font-size: 24px;")
                style_list.append("font-weight: 400;")
                style_list.append("text-align: center;")
                style_list.append("line-height: 1.5;")
                style_list.append("margin: 0;")
            
            # 3. 价值卡片 (Card) - 重点改造
            elif 'card' in elem_type or 'value' in elem_type:
                # 强制白色背景
                style_list.append("background-color: var(--ant-bg-color-container);")
                
                # 添加高级感阴影
                style_list.append("box-shadow: var(--ant-box-shadow);")
                
                # 圆角
                style_list.append("border-radius: var(--ant-border-radius-base);")
                
                # 内边距
                style_list.append("padding: 24px;")
                
                # 【设计核心】使用 accent_color 做顶部装饰条，而不是全背景
                # 这样既区分了颜色（蓝/绿/橙），又保持了统一的白色卡片风格
                style_list.append(f"border-top: 4px solid {accent_color};")
                
                # 布局
                style_list.append("display: flex;")
                style_list.append("flex-direction: column;")
                style_list.append("justify-content: center;")  # 内容垂直居中
                style_list.append("align-items: flex-start;")  # 内容左对齐
                
            # 4. 其他通用元素
            else:
                bg_color = raw_style.get('background_color', 'transparent')
                if bg_color and bg_color != 'transparent':
                    style_list.append(f"background-color: {bg_color};")
            
            # 组装 style 字符串
            style_str = " ".join(style_list)
            
            # --- 内容内部 HTML 优化 ---
            final_html = ""
            
            if 'card' in elem_type or 'value' in elem_type:
                # 卡片标题样式 - 使用accent_color作为标题颜色（可选，更高级）
                h3_color = accent_color  # 卡片标题使用特征色
                h3_style = f"margin: 0 0 12px 0; font-size: 20px; font-weight: 600; color: {h3_color};"
                # 卡片内容样式
                p_style = f"margin: 0; font-size: 14px; color: var(--ant-text-color-secondary); line-height: 1.6;"
                
                processed_content = content
                processed_content = processed_content.replace('<h3>', f'<h3 style="{h3_style}">')
                processed_content = processed_content.replace('<p>', f'<p style="{p_style}">')
                
                final_html = f'<div id="{elem_id}" class="element-card" style="{style_str}">{processed_content}</div>'
                
            elif 'title' in elem_type:
                final_html = f'<h1 id="{elem_id}" style="{style_str}">{content}</h1>'
                
            else:
                final_html = f'<div id="{elem_id}" style="{style_str}">{content}</div>'
            
            elements_html.append(final_html)
        
        return "\n            ".join(elements_html)
    
    def coordinate_to_css(
        self,
        left: float,
        bottom: float,
        width: float,
        height: float
    ) -> Dict[str, float]:
        """
        将坐标系坐标转换为CSS位置
        坐标系：左下角为原点
        CSS：top-left为原点
        
        Args:
            left: 距离左边缘的像素
            bottom: 距离下边缘的像素
            width: 宽度
            height: 高度
            
        Returns:
            CSS位置字典 {left, top, width, height}
        """
        # 转换为CSS的top位置
        css_top = self.CANVAS_HEIGHT - bottom - height
        
        return {
            'left': left,
            'top': css_top,
            'width': width,
            'height': height
        }


```


## File: html_flow_layout_generator.py

```python
"""
流式布局 HTML 生成器
按照新架构原则：LLM 负责"定性"，生成流式布局 HTML（Flex/Grid）

核心原则：
1. 不使用绝对定位（position: absolute）
2. 使用 Ant Design 的 Flex/Grid 布局
3. 应用 Design Tokens（CSS 变量）
4. 为每个元素添加 data-ppt-element 属性，便于浏览器提取坐标
"""

from typing import Dict, Any, List, Optional
from loguru import logger
from ant_design_theme import ant_design_theme


class FlowLayoutHTMLGenerator:
    """
    流式布局 HTML 生成器
    
    生成符合 Ant Design 规范的流式布局 HTML
    让浏览器负责计算坐标，而不是 Python 计算
    """
    
    CANVAS_WIDTH = 1920
    CANVAS_HEIGHT = 1080
    
    def __init__(self):
        """初始化流式布局生成器"""
        logger.info("--- [FlowLayoutHTMLGenerator]: Initialized")
    
    def generate_flow_layout_html(
        self,
        layout_structure: Dict[str, Any],
        polished_slide: Dict[str, Any],
        color_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        生成流式布局 HTML
        
        Args:
            layout_structure: 布局结构（Ant Design 组件树）
            polished_slide: 润色后的幻灯片内容
            color_config: 颜色配置
            
        Returns:
            完整的 HTML 字符串
        """
        # 生成 CSS（包含 Design Tokens）
        css = self._generate_css_with_tokens()
        
        # 生成 HTML 结构（Flex/Grid 布局）
        html_body = self._generate_flow_layout_body(
            layout_structure, polished_slide, color_config
        )
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{polished_slide.get('title', 'Slide')}</title>
    <style>
        {css}
    </style>
</head>
<body>
    {html_body}
</body>
</html>"""
        
        return html
    
    def _generate_css_with_tokens(self) -> str:
        """
        生成包含 Design Tokens 的 CSS
        
        使用 CSS 变量统一管理样式
        """
        return f"""
        :root {{
            /* --- Ant Design Color Tokens --- */
            --ant-color-primary: #1677FF;
            --ant-color-success: #52C41A;
            --ant-color-warning: #FA8C16;
            --ant-color-error: #F5222D;
            
            /* --- Text Colors --- */
            --ant-text-color: rgba(0, 0, 0, 0.88);
            --ant-text-color-secondary: rgba(0, 0, 0, 0.65);
            --ant-text-color-tertiary: rgba(0, 0, 0, 0.45);
            
            /* --- Backgrounds --- */
            --ant-bg-color-layout: #F0F2F5;
            --ant-bg-color-container: #FFFFFF;
            
            /* --- Borders & Shadows --- */
            --ant-border-color: #F0F0F0;
            --ant-border-radius-base: 8px;
            --ant-box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            width: {self.CANVAS_WIDTH}px;
            height: {self.CANVAS_HEIGHT}px;
            background-color: var(--ant-bg-color-layout);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            padding: 40px;
            /* 使用 Flex 布局，让浏览器自动计算位置 */
            display: flex;
            flex-direction: column;
        }}
        
        /* Ant Design 风格的卡片 */
        .ant-card {{
            background-color: var(--ant-bg-color-container);
            border-radius: var(--ant-border-radius-base);
            box-shadow: var(--ant-box-shadow);
            padding: 24px;
            border-top: 4px solid var(--ant-color-primary);
        }}
        
        /* 标题样式 */
        .ant-typography-title {{
            color: var(--ant-color-primary);
            font-size: 48px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 24px;
        }}
        
        /* 副标题样式 */
        .ant-typography-subtitle {{
            color: var(--ant-text-color-secondary);
            font-size: 24px;
            font-weight: 400;
            text-align: center;
            margin-bottom: 40px;
        }}
        
        /* Flex 容器 */
        .ant-flex {{
            display: flex;
        }}
        
        .ant-flex-row {{
            flex-direction: row;
        }}
        
        .ant-flex-column {{
            flex-direction: column;
        }}
        
        .ant-flex-center {{
            justify-content: center;
            align-items: center;
        }}
        
        .ant-flex-space-between {{
            justify-content: space-between;
        }}
        
        .ant-flex-gap-small {{
            gap: 16px;
        }}
        
        .ant-flex-gap-medium {{
            gap: 24px;
        }}
        
        .ant-flex-gap-large {{
            gap: 32px;
        }}
        """
    
    def _generate_flow_layout_body(
        self,
        layout_structure: Dict[str, Any],
        polished_slide: Dict[str, Any],
        color_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        生成流式布局的 HTML body
        
        根据布局结构生成 Flex/Grid 布局
        """
        # 提取元素
        visual_elements = polished_slide.get('visual_elements_detail', [])
        
        # 构建颜色映射
        color_map = {}
        if color_config:
            for elem_color in color_config.get('color_config', {}).get('element_colors', []):
                elem_id = elem_color.get('element_id', '')
                if elem_id:
                    color_map[elem_id] = elem_color
        
        # 生成标题
        title_html = ""
        title_elem = next((e for e in visual_elements if 'title' in e.get('element_type', '') and 'subtitle' not in e.get('element_type', '')), None)
        if title_elem:
            title_html = f"""
            <h1 class="ant-typography-title ppt-element" 
                data-ppt-element="true"
                data-ppt-element-id="{title_elem.get('element_id', '')}"
                data-ppt-element-type="title">
                {title_elem.get('title', '')}
            </h1>"""
        
        # 生成副标题
        subtitle_html = ""
        subtitle_elem = next((e for e in visual_elements if 'subtitle' in e.get('element_type', '')), None)
        if subtitle_elem:
            subtitle_html = f"""
            <p class="ant-typography-subtitle ppt-element"
               data-ppt-element="true"
               data-ppt-element-id="{subtitle_elem.get('element_id', '')}"
               data-ppt-element-type="text">
                {subtitle_elem.get('title', '')}<br/>{subtitle_elem.get('content', '')}
            </p>"""
        
        # 生成卡片（使用 Flex 布局）
        card_elements = [e for e in visual_elements if 'card' in e.get('element_type', '')]
        cards_html = ""
        if card_elements:
            cards_html = '<div class="ant-flex ant-flex-row ant-flex-center ant-flex-gap-medium" style="flex: 1; align-items: stretch;">'
            for card_elem in card_elements:
                elem_id = card_elem.get('element_id', '')
                accent_color = color_map.get(elem_id, {}).get('border_color', '#1677FF')
                cards_html += f"""
                <div class="ant-card ppt-element"
                     data-ppt-element="true"
                     data-ppt-element-id="{elem_id}"
                     data-ppt-element-type="card"
                     style="border-top-color: {accent_color}; flex: 1;">
                    <h3 style="margin: 0 0 12px 0; font-size: 20px; font-weight: 600; color: {accent_color};">
                        {card_elem.get('title', '')}
                    </h3>
                    <p style="margin: 0; font-size: 14px; color: var(--ant-text-color-secondary); line-height: 1.6;">
                        {card_elem.get('content', '')}
                    </p>
                </div>"""
            cards_html += '</div>'
        
        # 组装完整 body
        body_html = f"""
        <div class="ant-flex ant-flex-column" style="height: 100%;">
            {title_html}
            {subtitle_html}
            {cards_html}
        </div>"""
        
        return body_html


```


## File: html_generator.py

```python
"""
HTML生成器
根据内容和Ant Design规范生成HTML模板
融合中国述职PPT风格
"""

from typing import Dict, Any, List, Optional, Tuple
from loguru import logger
from ant_design_theme import ant_design_theme
from chinese_ppt_theme import chinese_ppt_theme
from html_canvas_generator import HTMLCanvasGenerator


class HTMLGenerator:
    """
    HTML生成器
    生成符合Ant Design规范的HTML模板（16:9画布，24栅格系统）
    
    坐标系系统：
    - 原点：左下角 (0, 0)
    - X轴：向右为正
    - Y轴：向上为正
    - 画布尺寸：1920px × 1080px (16:9)
    - 内容区域：1872px × 1032px (减去padding 24px)
    - 栅格系统：24列 × 13.5行
    """
    
    # 16:9画布尺寸
    CANVAS_WIDTH = 1920
    CANVAS_HEIGHT = 1080
    GRID_COLUMNS = 24
    GRID_ROWS = 13.5
    
    # Padding（与坐标映射器保持一致）
    HTML_PADDING = 24  # px
    
    # 内容区域尺寸（减去padding）
    CONTENT_WIDTH = CANVAS_WIDTH - 2 * HTML_PADDING  # 1872px
    CONTENT_HEIGHT = CANVAS_HEIGHT - 2 * HTML_PADDING  # 1032px
    
    # 栅格单元尺寸
    CELL_WIDTH = CONTENT_WIDTH / GRID_COLUMNS  # ≈ 78px
    CELL_HEIGHT = CONTENT_HEIGHT / GRID_ROWS   # ≈ 76.4px
    
    def __init__(self):
        """初始化HTML生成器"""
        logger.info("--- [HTMLGenerator]: Initialized")
        # 初始化画布生成器
        self.canvas_generator = HTMLCanvasGenerator()
    
    def _grid_to_pixel(self, grid_x: float, grid_y: float, span_x: float, span_y: float) -> tuple:
        """
        将栅格坐标转换为像素坐标（左下角为原点）
        
        Args:
            grid_x: 栅格列位置（0-23）
            grid_y: 栅格行位置（0-12.5，从下往上）
            span_x: 占据的列数
            span_y: 占据的行数
        
        Returns:
            (left, top, width, height) 像素值（CSS使用top-left原点）
        """
        # 计算像素位置（左下角为原点）
        left_px = self.HTML_PADDING + grid_x * self.CELL_WIDTH
        bottom_px = self.HTML_PADDING + grid_y * self.CELL_HEIGHT
        width_px = span_x * self.CELL_WIDTH
        height_px = span_y * self.CELL_HEIGHT
        
        # 转换为CSS的top定位（CSS使用top-left原点）
        # top = 画布高度 - bottom - height
        top_px = self.CANVAS_HEIGHT - bottom_px - height_px
        
        return (left_px, top_px, width_px, height_px)
    
    def generate_slide_html(
        self,
        title: Optional[str] = None,
        content_blocks: Optional[List[Dict[str, Any]]] = None,
        layout: str = "standard"
    ) -> str:
        """
        生成单张幻灯片的HTML
        
        Args:
            title: 标题
            content_blocks: 内容块列表，每个块包含：
                - text: 文本内容
                - type: 类型（title, subtitle, body, key_points, data_highlight, case_study）
                - grid_position: 栅格位置 {'x': 0, 'y': 0, 'span_x': 12, 'span_y': 4}
            layout: 布局类型（standard, centered, two_column）
            
        Returns:
            HTML字符串
        """
        content_blocks = content_blocks or []
        
        # 生成HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title or 'Slide'}</title>
    <style>
        {self._generate_css()}
    </style>
</head>
<body>
    <div class="canvas">
        <div class="container">
            {self._generate_title_html(title)}
            {self._generate_content_blocks_html(content_blocks)}
        </div>
    </div>
</body>
</html>
"""
        return html
    
    def _generate_css(self) -> str:
        """生成CSS样式（Ant Design规范）"""
        # 将cm转换为px（1cm ≈ 37.8px at 96dpi）
        cm_to_px = 37.8
        padding_lg_px = int(ant_design_theme.get_spacing_cm('lg') * cm_to_px)  # 24px
        padding_md_px = int(ant_design_theme.get_spacing_cm('md') * cm_to_px)  # 16px
        padding_sm_px = int(ant_design_theme.get_spacing_cm('sm') * cm_to_px)  # 12px
        padding_xs_px = int(ant_design_theme.get_spacing_cm('xs') * cm_to_px)  # 8px
        
        return f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            width: {self.CANVAS_WIDTH}px;
            height: {self.CANVAS_HEIGHT}px;
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            /* 渐变背景 - 提升美感 */
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            overflow: visible; /* 允许内容溢出，不截断 */
            position: relative;
        }}
        
        /* 装饰性背景元素 */
        body::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 40%;
            height: 100%;
            background: linear-gradient(135deg, rgba(24, 144, 255, 0.05) 0%, rgba(24, 144, 255, 0.02) 100%);
            pointer-events: none;
        }}
        
        .canvas {{
            width: 100%;
            height: 100%;
            position: relative; /* 为绝对定位的子元素提供定位上下文 */
            padding: 0; /* 移除padding，使用绝对定位 */
        }}
        
        .container {{
            position: relative; /* 为绝对定位的子元素提供定位上下文 */
            width: 100%;
            height: 100%;
            /* 不再使用Grid布局，改用绝对定位 */
        }}
        
        /* Card样式（融合Ant Design间距原则与中式布局习惯） */
        .card {{
            position: absolute; /* 使用绝对定位，基于坐标系 */
            background: {ant_design_theme.colors.colorBgContainer}; /* 使用Ant Design背景色 */
            border: 1px solid {ant_design_theme.colors.colorBorder}; /* 使用Ant Design边框色 */
            border-radius: {ant_design_theme.borderRadius.borderRadius}px; /* 使用Ant Design圆角 */
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            padding: {padding_lg_px}px; /* 24px，基于Ant Design 8px原则 */
            display: flex;
            flex-direction: row; /* 水平排列，确保文字水平显示 */
            flex-wrap: wrap; /* 允许换行 */
            align-items: flex-start; /* 中式PPT习惯：内容左对齐 */
            overflow: visible; /* 允许内容溢出，不截断 */
            word-wrap: break-word; /* 允许长单词换行 */
            word-break: break-word; /* 允许在任意字符间换行（中文友好） */
            overflow-wrap: break-word; /* 现代浏览器支持 */
            writing-mode: horizontal-tb; /* 确保水平文字方向 */
        }}
        
        /* 标题样式（中式布局，但保持Ant Design配色，增强美感） */
        .title {{
            font-family: {chinese_ppt_theme.typography.fontFamilyHeading};
            font-size: {chinese_ppt_theme.typography.fontSizeHeading1}px;
            font-weight: {chinese_ppt_theme.typography.fontWeightStrong};
            /* 渐变文字效果 - 提升美感 */
            background: linear-gradient(135deg, {ant_design_theme.colors.colorPrimary} 0%, #40a9ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin: 0;
            word-wrap: break-word;
            word-break: break-word;
            line-height: {chinese_ppt_theme.typography.lineHeightHeading};
            position: relative;
            letter-spacing: 2px; /* 增加字间距，更优雅 */
        }}
        
        /* 标题装饰线 */
        .title::after {{
            content: '';
            position: absolute;
            bottom: -{padding_sm_px}px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, transparent, {ant_design_theme.colors.colorPrimary}, transparent);
            border-radius: 2px;
        }}
        
        .subtitle {{
            font-family: {chinese_ppt_theme.typography.fontFamilyHeading};
            font-size: {chinese_ppt_theme.typography.fontSizeHeading3}px;
            font-weight: {chinese_ppt_theme.typography.fontWeightStrong};
            color: {ant_design_theme.colors.colorText}; /* 使用Ant Design文本色 */
            text-align: left; /* 中式PPT习惯：左对齐 */
            margin-bottom: {padding_md_px}px;
            word-wrap: break-word;
            word-break: break-word;
        }}
        
        /* 正文样式（中式布局：左对齐，但保持Ant Design配色） */
        .body-text {{
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            font-weight: {chinese_ppt_theme.typography.fontWeight};
            color: {ant_design_theme.colors.colorText}; /* 使用Ant Design文本色 */
            line-height: {chinese_ppt_theme.typography.lineHeight};
            margin: {padding_sm_px}px 0;
            text-align: left; /* 中式PPT习惯：左对齐 */
            word-wrap: break-word;
            word-break: break-word;
            overflow-wrap: break-word;
            white-space: normal; /* 允许换行 */
            overflow: visible; /* 不截断内容 */
            max-width: 100%; /* 确保不超出容器 */
        }}
        
        /* 正文段落间距 */
        .body-text p {{
            margin: {padding_sm_px}px 0;
        }}
        
        /* 关键要点样式（中式布局：左对齐，但保持Ant Design配色） */
        .key-points {{
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            font-weight: {chinese_ppt_theme.typography.fontWeightStrong};
            color: {ant_design_theme.colors.colorText}; /* 使用Ant Design文本色 */
            line-height: {chinese_ppt_theme.typography.lineHeight};
            text-align: left; /* 中式PPT习惯：左对齐 */
            word-wrap: break-word;
            word-break: break-word;
            overflow-wrap: break-word;
            white-space: normal; /* 允许换行 */
            overflow: visible; /* 不截断内容 */
            max-width: 100%; /* 确保不超出容器 */
            margin: 0;
            padding: 0;
        }}
        
        /* 关键要点列表项样式 */
        .key-points li {{
            margin-bottom: {padding_md_px}px;
            padding-left: {padding_lg_px}px;
            position: relative;
        }}
        
        .key-points li::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: {ant_design_theme.colors.colorPrimary};
            font-weight: bold;
            font-size: {chinese_ppt_theme.typography.fontSizeHeading3}px;
        }}
        
        /* 数据高亮样式（根据重要性优化） */
        .data-highlight {{
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            color: {ant_design_theme.colors.colorText};
            text-align: left;
            margin: {padding_md_px}px 0;
            padding: {padding_md_px}px;
            background: {ant_design_theme.colors.colorBgLayout};
            border-radius: {ant_design_theme.borderRadius.borderRadius}px;
        }}
        
        .data-highlight-important {{
            background: linear-gradient(135deg, #e6f7ff 0%, #bae7ff 100%);
            border-left: 4px solid {ant_design_theme.colors.colorPrimary};
            padding: {padding_lg_px}px;
            margin: {padding_md_px}px 0;
            border-radius: {ant_design_theme.borderRadius.borderRadius + 2}px;
            box-shadow: 
                0 4px 12px rgba(24, 144, 255, 0.15),
                0 2px 4px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }}
        
        /* 数据高亮装饰效果 */
        .data-highlight-important::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, rgba(24, 144, 255, 0.1) 0%, transparent 70%);
            border-radius: 50%;
            transform: translate(30%, -30%);
        }}
        
        .data-value {{
            font-size: {chinese_ppt_theme.typography.fontSizeHeading2}px;
            font-weight: {chinese_ppt_theme.typography.fontWeightStrong};
            /* 渐变文字效果 */
            background: linear-gradient(135deg, {ant_design_theme.colors.colorPrimary} 0%, #40a9ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            display: inline-block;
            margin-right: {padding_md_px}px;
            text-shadow: 0 2px 4px rgba(24, 144, 255, 0.2);
        }}
        
        .data-label {{
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            color: {ant_design_theme.colors.colorText};
            display: inline-block;
        }}
        
        /* 案例研究样式（结构化展示） */
        .case-study {{
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            color: {ant_design_theme.colors.colorText};
            text-align: left;
            margin: {padding_lg_px}px 0;
            padding: {padding_lg_px}px;
            background: {ant_design_theme.colors.colorBgLayout};
            border-radius: {ant_design_theme.borderRadius.borderRadius}px;
            border-left: 4px solid {ant_design_theme.colors.colorSuccess};
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .case-header {{
            font-weight: {chinese_ppt_theme.typography.fontWeightStrong};
            margin-bottom: {padding_md_px}px;
        }}
        
        .case-company {{
            font-size: {chinese_ppt_theme.typography.fontSizeHeading4}px;
            color: {ant_design_theme.colors.colorPrimary};
        }}
        
        .case-industry {{
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            color: {ant_design_theme.colors.colorTextSecondary};
            margin-left: {padding_md_px}px;
        }}
        
        .case-content {{
            margin: {padding_md_px}px 0;
        }}
        
        .case-key-points {{
            margin-top: {padding_md_px}px;
            padding-left: {padding_lg_px}px;
        }}
        
        /* 列表样式 */
        .key-points ul {{
            margin: 0;
            padding-left: {padding_lg_px}px;
            word-wrap: break-word;
            word-break: break-word;
            list-style: none; /* 移除默认列表样式，使用自定义样式 */
        }}
        
        .key-points li {{
            margin-bottom: {padding_md_px}px;
            word-wrap: break-word;
            word-break: break-word;
            padding-left: {padding_lg_px}px;
            position: relative;
        }}
        
        .key-points li::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: {ant_design_theme.colors.colorPrimary};
            font-weight: bold;
            font-size: {chinese_ppt_theme.typography.fontSizeHeading3}px;
        }}
        
        /* 不同类型内容块的视觉区分 - 增强美感 */
        .card.key-points {{
            background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
            border-left: 4px solid {ant_design_theme.colors.colorPrimary};
            box-shadow: 
                0 4px 16px rgba(24, 144, 255, 0.1),
                0 2px 8px rgba(0, 0, 0, 0.06),
                0 0 0 1px rgba(24, 144, 255, 0.05);
            padding: {padding_lg_px}px !important; /* 确保内边距 */
        }}
        
        /* 单个要点卡片样式（独立卡片设计） */
        .card.key-point-card {{
            background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
            border-left: 4px solid {ant_design_theme.colors.colorPrimary};
            box-shadow: 
                0 4px 16px rgba(24, 144, 255, 0.1),
                0 2px 8px rgba(0, 0, 0, 0.06),
                0 0 0 1px rgba(24, 144, 255, 0.05);
            padding: {padding_lg_px}px !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}
        
        .key-point-title {{
            font-family: {chinese_ppt_theme.typography.fontFamilyHeading};
            font-size: {chinese_ppt_theme.typography.fontSizeHeading3}px;
            font-weight: {chinese_ppt_theme.typography.fontWeightStrong};
            color: {ant_design_theme.colors.colorPrimary};
            margin: 0 0 {padding_sm_px}px 0;
        }}
        
        .key-point-desc {{
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            color: {ant_design_theme.colors.colorText};
            margin: 0;
            line-height: {chinese_ppt_theme.typography.lineHeight};
        }}
        
        .key-point-text {{
            font-family: {chinese_ppt_theme.typography.fontFamilyBody};
            font-size: {chinese_ppt_theme.typography.fontSizeBody}px;
            color: {ant_design_theme.colors.colorText};
            margin: 0;
            line-height: {chinese_ppt_theme.typography.lineHeight};
        }}
        
        .card.data-highlight {{
            background: linear-gradient(135deg, #f0f9ff 0%, #e6f7ff 100%);
            border-left: 4px solid {ant_design_theme.colors.colorPrimary};
            box-shadow: 
                0 4px 16px rgba(24, 144, 255, 0.1),
                0 2px 8px rgba(0, 0, 0, 0.06),
                0 0 0 1px rgba(24, 144, 255, 0.05);
            padding: {padding_lg_px}px !important; /* 确保内边距 */
        }}
        
        .card.case-study {{
            background: linear-gradient(135deg, #f6ffed 0%, #f0f9e8 100%);
            border-left: 4px solid {ant_design_theme.colors.colorSuccess};
            box-shadow: 
                0 4px 16px rgba(82, 196, 26, 0.1),
                0 2px 8px rgba(0, 0, 0, 0.06),
                0 0 0 1px rgba(82, 196, 26, 0.05);
            padding: {padding_lg_px}px !important; /* 确保内边距 */
        }}
        
        /* 数据高亮样式 */
        .data-highlight {{
            background: {ant_design_theme.colors.colorBgLayout};
            border-left: 3px solid {ant_design_theme.colors.colorPrimary};
            padding-left: {padding_md_px}px;
        }}
        
        /* 案例样式 */
        .case-study {{
            font-style: italic;
            color: {ant_design_theme.colors.colorTextSecondary};
        }}
        
        /* 列表样式 */
        ul, ol {{
            margin: {padding_sm_px}px 0;
            padding-left: {padding_lg_px}px;
        }}
        
        li {{
            margin: {padding_xs_px}px 0;
            line-height: {ant_design_theme.typography.lineHeight};
        }}
        """
    
    def _generate_title_html(self, title: Optional[str]) -> str:
        """生成标题HTML"""
        if not title:
            logger.debug("--- [HTMLGenerator]: 无标题，跳过标题HTML生成")
            return ""
        
        logger.info(f"--- [HTMLGenerator]: 【标题】生成标题HTML: {title[:50]}...")
        logger.info(f"    栅格位置: 列 2-24, 行 1-3 (留左右边距)")
        
        # 标题容器：留一些边距，不占满整行（例如：列2-24，留左右边距）
        # 使用坐标转换：grid_x=2, grid_y=0, span_x=22, span_y=2
        left, top, width, height = self._grid_to_pixel(2, 0, 22, 2)
        return f"""
        <div class="card" style="left: {left}px; top: {top}px; width: {width}px; height: {height}px; justify-content: center; align-items: center;">
            <h1 class="title">{title}</h1>
        </div>
        """
    
    def _generate_content_blocks_html(self, content_blocks: List[Dict[str, Any]]) -> str:
        """生成内容块HTML"""
        if not content_blocks:
            logger.debug("--- [HTMLGenerator]: 无内容块，返回空")
            return ""
        
        html_parts = []
        
        # 智能布局分配
        num_blocks = len(content_blocks)
        logger.info(f"--- [HTMLGenerator]: 开始生成{num_blocks}个内容块的HTML")
        
        # 根据内容块数量和类型分配布局
        grid_positions = []
        
        if num_blocks == 1:
            # 单个内容块：居中，留边距，增加高度以容纳更多内容
            grid_positions = [{'x': 3, 'y': 4, 'span_x': 18, 'span_y': 8}]
        elif num_blocks == 2:
            # 两个内容块：根据类型智能布局
            left_type = content_blocks[0].get('type', 'body')
            right_type = content_blocks[1].get('type', 'body')
            left_content = content_blocks[0].get('text', '').strip()
            right_content = content_blocks[1].get('text', '').strip()
            left_len = len(left_content)
            right_len = len(right_content)
            
            # 如果一个是关键要点，一个是数据高亮，使用上下布局
            if (left_type == 'key_points' and right_type == 'data_highlight') or \
               (left_type == 'data_highlight' and right_type == 'key_points'):
                # 关键要点在上，数据高亮在下（或反之）
                if left_type == 'key_points':
                    grid_positions = [
                        {'x': 3, 'y': 4, 'span_x': 18, 'span_y': 5},  # 上：关键要点
                        {'x': 3, 'y': 10, 'span_x': 18, 'span_y': 3}  # 下：数据高亮
                    ]
                else:
                    grid_positions = [
                        {'x': 3, 'y': 4, 'span_x': 18, 'span_y': 3},  # 上：数据高亮
                        {'x': 3, 'y': 8, 'span_x': 18, 'span_y': 5}   # 下：关键要点
                    ]
            else:
                # 其他情况：左右对称布局
                length_diff = abs(left_len - right_len)
                length_ratio = max(left_len, right_len) / max(min(left_len, right_len), 1)
                
                if length_ratio > 3 and length_diff > 150:
                    # 内容长度差异很大：主次分明布局
                    if left_len > right_len:
                        grid_positions = [
                            {'x': 2, 'y': 4, 'span_x': 13, 'span_y': 8},  # 左：主
                            {'x': 16, 'y': 4, 'span_x': 6, 'span_y': 8}   # 右：次
                        ]
                    else:
                        grid_positions = [
                            {'x': 2, 'y': 4, 'span_x': 6, 'span_y': 8},   # 左：次
                            {'x': 9, 'y': 4, 'span_x': 13, 'span_y': 8}   # 右：主
                        ]
                else:
                    # 对称均衡布局
                    grid_positions = [
                        {'x': 2, 'y': 4, 'span_x': 10, 'span_y': 8},  # 左
                        {'x': 13, 'y': 4, 'span_x': 10, 'span_y': 8}  # 右
                    ]
                    logger.info(f"--- [HTMLGenerator]: 使用对称均衡布局（中国述职PPT风格）")
        elif num_blocks == 3:
            # 三个内容块：根据类型智能布局
            # 常见情况：关键要点 + 数据高亮 + 案例说明
            block_types = [b.get('type', 'body') for b in content_blocks]
            
            if 'key_points' in block_types and 'data_highlight' in block_types:
                # 关键要点在上，数据和案例在下
                key_idx = next(i for i, t in enumerate(block_types) if t == 'key_points')
                data_idx = next(i for i, t in enumerate(block_types) if t == 'data_highlight')
                other_idx = next(i for i in range(3) if i not in [key_idx, data_idx])
                
                grid_positions = [None] * 3
                grid_positions[key_idx] = {'x': 3, 'y': 4, 'span_x': 18, 'span_y': 4}  # 上：关键要点
                grid_positions[data_idx] = {'x': 2, 'y': 9, 'span_x': 10, 'span_y': 4}  # 左下：数据
                grid_positions[other_idx] = {'x': 13, 'y': 9, 'span_x': 10, 'span_y': 4}  # 右下：其他
            else:
                # 默认：上1下2
                grid_positions = [
                    {'x': 3, 'y': 4, 'span_x': 18, 'span_y': 3},  # 上：居中
                    {'x': 2, 'y': 8, 'span_x': 10, 'span_y': 5},   # 左下
                    {'x': 13, 'y': 8, 'span_x': 10, 'span_y': 5}   # 右下
                ]
        else:
            # 多个内容块：网格布局，留边距，增加高度
            cols = 2
            rows = (num_blocks + cols - 1) // cols
            for idx in range(num_blocks):
                col = idx % cols
                row = idx // cols
                grid_positions.append({
                    'x': 2 + col * 11,  # 从第2列开始，每列占11格
                    'y': 4 + row * 3,
                    'span_x': 10,  # 每个块占10列
                    'span_y': 3  # 增加高度
                })
        
        for idx, block in enumerate(content_blocks):
            block_type = block.get('type', 'body')
            text = block.get('text', '').strip()
            block_key = block.get('key', f'block_{idx}')
            
            # 跳过空内容
            if not text:
                logger.debug(f"--- [HTMLGenerator]: 跳过空内容块 {idx} ({block_key})")
                continue
            
            # 获取栅格位置
            grid_pos = grid_positions[idx] if idx < len(grid_positions) else grid_positions[-1]
            
            # 【日志探针】记录布局信息
            logger.info(f"--- [HTMLGenerator]: 【布局】内容块 {idx+1}/{num_blocks}")
            logger.info(f"    Key: {block_key}")
            logger.info(f"    类型: {block_type}")
            logger.info(f"    内容长度: {len(text)} 字符")
            logger.info(f"    内容预览: {text[:50]}...")
            logger.info(f"    栅格位置: x={grid_pos['x']}, y={grid_pos['y']}, span_x={grid_pos['span_x']}, span_y={grid_pos['span_y']}")
            logger.info(f"    实际位置: 列 {grid_pos['x']}-{grid_pos['x']+grid_pos['span_x']}, 行 {grid_pos['y']}-{grid_pos['y']+grid_pos['span_y']}")
            
            # 检查重叠
            for prev_idx, prev_block in enumerate(content_blocks[:idx]):
                if prev_block.get('text', '').strip():
                    prev_grid_pos = grid_positions[prev_idx] if prev_idx < len(grid_positions) else grid_positions[-1]
                    # 检查是否重叠
                    x_overlap = not (grid_pos['x'] >= prev_grid_pos['x'] + prev_grid_pos['span_x'] or 
                                   grid_pos['x'] + grid_pos['span_x'] <= prev_grid_pos['x'])
                    y_overlap = not (grid_pos['y'] >= prev_grid_pos['y'] + prev_grid_pos['span_y'] or 
                                   grid_pos['y'] + grid_pos['span_y'] <= prev_grid_pos['y'])
                    if x_overlap and y_overlap:
                        logger.warning(f"--- [HTMLGenerator]: ⚠️ 检测到重叠！")
                        logger.warning(f"    块 {prev_idx+1} ({prev_grid_pos}) 与 块 {idx+1} ({grid_pos}) 重叠")
            
            # 生成CSS类名
            css_class = self._get_css_class_for_type(block_type)
            
            # 生成HTML
            # 使用坐标转换函数计算像素位置
            left, top, width, height = self._grid_to_pixel(
                grid_pos['x'], 
                grid_pos['y'], 
                grid_pos['span_x'], 
                grid_pos['span_y']
            )
            grid_style = (
                f"left: {left}px; "
                f"top: {top}px; "
                f"width: {width}px; "
                f"height: {height}px;"
            )
            
            html_parts.append(f"""
            <div class="card {css_class}" style="{grid_style}">
                {self._format_text_content(text, block_type)}
            </div>
            """)
        
        logger.info(f"--- [HTMLGenerator]: 完成生成{len(html_parts)}个内容块的HTML")
        return "\n".join(html_parts)
    
    def _get_css_class_for_type(self, block_type: str) -> str:
        """根据内容类型获取CSS类名"""
        type_map = {
            'title': '',
            'subtitle': 'subtitle',
            'body': 'body-text',
            'key_points': 'key-points',
            'key_point_card': 'key-point-card',  # 单个要点卡片
            'data_highlight': 'data-highlight',
            'case_study': 'case-study',
        }
        return type_map.get(block_type, 'body-text')
    
    def _format_text_content(self, text: str, block_type: str) -> str:
        """格式化文本内容（中式布局：左对齐，支持数据高亮和案例结构化展示）"""
        if block_type == 'key_point_card':
            # 单个要点卡片：作为独立的卡片内容，不显示列表符号
            # 尝试提取标题和描述（如果有冒号分隔）
            if ':' in text or '：' in text:
                # 支持中英文冒号
                separator = ':' if ':' in text else '：'
                parts = text.split(separator, 1)
                title = parts[0].strip()
                desc = parts[1].strip() if len(parts) > 1 else ""
                if desc:
                    return f"""
                    <h3 class='key-point-title'>{title}</h3>
                    <p class='key-point-desc'>{desc}</p>
                    """
            
            # 【改进】如果没有冒号，智能提取标题
            # 方法1: 如果内容较长（>20字），提取前几个关键词作为标题
            if len(text) > 20:
                # 尝试提取关键词（常见模式：前几个字 + 逗号/句号）
                import re
                # 模式1: 提取前几个字（到第一个逗号或句号）
                match = re.match(r'^([^，。、；：！？]{4,12})[，。、；：！？]', text)
                if match:
                    title = match.group(1)
                    desc = text[len(title):].lstrip('，。、；：！？').strip()
                    if desc:
                        return f"""
                        <h3 class='key-point-title'>{title}</h3>
                        <p class='key-point-desc'>{desc}</p>
                        """
                
                # 模式2: 提取关键词（如"多元化"、"外部合作"等）
                # 常见关键词模式：2-4字的词
                keywords = re.findall(r'[多元化|外部|合作|生态|体系|渠道|平台|系统|团队|模式|转型|推广|集成|对接]{2,4}', text[:30])
                if keywords:
                    # 取第一个关键词作为标题
                    title = keywords[0]
                    desc = text
                    return f"""
                    <h3 class='key-point-title'>{title}</h3>
                    <p class='key-point-desc'>{desc}</p>
                    """
            
            # 如果内容较短或无法提取，直接显示文本（但格式化为标题样式）
            if len(text) <= 15:
                # 短文本：作为标题
                return f"<h3 class='key-point-title'>{text}</h3>"
            else:
                # 长文本：提取前几个字作为标题，剩余作为描述
                title = text[:8] + '...' if len(text) > 8 else text
                desc = text
                return f"""
                <h3 class='key-point-title'>{title}</h3>
                <p class='key-point-desc'>{desc}</p>
                """
        elif block_type == 'key_points':
            # 关键要点：转换为列表，左对齐（保留兼容性）
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            list_items = "\n".join([f"<li style='text-align: left;'>{line}</li>" for line in lines])
            return f"<ul class='key-points' style='text-align: left;'>{list_items}</ul>"
        elif block_type == 'subtitle':
            # 副标题：左对齐
            return f"<h2 class='subtitle' style='text-align: left;'>{text}</h2>"
        elif block_type == 'data_highlight':
            # 数据高亮：结构化展示
            # 尝试解析数据格式（如"40-60% (成本降低)"或"• 40-60%"）
            import re
            data_match = re.search(r'(\d+[%％]|\d+\.\d+%|\d+[-\d]*%)', text)
            if data_match:
                data_value = data_match.group(1)
                label = text.replace(data_value, '').strip(' •()')
                return f"""
                <div class="data-highlight-important">
                    <span class="data-value">{data_value}</span>
                    {f'<span class="data-label">{label}</span>' if label else ''}
                </div>
                """
            else:
                # 简单格式
                return f"<div class='data-highlight'>{text}</div>"
        elif block_type == 'case_study':
            # 案例研究：结构化展示
            return f"""
            <div class="case-study">
                <div class="case-content">
                    <p>{text}</p>
                </div>
            </div>
            """
        else:
            # 正文：保留换行，左对齐
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
            para_html = "\n".join([f"<p class='body-text' style='text-align: left;'>{p}</p>" for p in paragraphs])
            return para_html
    
    def generate_from_content_map(
        self,
        content_map: Dict[str, str],
        slide_structure: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        根据内容映射生成HTML
        
        Args:
            content_map: 内容映射字典 {key: content}
            slide_structure: 幻灯片结构信息
            
        Returns:
            HTML字符串
        """
        logger.info("="*80)
        logger.info("--- [HTMLGenerator]: 开始生成HTML")
        logger.info(f"    内容映射项数: {len(content_map)}")
        logger.info("="*80)
        
        # 按幻灯片分组内容
        slides_content = {}
        
        for key, content in content_map.items():
            logger.debug(f"--- [HTMLGenerator]: 处理内容项: {key} (长度: {len(content)} 字符)")
            # 解析slide_idx
            slide_idx = 0
            if 'slide_' in key:
                try:
                    slide_idx = int(key.split('_')[1])
                except:
                    pass
            
            if slide_idx not in slides_content:
                slides_content[slide_idx] = {
                    'title': None,
                    'content_blocks': []
                }
            
            # 判断是否为标题
            is_title = 'placeholder_0' in key or ('title' in key.lower() and 'placeholder' in key)
            logger.debug(f"--- [HTMLGenerator]: Key={key}, Slide={slide_idx}, IsTitle={is_title}")
            
            if is_title:
                # 只取第一个标题，避免重复
                if slides_content[slide_idx]['title'] is None:
                    slides_content[slide_idx]['title'] = content
                    logger.info(f"--- [HTMLGenerator]: 【标题】幻灯片{slide_idx}: {content[:50]}...")
                else:
                    logger.warning(f"--- [HTMLGenerator]: ⚠️ 跳过重复标题 (幻灯片{slide_idx}): {content[:50]}...")
            else:
                # 判断内容类型
                block_type = self._detect_content_type(content)
                
                # 【改进】根据key名称更精确地识别内容类型
                if 'key_points' in key.lower() or content.strip().startswith('•'):
                    # 关键要点：以•开头或key包含key_points
                    block_type = 'key_points'
                elif 'data' in key.lower() or '📊' in content:
                    # 数据高亮：包含📊或key包含data
                    block_type = 'data_highlight'
                elif 'case' in key.lower() or '💡' in content:
                    # 案例说明：包含💡或key包含case
                    block_type = 'case_study'
                
                logger.debug(f"--- [HTMLGenerator]: 内容块类型检测: {block_type} (Key: {key})")
                
                # 【关键改进】如果是关键要点类型，且包含多个要点，拆分成独立的卡片
                if block_type == 'key_points':
                    # 检测是否包含多个要点（以•开头或换行分隔）
                    lines = [line.strip() for line in content.split('\n') if line.strip()]
                    points = []
                    for line in lines:
                        # 移除开头的•或●等符号
                        clean_line = line.lstrip('•●·- ')
                        if clean_line:
                            points.append(clean_line)
                    
                    if len(points) > 1:
                        # 多个要点：拆分成独立的卡片
                        logger.info(f"--- [HTMLGenerator]: 【设计改进】检测到{len(points)}个关键要点，拆分成独立卡片")
                        for point_idx, point in enumerate(points):
                            slides_content[slide_idx]['content_blocks'].append({
                                'text': point,
                                'type': 'key_point_card',  # 新的类型：单个要点卡片
                                'key': f"{key}_point_{point_idx}"
                            })
                    else:
                        # 单个要点：作为普通内容块
                        slides_content[slide_idx]['content_blocks'].append({
                            'text': content,
                            'type': block_type,
                            'key': key
                        })
                else:
                    # 其他类型：正常添加
                    slides_content[slide_idx]['content_blocks'].append({
                        'text': content,
                        'type': block_type,
                        'key': key  # 保留key用于调试
                    })
        
        logger.info(f"--- [HTMLGenerator]: 幻灯片分组完成，共{len(slides_content)}张")
        logger.info(f"--- [HTMLGenerator]: 【探针】幻灯片内容分布:")
        for slide_idx in sorted(slides_content.keys()):
            slide_data = slides_content[slide_idx]
            logger.info(f"   幻灯片{slide_idx}: 标题={'有' if slide_data['title'] else '无'}, 内容块数={len(slide_data['content_blocks'])}")
        
        if slides_content:
            # 【探针】检查是否应该生成多张幻灯片
            # 如果有多张幻灯片且每张都有内容，应该生成多张
            # 但目前浏览器渲染只支持单张，所以合并所有内容
            # TODO: 未来可以扩展为支持多张幻灯片
            
            first_slide_idx = min(slides_content.keys())
            first_slide = slides_content[first_slide_idx]
            logger.info(f"--- [HTMLGenerator]: 第一张幻灯片: {first_slide_idx}")
            logger.info(f"    标题: {first_slide['title'][:50] if first_slide['title'] else '(无)'}...")
            logger.info(f"    内容块数: {len(first_slide['content_blocks'])}")
            
            # 如果没有标题，尝试从其他幻灯片获取
            if first_slide['title'] is None:
                logger.warning("--- [HTMLGenerator]: ⚠️ 第一张幻灯片无标题，尝试从其他幻灯片获取")
                for slide_idx in sorted(slides_content.keys()):
                    if slides_content[slide_idx]['title']:
                        first_slide['title'] = slides_content[slide_idx]['title']
                        logger.info(f"--- [HTMLGenerator]: 从幻灯片{slide_idx}获取标题: {first_slide['title'][:50]}...")
                        break
            
            # 【修复】支持多张幻灯片：为每张幻灯片生成独立的HTML
            if len(slides_content) == 1:
                logger.info("--- [HTMLGenerator]: 单张幻灯片模式")
                return [self.generate_slide_html(
                    title=first_slide['title'],
                    content_blocks=first_slide['content_blocks']
                )]
            else:
                # 多张幻灯片：为每张生成独立的HTML
                logger.info(f"--- [HTMLGenerator]: 检测到{len(slides_content)}张幻灯片，为每张生成独立的HTML")
                logger.info(f"--- [HTMLGenerator]: 【探针】各幻灯片内容块数:")
                for slide_idx in sorted(slides_content.keys()):
                    logger.info(f"   幻灯片{slide_idx}: {len(slides_content[slide_idx]['content_blocks'])}个内容块")
                
                html_slides = []
                for slide_idx in sorted(slides_content.keys()):
                    slide_data = slides_content[slide_idx]
                    logger.info(f"--- [HTMLGenerator]: 生成幻灯片{slide_idx}的HTML")
                    html_slide = self.generate_slide_html(
                        title=slide_data['title'],
                        content_blocks=slide_data['content_blocks']
                    )
                    html_slides.append(html_slide)
                
                logger.info(f"--- [HTMLGenerator]: 总计生成{len(html_slides)}张独立的HTML幻灯片")
                return html_slides
        
        logger.warning("--- [HTMLGenerator]: ⚠️ 无内容，生成空幻灯片")
        return self.generate_slide_html()
    
    def _detect_content_type(self, content: str) -> str:
        """检测内容类型"""
        if not content:
            return 'body'
        
        content_lower = content.lower()
        content_stripped = content.strip()
        
        # 关键要点：包含"关键要点"或以项目符号开头
        if '关键要点' in content or content_stripped.startswith('•') or content_stripped.startswith('-'):
            return 'key_points'
        # 数据高亮：包含"数据"或百分比
        elif '数据' in content or '%' in content or '增长' in content or '提升' in content:
            return 'data_highlight'
        # 案例研究：包含"案例"或"例子"
        elif '案例' in content or '例子' in content or '实例' in content:
            return 'case_study'
        # 副标题：短文本且可能是标题
        elif len(content_stripped) < 50 and ('介绍' in content or '概述' in content or '解析' in content):
            return 'subtitle'
        else:
            return 'body'
    
    def generate_from_layout_plan(
        self,
        layout_plans: List[Dict[str, Any]],
        polished_slides: List[Dict[str, Any]],
        color_configs: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """
        根据布局规划生成HTML（精确布局）
        
        Args:
            layout_plans: 布局规划列表，每个元素包含：
                - slide_index: 幻灯片索引
                - layout_plan: 布局规划详情
                    - overall_structure: 整体布局结构描述
                    - element_positions: 元素位置列表
                        - element_id: 元素ID
                        - element_type: 元素类型
                        - position_description: 位置描述
                        - size_description: 尺寸描述
                        - alignment: 对齐方式
                        - spacing: 间距对象
                    - element_spacing: 元素间距说明
                    - visual_hierarchy: 视觉层次说明
                    - design_specifications: 设计规范说明
            polished_slides: 润色后的幻灯片列表，每个元素包含：
                - slide_index: 幻灯片索引
                - title: 标题
                - content: 内容描述
                - visual_elements_detail: 视觉元素详情列表
                    - element_id: 元素ID
                    - element_type: 元素类型
                    - title: 标题
                    - content: 内容
                    - data: 数据
                    - description: 描述
                    
        Returns:
            HTML字符串列表，每个元素对应一张幻灯片
        """
        logger.info("="*80)
        logger.info("--- [HTMLGenerator]: 根据布局规划和颜色配置生成HTML（精确布局+颜色）")
        logger.info(f"    布局规划数量: {len(layout_plans)}")
        logger.info(f"    润色幻灯片数量: {len(polished_slides)}")
        logger.info(f"    颜色配置数量: {len(color_configs) if color_configs else 0}")
        logger.info("="*80)
        
        # 【探针】检查输入数据
        logger.info("="*80)
        logger.info("--- [HTMLGenerator]: 【探针0】generate_from_layout_plan输入数据检查")
        logger.info(f"--- [HTMLGenerator]: layout_plans数量: {len(layout_plans)}")
        logger.info(f"--- [HTMLGenerator]: polished_slides数量: {len(polished_slides)}")
        logger.info(f"--- [HTMLGenerator]: color_configs数量: {len(color_configs) if color_configs else 0}")
        
        # 检查slide_index分布
        if layout_plans:
            layout_indices = [l.get('slide_index', 0) for l in layout_plans]
            logger.info(f"--- [HTMLGenerator]: layout_plans的slide_index范围: {min(layout_indices)} - {max(layout_indices)}")
        
        if polished_slides:
            polished_indices = [p.get('slide_index', 0) for p in polished_slides]
            logger.info(f"--- [HTMLGenerator]: polished_slides的slide_index范围: {min(polished_indices)} - {max(polished_indices)}")
        
        logger.info("="*80)
        
        html_slides = []
        
        # 按slide_index排序
        layout_plans_sorted = sorted(layout_plans, key=lambda x: x.get('slide_index', 0))
        polished_slides_sorted = sorted(polished_slides, key=lambda x: x.get('slide_index', 0))
        color_configs_sorted = sorted(color_configs, key=lambda x: x.get('slide_index', 0)) if color_configs else []
        
        # 创建润色内容的索引（使用(slide_index, element_id)作为键，避免冲突）
        polished_content_map = {}
        logger.info("="*80)
        logger.info("--- [HTMLGenerator]: 【探针1】构建polished_content_map（使用(slide_index, element_id)作为键）")
        logger.info(f"--- [HTMLGenerator]: polished_slides数量: {len(polished_slides_sorted)}")
        
        for polished_slide in polished_slides_sorted:
            slide_idx = polished_slide.get('slide_index', 0)
            visual_elements = polished_slide.get('visual_elements_detail', [])
            logger.info(f"--- [HTMLGenerator]: 幻灯片{slide_idx}: {len(visual_elements)}个视觉元素")
            
            for elem in visual_elements:
                elem_id = elem.get('element_id', '')
                if elem_id:
                    # 使用(slide_index, element_id)作为键，避免不同幻灯片的相同element_id冲突
                    key = (slide_idx, elem_id)
                    polished_content_map[key] = {
                        'slide_index': slide_idx,
                        'element': elem,
                        'polished_slide': polished_slide
                    }
                else:
                    logger.warning(f"--- [HTMLGenerator]: ⚠️ 幻灯片{slide_idx}发现缺失element_id的元素: {elem.get('element_type', 'unknown')}")
        
        logger.info(f"--- [HTMLGenerator]: polished_content_map键数量: {len(polished_content_map)}")
        logger.info("="*80)
        
        # 创建颜色配置的索引（使用(slide_index, element_id)作为键，避免冲突）
        color_map = {}
        for color_config in color_configs_sorted:
            slide_idx = color_config.get('slide_index', 0)
            element_colors = color_config.get('color_config', {}).get('element_colors', [])
            for elem_color in element_colors:
                elem_id = elem_color.get('element_id', '')
                if elem_id:
                    # 使用(slide_index, element_id)作为键，避免不同幻灯片的相同element_id冲突
                    key = (slide_idx, elem_id)
                    color_map[key] = elem_color
        
        # 为每张布局规划生成HTML
        logger.info("="*80)
        logger.info("--- [HTMLGenerator]: 【探针2】开始生成HTML，检查slide_index匹配")
        logger.info(f"--- [HTMLGenerator]: layout_plans数量: {len(layout_plans_sorted)}")
        logger.info(f"--- [HTMLGenerator]: polished_slides数量: {len(polished_slides_sorted)}")
        
        # 检查slide_index分布
        layout_slide_indices = [l.get('slide_index', 0) for l in layout_plans_sorted]
        polished_slide_indices = [p.get('slide_index', 0) for p in polished_slides_sorted]
        logger.info(f"--- [HTMLGenerator]: layout_plans的slide_index列表: {sorted(set(layout_slide_indices))}")
        logger.info(f"--- [HTMLGenerator]: polished_slides的slide_index列表: {sorted(set(polished_slide_indices))}")
        
        # 检查是否有重复的slide_index
        if len(layout_slide_indices) != len(set(layout_slide_indices)):
            logger.warning(f"--- [HTMLGenerator]: ⚠️ layout_plans中有重复的slide_index")
            from collections import Counter
            duplicates = [k for k, v in Counter(layout_slide_indices).items() if v > 1]
            logger.warning(f"--- [HTMLGenerator]:   重复的slide_index: {duplicates}")
        
        if len(polished_slide_indices) != len(set(polished_slide_indices)):
            logger.warning(f"--- [HTMLGenerator]: ⚠️ polished_slides中有重复的slide_index")
            from collections import Counter
            duplicates = [k for k, v in Counter(polished_slide_indices).items() if v > 1]
            logger.warning(f"--- [HTMLGenerator]:   重复的slide_index: {duplicates}")
        
        logger.info("="*80)
        
        for layout_plan_data in layout_plans_sorted:
            slide_idx = layout_plan_data.get('slide_index', 0)
            layout_plan = layout_plan_data.get('layout_plan', {})
            
            logger.info(f"--- [HTMLGenerator]: 生成幻灯片{slide_idx}的HTML（基于布局规划+颜色配置）")
            
            # 找到对应的润色内容
            polished_slide = None
            matched_slides = []
            for ps in polished_slides_sorted:
                if ps.get('slide_index', 0) == slide_idx:
                    matched_slides.append(ps)
                    if polished_slide is None:
                        polished_slide = ps
            
            if len(matched_slides) > 1:
                logger.warning(f"--- [HTMLGenerator]: ⚠️ 幻灯片{slide_idx}匹配到{len(matched_slides)}个polished_slide，使用第一个")
            
            if not polished_slide:
                logger.warning(f"--- [HTMLGenerator]: ⚠️ 未找到幻灯片{slide_idx}的润色内容，使用默认内容")
                continue
            
            # 找到对应的颜色配置
            color_config = None
            for cc in color_configs_sorted:
                if cc.get('slide_index', 0) == slide_idx:
                    color_config = cc
                    break
            
            # 生成HTML
            html_content = self._generate_html_from_layout_plan(
                layout_plan=layout_plan,
                polished_slide=polished_slide,
                polished_content_map=polished_content_map,
                color_map=color_map
            )
            html_slides.append(html_content)
        
        logger.info(f"--- [HTMLGenerator]: ✅ 总计生成{len(html_slides)}张HTML幻灯片（基于布局规划）")
        return html_slides
    
    def generate_merged_html(
        self,
        layout_plans: List[Dict[str, Any]],
        polished_slides: List[Dict[str, Any]],
        color_configs: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        生成合并的HTML文件（所有幻灯片在一个文件中）
        使用新的画布生成器，确保每张幻灯片独立显示
        
        Args:
            layout_plans: 布局规划列表
            polished_slides: 润色后的幻灯片列表
            color_configs: 颜色配置列表
            
        Returns:
            合并后的HTML字符串
        """
        logger.info("="*80)
        logger.info("--- [HTMLGenerator]: 生成合并的HTML文件（所有幻灯片）")
        logger.info(f"    布局规划数量: {len(layout_plans)}")
        logger.info(f"    润色幻灯片数量: {len(polished_slides)}")
        logger.info("="*80)
        
        # 先生成所有单独的HTML幻灯片
        html_slides = self.generate_from_layout_plan(
            layout_plans=layout_plans,
            polished_slides=polished_slides,
            color_configs=color_configs
        )
        
        # 提取每张幻灯片的canvas-container内容（只提取画布部分，避免重复）
        slide_canvases = []
        for idx, html_content in enumerate(html_slides):
            # 提取canvas-container及其内容
            import re
            # 匹配canvas-container及其内部所有内容（包括嵌套的div）
            # 使用更精确的匹配，找到canvas-container的开始和结束
            canvas_start = re.search(r'<div[^>]*id=["\']canvas-container["\'][^>]*>', html_content)
            if canvas_start:
                start_pos = canvas_start.start()
                # 从开始位置查找匹配的结束标签
                depth = 0
                pos = start_pos
                while pos < len(html_content):
                    if html_content[pos:pos+4] == '<div':
                        depth += 1
                        pos = html_content.find('>', pos) + 1
                    elif html_content[pos:pos+6] == '</div>':
                        depth -= 1
                        if depth == 0:
                            end_pos = pos + 6
                            canvas_content = html_content[start_pos:end_pos]
                            break
                        pos += 6
                    else:
                        pos += 1
                else:
                    # 如果没找到匹配的结束标签，使用简单匹配
                    canvas_match = re.search(
                        r'<div[^>]*id=["\']canvas-container["\'][^>]*>.*?</div>',
                        html_content,
                        re.DOTALL
                    )
                    if canvas_match:
                        canvas_content = canvas_match.group(0)
                    else:
                        canvas_content = None
            else:
                canvas_content = None
            
            if canvas_content:
                slide_canvases.append(f"""
        <!-- 幻灯片 {idx} -->
        <div class="slide" id="slide-{idx}">
            {canvas_content}
        </div>""")
            else:
                # 如果没找到canvas-container，尝试提取body内容
                body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
                if body_match:
                    body_content = body_match.group(1)
                    slide_canvases.append(f"""
        <!-- 幻灯片 {idx} -->
        <div class="slide" id="slide-{idx}">
            {body_content}
        </div>""")
        
        # 使用画布生成器的CSS样式
        canvas_css = self.canvas_generator._generate_canvas_css(show_grid=True)
        
        # 生成合并的HTML（使用新的画布样式）
        merged_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>演示文稿 - 所有幻灯片</title>
    <style>
        {canvas_css}
        
        /* 幻灯片容器样式 */
        .slide {{
            margin: 20px auto; /* 居中显示，上下间距20px */
            display: block; /* 确保每个幻灯片独立显示 */
        }}
        
        body {{
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            font-family: 'Microsoft YaHei', 'SimHei', 'Arial', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center; /* 水平居中 */
            min-height: 100vh;
        }}
    </style>
</head>
<body>
    {''.join(slide_canvases)}
</body>
</html>"""
        
        logger.info(f"--- [HTMLGenerator]: ✅ 合并HTML文件生成完成，包含{len(slide_canvases)}张幻灯片")
        return merged_html
    
    def _generate_html_from_layout_plan(
        self,
        layout_plan: Dict[str, Any],
        polished_slide: Dict[str, Any],
        polished_content_map: Dict[Tuple[int, str], Dict[str, Any]],
        color_map: Optional[Dict[Tuple[int, str], Dict[str, Any]]] = None
    ) -> str:
        """
        根据单张幻灯片的布局规划生成HTML
        
        【CSS-First 架构】：优先使用 LLM 生成的 HTML/CSS 代码
        【向后兼容】：如果没有 html_code，回退到 Python 坐标计算模式
        
        Args:
            layout_plan: 布局规划详情
            polished_slide: 润色后的幻灯片内容
            polished_content_map: 润色内容映射（按element_id索引）
            color_map: 颜色配置映射
            
        Returns:
            HTML字符串
        """
        # 【CSS-First 架构】优先检查新架构字段
        if 'html_code' in layout_plan:
            logger.info("🚀 [HTMLGenerator]: 检测到 CSS-First 新架构，使用 LLM 生成的 HTML...")
            return self._generate_html_from_llm_code(
                llm_html_code=layout_plan['html_code'],
                polished_slide=polished_slide,
                color_map=color_map
            )
        
        # 【向后兼容】回退到旧架构（Python 坐标计算模式）
        logger.info("⚠️ [HTMLGenerator]: 未检测到 html_code，回退到 Python 坐标计算模式...")
        return self._generate_html_legacy(
            layout_plan=layout_plan,
            polished_slide=polished_slide,
            polished_content_map=polished_content_map,
            color_map=color_map
        )
    
    def _generate_html_from_llm_code(
        self,
        llm_html_code: str,
        polished_slide: Dict[str, Any],
        color_map: Optional[Dict[Tuple[int, str], Dict[str, Any]]] = None
    ) -> str:
        """
        从 LLM 生成的 HTML 代码生成完整 HTML
        
        【核心职责】：不做数学计算，只做"拼装"
        - 注入 Design Tokens (CSS 变量)
        - 组装完整的 HTML 结构
        - 确保所有元素都有 data-ppt-element 属性
        
        Args:
            llm_html_code: LLM 生成的 HTML 代码（通常是 body 内容）
            polished_slide: 润色后的幻灯片内容（用于提取标题等元信息）
            color_map: 颜色配置映射
            
        Returns:
            完整的 HTML 字符串
        """
        logger.info("--- [HTMLGenerator]: 开始组装 CSS-First HTML...")
        
        # 1. 生成 Design Tokens (CSS 变量)
        css_vars = self._generate_css_design_tokens(color_map)
        
        # 2. 提取标题（用于 <title> 标签）
        slide_title = polished_slide.get('title', 'CSS-First PPT Slide')
        
        # 3. 组装完整 HTML
        full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{slide_title}</title>
    <style>
        /* 全局重置 */
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        /* 注入 Ant Design Design Tokens */
        {css_vars}
        
        /* 基础样式 */
        html, body {{
            width: 100%;
            height: 100%;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: var(--ant-bg-color-layout, #F0F2F5);
            overflow: hidden; /* 防止滚动条 */
        }}
        
        /* Utility Classes (类似 Tailwind，方便 LLM 使用) */
        .flex {{ display: flex; }}
        .flex-col {{ flex-direction: column; }}
        .flex-row {{ flex-direction: row; }}
        .flex-1 {{ flex: 1; }}
        .h-full {{ height: 100%; }}
        .h-screen {{ height: 100vh; }}
        .w-full {{ width: 100%; }}
        .w-screen {{ width: 100vw; }}
        .items-center {{ align-items: center; }}
        .items-start {{ align-items: flex-start; }}
        .items-end {{ align-items: flex-end; }}
        .justify-center {{ justify-content: center; }}
        .justify-between {{ justify-content: space-between; }}
        .justify-start {{ justify-content: flex-start; }}
        .justify-end {{ justify-content: flex-end; }}
        .gap-4 {{ gap: 16px; }}
        .gap-6 {{ gap: 24px; }}
        .gap-8 {{ gap: 32px; }}
        .p-4 {{ padding: 16px; }}
        .p-6 {{ padding: 24px; }}
        .p-8 {{ padding: 32px; }}
        .p-12 {{ padding: 48px; }}
        .mb-4 {{ margin-bottom: 16px; }}
        .mb-6 {{ margin-bottom: 24px; }}
        .mb-8 {{ margin-bottom: 32px; }}
        .mt-4 {{ margin-top: 16px; }}
        .mt-6 {{ margin-top: 24px; }}
        .mt-8 {{ margin-top: 32px; }}
        .text-center {{ text-align: center; }}
        .text-left {{ text-align: left; }}
        .text-right {{ text-align: right; }}
    </style>
</head>
<body>
    <!-- LLM 生成的 HTML 内容（直接嵌入） -->
    {llm_html_code}
</body>
</html>"""
        
        logger.info("--- [HTMLGenerator]: ✅ CSS-First HTML 组装完成")
        return full_html
    
    def _generate_css_design_tokens(
        self,
        color_map: Optional[Dict[Tuple[int, str], Dict[str, Any]]] = None
    ) -> str:
        """
        生成 Ant Design Design Tokens (CSS 变量)
        
        确保风格统一，即使 LLM 生成的 HTML 不同
        如果提供了 color_map，会从中提取颜色并动态调整 CSS 变量
        
        Args:
            color_map: 颜色配置映射（可选，用于动态调整颜色）
            格式: {(slide_idx, element_id): {'text_color': '#xxx', 'border_color': '#xxx', ...}}
            
        Returns:
            CSS 变量定义字符串
        """
        # 默认颜色值
        default_primary = "#1677FF"
        default_success = "#52C41A"
        default_warning = "#FA8C16"
        default_error = "#F5222D"
        
        # 从 color_map 中提取颜色（如果提供）
        if color_map:
            # 提取主色（从标题或第一个元素的 border_color）
            primary_colors = []
            for key, color_config in color_map.items():
                border_color = color_config.get('border_color', '')
                text_color = color_config.get('text_color', '')
                if border_color and border_color.startswith('#'):
                    primary_colors.append(border_color)
                elif text_color and text_color.startswith('#'):
                    primary_colors.append(text_color)
            
            if primary_colors:
                # 使用第一个找到的颜色作为主色
                default_primary = primary_colors[0]
                logger.info(f"--- [HTMLGenerator]: 从 color_map 提取主色: {default_primary}")
        
        return f"""
        :root {{
            /* --- Ant Design Color Tokens --- */
            --ant-color-primary: {default_primary};
            --ant-color-success: {default_success};
            --ant-color-warning: {default_warning};
            --ant-color-error: {default_error};
            --ant-color-info: {default_primary};
            
            /* --- Text Colors (文本语义色) --- */
            --ant-text-color: rgba(0, 0, 0, 0.88);
            --ant-text-color-heading: rgba(0, 0, 0, 0.88); /* #262626, 用于大标题 (H1, H2, H3) - 深黑色，庄重 */
            --ant-text-color-body: rgba(0, 0, 0, 0.65);    /* #595959, 用于正文 (段落文本) - 深灰 */
            --ant-text-color-secondary: rgba(0, 0, 0, 0.45); /* #8C8C8C, 用于Footer或辅助说明 - 浅灰 */
            --ant-text-color-tertiary: rgba(0, 0, 0, 0.45);
            --ant-text-color-disabled: rgba(0, 0, 0, 0.25);
            
            /* --- Backgrounds --- */
            --ant-bg-color-layout: #F0F2F5;
            --ant-bg-color-container: #FFFFFF;
            --ant-bg-color-elevated: #FFFFFF;
            
            /* --- Borders & Shadows --- */
            --ant-border-color: #F0F0F0;
            --ant-border-color-split: #F0F0F0;
            --ant-border-radius-base: 8px;
            --ant-border-radius-sm: 4px;
            --ant-border-radius-lg: 12px;
            --ant-box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02);
            --ant-box-shadow-card: 0 1px 2px 0 rgba(0, 0, 0, 0.03), 0 1px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px 0 rgba(0, 0, 0, 0.02);
            --ant-box-shadow-hover: 0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 9px 28px 8px rgba(0, 0, 0, 0.05);
            
            /* --- Spacing --- */
            --ant-padding-xs: 8px;
            --ant-padding-sm: 12px;
            --ant-padding-md: 16px;
            --ant-padding-lg: 24px;
            --ant-padding-xl: 32px;
            
            /* --- Typography --- */
            --ant-font-size-sm: 12px;
            --ant-font-size-base: 14px;
            --ant-font-size-lg: 16px;
            --ant-font-size-xl: 20px;
            --ant-font-size-xxl: 24px;
            --ant-font-size-title: 48px;
            --ant-line-height-base: 1.5715;
            --ant-line-height-lg: 1.5;
        }}
        """
    
    def _generate_html_legacy(
        self,
        layout_plan: Dict[str, Any],
        polished_slide: Dict[str, Any],
        polished_content_map: Dict[Tuple[int, str], Dict[str, Any]],
        color_map: Optional[Dict[Tuple[int, str], Dict[str, Any]]] = None
    ) -> str:
        """
        【向后兼容】旧架构：使用 Python 计算坐标
        
        当 LLM 没有生成 html_code 时，回退到此方法
        
        Args:
            layout_plan: 布局规划详情
            polished_slide: 润色后的幻灯片内容
            polished_content_map: 润色内容映射（按element_id索引）
            color_map: 颜色配置映射
            
        Returns:
            HTML字符串
        """
        element_positions = layout_plan.get('element_positions', [])
        overall_structure = layout_plan.get('overall_structure', '')
        visual_hierarchy = layout_plan.get('visual_hierarchy', '')
        design_specs = layout_plan.get('design_specifications', '')
        
        # 获取当前幻灯片的slide_index
        slide_idx = polished_slide.get('slide_index', 0)
        
        # 【新方法】使用画布生成器
        # 1. 将布局规划转换为画布元素格式
        canvas_elements = []
        
        # 按元素位置排序（确保渲染顺序正确）
        sorted_elements = sorted(element_positions, key=lambda x: self._parse_position_priority(x))
        
        logger.info("="*80)
        logger.info(f"--- [HTMLGenerator]: 【探针3】处理幻灯片{slide_idx}的元素")
        logger.info(f"--- [HTMLGenerator]: element_positions数量: {len(element_positions)}")
        logger.info(f"--- [HTMLGenerator]: polished_content_map键数量: {len(polished_content_map)}")
        
        # 去重：使用element_id和内容哈希去重，避免重复内容
        seen_ids = set()
        seen_content_hashes = set()
        
        missing_element_ids = []  # 记录缺失的element_id
        duplicate_element_ids = []  # 记录重复的element_id
        duplicate_content_hashes = []  # 记录重复的内容哈希
        
        # 【新增】统计元素类型，用于智能布局
        element_type_counts = {}
        for elem_pos in sorted_elements:
            elem_type = elem_pos.get('element_type', '')
            if 'card' in elem_type:
                element_type_counts['card'] = element_type_counts.get('card', 0) + 1
            elif 'title' in elem_type:
                element_type_counts['title'] = element_type_counts.get('title', 0) + 1
            elif 'text' in elem_type or 'content' in elem_type:
                element_type_counts['text'] = element_type_counts.get('text', 0) + 1
        
        # 【新增】记录已处理的元素，用于计算相对位置
        processed_elements = []  # 存储已处理的元素信息，用于计算后续元素的位置
        
        for elem_pos in sorted_elements:
            elem_id = elem_pos.get('element_id', '')
            elem_type = elem_pos.get('element_type', '')
            
            # 检查element_id是否缺失
            if not elem_id:
                logger.warning(f"--- [HTMLGenerator]: ⚠️ element_positions中发现缺失element_id的元素，类型: {elem_type}")
                continue
            
            # 跳过重复的元素ID（在同一张幻灯片内）
            if elem_id in seen_ids:
                duplicate_element_ids.append(elem_id)
                logger.warning(f"--- [HTMLGenerator]: ⚠️ 跳过重复元素ID {elem_id}（在同一张幻灯片内）")
                continue
            seen_ids.add(elem_id)
            
            # 从润色内容中获取实际内容（使用(slide_index, element_id)作为键）
            key = (slide_idx, elem_id)
            polished_content_entry = polished_content_map.get(key, {})
            elem_content_data = polished_content_entry.get('element', {})
            
            # 检查element_id是否在polished_content_map中
            if key not in polished_content_map:
                missing_element_ids.append(elem_id)
                logger.warning(f"--- [HTMLGenerator]: ⚠️ element_id {elem_id} (幻灯片{slide_idx}) 在polished_content_map中不存在！")
                logger.warning(f"--- [HTMLGenerator]:   元素类型: {elem_type}")
                logger.warning(f"--- [HTMLGenerator]:   位置描述: {elem_pos.get('position_description', '')[:50]}")
                # 继续处理，但使用空内容
                elem_content_data = {}
            else:
                logger.info(f"--- [HTMLGenerator]: ✅ element_id {elem_id} (幻灯片{slide_idx}) 匹配成功")
                logger.info(f"--- [HTMLGenerator]:   来源幻灯片: {polished_content_entry.get('slide_index', 'unknown')}")
                logger.info(f"--- [HTMLGenerator]:   元素标题: {elem_content_data.get('title', '')[:50]}")
            
            # 获取元素内容文本
            title = elem_content_data.get('title', '')
            content = elem_content_data.get('content', '')
            description = elem_content_data.get('description', '')
            
            # 生成内容哈希（用于去重）
            content_hash = hash(f"{title}|{content}|{description}")
            if content_hash in seen_content_hashes:
                duplicate_content_hashes.append({
                    'element_id': elem_id,
                    'title': title[:30] if title else '无标题'
                })
                logger.warning(f"--- [HTMLGenerator]: ⚠️ 跳过重复内容元素 {elem_id} (内容: {title[:30] if title else '无标题'}...)")
                continue
            seen_content_hashes.add(content_hash)
            
            # 组合内容
            # 【修复】根据元素类型生成不同的HTML结构，避免嵌套问题
            if 'title' in elem_type and 'subtitle' not in elem_type:
                # 标题元素：只显示标题文本，不嵌套h3标签（因为外层已经是h1）
                if title:
                    display_content = title
                elif content:
                    display_content = content
                else:
                    display_content = description or ''
            elif 'subtitle' in elem_type:
                # 副标题元素：显示标题和内容，使用换行符分隔，不嵌套h3/p标签
                if title and content:
                    display_content = f"{title}<br/>{content}"
                elif title:
                    display_content = title
                elif content:
                    display_content = content
                else:
                    display_content = description or ''
            else:
                # 其他元素（如卡片）：保持原有逻辑，可以嵌套h3/p标签
                if title:
                    display_content = f"<h3>{title}</h3>"
                    if content:
                        display_content += f"<p>{content}</p>"
                    elif description:
                        display_content += f"<p>{description}</p>"
                elif content:
                    display_content = content
                elif description:
                    display_content = description
                else:
                    continue  # 跳过空内容
            
            # 解析位置描述，转换为坐标
            position_desc = elem_pos.get('position_description', '')
            size_desc = elem_pos.get('size_description', '')
            alignment = elem_pos.get('alignment', 'center')
            spacing = elem_pos.get('spacing', {})
            
            # 【改进】优先使用spacing信息，然后从位置描述中解析
            # 传入已处理的元素信息，用于计算相对位置
            # 注意：在计算卡片位置时，需要知道当前卡片的索引
            # 所以先统计当前元素之前的同类型元素数量
            current_card_index = len([e for e in processed_elements if 'card' in e.get('element_type', '')])
            current_title_index = len([e for e in processed_elements if 'title' in e.get('element_type', '')])
            current_text_index = len([e for e in processed_elements if 'text' in e.get('element_type', '') or 'content' in e.get('element_type', '')])
            
            # 【新增】查找已处理的标题元素，用于计算副标题位置
            previous_title_element = None
            if 'subtitle' in elem_type:
                logger.info(f"--- [HTMLGenerator]: 【调试】查找标题元素，processed_elements数量: {len(processed_elements)}")
                # 查找最后一个标题元素
                for e in reversed(processed_elements):
                    elem_type_check = e.get('element_type', '')
                    if 'title' in elem_type_check and 'subtitle' not in elem_type_check:
                        previous_title_element = e
                        logger.info(f"--- [HTMLGenerator]: 【调试】找到标题元素: {e.get('element_id', 'unknown')}, element_type={elem_type_check}, coordinates={e.get('coordinates', {})}")
                        break
                if not previous_title_element:
                    logger.warning(f"--- [HTMLGenerator]: 【调试】未找到标题元素，processed_elements数量: {len(processed_elements)}")
                    for e in processed_elements:
                        logger.warning(f"--- [HTMLGenerator]: 【调试】已处理元素: {e.get('element_id', 'unknown')}, element_type={e.get('element_type', '')}, has_coordinates={'coordinates' in e}")
            
            coordinates = self._parse_coordinates_from_description(
                position_desc, size_desc, elem_type, alignment, spacing,
                processed_elements=processed_elements,
                element_type_counts=element_type_counts,
                current_card_index=current_card_index if 'card' in elem_type else None,
                current_title_index=current_title_index if 'title' in elem_type else None,
                current_text_index=current_text_index if ('text' in elem_type or 'content' in elem_type) else None,
                previous_title_element=previous_title_element
            )
            
            # 记录已处理的元素
            processed_elements.append({
                'element_id': elem_id,
                'element_type': elem_type,
                'coordinates': coordinates
            })
            
            # 转换为画布元素格式
            # 【修复】根据元素类型设置正确的type
            if 'title' in elem_type and 'subtitle' not in elem_type:
                elem_type_for_canvas = 'title'
            elif 'subtitle' in elem_type:
                elem_type_for_canvas = 'text'  # 副标题也使用text类型
            elif 'card' in elem_type:
                elem_type_for_canvas = 'card'
            else:
                elem_type_for_canvas = 'text'
            
            # 获取颜色配置（如果存在）
            style_config = {}
            if color_map:
                color_key = (slide_idx, elem_id)
                color_config = color_map.get(color_key, {})
                if color_config:
                    style_config = {
                        'text_color': color_config.get('text_color', ''),
                        'background_color': color_config.get('background_color', ''),
                        'border_color': color_config.get('border_color', '')
                    }
            
            canvas_elem = {
                'id': elem_id,
                'type': elem_type_for_canvas,
                'content': display_content,
                'coordinates': coordinates,
                'style_config': style_config  # 添加颜色配置
            }
            canvas_elements.append(canvas_elem)
        
        # 探针总结
        logger.info(f"--- [HTMLGenerator]: 【探针3总结】")
        logger.info(f"--- [HTMLGenerator]:   处理前element_positions数量: {len(element_positions)}")
        logger.info(f"--- [HTMLGenerator]:   处理后canvas_elements数量: {len(canvas_elements)}")
        logger.info(f"--- [HTMLGenerator]:   缺失element_id数量: {len(missing_element_ids)}")
        logger.info(f"--- [HTMLGenerator]:   重复element_id数量: {len(duplicate_element_ids)}")
        logger.info(f"--- [HTMLGenerator]:   重复内容哈希数量: {len(duplicate_content_hashes)}")
        if missing_element_ids:
            logger.warning(f"--- [HTMLGenerator]:   缺失的element_id列表: {missing_element_ids[:10]}")
        if duplicate_element_ids:
            logger.warning(f"--- [HTMLGenerator]:   重复的element_id列表: {duplicate_element_ids[:10]}")
        logger.info("="*80)
        
        # 2. 使用画布生成器生成HTML
        title = polished_slide.get('title', '')
        html = self.canvas_generator.create_canvas_html(
            elements=canvas_elements,
            show_grid=True  # 显示栅格标准尺
        )
        
        # 3. 替换标题
        html = html.replace('<title>16:9画布 - 坐标系演示</title>', f'<title>{title or "Slide"}</title>')
        
        return html
    
    def _parse_coordinates_from_description(
        self,
        position_description: str,
        size_description: str,
        element_type: str,
        alignment: str = 'center',
        spacing: Dict[str, Any] = None,
        processed_elements: List[Dict[str, Any]] = None,
        element_type_counts: Dict[str, int] = None,
        current_card_index: int = None,
        current_title_index: int = None,
        current_text_index: int = None,
        previous_title_element: Dict[str, Any] = None
    ) -> Dict[str, float]:
        """
        从位置描述中解析坐标
        返回坐标系坐标（左下角为原点）
        
        Args:
            position_description: 位置描述（如"位于页面顶部，距离上边距80px"）
            size_description: 尺寸描述（如"宽度占页面80%"）
            element_type: 元素类型
            alignment: 对齐方式（left|center|right）
            spacing: 间距信息（包含margin_top, margin_bottom, margin_left, margin_right）
            
        Returns:
            坐标字典 {left, bottom, width, height}
        """
        import re
        
        if spacing is None:
            spacing = {}
        if processed_elements is None:
            processed_elements = []
        if element_type_counts is None:
            element_type_counts = {}
        
        # ---------------------------------------------------------
        # 1. 初始位置计算 (Initial Position Calculation)
        # ---------------------------------------------------------
        logger.info(f"--- [HTMLGenerator]: 【调试】_parse_coordinates_from_description: element_type={element_type}, previous_title_element={previous_title_element is not None}")
        
        # 场景 A: 标题元素 (通常位于顶部)
        if 'title' in element_type and 'subtitle' not in element_type:
            width = self.CANVAS_WIDTH * 0.7  # 70%宽度
            height = 80
            left = (self.CANVAS_WIDTH - width) / 2  # 居中
            
            # 默认距离顶部 80px (或者使用 LayoutPlan 中的 margin_top)
            # 注意：bottom 是距离底部的距离
            default_top_margin = 80
            
            # 优先读取 spacing 中的 margin_top
            if spacing.get('margin_top'):
                m_top = str(spacing.get('margin_top'))
                match = re.search(r'(\d+)px', m_top)
                if match:
                    default_top_margin = float(match.group(1))
            
            # 核心修复公式：bottom = 画布高度 - 上边距 - 元素高度
            bottom = self.CANVAS_HEIGHT - default_top_margin - height
            logger.info(f"--- [HTMLGenerator]: 【修复】标题位置计算: margin_top={default_top_margin}px, bottom={bottom:.1f}px")
        
        # 场景 B: 副标题 (位于标题下方)
        elif 'subtitle' in element_type:
            width = self.CANVAS_WIDTH * 0.6  # 60%宽度
            height = 60
            left = (self.CANVAS_WIDTH - width) / 2  # 居中
            
            # 尝试找到前一个标题元素
            logger.info(f"--- [HTMLGenerator]: 【调试】副标题元素处理: previous_title_element={previous_title_element is not None}")
            if previous_title_element:
                prev_coords = previous_title_element.get('coordinates', {})
                prev_bottom = prev_coords.get('bottom', 0)
                prev_height = prev_coords.get('height', 0)
                logger.info(f"--- [HTMLGenerator]: 【调试】标题元素坐标: prev_bottom={prev_bottom:.1f}, prev_height={prev_height:.1f}")
                
                # 获取间距，默认为 24px (Ant Design Large Spacing)
                gap = 24
                if spacing.get('margin_top'):  # 如果副标题定义了上边距，用作与标题的间距
                    match = re.search(r'(\d+)px', str(spacing.get('margin_top')))
                    if match:
                        gap = float(match.group(1))
                
                # 核心修复公式：向下移动 = 减法
                # 副标题底部 = 标题底部 - 间距 - 副标题高度
                # prev_bottom 是标题的下边缘，副标题的下边缘应该在标题下边缘下方
                bottom = prev_bottom - gap - height
                logger.info(f"--- [HTMLGenerator]: 【修复】副标题位置计算: 基于标题元素, prev_bottom={prev_bottom:.1f}, gap={gap:.1f}px, bottom={bottom:.1f}px")
            else:
                # 如果没找到标题，默认放在较上方
                bottom = self.CANVAS_HEIGHT - 200 - height
                logger.warning(f"--- [HTMLGenerator]: 【调试】副标题位置计算: 未找到标题元素，使用默认位置, bottom={bottom:.1f}")
        # 卡片元素：根据卡片数量智能布局
        elif 'card' in element_type:
            card_count = element_type_counts.get('card', 1)
            # 计算每个卡片的宽度（考虑间距）
            card_spacing = 24  # 卡片之间的间距
            total_spacing = (card_count - 1) * card_spacing
            available_width = self.CANVAS_WIDTH - 200  # 左右各留100px边距
            width = (available_width - total_spacing) / card_count
            
            height = 200
            
            # 计算当前卡片的位置（使用传入的current_card_index）
            card_index = current_card_index if current_card_index is not None else 0
            logger.info(f"--- [HTMLGenerator]: 【调试】卡片布局计算: card_count={card_count}, card_index={card_index}, width={width:.1f}px")
            
            if card_count == 1:
                # 单个卡片：居中
                left = (self.CANVAS_WIDTH - width) / 2
            elif card_count == 2:
                # 两个卡片：左右分屏
                left = 100 + card_index * (width + card_spacing)
            elif card_count == 3:
                # 三个卡片：横向等分，居中分布
                total_width = card_count * width + (card_count - 1) * card_spacing
                start_left = (self.CANVAS_WIDTH - total_width) / 2
                left = start_left + card_index * (width + card_spacing)
                logger.info(f"--- [HTMLGenerator]: 【调试】三个卡片布局: start_left={start_left:.1f}px, left={left:.1f}px (card_index={card_index})")
            else:
                # 多个卡片：横向排列
                total_width = card_count * width + (card_count - 1) * card_spacing
                start_left = (self.CANVAS_WIDTH - total_width) / 2
                left = start_left + card_index * (width + card_spacing)
            
            # 卡片通常在中间区域
            bottom = (self.CANVAS_HEIGHT - height) / 2
        # 文本元素：较宽，居中
        elif 'text' in element_type or 'content' in element_type:
            width = self.CANVAS_WIDTH * 0.6  # 60%宽度
            height = 150
            left = (self.CANVAS_WIDTH - width) / 2  # 居中
            # 根据已处理的元素计算位置
            if processed_elements:
                # 在最后一个元素下方
                last_elem = processed_elements[-1]
                last_coords = last_elem.get('coordinates', {})
                last_bottom = last_coords.get('bottom', 0)
                last_height = last_coords.get('height', 0)
                bottom = last_bottom - last_height - 50  # 在下方50px
            else:
                bottom = 200
        # 其他元素：默认值
        else:
            width = 400
            height = 100
            left = 100
            bottom = 100
        
        # 解析位置
        # 【重要】对于副标题元素，如果已经通过previous_title_element计算了bottom，不要被position_description覆盖
        if 'subtitle' in element_type and previous_title_element:
            # 副标题：保持基于标题元素计算的结果，忽略position_description
            pass  # bottom已经在上面通过previous_title_element计算好了
        # 顶部
        elif '顶部' in position_description or '上方' in position_description:
            top_match = re.search(r'(\d+)px', position_description)
            if top_match:
                top_px = float(top_match.group(1))
                # 转换为bottom（从底部计算）
                bottom = self.CANVAS_HEIGHT - top_px - height
        # 中间
        elif '中间' in position_description or '中央' in position_description:
            bottom = (self.CANVAS_HEIGHT - height) / 2
        # 底部
        elif '底部' in position_description or '下方' in position_description:
            bottom_match = re.search(r'(\d+)px', position_description)
            if bottom_match:
                bottom = float(bottom_match.group(1))
            else:
                bottom = 50
        
        # 【改进】优先使用spacing信息（但不要覆盖智能布局计算的结果）
        # ---------------------------------------------------------
        # 2. Spacing 覆盖保护 (Spacing Override Protection)
        # ---------------------------------------------------------
        
        # 解析上边距（margin_top）
        # 【修复】对于标题和副标题，已经通过初始计算设置了bottom，不要被spacing覆盖
        if 'subtitle' in element_type and previous_title_element:
            # 副标题：保持基于标题元素计算的结果，忽略spacing中的margin_top
            pass  # bottom已经在上面通过previous_title_element计算好了
        elif 'title' in element_type and 'subtitle' not in element_type:
            # 标题：保持基于margin_top计算的结果，不再被spacing覆盖
            pass  # bottom已经在上面通过margin_top计算好了
        elif spacing.get('margin_top'):
            margin_top_str = str(spacing.get('margin_top', ''))
            if margin_top_str and margin_top_str != 'auto':
                top_match = re.search(r'(\d+)px', margin_top_str)
                if top_match:
                    top_px = float(top_match.group(1))
                    bottom = self.CANVAS_HEIGHT - top_px - height
        
        # 解析下边距（margin_bottom）
        # 【修复】仅当元素确实是"底部对齐"的组件(如页脚)时，才允许 margin_bottom 决定绝对位置
        # 否则 margin_bottom 只是用于把别的元素推开，不影响自己
        if 'subtitle' in element_type and previous_title_element:
            # 副标题：保持基于标题元素计算的结果，忽略spacing中的margin_bottom
            pass  # bottom已经在上面通过previous_title_element计算好了
        elif 'title' in element_type and 'subtitle' not in element_type:
            # 标题：保持基于margin_top计算的结果，忽略margin_bottom（防止被覆盖）
            pass  # bottom已经在上面通过margin_top计算好了
        elif spacing.get('margin_bottom') and 'footer' in element_type:
            # 仅对页脚元素，允许margin_bottom决定绝对位置
            margin_bottom_str = str(spacing.get('margin_bottom', ''))
            if margin_bottom_str and margin_bottom_str != 'auto':
                bottom_match = re.search(r'(\d+)px', margin_bottom_str)
                if bottom_match:
                    bottom = float(bottom_match.group(1))
                    logger.info(f"--- [HTMLGenerator]: 【修复】页脚元素使用margin_bottom: bottom={bottom:.1f}px")
        # 其他元素的margin_bottom被忽略（不作为绝对位置）
        
        # 解析左边距（margin_left）
        # 【重要】对于卡片元素，如果已经通过智能布局计算了left，不要被spacing覆盖
        # 卡片元素的智能布局优先级高于spacing信息
        if 'card' in element_type and current_card_index is not None:
            # 卡片元素：保持智能布局计算的结果，忽略spacing中的left/right
            pass  # left已经在上面通过智能布局计算好了
        elif spacing.get('margin_left'):
            margin_left_str = str(spacing.get('margin_left', ''))
            if margin_left_str == 'auto':
                # 居中
                left = (self.CANVAS_WIDTH - width) / 2
            elif margin_left_str and margin_left_str != 'auto':
                left_match = re.search(r'(\d+)px', margin_left_str)
                if left_match:
                    left = float(left_match.group(1))
        
        # 解析右边距（margin_right）
        # 【重要】对于卡片元素，如果已经通过智能布局计算了left，不要被spacing覆盖
        if 'card' in element_type and current_card_index is not None:
            # 卡片元素：保持智能布局计算的结果，忽略spacing中的left/right
            pass  # left已经在上面通过智能布局计算好了
        elif spacing.get('margin_right'):
            margin_right_str = str(spacing.get('margin_right', ''))
            if margin_right_str == 'auto':
                # 居中
                left = (self.CANVAS_WIDTH - width) / 2
            elif margin_right_str and margin_right_str != 'auto':
                right_match = re.search(r'(\d+)px', margin_right_str)
                if right_match:
                    right_px = float(right_match.group(1))
                    left = self.CANVAS_WIDTH - right_px - width
        
        # 解析水平位置（如果spacing没有提供，则从position_description解析）
        # 【重要】对于卡片元素，如果已经通过智能布局计算了left，不要被position_description覆盖
        if 'card' in element_type and current_card_index is not None:
            # 卡片元素：保持智能布局计算的结果，忽略position_description
            pass  # left已经在上面通过智能布局计算好了
        elif not spacing.get('margin_left') and not spacing.get('margin_right'):
            # 只有在spacing没有提供时才从position_description解析
            if '居中' in position_description or '水平居中' in position_description or alignment == 'center':
                # 先解析宽度，然后居中
                width_match = re.search(r'(\d+(?:\.\d+)?)%', size_description)
                if width_match:
                    width_pct = float(width_match.group(1))
                    width = (self.CANVAS_WIDTH * width_pct) / 100
                left = (self.CANVAS_WIDTH - width) / 2
            elif '左' in position_description or alignment == 'left':
                left_match = re.search(r'(\d+)px', position_description)
                if left_match:
                    left = float(left_match.group(1))
                else:
                    # 默认左对齐，留出边距
                    left = 100
            elif '右' in position_description or alignment == 'right':
                right_match = re.search(r'(\d+)px', position_description)
                if right_match:
                    right_px = float(right_match.group(1))
                    # 先解析宽度
                    width_match = re.search(r'(\d+(?:\.\d+)?)%', size_description)
                    if width_match:
                        width_pct = float(width_match.group(1))
                        width = (self.CANVAS_WIDTH * width_pct) / 100
                    left = self.CANVAS_WIDTH - right_px - width
                else:
                    # 默认右对齐，留出边距
                    left = self.CANVAS_WIDTH - width - 100
        
        # 解析尺寸
        if '宽度' in size_description:
            width_match = re.search(r'宽度[：:]\s*(\d+(?:\.\d+)?)%', size_description)
            if width_match:
                width_pct = float(width_match.group(1))
                width = (self.CANVAS_WIDTH * width_pct) / 100
            elif '栅格' in size_description:
                grid_match = re.search(r'(\d+)个?栅格', size_description)
                if grid_match:
                    grid_span = int(grid_match.group(1))
                    width = grid_span * self.canvas_generator.CELL_WIDTH
        
        if '高度' in size_description:
            height_match = re.search(r'高度[：:]\s*(\d+)px', size_description)
            if height_match:
                height = float(height_match.group(1))
            elif '栅格' in size_description:
                grid_match = re.search(r'(\d+)个?栅格', size_description)
                if grid_match:
                    grid_span = int(grid_match.group(1))
                    height = grid_span * self.canvas_generator.CELL_HEIGHT
        
        return {
            'left': left,
            'bottom': bottom,
            'width': width,
            'height': height
        }
    
    def _generate_css_with_layout_plan(
        self,
        layout_plan: Dict[str, Any],
        element_positions: List[Dict[str, Any]],
        color_map: Optional[Dict[Tuple[int, str], Dict[str, Any]]] = None,
        slide_idx: int = 0
    ) -> str:
        """
        生成包含布局规划样式的CSS
        
        Args:
            layout_plan: 布局规划详情
            element_positions: 元素位置列表
            
        Returns:
            CSS字符串
        """
        # 基础CSS
        base_css = self._generate_css()
        
        # 动态样式（基于布局规划）
        dynamic_styles = []
        
        for elem_pos in element_positions:
            elem_id = elem_pos.get('element_id', '')
            elem_type = elem_pos.get('element_type', '')
            position_desc = elem_pos.get('position_description', '')
            size_desc = elem_pos.get('size_description', '')
            alignment = elem_pos.get('alignment', 'center')
            spacing = elem_pos.get('spacing', {})
            
            # 尝试从位置描述中提取栅格坐标（如果布局规划器提供了）
            grid_x = elem_pos.get('grid_x')
            grid_y = elem_pos.get('grid_y')
            span_x = elem_pos.get('span_x')
            span_y = elem_pos.get('span_y')
            
            # 如果没有提供栅格坐标，尝试从位置描述中解析
            if grid_x is None or grid_y is None:
                grid_x, grid_y, span_x, span_y = self._parse_grid_from_description(
                    position_desc, size_desc, alignment
                )
            
            # 解析位置和尺寸（如果提供了栅格坐标，使用绝对定位）
            if grid_x is not None and grid_y is not None:
                # 使用坐标转换函数计算像素位置
                left, top, width, height = self._grid_to_pixel(grid_x, grid_y, span_x or 8, span_y or 2)
                css_props = f"position: absolute;\n            left: {left}px;\n            top: {top}px;\n            width: {width}px;\n            height: {height}px;"
            else:
                # 使用原来的方法（基于margin等）
                css_props = self._parse_position_to_css(
                    element_id=elem_id,
                    position_description=position_desc,
                    size_description=size_desc,
                    alignment=alignment,
                    spacing=spacing,
                    element_type=elem_type
                )
            
            # 【新增】应用颜色配置（使用(slide_idx, element_id)作为键）
            key = (slide_idx, elem_id)
            if color_map and key in color_map:
                elem_color = color_map[key]
                if elem_color.get('text_color'):
                    css_props += f"\n            color: {elem_color['text_color']};"
                if elem_color.get('background_color'):
                    css_props += f"\n            background-color: {elem_color['background_color']};"
                if elem_color.get('border_color'):
                    css_props += f"\n            border-color: {elem_color['border_color']};"
                    css_props += f"\n            border-width: 1px;"
                    css_props += f"\n            border-style: solid;"
            
            if css_props:
                dynamic_styles.append(f"""
        /* 元素: {elem_id} ({elem_type}) */
        #{elem_id} {{
            {css_props}
        }}""")
        
        return base_css + '\n'.join(dynamic_styles)
    
    def _parse_position_to_css(
        self,
        element_id: str,
        position_description: str,
        size_description: str,
        alignment: str,
        spacing: Dict[str, Any],
        element_type: str,
        grid_x: Optional[float] = None,
        grid_y: Optional[float] = None,
        span_x: Optional[float] = None,
        span_y: Optional[float] = None
    ) -> str:
        """
        解析位置描述，生成CSS属性
        
        Args:
            element_id: 元素ID
            position_description: 位置描述（文字）
            size_description: 尺寸描述（文字）
            alignment: 对齐方式
            spacing: 间距对象
            element_type: 元素类型
            
        Returns:
            CSS属性字符串
        """
        import re
        
        css_props = []
        
        # 1. 解析位置（margin-top, margin-left等）
        # 例如："距离上边距80px" → margin-top: 80px
        if '距离上边距' in position_description or '上' in position_description:
            margin_top_match = re.search(r'(\d+)px', position_description)
            if margin_top_match:
                css_props.append(f"margin-top: {margin_top_match.group(1)}px;")
            elif 'calc' in position_description:
                # 提取calc表达式
                calc_match = re.search(r'calc\([^)]+\)', position_description)
                if calc_match:
                    css_props.append(f"margin-top: {calc_match.group(0)};")
        
        if spacing.get('margin_top'):
            css_props.append(f"margin-top: {spacing['margin_top']};")
        if spacing.get('margin_bottom'):
            css_props.append(f"margin-bottom: {spacing['margin_bottom']};")
        if spacing.get('margin_left'):
            css_props.append(f"margin-left: {spacing['margin_left']};")
        if spacing.get('margin_right'):
            css_props.append(f"margin-right: {spacing['margin_right']};")
        
        # 2. 解析尺寸（width, height）
        # 例如："宽度占页面80%" → width: 80%
        if '宽度占页面' in size_description:
            width_match = re.search(r'(\d+(?:\.\d+)?)%', size_description)
            if width_match:
                css_props.append(f"width: {width_match.group(1)}%;")
        elif '宽度' in size_description:
            width_match = re.search(r'宽度[：:]\s*(\d+(?:\.\d+)?)%', size_description)
            if width_match:
                css_props.append(f"width: {width_match.group(1)}%;")
        
        # 栅格宽度（如"占据7个栅格宽度"）
        if '栅格' in size_description:
            grid_match = re.search(r'(\d+)个?栅格', size_description)
            if grid_match:
                grid_span = int(grid_match.group(1))
                # 计算百分比（24栅格系统）
                width_pct = (grid_span / 24) * 100
                css_props.append(f"width: {width_pct:.2f}%;")
        
        # 高度
        if '高度自适应' in size_description:
            css_props.append("height: auto;")
        elif '高度' in size_description:
            height_match = re.search(r'高度[：:]\s*(\d+)px', size_description)
            if height_match:
                css_props.append(f"height: {height_match.group(1)}px;")
            elif '最小高度' in size_description:
                min_height_match = re.search(r'(\d+)px', size_description)
                if min_height_match:
                    css_props.append(f"min-height: {min_height_match.group(1)}px;")
        
        # 3. 对齐方式
        if alignment == 'center':
            css_props.append("text-align: center;")
            css_props.append("margin-left: auto;")
            css_props.append("margin-right: auto;")
        elif alignment == 'left':
            css_props.append("text-align: left;")
        elif alignment == 'right':
            css_props.append("text-align: right;")
        
        # 4. 根据元素类型添加特定样式
        if 'card' in element_type:
            css_props.append("background: #ffffff;")
            css_props.append("border: 1px solid #d9d9d9;")
            css_props.append("border-radius: 6px;")
            css_props.append("box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);")
            css_props.append("padding: 24px;")
        elif 'title' in element_type:
            # 标题样式在基础CSS中已定义，这里可以覆盖特定属性
            pass
        
        # 5. 位置定位（如果需要绝对定位）
        if '居中' in position_description and '水平居中' in position_description:
            css_props.append("position: relative;")
            # 如果同时有垂直居中，使用flex或transform
            if '垂直' in position_description or '垂直和水平居中' in position_description:
                css_props.append("display: flex;")
                css_props.append("align-items: center;")
                css_props.append("justify-content: center;")
        
        return '\n            '.join(css_props) if css_props else ''
    
    def _parse_grid_from_description(
        self,
        position_description: str,
        size_description: str,
        alignment: str
    ) -> tuple:
        """
        从位置描述中解析栅格坐标（简化版本）
        
        Args:
            position_description: 位置描述
            size_description: 尺寸描述
            alignment: 对齐方式
            
        Returns:
            (grid_x, grid_y, span_x, span_y) 栅格坐标
        """
        import re
        
        # 默认值
        grid_x = 2
        grid_y = 0
        span_x = 20
        span_y = 2
        
        # 解析位置
        if '顶部' in position_description or '上方' in position_description:
            grid_y = 11.5  # 接近顶部
        elif '中间' in position_description or '中央' in position_description:
            grid_y = 5.75  # 中间
        elif '底部' in position_description or '下方' in position_description:
            grid_y = 0  # 底部
        
        # 解析对齐
        if alignment == 'center' or '居中' in position_description:
            # 居中：左右各留2列
            grid_x = 2
            span_x = 20
        elif alignment == 'left' or '左' in position_description:
            # 左对齐：左边留2列
            grid_x = 2
            span_x = 10
        elif alignment == 'right' or '右' in position_description:
            # 右对齐：右边留2列
            grid_x = 12
            span_x = 10
        
        # 解析尺寸
        if '栅格' in size_description:
            grid_match = re.search(r'(\d+)个?栅格', size_description)
            if grid_match:
                span_x = int(grid_match.group(1))
        
        return (grid_x, grid_y, span_x, span_y)
    
    def _parse_position_priority(self, element_position: Dict[str, Any]) -> int:
        """
        解析元素位置优先级（用于排序）
        
        Args:
            element_position: 元素位置对象
            
        Returns:
            优先级数值（越小越靠前）
        """
        position_desc = element_position.get('position_description', '')
        
        # 标题通常在顶部
        if '顶部' in position_desc or '上方' in position_desc:
            return 1
        # 内容在中间
        elif '中间' in position_desc or '中央' in position_desc:
            return 2
        # 底部内容
        elif '底部' in position_desc or '下方' in position_desc:
            return 3
        else:
            return 2
    
    def _generate_element_html(
        self,
        element_id: str,
        element_type: str,
        element_position: Dict[str, Any],
        element_content: Dict[str, Any],
        visual_hierarchy: str,
        color_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        生成单个元素的HTML
        
        Args:
            element_id: 元素ID
            element_type: 元素类型
            element_position: 元素位置信息
            element_content: 元素内容（从润色内容中获取）
            visual_hierarchy: 视觉层次说明
            
        Returns:
            HTML字符串
        """
        # 获取内容
        title = element_content.get('title', '')
        content = element_content.get('content', '')
        data = element_content.get('data', '')
        description = element_content.get('description', '')
        
        # 根据元素类型生成HTML
        if 'title_text' in element_type:
            text = title or content or description
            if text:
                # 解析字号（从visual_hierarchy中提取）
                font_size = self._extract_font_size(visual_hierarchy, element_id)
                return f'<h1 id="{element_id}" class="title" style="font-size: {font_size};">{text}</h1>'
        
        elif 'subtitle_text' in element_type:
            text = title or content or description
            if text:
                font_size = self._extract_font_size(visual_hierarchy, element_id, default='32pt')
                return f'<h2 id="{element_id}" class="subtitle" style="font-size: {font_size};">{text}</h2>'
        
        elif 'content_text' in element_type:
            text = content or description
            if text:
                font_size = self._extract_font_size(visual_hierarchy, element_id, default='20pt')
                return f'<p id="{element_id}" class="body-text" style="font-size: {font_size};">{text}</p>'
        
        elif 'card' in element_type:
            # 卡片元素
            card_title = title or ''
            card_content = content or description or ''
            card_data = data or ''
            
            card_html = f'<div id="{element_id}" class="card">'
            
            if card_title:
                card_html += f'<h3 class="card-title">{card_title}</h3>'
            
            if card_data:
                card_html += f'<div class="card-data">{card_data}</div>'
            
            if card_content:
                card_html += f'<div class="card-content">{card_content}</div>'
            
            card_html += '</div>'
            return card_html
        
        return ''
    
    def _extract_font_size(self, visual_hierarchy: str, element_id: str, default: str = '48pt') -> str:
        """
        从视觉层次说明中提取字号
        
        Args:
            visual_hierarchy: 视觉层次说明
            element_id: 元素ID
            default: 默认字号
            
        Returns:
            字号字符串（如"76pt"）
        """
        import re
        
        # 尝试从visual_hierarchy中提取
        if element_id in visual_hierarchy:
            # 查找该元素相关的字号
            pattern = rf'{element_id}[^。]*?(\d+)pt'
            match = re.search(pattern, visual_hierarchy)
            if match:
                return f"{match.group(1)}pt"
        
        # 查找通用字号描述
        if '76pt' in visual_hierarchy or '超大字号' in visual_hierarchy:
            return '76pt'
        elif '48pt' in visual_hierarchy or '大号字体' in visual_hierarchy:
            return '48pt'
        elif '32pt' in visual_hierarchy or '中等字号' in visual_hierarchy:
            return '32pt'
        elif '20pt' in visual_hierarchy or '小号字体' in visual_hierarchy:
            return '20pt'
        
        return default


```


## File: human_centered_analyzer.py

```python
"""
人类中心化分析器
按照人类理解文档的真实流程进行分析：
1. 通读理解 - 理解整体思想和含义
2. 板块拆分 - 识别各个板块及其核心思想
3. 论证逻辑 - 识别支撑核心思想的论据
4. 支撑材料 - 数据、图表等佐证材料
5. 表达风格 - 语言风格、文化特征
6. 呈现形式 - 格式、布局、视觉呈现
"""

from typing import List, Dict, Any, Optional
from loguru import logger
import re
import json
from collections import defaultdict
from llm_service import LLMService


class HumanCenteredAnalyzer:
    """
    人类中心化分析器
    按照人类理解文档的真实流程进行分析
    """
    
    def __init__(self, structure_data: Dict[str, Any], raw_text: str = "", llm_service: Optional[LLMService] = None):
        """
        初始化分析器
        
        Args:
            structure_data: 增强的结构数据（包含格式信息）
            raw_text: 原始文本内容（用于整体理解）
            llm_service: LLM服务实例（用于理解文档内容）
        """
        self.structure = structure_data
        self.raw_text = raw_text
        self.llm_service = llm_service or LLMService()
        logger.info("--- [HumanCenteredAnalyzer]: 初始化人类中心化分析器（使用LLM理解）")
    
    async def analyze_all(self) -> Dict[str, Any]:
        """
        执行完整的人类中心化分析
        
        Returns:
            包含6个理解层次的完整分析结果
        """
        logger.info("="*80)
        logger.info("--- [HumanCenteredAnalyzer]: 开始人类中心化分析（使用LLM）")
        logger.info("="*80)
        
        # 第1层：通读理解 - 理解整体思想和含义
        logger.info("--- [第1层] 通读理解：理解整体思想和含义...")
        overall_understanding = await self._understand_overall()
        
        # 第2层：板块拆分 - 识别各个板块及其核心思想
        logger.info("--- [第2层] 板块拆分：识别各个板块及其核心思想...")
        sections = await self._identify_sections()
        
        # 第3层：论证逻辑 - 识别支撑核心思想的论据
        logger.info("--- [第3层] 论证逻辑：识别支撑核心思想的论据...")
        arguments = await self._identify_arguments(sections)
        
        # 第4层：支撑材料 - 数据、图表等佐证材料
        logger.info("--- [第4层] 支撑材料：识别数据、图表等佐证材料...")
        supporting_materials = self._identify_supporting_materials()
        
        # 第5层：表达风格 - 语言风格、文化特征
        logger.info("--- [第5层] 表达风格：分析语言风格和文化特征...")
        expression_style = self._analyze_expression_style()
        
        # 第6层：呈现形式 - 格式、布局、视觉呈现
        logger.info("--- [第6层] 呈现形式：分析格式、布局、视觉呈现...")
        presentation_form = self._analyze_presentation_form()
        
        result = {
            "layer_1_overall_understanding": {
                "name": "通读理解层",
                "description": "理解文档的整体思想、主题、目的和核心价值主张",
                "data": overall_understanding
            },
            "layer_2_sections": {
                "name": "板块结构层",
                "description": "识别各个板块及其传递的核心思想",
                "data": sections
            },
            "layer_3_arguments": {
                "name": "论证逻辑层",
                "description": "识别每个板块的论据和论证方式",
                "data": arguments
            },
            "layer_4_supporting_materials": {
                "name": "支撑材料层",
                "description": "数据、图表、案例等佐证材料",
                "data": supporting_materials
            },
            "layer_5_expression_style": {
                "name": "表达风格层",
                "description": "语言风格、表达方式、文化特征",
                "data": expression_style
            },
            "layer_6_presentation_form": {
                "name": "呈现形式层",
                "description": "格式、布局、视觉呈现方式",
                "data": presentation_form
            }
        }
        
        logger.info("="*80)
        logger.info("--- [HumanCenteredAnalyzer]: 人类中心化分析完成")
        logger.info(f"   识别板块数: {len(sections.get('sections', []))}")
        logger.info(f"   核心思想: {overall_understanding.get('core_idea', '')[:50]}...")
        logger.info("="*80)
        
        return result
    
    async def _understand_overall(self) -> Dict[str, Any]:
        """
        第1层：通读理解
        使用LLM理解文档的整体思想、主题、目的和核心价值主张
        """
        logger.info("--- [HumanCenteredAnalyzer]: 【详细探针】第1层：通读理解（使用LLM）")
        
        # 收集所有文本内容
        all_texts = []
        if self.raw_text:
            # 优先使用raw_text（来自docx）
            full_text = self.raw_text
            logger.info(f"   使用raw_text，长度: {len(full_text)}字符")
        else:
            # 从structure中收集文本
            logger.info(f"   收集文本内容（从{len(self.structure.get('slides', []))}张幻灯片）...")
            for slide_idx, slide in enumerate(self.structure.get("slides", [])):
                slide_texts = []
                for shape in slide.get("shapes", []):
                    text = shape.get("text", "").strip()
                    if text:
                        slide_texts.append(text)
                        all_texts.append(text)
                logger.info(f"     幻灯片{slide_idx}: 收集到{len(slide_texts)}个文本块")
                if slide_texts:
                    logger.info(f"       文本预览: {slide_texts[0][:100]}...")
            
            full_text = "\n".join(all_texts)
            logger.info(f"   总文本长度: {len(full_text)}字符")
        
        logger.info(f"   文本预览: {full_text[:300]}...")
        
        # 使用LLM理解文档整体内容
        logger.info("   使用LLM理解文档整体内容...")
        
        system_prompt = """你是中国职场的述职汇报专家，专门为副总裁级别的职场高管筹备述职内容，最擅长将高管整理的文稿大纲转换成适合呈现在ppt上的语言内容。"""
        
        user_prompt = f"""请通读以下文档内容，理解其核心思想、主题、目的和核心价值主张。

文档内容：
{full_text}

请按照以下方向进行分析：
1. 先对文档进行整体的通读了解，确保知道文档表述的核心思想
2. 识别文档的核心主题、目的、目标受众
3. 识别文档的核心价值主张和关键信息

请以JSON格式输出分析结果：
{{
  "core_theme": "核心主题",
  "core_idea": "核心思想",
  "purpose": "文档目的",
  "target_audience": "目标受众",
  "value_propositions": ["价值主张1", "价值主张2", ...],
  "key_phrases": ["关键短语1", "关键短语2", ...]
}}"""
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # 解析JSON响应
            if isinstance(response, str):
                # 尝试提取JSON
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用默认值")
                    result = {}
            else:
                result = response
            
            logger.info(f"   LLM理解结果: 核心主题={result.get('core_theme', '未识别')}")
            logger.info(f"   价值主张数量: {len(result.get('value_propositions', []))}")
            
            return {
                "core_theme": result.get("core_theme", "未明确标识"),
                "core_idea": result.get("core_idea", ""),
                "value_propositions": result.get("value_propositions", []),
                "purpose": result.get("purpose", "通用文档"),
                "target_audience": result.get("target_audience", "通用受众"),
                "total_slides": self.structure.get("slide_count", 0),
                "text_length": len(full_text),
                "key_phrases": result.get("key_phrases", [])
            }
        except Exception as e:
            logger.error(f"   LLM理解失败: {e}，使用规则分析作为回退")
            # 回退到规则分析
            return self._understand_overall_fallback(full_text)
    
    def _understand_overall_fallback(self, full_text: str) -> Dict[str, Any]:
        """回退方法：使用规则分析"""
        core_theme = self._extract_core_theme(full_text)
        value_propositions = self._extract_value_propositions(full_text)
        purpose = self._identify_purpose(full_text)
        target_audience = self._identify_target_audience(full_text)
        
        return {
            "core_theme": core_theme,
            "core_idea": "",
            "value_propositions": value_propositions,
            "purpose": purpose,
            "target_audience": target_audience,
            "total_slides": self.structure.get("slide_count", 0),
            "text_length": len(full_text),
            "key_phrases": self._extract_key_phrases(full_text)
        }
    
    def _extract_core_theme(self, text: str) -> str:
        """提取核心主题"""
        # 查找标题、副标题等
        title_patterns = [
            r'^([^。，\n]{5,30})$',  # 短标题
            r'核心[主题|思想|观点]：(.+)',
            r'主题：(.+)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                return match.group(1) if len(match.groups()) > 0 else match.group(0)
        
        # 如果没有明确标题，取第一段作为主题
        first_line = text.split('\n')[0] if text else ""
        if len(first_line) < 50:
            return first_line
        
        return "未明确标识"
    
    def _extract_value_propositions(self, text: str) -> List[str]:
        """提取核心价值主张"""
        value_props = []
        
        # 查找价值主张模式
        patterns = [
            r'核心价值[：:](.+)',
            r'价值主张[：:](.+)',
            r'(.+?)\s*[|｜]\s*(.+?)\s*[|｜]\s*(.+)',  # 用|分隔的价值主张
            r'降低(.+?)\s*[%％]',  # 降低成本
            r'提升(.+?)\s*[%％]',  # 提升效率
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    value_props.extend([m for m in match if m.strip()])
                else:
                    value_props.append(match.strip())
        
        # 去重
        return list(set(value_props))[:5]  # 最多返回5个
    
    def _identify_purpose(self, text: str) -> str:
        """识别文档目的"""
        purpose_keywords = {
            "汇报": ["汇报", "报告", "总结", "回顾"],
            "提案": ["提案", "建议", "方案", "计划"],
            "介绍": ["介绍", "概述", "说明", "展示"],
            "分析": ["分析", "研究", "评估", "调研"]
        }
        
        for purpose, keywords in purpose_keywords.items():
            if any(kw in text for kw in keywords):
                return purpose
        
        return "通用文档"
    
    def _identify_target_audience(self, text: str) -> str:
        """识别目标受众"""
        audience_keywords = {
            "管理层": ["管理层", "领导", "决策", "战略"],
            "技术团队": ["技术", "开发", "工程师", "系统"],
            "业务团队": ["业务", "销售", "市场", "客户"],
            "投资者": ["投资", "融资", "股东", "回报"]
        }
        
        for audience, keywords in audience_keywords.items():
            if any(kw in text for kw in keywords):
                return audience
        
        return "通用受众"
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """提取关键短语"""
        # 简单的关键词提取（可以后续用更高级的方法）
        key_phrases = []
        
        # 查找加粗、大字体等强调的内容
        for slide in self.structure["slides"]:
            for shape in slide["shapes"]:
                format_info = shape.get("format", {})
                if format_info.get("is_bold") or (format_info.get("font_size_pt") or 0) >= 20:
                    text = shape.get("text", "").strip()
                    if text and len(text) < 50:
                        key_phrases.append(text)
        
        return list(set(key_phrases))[:10]
    
    async def _identify_sections(self) -> Dict[str, Any]:
        """
        第2层：板块拆分
        使用LLM识别各个板块及其传递的核心思想
        """
        logger.info("--- [HumanCenteredAnalyzer]: 【详细探针】第2层：板块拆分（使用LLM）")
        
        # 收集所有文本内容
        if self.raw_text:
            full_text = self.raw_text
        else:
            all_texts = []
            for slide in self.structure.get("slides", []):
                for shape in slide.get("shapes", []):
                    text = shape.get("text", "").strip()
                    if text:
                        all_texts.append(text)
            full_text = "\n".join(all_texts)
        
        logger.info(f"   文档总长度: {len(full_text)}字符")
        
        # 使用LLM进行板块拆分
        system_prompt = """你是中国职场的述职汇报专家，专门为副总裁级别的职场高管筹备述职内容，最擅长将高管整理的文稿大纲转换成适合呈现在ppt上的语言内容。"""
        
        user_prompt = f"""请仔细重读以下文档内容，根据文档的具体内容进行细分板块的拆解，以确保让整个文档叙事具备高逻辑性、高叙事性。

文档内容：
{full_text}

请按照以下方向进行分析：
1. 仔细重读文档，识别文档中的各个板块
2. 为每个板块识别其主题、核心思想
3. 确保板块之间的逻辑连贯性和叙事性

请以JSON格式输出分析结果：
{{
  "total_sections": 板块总数,
  "sections": [
    {{
      "section_index": 板块索引（从0开始）,
      "theme": "板块主题",
      "core_idea": "板块核心思想",
      "content_summary": "板块内容摘要",
      "slides": [该板块涉及的幻灯片索引列表]
    }},
    ...
  ]
}}"""
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # 解析JSON响应
            if isinstance(response, str):
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用规则分析作为回退")
                    return self._identify_sections_fallback()
            else:
                result = response
            
            logger.info(f"   LLM识别板块数: {result.get('total_sections', 0)}")
            for section in result.get("sections", [])[:5]:  # 显示前5个
                logger.info(f"     板块{section.get('section_index', 0)}: {section.get('theme', '')}")
            
            return result
        except Exception as e:
            logger.error(f"   LLM板块拆分失败: {e}，使用规则分析作为回退")
            return self._identify_sections_fallback()
    
    def _identify_sections_fallback(self) -> Dict[str, Any]:
        """回退方法：使用规则分析"""
        sections = []
        current_section = None
        
        for slide_idx, slide in enumerate(self.structure.get("slides", [])):
            slide_theme = self._extract_slide_theme(slide)
            
            if slide_theme:
                if current_section:
                    sections.append(current_section)
                
                current_section = {
                    "section_index": len(sections),
                    "theme": slide_theme,
                    "core_idea": self._extract_core_idea(slide),
                    "slides": [slide_idx],
                    "content_summary": self._summarize_slide_content(slide)
                }
            else:
                if current_section:
                    current_section["slides"].append(slide_idx)
                    current_section["content_summary"] += " " + self._summarize_slide_content(slide)
                else:
                    current_section = {
                        "section_index": len(sections),
                        "theme": f"板块{len(sections) + 1}",
                        "core_idea": self._extract_core_idea(slide),
                        "slides": [slide_idx],
                        "content_summary": self._summarize_slide_content(slide)
                    }
        
        if current_section:
            sections.append(current_section)
        
        return {
            "total_sections": len(sections),
            "sections": sections
        }
    
    def _extract_slide_theme(self, slide: Dict[str, Any]) -> Optional[str]:
        """提取幻灯片主题"""
        # 查找标题占位符
        for shape in slide["shapes"]:
            if shape.get("is_placeholder"):
                placeholder_type = shape.get("placeholder_type", "")
                if "TITLE" in placeholder_type or "CENTER_TITLE" in placeholder_type:
                    text = shape.get("text", "").strip()
                    if text:
                        return text
        
        # 查找大字体、加粗的文本（可能是标题）
        # 【改进】优先查找第一个shape（通常是标题）
        for shape_idx, shape in enumerate(slide["shapes"]):
            format_info = shape.get("format", {})
            text = shape.get("text", "").strip()
            
            # 如果是第一个shape且是短文本，很可能是标题
            if shape_idx == 0 and text and len(text) < 50:
                # 检查是否包含标题特征（emoji、数字编号、关键词等）
                has_emoji = any(ord(c) > 127 and c not in '，。、；：！？""''（）【】《》' for c in text[:10])
                has_numbering = re.match(r'^[0-9一二三四五六七八九十]+[、.]', text) if text else False
                has_keywords = any(kw in text for kw in ['分析', '战略', '路线图', '回顾', '市场', '商业化', '技术', '产品', '文档', '启示', '规划', '能力', '路径'])
                
                if has_emoji or has_numbering or has_keywords or format_info.get("is_bold"):
                    return text
            
            # 或者检查大字体、加粗的文本
            if (format_info.get("font_size_pt") or 0) >= 20 and format_info.get("is_bold"):
                if text and len(text) < 50:
                    return text
        
        return None
    
    def _extract_core_idea(self, slide: Dict[str, Any]) -> str:
        """提取板块核心思想"""
        # 收集所有文本
        texts = []
        for shape in slide["shapes"]:
            text = shape.get("text", "").strip()
            if text:
                texts.append(text)
        
        # 取第一段作为核心思想
        if texts:
            return texts[0][:100]  # 限制长度
        
        return ""
    
    def _summarize_slide_content(self, slide: Dict[str, Any]) -> str:
        """总结幻灯片内容"""
        texts = []
        for shape in slide["shapes"]:
            text = shape.get("text", "").strip()
            if text:
                texts.append(text)
        
        return " | ".join(texts[:3])  # 最多3段
    
    async def _identify_arguments(self, sections: Dict[str, Any]) -> Dict[str, Any]:
        """
        第3层：论证逻辑
        使用LLM深入探寻每个板块的核心内容、核心思想、具体论点、核心论据以及必要的数据呈现
        """
        logger.info("--- [HumanCenteredAnalyzer]: 【详细探针】第3层：论证逻辑（使用LLM）")
        
        # 收集所有文本内容
        if self.raw_text:
            full_text = self.raw_text
        else:
            all_texts = []
            for slide in self.structure.get("slides", []):
                for shape in slide.get("shapes", []):
                    text = shape.get("text", "").strip()
                    if text:
                        all_texts.append(text)
            full_text = "\n".join(all_texts)
        
        # 为每个板块准备内容
        sections_text = []
        for section in sections.get("sections", []):
            section_text = f"板块{section.get('section_index', 0)}: {section.get('theme', '')}\n"
            section_text += f"核心思想: {section.get('core_idea', '')}\n"
            section_text += f"内容摘要: {section.get('content_summary', '')}\n"
            sections_text.append(section_text)
        
        system_prompt = """你是中国职场的述职汇报专家，专门为副总裁级别的职场高管筹备述职内容，最擅长将高管整理的文稿大纲转换成适合呈现在ppt上的语言内容。"""
        
        user_prompt = f"""请对以下文档的每个板块进行深入探寻，深度理解每个板块的核心内容、核心思想、具体论点、核心论据以及必要的数据呈现。

文档内容：
{full_text}

已识别的板块：
{chr(10).join(sections_text)}

请按照以下方向进行分析：
1. 对每个板块进行深入探寻
2. 识别每个板块的核心内容、核心思想
3. 识别每个板块的具体论点
4. 识别每个板块的核心论据
5. 识别必要的数据呈现

请以JSON格式输出分析结果：
{{
  "total_sections_with_arguments": 有论证的板块总数,
  "arguments": [
    {{
      "section_index": 板块索引,
      "section_theme": "板块主题",
      "core_content": "核心内容",
      "core_idea": "核心思想",
      "specific_arguments": ["具体论点1", "具体论点2", ...],
      "core_evidence": ["核心论据1", "核心论据2", ...],
      "data_points": ["数据点1", "数据点2", ...],
      "argument_types": ["论证类型1", "论证类型2", ...]
    }},
    ...
  ]
}}"""
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # 解析JSON响应
            if isinstance(response, str):
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用规则分析作为回退")
                    return self._identify_arguments_fallback(sections)
            else:
                result = response
            
            logger.info(f"   LLM识别论证板块数: {result.get('total_sections_with_arguments', 0)}")
            
            return result
        except Exception as e:
            logger.error(f"   LLM论证逻辑分析失败: {e}，使用规则分析作为回退")
            return self._identify_arguments_fallback(sections)
    
    def _identify_arguments_fallback(self, sections: Dict[str, Any]) -> Dict[str, Any]:
        """回退方法：使用规则分析"""
        arguments = []
        
        for section in sections.get("sections", []):
            section_args = {
                "section_index": section["section_index"],
                "section_theme": section["theme"],
                "core_content": section.get("content_summary", ""),
                "core_idea": section.get("core_idea", ""),
                "specific_arguments": [],
                "core_evidence": [],
                "data_points": [],
                "argument_types": []
            }
            
            # 分析每个幻灯片中的论据
            for slide_idx in section.get("slides", []):
                if slide_idx < len(self.structure.get("slides", [])):
                    slide = self.structure["slides"][slide_idx]
                    
                    # 识别论据类型
                    arg_types = self._identify_argument_types(slide)
                    section_args["argument_types"].extend(arg_types)
                    
                    # 识别证据点
                    evidence = self._extract_evidence_points(slide)
                    section_args["core_evidence"].extend(evidence)
            
            # 去重
            section_args["argument_types"] = list(set(section_args["argument_types"]))
            arguments.append(section_args)
        
        return {
            "total_sections_with_arguments": len(arguments),
            "arguments": arguments
        }
    
    def _identify_argument_types(self, slide: Dict[str, Any]) -> List[str]:
        """识别论证类型"""
        arg_types = []
        text = " ".join([s.get("text", "") for s in slide["shapes"]])
        
        # 数据论证
        if re.search(r'\d+[%％]|\d+\.\d+', text):
            arg_types.append("数据论证")
        
        # 案例论证
        if any(kw in text for kw in ["案例", "例子", "实例", "客户", "项目"]):
            arg_types.append("案例论证")
        
        # 对比论证
        if any(kw in text for kw in ["对比", "比较", "vs", "相比", "优于"]):
            arg_types.append("对比论证")
        
        # 因果论证
        if any(kw in text for kw in ["因为", "所以", "导致", "因此", "由于"]):
            arg_types.append("因果论证")
        
        return arg_types
    
    def _extract_evidence_points(self, slide: Dict[str, Any]) -> List[str]:
        """提取证据点"""
        evidence = []
        
        for shape in slide["shapes"]:
            text = shape.get("text", "").strip()
            if not text:
                continue
            
            # 查找数据点
            data_matches = re.findall(r'\d+[%％]|\d+\.\d+%', text)
            evidence.extend([f"数据: {m}" for m in data_matches])
            
            # 查找列表项（可能是证据点）
            if re.match(r'^[•·▪▫○●■□\d]', text):
                evidence.append(f"要点: {text[:50]}")
        
        return evidence[:5]  # 最多5个证据点
    
    def _identify_supporting_materials(self) -> Dict[str, Any]:
        """
        第4层：支撑材料
        识别数据、图表、案例等佐证材料
        """
        materials = {
            "data_points": [],
            "charts": [],
            "tables": [],
            "cases": [],
            "quotes": []
        }
        
        for slide_idx, slide in enumerate(self.structure["slides"]):
            # 查找数据点
            for shape in slide["shapes"]:
                text = shape.get("text", "").strip()
                if not text:
                    continue
                
                # 提取数据
                data_matches = re.findall(r'\d+[%％]|\d+\.\d+%|\d+万|\d+亿', text)
                for data in data_matches:
                    materials["data_points"].append({
                        "slide_index": slide_idx,
                        "data": data,
                        "context": text[:50]
                    })
                
                # 查找案例
                if any(kw in text for kw in ["案例", "例子", "客户", "项目"]):
                    materials["cases"].append({
                        "slide_index": slide_idx,
                        "content": text[:100]
                    })
        
        return {
            "total_data_points": len(materials["data_points"]),
            "total_cases": len(materials["cases"]),
            "materials": materials
        }
    
    def _analyze_expression_style(self) -> Dict[str, Any]:
        """
        第5层：表达风格
        分析语言风格、表达方式、文化特征
        """
        # 收集所有文本
        all_texts = []
        for slide in self.structure["slides"]:
            for shape in slide["shapes"]:
                text = shape.get("text", "").strip()
                if text:
                    all_texts.append(text)
        
        full_text = " ".join(all_texts)
        
        # 分析语言风格
        style_features = {
            "formality_level": self._assess_formality(full_text),
            "tone": self._assess_tone(full_text),
            "cultural_features": self._identify_cultural_features(full_text),
            "use_of_numbers": self._count_numbers(full_text),
            "use_of_emojis": self._count_emojis(full_text)
        }
        
        return style_features
    
    def _assess_formality(self, text: str) -> str:
        """评估正式程度"""
        formal_keywords = ["汇报", "报告", "总结", "分析", "评估"]
        informal_keywords = ["我们", "大家", "一起", "💎", "🚀"]
        
        formal_count = sum(1 for kw in formal_keywords if kw in text)
        informal_count = sum(1 for kw in informal_keywords if kw in text)
        
        if formal_count > informal_count:
            return "正式"
        elif informal_count > formal_count:
            return "非正式"
        else:
            return "中性"
    
    def _assess_tone(self, text: str) -> str:
        """评估语调"""
        if any(kw in text for kw in ["优秀", "卓越", "领先", "突破"]):
            return "积极"
        elif any(kw in text for kw in ["问题", "挑战", "困难", "风险"]):
            return "谨慎"
        else:
            return "中性"
    
    def _identify_cultural_features(self, text: str) -> List[str]:
        """识别文化特征"""
        features = []
        
        if any(kw in text for kw in ["朋友", "交个朋友", "我们"]):
            features.append("强调团队协作")
        
        if any(kw in text for kw in ["价值", "价值主张", "核心价值"]):
            features.append("强调价值导向")
        
        if re.search(r'\d+[%％]', text):
            features.append("数据驱动表达")
        
        return features
    
    def _count_numbers(self, text: str) -> int:
        """统计数字使用"""
        return len(re.findall(r'\d+', text))
    
    def _count_emojis(self, text: str) -> int:
        """统计表情符号使用"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "]+"
        )
        return len(emoji_pattern.findall(text))
    
    def _analyze_presentation_form(self) -> Dict[str, Any]:
        """
        第6层：呈现形式
        分析格式、布局、视觉呈现方式
        """
        form_features = {
            "layout_style": self._analyze_layout_style(),
            "typography": self._analyze_typography(),
            "visual_hierarchy": self._analyze_visual_hierarchy(),
            "color_usage": self._analyze_color_usage()
        }
        
        return form_features
    
    def _analyze_layout_style(self) -> Dict[str, Any]:
        """分析布局风格"""
        # 分析幻灯片尺寸比例
        width = self.structure.get("slide_width", 0)
        height = self.structure.get("slide_height", 0)
        ratio = width / height if height > 0 else 0
        
        if 1.7 <= ratio <= 1.8:
            aspect_ratio = "16:9"
        elif 1.3 <= ratio <= 1.35:
            aspect_ratio = "4:3"
        else:
            aspect_ratio = "其他"
        
        return {
            "aspect_ratio": aspect_ratio,
            "width_cm": width,
            "height_cm": height
        }
    
    def _analyze_typography(self) -> Dict[str, Any]:
        """分析字体排版"""
        font_sizes = set()
        font_names = set()
        bold_count = 0
        
        for slide in self.structure["slides"]:
            for shape in slide["shapes"]:
                format_info = shape.get("format", {})
                if format_info.get("font_size_pt"):
                    font_sizes.add(format_info["font_size_pt"])
                if format_info.get("font_name"):
                    font_names.add(format_info["font_name"])
                if format_info.get("is_bold"):
                    bold_count += 1
        
        return {
            "font_sizes": sorted(list(font_sizes)),
            "font_names": list(font_names),
            "bold_usage_count": bold_count
        }
    
    def _analyze_visual_hierarchy(self) -> Dict[str, Any]:
        """分析视觉层次"""
        hierarchy = {
            "title_levels": 0,
            "body_levels": 0,
            "emphasis_count": 0
        }
        
        for slide in self.structure["slides"]:
            for shape in slide["shapes"]:
                format_info = shape.get("format", {})
                font_size = format_info.get("font_size_pt") or 0
                
                if font_size >= 20:
                    hierarchy["title_levels"] += 1
                elif font_size >= 14:
                    hierarchy["body_levels"] += 1
                
                if format_info.get("is_bold"):
                    hierarchy["emphasis_count"] += 1
        
        return hierarchy
    
    def _analyze_color_usage(self) -> Dict[str, Any]:
        """分析颜色使用"""
        colors = set()
        
        for slide in self.structure["slides"]:
            for shape in slide["shapes"]:
                format_info = shape.get("format", {})
                if format_info.get("font_color"):
                    colors.add(format_info["font_color"])
        
        return {
            "unique_colors": len(colors),
            "colors": list(colors)
        }


```


## File: layout_generator.py

```python
"""
LLM辅助的布局生成器
使用LLM生成VML布局代码和内容
"""

import json
import re
from typing import Optional, Dict, List, Any
from loguru import logger

from llm_service import LLMService, create_llm_service
from ant_design_theme import ant_design_theme


class LayoutGenerator:
    """
    LLM辅助的布局生成器
    使用LLM生成VML布局代码和内容映射
    """
    
    VML_SYNTAX_GUIDE = """
VML (Virtual Markup Language) 语法指南（遵循Ant Design设计规范）：

【重要】所有设计应遵循Ant Design设计规范：
- 颜色：使用Ant Design颜色系统（主色#1890ff，成功#52c41a，警告#faad14，错误#f5222d）
- 间距：基于8px基础单位（8px, 16px, 24px, 32px等）
- 字体：使用系统字体栈（-apple-system, BlinkMacSystemFont, Segoe UI, Roboto等）
- 字号：标题38pt/30pt/24pt，正文14pt/16pt
- 圆角：基础6px，小2px，大8px

核心元素：
- <Slide padding="1.5cm" background="#ffffff">...</Slide> - 幻灯片容器（16:9横版）
  - padding: 内边距（推荐使用Ant Design间距：0.4cm/8px, 0.6cm/12px, 0.8cm/16px, 1.2cm/24px）
  - background: 背景色（推荐：#ffffff白色或#f0f2f5浅灰）

- <VStack gap="0.8cm" align="center">...</VStack> - 垂直堆叠容器
  - gap: 子元素间距（推荐：0.4cm/8px, 0.6cm/12px, 0.8cm/16px）
  - align: 对齐方式（"left", "center", "right"）

- <HStack gap="0.8cm" align="center">...</HStack> - 水平堆叠容器
  - gap: 子元素间距（同上）
  - align: 对齐方式（"top", "center", "bottom"）

- <TextBox style="title|subtitle|body" ref="ref_name" align="left|center|right" justify="top|center|bottom" color="rgba(0,0,0,0.85)" fontSize="38pt" fontWeight="bold|normal">...</TextBox>
  - style: 样式预设
    * "title": 标题（38pt，加粗，颜色rgba(0,0,0,0.85)）
    * "subtitle": 副标题（24pt，常规，颜色rgba(0,0,0,0.65)）
    * "body": 正文（14pt，常规，颜色rgba(0,0,0,0.85)）
  - ref: 内容引用名称（必需）
  - align: 水平对齐
  - justify: 垂直对齐
  - color: 文字颜色（推荐Ant Design文本色：rgba(0,0,0,0.85)主文本，rgba(0,0,0,0.65)次文本）
  - fontSize: 字体大小（推荐：38pt标题，24pt副标题，14pt正文）
  - fontWeight: 字体粗细（bold/600用于标题，normal/400用于正文）

- <ImageBox ref="ref_name" width="80%" height="60%" /> - 图片元素
  - ref: 图片引用名称（必需）
  - width: 宽度
  - height: 高度

样式容器（带背景、边框、阴影等，遵循Ant Design规范）：
- background: 背景色（推荐：#ffffff白色，#f0f2f5浅灰，#fafafa极浅灰）
- border: 边框（推荐：1px solid #d9d9d9）
- borderRadius: 圆角（推荐：6px基础，2px小，8px大）
- shadow: 阴影（推荐：0 2px 8px rgba(0,0,0,0.15)）

Ant Design配色示例：
- 主色：#1890ff（蓝色）
- 成功：#52c41a（绿色）
- 警告：#faad14（橙色）
- 错误：#f5222d（红色）
- 文本主色：rgba(0,0,0,0.85)
- 文本次色：rgba(0,0,0,0.65)
- 背景色：#ffffff（白色）
- 边框色：#d9d9d9

示例（遵循Ant Design规范）：
<Slide padding="0.8cm" background="#ffffff">
  <VStack gap="0.8cm" align="center">
    <TextBox style="title" ref="title" align="center" color="rgba(0,0,0,0.85)" />
    <TextBox style="subtitle" ref="subtitle" align="center" color="rgba(0,0,0,0.65)" />
  </VStack>
</Slide>
"""
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        初始化布局生成器
        
        Args:
            llm_service: LLM服务实例，如果为None则尝试创建
        """
        if llm_service is None:
            self.llm_service = create_llm_service(use_async=True)
            if self.llm_service is None:
                logger.warning("--- [LayoutGenerator]: LLM service not available, layout generation will be disabled")
        else:
            self.llm_service = llm_service
        
        logger.info("--- [LayoutGenerator]: Initialized")
    
    def _extract_json_from_response(self, response: str) -> Optional[Dict[str, Any]]:
        """
        从LLM响应中提取JSON
        
        Args:
            response: LLM响应文本
            
        Returns:
            解析后的JSON字典，如果失败则返回None
        """
        # 尝试直接解析
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # 尝试提取JSON代码块
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # 尝试提取任何JSON对象
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        logger.warning("--- [LayoutGenerator]: Failed to extract JSON from response")
        return None
    
    async def generate_layout_from_prompt(
        self,
        prompt: str,
        num_slides: int = 3,
        include_charts: bool = False
    ) -> Dict[str, Any]:
        """
        根据自然语言提示生成VML布局和内容
        
        Args:
            prompt: 自然语言提示，描述PPT的需求
            num_slides: 幻灯片数量
            include_charts: 是否包含图表
            
        Returns:
            包含 vml_plan 和 content_map 的字典
        """
        if not self.llm_service:
            raise ValueError("LLM service is not available")
        
        system_prompt = f"""你是一个专业的PPT布局设计师，擅长使用VML (Virtual Markup Language) 设计精美的演示文稿布局。

{self.VML_SYNTAX_GUIDE}

任务要求：
1. 根据用户的需求生成VML布局代码，**严格遵循Ant Design设计规范**
2. 使用Ant Design颜色系统（主色#1890ff，文本色rgba(0,0,0,0.85)等）
3. 使用Ant Design间距系统（基于8px：8px, 16px, 24px, 32px）
4. 使用Ant Design字体系统（系统字体栈，字号：标题38pt，副标题24pt，正文14pt）
5. 使用Ant Design圆角系统（基础6px）
6. 确保布局美观、专业、符合Ant Design设计语言
7. 如果用户提到图表，在VML中使用ImageBox引用，并在chart_insights中提供数据
8. **所有PPT必须是16:9横版比例**

输出格式（JSON）：
{{
  "vml_plan": [
    {{
      "vml_code": "<Slide>...</Slide>"
    }}
  ],
  "content_map": {{
    "ref_name": "内容文本"
  }},
  "chart_insights": [
    {{
      "insightId": "chart_ref",
      "type": "bar_chart",
      "title": "图表标题",
      "data": [...]
    }}
  ]
}}

重要规则：
- 每个TextBox必须有唯一的ref属性
- ref名称应该语义化（如 "title", "subtitle", "content_1"）
- 内容应该符合用户需求，专业且相关
- 布局应该层次清晰，视觉平衡
- 使用合适的间距和对齐方式"""
        
        user_prompt = f"""请为以下需求生成一个包含 {num_slides} 张幻灯片的PPT布局：

需求：{prompt}

{f"注意：用户可能需要图表，请根据需求在适当位置添加图表引用。" if include_charts else ""}

请生成完整的VML布局代码和内容映射。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=messages,
                temperature=0.7,
                max_tokens=4000,
                response_format={"type": "json_object"} if hasattr(self.llm_service.client, 'chat') else None
            )
            
            result = self._extract_json_from_response(response)
            if result:
                # 验证和规范化结果
                if "vml_plan" not in result:
                    result["vml_plan"] = []
                if "content_map" not in result:
                    result["content_map"] = {}
                if "chart_insights" not in result:
                    result["chart_insights"] = []
                
                logger.success(f"--- [LayoutGenerator]: Generated layout with {len(result.get('vml_plan', []))} slides")
                return result
            else:
                raise ValueError("Failed to parse LLM response as JSON")
                
        except Exception as e:
            logger.error(f"--- [LayoutGenerator]: Failed to generate layout: {e}", exc_info=True)
            raise
    
    async def optimize_layout(
        self,
        vml_plan: List[Dict[str, Any]],
        content_map: Dict[str, str],
        optimization_prompt: str
    ) -> Dict[str, Any]:
        """
        优化现有布局
        
        Args:
            vml_plan: 现有的VML计划
            content_map: 现有的内容映射
            optimization_prompt: 优化需求描述
            
        Returns:
            优化后的布局和内容
        """
        if not self.llm_service:
            raise ValueError("LLM service is not available")
        
        system_prompt = f"""你是一个专业的PPT布局优化师，擅长优化VML布局代码。

{self.VML_SYNTAX_GUIDE}

任务：根据用户的优化需求，改进现有的VML布局和内容。"""
        
        user_prompt = f"""现有布局：
VML Plan:
{json.dumps(vml_plan, ensure_ascii=False, indent=2)}

Content Map:
{json.dumps(content_map, ensure_ascii=False, indent=2)}

优化需求：{optimization_prompt}

请生成优化后的完整布局和内容。保持原有的ref名称，但可以调整布局结构和内容。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=messages,
                temperature=0.7,
                max_tokens=4000
            )
            
            result = self._extract_json_from_response(response)
            if result:
                # 确保包含所有必需字段
                if "vml_plan" not in result:
                    result["vml_plan"] = vml_plan
                if "content_map" not in result:
                    result["content_map"] = content_map
                
                logger.success("--- [LayoutGenerator]: Layout optimized")
                return result
            else:
                raise ValueError("Failed to parse LLM response as JSON")
                
        except Exception as e:
            logger.error(f"--- [LayoutGenerator]: Failed to optimize layout: {e}", exc_info=True)
            raise
    
    async def generate_content_for_layout(
        self,
        vml_plan: List[Dict[str, Any]],
        topic: str,
        style: str = "professional"
    ) -> Dict[str, str]:
        """
        为现有布局生成内容
        
        Args:
            vml_plan: VML布局计划
            topic: 主题/话题
            style: 内容风格（"professional", "casual", "academic"等）
            
        Returns:
            内容映射字典
        """
        if not self.llm_service:
            raise ValueError("LLM service is not available")
        
        # 提取所有ref
        refs = []
        for slide in vml_plan:
            vml_code = slide.get("vml_code", "")
            # 简单提取ref（实际应该用XML解析，这里简化处理）
            ref_matches = re.findall(r'ref="([^"]+)"', vml_code)
            refs.extend(ref_matches)
        
        system_prompt = """你是一个专业的内容创作助手，擅长为演示文稿生成高质量的内容。

任务：根据主题和布局结构，为每个内容引用生成合适的内容文本。"""
        
        user_prompt = f"""主题：{topic}
风格：{style}
内容引用：{', '.join(refs)}

请为每个引用生成合适的内容。内容应该：
- 符合主题
- 风格一致
- 专业且相关
- 长度适中（标题简短，正文可稍长）

输出JSON格式：
{{
  "ref_name": "内容文本"
}}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=messages,
                temperature=0.8,
                max_tokens=2000
            )
            
            result = self._extract_json_from_response(response)
            if result:
                logger.success(f"--- [LayoutGenerator]: Generated content for {len(result)} refs")
                return result
            else:
                raise ValueError("Failed to parse LLM response as JSON")
                
        except Exception as e:
            logger.error(f"--- [LayoutGenerator]: Failed to generate content: {e}", exc_info=True)
            raise


def create_layout_generator(llm_service: Optional[LLMService] = None) -> Optional[LayoutGenerator]:
    """
    创建布局生成器实例
    
    Args:
        llm_service: LLM服务实例
        
    Returns:
        LayoutGenerator实例，如果LLM不可用则返回None
    """
    try:
        return LayoutGenerator(llm_service=llm_service)
    except Exception as e:
        logger.warning(f"--- [LayoutGenerator]: Failed to create layout generator: {e}")
        return None


```


## File: layout_planner.py

```python
"""
布局规划器
基于视觉元素查询Ant Design和AntV设计规范，输出详细的文字布局规划说明
"""

from typing import List, Dict, Any, Optional
from loguru import logger
from llm_service import LLMService, create_llm_service


class LayoutPlanner:
    """
    布局规划器
    基于润色结果和展示策划，查询设计规范，输出详细的文字布局规划说明
    """
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        初始化布局规划器
        
        Args:
            llm_service: LLM服务实例
        """
        self.llm_service = llm_service or create_llm_service()
        if not self.llm_service:
            logger.warning("   ⚠️ LLM服务不可用，布局规划功能将受限")
    
    async def plan_layout(
        self,
        polished_slides: List[Dict[str, Any]],
        presentation_plan: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        规划布局
        
        Args:
            polished_slides: 润色后的幻灯片列表
            presentation_plan: 展示策划结果
            
        Returns:
            布局规划结果列表，每个元素包含详细的文字布局说明
        """
        if not self.llm_service:
            logger.warning("   ⚠️ LLM服务不可用，使用默认布局规划")
            return self._default_layout_plan(polished_slides, presentation_plan)
        
        logger.info(f"--- [LayoutPlanner]: 开始布局规划，共{len(polished_slides)}张幻灯片")
        
        layout_plans = []
        
        for idx, (polished_slide, plan) in enumerate(zip(polished_slides, presentation_plan)):
            logger.info(f"--- [LayoutPlanner]: 规划幻灯片{idx + 1}...")
            
            try:
                layout_plan = await self._plan_single_slide(
                    polished_slide=polished_slide,
                    presentation_plan=plan
                )
                layout_plans.append(layout_plan)
                logger.info(f"   ✅ 幻灯片{idx + 1}布局规划完成")
            except Exception as e:
                logger.error(f"   ❌ 幻灯片{idx + 1}布局规划失败: {e}", exc_info=True)
                # 使用默认规划
                default_plan = self._default_single_slide_plan(polished_slide, plan)
                layout_plans.append(default_plan)
        
        logger.info(f"--- [LayoutPlanner]: ✅ 布局规划完成，共规划{len(layout_plans)}张幻灯片")
        return layout_plans
    
    async def _plan_single_slide(
        self,
        polished_slide: Dict[str, Any],
        presentation_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        规划单张幻灯片的布局
        
        Args:
            polished_slide: 润色后的幻灯片
            presentation_plan: 展示策划结果
            
        Returns:
            布局规划结果
        """
        # 提取视觉元素信息
        visual_elements = polished_slide.get('visual_elements_detail', [])
        layout_type = presentation_plan.get('layout_type', '')
        layout_description = presentation_plan.get('layout_description', '')
        visual_guidance = presentation_plan.get('visual_guidance', {})
        
        # 读取设计规范文档
        design_specs = self._load_design_specifications()
        
        # 构建系统提示词（按照新架构原则：LLM生成CSS，浏览器计算坐标）
        system_prompt = """你是一个专业的UI/UX设计师，精通Ant Design和AntV设计规范。

【核心原则】：用CSS描述布局意图，让浏览器负责计算坐标。不要输出坐标，输出HTML/CSS代码。

你的任务是：
1. 基于视觉元素的数量和类型，生成完整的HTML/CSS代码
2. 使用Flex/Grid布局，让浏览器自动计算位置
3. 应用Design Tokens（CSS变量）统一管理样式
4. 为每个元素添加 data-ppt-element 属性，便于后续提取坐标

【Ant Design设计规范】：
""" + design_specs + """

【布局组件使用指南】：
- **Flex布局**：用于垂直或水平排列
  - `display: flex; flex-direction: column;` - 垂直排列
  - `display: flex; flex-direction: row;` - 水平排列
  - `justify-content: center;` - 主轴居中
  - `align-items: center;` - 交叉轴居中
  - `gap: 24px;` - 元素间距（使用Design Tokens：16px/24px/32px）

- **Grid布局**：用于网格排列
  - `display: grid; grid-template-columns: repeat(3, 1fr);` - 三列等分
  - `gap: 24px;` - 网格间距

- **卡片布局**：
  - 使用 `.ant-card` 类名
  - 白色背景，顶部装饰条（border-top: 4px solid）
  - 内边距：24px（padding-lg）
  - 圆角：8px（border-radius-base）
  - 阴影：使用Design Token（--ant-box-shadow）

【颜色使用规范（重要）】：
- **大标题 (H1)**：使用 `color: var(--ant-text-color-heading);` (深黑色 #262626)，不要使用主色
- **卡片标题 (H3)**：使用 `color: var(--ant-text-color-heading);` (深黑色)，保持专业稳重
- **正文 (P)**：使用 `color: var(--ant-text-color-body);` (深灰 #595959)
- **Footer/副标题**：使用 `color: var(--ant-text-color-secondary);` (浅灰 #8C8C8C)
- **装饰元素**：使用 `var(--ant-color-primary)` (品牌色 #1677FF)，如左侧装饰条、卡片顶部横条
- **原则**：品牌色用于装饰和强调，文本色用于内容，确保可读性和专业性

【查询设计规范的方法】：
当遇到特定数量的视觉元素时，使用对应的布局模式：
- 1个元素：Flex居中，`justify-content: center; align-items: center;`
- 2个元素：Flex水平排列，`flex-direction: row; gap: 24px;`
- 3个元素：Flex水平排列，`flex-direction: row; justify-content: space-between; gap: 24px;`
- 4个元素：Grid 2x2布局，`grid-template-columns: repeat(2, 1fr); gap: 24px;`
- 多个卡片：Flex水平排列，每个卡片 `flex: 1;`，间距使用 `gap: 24px;`

【输出要求】：
直接生成完整的HTML/CSS代码，包括：
1. 完整的HTML结构（使用Flex/Grid布局）
2. 内联CSS样式（或<style>标签）
3. 每个元素必须有 data-ppt-element 属性
4. 使用CSS变量（Design Tokens）统一管理样式

【布局策略】：
根据场景选择合适的布局：
- 述职汇报：左对齐标题 + 三列数据卡片 + 底部总结
- 产品发布：居中标题 + 大图 + 底部CTA
- 数据展示：顶部标题 + 图表网格 + 底部说明

【CSS布局示例】：
```html
<div class="slide-container" style="display: flex; flex-direction: column; height: 100vh; padding: 40px; background: var(--ant-bg-color-layout);">
  <header style="margin-bottom: 60px; border-left: 12px solid var(--ant-color-primary); padding-left: 24px;">
    <h1 data-ppt-element="true" data-ppt-element-id="title_text_0" data-ppt-element-type="title" 
        style="font-size: 48px; font-weight: 600; color: var(--ant-color-primary); text-align: left; margin: 0;">
      核心价值主张
    </h1>
  </header>
  <main style="flex: 1; display: flex; gap: 24px; align-items: stretch;">
    <div class="ant-card" data-ppt-element="true" data-ppt-element-id="value_card_0" data-ppt-element-type="card"
         style="flex: 1; background: var(--ant-bg-color-container); padding: 40px 32px; border-radius: var(--ant-border-radius-base); box-shadow: var(--ant-box-shadow); border-top: 6px solid #1677FF;">
      <h3 style="margin: 0 0 24px 0; font-size: 32px; font-weight: 700; color: #1677FF; text-align: center;">成本降低</h3>
      <p style="margin: 0; font-size: 18px; color: var(--ant-text-color-secondary); line-height: 1.8; text-align: center;">降低运营成本40-60%</p>
    </div>
    <!-- 更多卡片... -->
  </main>
  <footer style="margin-top: 40px; text-align: center; padding: 8px; background: rgba(0,0,0,0.02); border-radius: 4px;">
    <p data-ppt-element="true" data-ppt-element-id="subtitle_text_0" data-ppt-element-type="text"
       style="margin: 0; font-size: 24px; color: var(--ant-text-color-secondary);">
      全链路AI赋能解决方案
    </p>
  </footer>
</div>
```

输出格式（JSON）：
{
  "slide_index": 幻灯片索引,
  "layout_plan": {
    "html_code": "完整的HTML代码（包含<style>标签和<body>内容）",
    "layout_strategy": "布局策略说明（如：述职汇报风格，左对齐标题+三列卡片+底部总结）",
    "design_tokens_used": ["--ant-color-primary", "--ant-bg-color-container", ...]
  }
}"""
        
        # 构建用户提示词
        visual_elements_info = []
        for elem in visual_elements:
            elem_id = elem.get('element_id', '')
            elem_type = elem.get('element_type', '')
            elem_title = elem.get('title', '')
            elem_content = elem.get('content', '')[:100]
            elem_data = elem.get('data', '')
            elem_desc = elem.get('description', '')
            elem_info = f"""
- 元素ID: {elem_id}
- 元素类型: {elem_type}
- 标题: {elem_title}
- 内容: {elem_content}...
- 数据: {elem_data}
- 说明: {elem_desc}"""
            visual_elements_info.append(elem_info)
        
        # 避免f-string嵌套，使用字符串拼接
        slide_title = polished_slide.get('title', '')
        slide_content = polished_slide.get('content', '')
        slide_content_type = polished_slide.get('content_type', '')
        font_size = visual_guidance.get('font_size', '')
        font_weight = visual_guidance.get('font_weight', '')
        alignment = visual_guidance.get('alignment', '')
        spacing = visual_guidance.get('spacing', '')
        color_scheme = visual_guidance.get('color_scheme', '')
        elements_count = len(visual_elements)
        elements_info_str = ''.join(visual_elements_info)
        
        user_prompt = f"""请为以下幻灯片进行布局规划。

幻灯片信息：
- 标题: {slide_title}
- 内容: {slide_content}
- 内容类型: {slide_content_type}
- 布局类型: {layout_type}
- 布局描述: {layout_description}

视觉指导：
- 字体大小: {font_size}
- 字体粗细: {font_weight}
- 对齐方式: {alignment}
- 间距: {spacing}
- 配色: {color_scheme}

视觉元素（共{elements_count}个）：
{elements_info_str}

请基于这些视觉元素的数量和类型，查询Ant Design和AntV的设计规范，输出详细的文字布局规划说明。

要求：
1. 明确说明整体布局结构（如：三个价值卡片并排排列）
2. 详细描述每个元素的位置、尺寸、对齐方式
3. 说明元素间距（使用px单位）
4. 说明视觉层次
5. 引用具体的设计规范（如：遵循Ant Design卡片设计规范，圆角6px，内边距16px）"""
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # 解析JSON响应
            import json
            import re
            
            if isinstance(response, str):
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    layout_plan = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用默认规划")
                    return self._default_single_slide_plan(polished_slide, presentation_plan)
            else:
                layout_plan = response
            
            # 验证和规范化
            if 'layout_plan' not in layout_plan:
                logger.warning("   LLM响应缺少layout_plan字段，使用默认规划")
                return self._default_single_slide_plan(polished_slide, presentation_plan)
            
            # 确保包含slide_index
            layout_plan['slide_index'] = polished_slide.get('slide_index', 0)
            
            return layout_plan
            
        except Exception as e:
            logger.error(f"   布局规划失败: {e}", exc_info=True)
            return self._default_single_slide_plan(polished_slide, presentation_plan)
    
    def _default_single_slide_plan(
        self,
        polished_slide: Dict[str, Any],
        presentation_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """默认单张幻灯片布局规划"""
        visual_elements = polished_slide.get('visual_elements_detail', [])
        layout_type = presentation_plan.get('layout_type', 'standard')
        
        # 根据布局类型生成默认规划
        if layout_type == 'blank_center':
            overall_structure = "页面居中布局，标题和副标题垂直居中排列"
        elif layout_type == 'cards_grid':
            num_cards = len([e for e in visual_elements if 'card' in e.get('element_type', '')])
            overall_structure = f"{num_cards}个卡片横向等分排列，居中分布"
        else:
            overall_structure = "标准布局，元素按顺序排列"
        
        return {
            "slide_index": polished_slide.get('slide_index', 0),
            "layout_plan": {
                "overall_structure": overall_structure,
                "element_positions": [],
                "element_spacing": {
                    "between_elements": "默认间距24px",
                    "internal_padding": "默认内边距16px"
                },
                "visual_hierarchy": "默认视觉层次",
                "design_specifications": "遵循Ant Design基础设计规范"
            }
        }
    
    def _default_layout_plan(
        self,
        polished_slides: List[Dict[str, Any]],
        presentation_plan: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """默认布局规划"""
        return [
            self._default_single_slide_plan(slide, plan)
            for slide, plan in zip(polished_slides, presentation_plan)
        ]
    
    def _load_design_specifications(self) -> str:
        """加载设计规范文档"""
        try:
            from pathlib import Path
            design_file = Path(__file__).parent / "DESIGN_SYSTEM.md"
            if design_file.exists():
                return design_file.read_text(encoding='utf-8')
        except Exception as e:
            logger.warning(f"   无法加载设计规范文档: {e}")
        
        # 返回基础设计规范
        return """【Ant Design设计规范要点】：
- 间距系统：基于8px基础单位（8px, 16px, 24px, 32px, 48px等）
- 布局系统：24栅格系统，支持响应式布局
- 卡片设计：圆角6px，内边距16px或24px，阴影0 2px 8px rgba(0,0,0,0.15)
- 文字层级：标题38pt/30pt/24pt，正文14pt/16pt
- 对齐原则：左对齐为主，居中用于标题和强调
- 颜色系统：主色#1890ff，成功#52c41a，警告#faad14，错误#f5222d
- 文本色：主文本rgba(0,0,0,0.85)，次文本rgba(0,0,0,0.65)
- 背景色：#ffffff（白色），#f0f2f5（浅灰）
- 边框色：#d9d9d9（基础），#f0f0f0（次要）

【AntV设计规范要点】：
- 图表容器：保持适当的内边距（16px或24px），确保图表元素不贴边
- 数据可视化：遵循数据-图形映射原则
- 颜色使用：使用Ant Design颜色系统（category10分类色）
- 图表背景：白色（#ffffff）
- 网格线：浅灰（#f0f0f0）
- 坐标轴：灰色（#d9d9d9）"""


```


## File: llm_service.py

```python
"""
独立的LLM服务模块
支持DeepSeek、OpenAI等兼容OpenAI API的模型
"""

import os
from typing import Optional, List, Dict, Any
from openai import OpenAI, AsyncOpenAI
from loguru import logger


class LLMService:
    """
    独立的LLM服务类
    支持多种模型提供商（DeepSeek、OpenAI等）
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        use_async: bool = False
    ):
        """
        初始化LLM服务
        
        Args:
            api_key: API密钥，如果为None则从环境变量读取
            base_url: API基础URL，如果为None则从环境变量读取
            model_name: 模型名称，如果为None则从环境变量读取
            use_async: 是否使用异步客户端
        """
        # 从环境变量读取配置（如果未提供）
        self.api_key = api_key or os.getenv("CHAT_MODEL_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("CHAT_MODEL_BASE_URL") or os.getenv("OPENAI_BASE_URL")
        self.model_name = model_name or os.getenv("CHAT_MODEL_NAME") or "gpt-3.5-turbo"
        self.use_async = use_async
        
        if not self.api_key:
            raise ValueError(
                "API key is required. Please set CHAT_MODEL_API_KEY or OPENAI_API_KEY environment variable."
            )
        
        if not self.base_url:
            # 智能检测：如果API密钥以"sk-"开头且长度较长，可能是DeepSeek
            # DeepSeek的API密钥通常是sk-开头的长字符串
            # 默认使用DeepSeek（因为用户提供的密钥是DeepSeek的）
            if self.api_key.startswith("sk-") and len(self.api_key) > 30:
                self.base_url = "https://api.deepseek.com/v1"
                # 如果模型名是默认的，也改为DeepSeek的模型
                if self.model_name == "gpt-3.5-turbo" and not model_name:
                    self.model_name = "deepseek-chat"
                logger.info(f"--- [LLMService]: 检测到DeepSeek API密钥，使用DeepSeek URL: {self.base_url}")
            else:
                # 默认使用OpenAI的URL
                self.base_url = "https://api.openai.com/v1"
                logger.warning(f"--- [LLMService]: Base URL not set, using default: {self.base_url}")
        
        # 初始化客户端
        if use_async:
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        
        logger.info(f"--- [LLMService]: Initialized with model={self.model_name}, base_url={self.base_url}")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        同步聊天完成
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            model: 模型名称，如果为None则使用初始化时的模型
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Returns:
            生成的文本内容
        """
        model = model or self.model_name
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"--- [LLMService]: Chat completion failed: {e}", exc_info=True)
            raise
    
    async def chat_completion_async(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        异步聊天完成
        
        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            **kwargs: 其他参数
            
        Returns:
            生成的文本内容
        """
        if not self.use_async:
            # 如果初始化时没有使用异步，创建一个临时异步客户端
            async_client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            async_client = self.client
        
        model = model or self.model_name
        
        try:
            response = await async_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"--- [LLMService]: Async chat completion failed: {e}", exc_info=True)
            raise
        finally:
            if not self.use_async:
                await async_client.close()


def create_llm_service(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model_name: Optional[str] = None,
    use_async: bool = False
) -> Optional[LLMService]:
    """
    创建LLM服务实例
    
    Args:
        api_key: API密钥
        base_url: API基础URL
        model_name: 模型名称
        use_async: 是否使用异步
        
    Returns:
        LLMService实例，如果配置不可用则返回None
    """
    try:
        return LLMService(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            use_async=use_async
        )
    except Exception as e:
        logger.warning(f"--- [LLMService]: Failed to create LLM service: {e}")
        return None


```


## File: ppt_filler.py

```python
"""
PPT内容填充器
根据PPT框架和LLM生成的内容，填充完整的PPT
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import re
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
from loguru import logger

from ppt_parser import PPTParser
from llm_service import LLMService, create_llm_service
from layout_generator import LayoutGenerator
from ant_design_theme import ant_design_theme
from enhanced_ppt_parser import EnhancedPPTParser
from human_centered_analyzer import HumanCenteredAnalyzer
from content_strategy_generator import ContentStrategyGenerator
from content_polisher import ContentPolisher
from presentation_planner import PresentationPlanner
from layout_planner import LayoutPlanner
from html_generator import HTMLGenerator
from browser_to_ppt_replicator import BrowserToPPTReplicator


class PPTFiller:
    """
    PPT内容填充器
    根据框架PPT和用户需求，使用LLM生成内容并填充
    """
    
    def __init__(
        self,
        framework_path: str,
        llm_service: Optional[LLMService] = None,
        use_browser_rendering: bool = False
    ):
        """
        初始化PPT填充器
        
        Args:
            framework_path: 框架PPT文件路径
            llm_service: LLM服务实例
            use_browser_rendering: 是否使用浏览器渲染（Ant Design规范）
        """
        self.parser = PPTParser(framework_path)
        self.framework_path = Path(framework_path)
        self.use_browser_rendering = use_browser_rendering
        
        if llm_service is None:
            self.llm_service = create_llm_service(use_async=True)
            if self.llm_service is None:
                logger.warning("--- [PPTFiller]: LLM service not available")
        else:
            self.llm_service = llm_service
        
        # 如果使用浏览器渲染，初始化相关组件
        if use_browser_rendering:
            self.html_generator = HTMLGenerator()
            self.replicator = BrowserToPPTReplicator()
            logger.info("--- [PPTFiller]: Initialized with browser rendering enabled")
        else:
            self.html_generator = None
            self.replicator = None
            logger.info("--- [PPTFiller]: Initialized")
    
    async def fill_from_prompt(
        self,
        prompt: str,
        output_path: Optional[str] = None,
        preserve_structure: bool = True,
        use_enhanced_analysis: bool = True,
        use_browser_rendering: Optional[bool] = None,
        skip_ppt_conversion: bool = False
    ) -> str:
        """
        根据用户提示填充PPT内容
        
        Args:
            prompt: 用户需求描述
            output_path: 输出文件路径，如果为None则自动生成
            preserve_structure: 是否保持原有结构
            use_enhanced_analysis: 是否使用增强分析（人类中心化分析）
            use_browser_rendering: 是否使用浏览器渲染（如果为None，使用初始化时的设置）
            skip_ppt_conversion: 是否跳过HTML到PPT的转换（仅生成HTML文件）
            
        Returns:
            生成的PPT文件路径（如果skip_ppt_conversion=True，返回HTML目录路径）
        """
        if not self.llm_service:
            raise ValueError("LLM service is required for content generation")
        
        # 确定是否使用浏览器渲染
        if use_browser_rendering is None:
            use_browser_rendering = self.use_browser_rendering
        
        # 如果使用浏览器渲染，使用新的流程
        if use_browser_rendering:
            if not self.html_generator or not self.replicator:
                raise ValueError("Browser rendering components not initialized. Set use_browser_rendering=True in __init__")
            return await self._fill_with_browser_rendering(
                prompt, output_path, use_enhanced_analysis, skip_ppt_conversion
            )
        
        if use_enhanced_analysis:
            # 使用增强分析流程
            logger.info("--- [PPTFiller]: Using enhanced analysis workflow...")
            
            # 1. 提取增强结构
            logger.info("--- [PPTFiller]: Extracting enhanced structure...")
            enhanced_parser = EnhancedPPTParser(str(self.framework_path))
            enhanced_structure = enhanced_parser.extract_structure_enhanced()
            
            # 2. 人类中心化分析
            logger.info("--- [PPTFiller]: Performing human-centered analysis...")
            analyzer = HumanCenteredAnalyzer(enhanced_structure)
            human_analysis = analyzer.analyze_all()
            
            # 3. 生成内容策略
            logger.info("--- [PPTFiller]: Generating content strategy...")
            strategy_gen = ContentStrategyGenerator(human_analysis)
            content_strategy = strategy_gen.generate_strategy()
            
            # 4. 使用策略生成内容
            logger.info("--- [PPTFiller]: Generating content by sections...")
            content_map = await self._generate_content_by_sections(
                human_analysis=human_analysis,
                content_strategy=content_strategy,
                user_prompt=prompt
            )
        else:
            # 使用原有流程（向后兼容）
            logger.info("--- [PPTFiller]: Using legacy workflow...")
            structure = self.parser.extract_structure()
            text_summary = self.parser.extract_text_summary()
            placeholder_mapping = self.parser.get_placeholder_mapping()
            
            content_map = await self._generate_content_for_framework(
                prompt=prompt,
                structure=structure,
                text_summary=text_summary,
                placeholder_mapping=placeholder_mapping
            )
        
        # 填充PPT
        logger.info("--- [PPTFiller]: Filling PPT with generated content...")
        output_path = output_path or self._generate_output_path()
        
        # 传递分析结果和策略（如果使用了增强分析）
        if use_enhanced_analysis:
            self._fill_ppt(content_map, output_path, preserve_structure, human_analysis, content_strategy)
        else:
            self._fill_ppt(content_map, output_path, preserve_structure)
        
        logger.success(f"--- [PPTFiller]: PPT filled and saved to {output_path}")
        return str(output_path)
    
    async def _fill_with_browser_rendering(
        self,
        prompt: str,
        output_path: Optional[str] = None,
        use_enhanced_analysis: bool = True,
        skip_ppt_conversion: bool = False
    ) -> str:
        """
        使用浏览器渲染方式填充PPT（Ant Design规范）
        
        Args:
            prompt: 用户提示
            output_path: 输出路径
            use_enhanced_analysis: 是否使用增强分析
            skip_ppt_conversion: 是否跳过HTML到PPT的转换（仅生成HTML文件）
            
        Returns:
            输出文件路径（如果skip_ppt_conversion=True，返回HTML目录路径）
        """
        logger.info("="*80)
        logger.info("--- [PPTFiller]: 使用浏览器渲染方式（Ant Design规范）")
        logger.info("="*80)
        
        # 1. 提取框架结构
        if use_enhanced_analysis:
            logger.info("--- [PPTFiller]: 提取增强结构...")
            enhanced_parser = EnhancedPPTParser(str(self.framework_path))
            enhanced_structure = enhanced_parser.extract_structure_enhanced()
            
            # 2. 人类中心化分析
            # 如果prompt包含docx内容，使用docx内容进行分析，否则使用框架PPT结构
            logger.info("--- [PPTFiller]: 执行人类中心化分析...")
            
            # 检查prompt是否包含docx内容（通过检查是否包含"【文档内容】"标记）
            if "【文档内容】" in prompt or "文档内容" in prompt:
                # 从prompt中提取docx内容
                import re
                docx_content_match = re.search(r'【文档内容】\s*\n(.*?)(?=\n【|$)', prompt, re.DOTALL)
                if docx_content_match:
                    docx_content = docx_content_match.group(1).strip()
                    logger.info(f"--- [PPTFiller]: 检测到docx内容，长度: {len(docx_content)}字符")
                    logger.info(f"--- [PPTFiller]: 使用docx内容进行人类中心化分析（而不是框架PPT内容）")
                    # 创建基于docx内容的结构数据
                    docx_structure = self._create_structure_from_docx_content(docx_content, enhanced_structure)
                    analyzer = HumanCenteredAnalyzer(docx_structure, raw_text=docx_content, llm_service=self.llm_service)
                else:
                    logger.warning("--- [PPTFiller]: 未找到docx内容，使用框架PPT结构进行分析")
                    analyzer = HumanCenteredAnalyzer(enhanced_structure, llm_service=self.llm_service)
            else:
                logger.info("--- [PPTFiller]: 使用框架PPT结构进行分析")
                analyzer = HumanCenteredAnalyzer(enhanced_structure, llm_service=self.llm_service)
            
            human_analysis = await analyzer.analyze_all()
            
            # 3. 生成内容策略
            logger.info("--- [PPTFiller]: 生成内容策略...")
            strategy_generator = ContentStrategyGenerator(human_analysis)
            content_strategy = strategy_generator.generate_strategy()
            
            # 4. 智能识别支撑材料
            logger.info("--- [PPTFiller]: 智能识别支撑材料...")
            from supporting_materials_analyzer import SupportingMaterialsAnalyzer
            materials_analyzer = SupportingMaterialsAnalyzer(self.llm_service)
            
            supporting_materials = human_analysis.get("layer_4_supporting_materials", {}).get("data", {})
            raw_data_points = supporting_materials.get("materials", {}).get("data_points", [])
            raw_cases = supporting_materials.get("materials", {}).get("cases", [])
            
            # 智能识别数据点和案例
            intelligent_data_points = await materials_analyzer.intelligently_identify_data_points(raw_data_points)
            intelligent_cases = await materials_analyzer.intelligently_identify_cases(raw_cases)
            
            logger.info(f"--- [PPTFiller]: 识别出{len(intelligent_data_points)}个数据点，{len(intelligent_cases)}个案例")
            
            # 5. 逐板块生成内容（整合支撑材料）
            logger.info("--- [PPTFiller]: 逐板块生成内容（整合支撑材料）...")
            generation_result = await self._generate_content_by_sections(
                human_analysis, content_strategy, prompt,
                intelligent_data_points, intelligent_cases
            )
            
            # 【新增】提取内容映射、润色结果、布局规划结果和颜色配置结果
            if isinstance(generation_result, dict):
                content_map = generation_result.get('content_map', {})
                polished_slides = generation_result.get('polished_slides', [])
                presentation_plans = generation_result.get('presentation_plans', [])
                layout_plans = generation_result.get('layout_plans', [])
                color_configs = generation_result.get('color_configs', [])
            else:
                # 向后兼容：如果返回的是旧格式（只有content_map）
                content_map = generation_result
                polished_slides = []
                presentation_plans = []
                layout_plans = []
                color_configs = []
            
            # 【探针】检查内容映射
            logger.info("="*80)
            logger.info("--- [PPTFiller]: 【探针】内容映射总览")
            logger.info("="*80)
            logger.info(f"   总内容映射项数: {len(content_map)}")
            logger.info(f"   润色幻灯片数量: {len(polished_slides)}")
            logger.info(f"   展示策划数量: {len(presentation_plans)}")
            logger.info(f"   布局规划数量: {len(layout_plans)}")
            logger.info(f"   颜色配置数量: {len(color_configs)}")
            slides_in_map = set()
            for key in content_map.keys():
                if 'slide_' in key:
                    try:
                        slide_idx = int(key.split('_')[1])
                        slides_in_map.add(slide_idx)
                    except:
                        pass
            logger.info(f"   涉及幻灯片: {sorted(slides_in_map)}")
            logger.info(f"   内容映射键列表:")
            for key in sorted(content_map.keys()):
                logger.info(f"     - {key}: {len(content_map[key])}字符")
            logger.info("="*80)
        else:
            # 使用简单方式生成内容
            logger.info("--- [PPTFiller]: 使用简单方式生成内容...")
            structure = self.parser.extract_structure()
            text_summary = self.parser.extract_text_summary()
            placeholder_mapping = self.parser.get_placeholder_mapping()
            content_map = await self._generate_content_for_framework(
                prompt=prompt,
                structure=structure,
                text_summary=text_summary,
                placeholder_mapping=placeholder_mapping
            )
        
        # 5. 生成HTML（Ant Design规范）
        # 【新增】优先使用布局规划结果和颜色配置生成HTML，如果没有则使用content_map
        output_path_obj = Path(output_path) if output_path else Path(self._generate_output_path())
        html_output_dir = output_path_obj.parent / "html_output"
        html_output_dir.mkdir(parents=True, exist_ok=True)
        
        if layout_plans and polished_slides:
            logger.info("--- [PPTFiller]: 使用布局规划和颜色配置生成HTML（精确布局+颜色）...")
            
            # 【新增】生成合并的HTML文件
            merged_html = self.html_generator.generate_merged_html(
                layout_plans=layout_plans,
                polished_slides=polished_slides,
                color_configs=color_configs if color_configs else None
            )
            
            # 保存合并的HTML文件
            merged_html_file = html_output_dir / "presentation.html"
            merged_html_file.write_text(merged_html, encoding='utf-8')
            logger.info(f"--- [PPTFiller]: ✅ 保存合并HTML到: {merged_html_file}")
            
            # 同时保存单独的HTML文件（用于调试）
            html_contents = self.html_generator.generate_from_layout_plan(
                layout_plans=layout_plans,
                polished_slides=polished_slides,
                color_configs=color_configs if color_configs else None
            )
            for idx, html_content in enumerate(html_contents):
                html_file = html_output_dir / f"slide_{idx:03d}.html"
                html_file.write_text(html_content, encoding='utf-8')
                logger.info(f"--- [PPTFiller]: ✅ 保存单独HTML到: {html_file}")
        else:
            logger.info("--- [PPTFiller]: 使用内容映射生成HTML（标准方式）...")
            html_contents = self.html_generator.generate_from_content_map(content_map)
            
            # 【修复】支持多张幻灯片：html_contents现在可能是列表
            if not isinstance(html_contents, list):
                html_contents = [html_contents]
            
            for idx, html_content in enumerate(html_contents):
                html_file = html_output_dir / f"slide_{idx:03d}.html"
                html_file.write_text(html_content, encoding='utf-8')
                logger.info(f"--- [PPTFiller]: ✅ 保存HTML到: {html_file}")
        
        logger.info(f"--- [PPTFiller]: 生成了{len(html_contents) if isinstance(html_contents, list) else 1}张HTML幻灯片")
        
        # 【新增】如果跳过PPT转换，直接返回HTML目录路径
        if skip_ppt_conversion:
            logger.info("="*80)
            logger.info("--- [PPTFiller]: ⏭️  跳过HTML到PPT的转换（仅生成HTML）")
            logger.info(f"--- [PPTFiller]: ✅ HTML文件已保存到: {html_output_dir}")
            logger.info(f"--- [PPTFiller]: 共生成 {len(html_contents)} 张HTML幻灯片")
            logger.info("="*80)
            logger.success(f"--- [PPTFiller]: HTML生成完成，保存到 {html_output_dir}")
            return str(html_output_dir)
        
        # 6. 浏览器渲染并复刻到PPT
        logger.info("--- [PPTFiller]: 浏览器渲染并复刻到PPT...")
        output_path = output_path or self._generate_output_path()
        output_path_obj = Path(output_path)
        
        # 【修复】为每张HTML幻灯片创建独立的PPT幻灯片
        from pptx import Presentation
        from pptx.util import Cm
        prs = Presentation()
        prs.slide_width = Cm(33.867)  # 16:9
        prs.slide_height = Cm(19.05)
        
        from browser_to_ppt_replicator.browser_renderer import BrowserRenderer
        from browser_to_ppt_replicator.element_analyzer import ElementAnalyzer
        from browser_to_ppt_replicator.container_extractor import ContainerExtractor
        from browser_to_ppt_replicator.text_extractor import TextExtractor
        from browser_to_ppt_replicator.ppt_replicator import PPTReplicator
        from browser_to_ppt_replicator.coordinate_mapper import CoordinateMapper
        
        coordinate_mapper = CoordinateMapper()
        browser_renderer = BrowserRenderer()
        element_analyzer = ElementAnalyzer()
        
        # ContainerExtractor需要output_dir参数
        containers_dir = output_path_obj.parent / "replicated_outputs" / "containers"
        containers_dir.mkdir(parents=True, exist_ok=True)
        container_extractor = ContainerExtractor(containers_dir)
        
        text_extractor = TextExtractor()
        
        try:
            for slide_idx, html_content in enumerate(html_contents):
                logger.info(f"--- [PPTFiller]: 处理第{slide_idx + 1}/{len(html_contents)}张HTML幻灯片...")
                
                # 渲染HTML
                page = await browser_renderer.render_html(html_content)
                
                try:
                    # 分析元素
                    elements = await element_analyzer.analyze_elements(page)
                    containers_info = elements['containers']
                    texts_info = elements['texts']
                    
                    # 提取容器（截图）
                    containers = await container_extractor.extract_all_containers(containers_info)
                    
                    # 提取文本
                    texts = await text_extractor.extract_all_texts(texts_info)
                    
                    # 创建replicator，使用共享的prs对象（用于多张幻灯片）
                    ppt_replicator = PPTReplicator(coordinate_mapper, None, prs=prs)
                    ppt_replicator.replicate_slide(containers, texts)
                    
                finally:
                    await page.close()
            
            # 保存PPT
            prs.save(str(output_path_obj))
            replicated_path = output_path_obj
            
            logger.info(f"--- [PPTFiller]: 成功生成{len(prs.slides)}张PPT幻灯片")
            
        except Exception as e:
            logger.error(f"--- [PPTFiller]: 浏览器渲染失败: {e}", exc_info=True)
            raise
        finally:
            await browser_renderer.close()
        
        # 7. 整合图表（如果有可可视化数据）
        if intelligent_data_points:
            logger.info("--- [PPTFiller]: 整合图表...")
            from chart_integrator import ChartIntegrator
            chart_integrator = ChartIntegrator(
                materials_analyzer=materials_analyzer
            )
            
            # 打开PPT并插入图表
            from pptx import Presentation
            prs = Presentation(str(replicated_path))
            chart_count = await chart_integrator.integrate_charts(
                prs,
                intelligent_data_points,
                output_dir=replicated_path.parent / "charts"
            )
            prs.save(str(replicated_path))
            
            if chart_count > 0:
                logger.info(f"--- [PPTFiller]: 成功整合{chart_count}个图表")
        
        logger.success(f"--- [PPTFiller]: PPT filled and saved to {replicated_path}")
        return str(replicated_path)
    
    async def _generate_content_for_framework(
        self,
        prompt: str,
        structure: Dict[str, Any],
        text_summary: str,
        placeholder_mapping: Dict[int, List[Dict[str, Any]]]
    ) -> Dict[str, str]:
        """
        为框架生成内容映射
        
        Args:
            prompt: 用户需求
            structure: PPT结构信息
            text_summary: 文本摘要
            placeholder_mapping: 占位符映射
            
        Returns:
            内容映射字典，键是占位符标识，值是生成的内容
        """
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
        
        user_prompt = f"""PPT框架信息：
{text_summary}

用户需求：{prompt}

请为每张幻灯片的占位符生成合适的内容。如果占位符已有内容，可以基于现有内容进行扩展或优化。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=messages,
                temperature=0.7,
                max_tokens=4000
            )
            
            # 解析JSON响应
            import json
            import re
            
            # 尝试提取JSON
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                content_map = json.loads(json_match.group(0))
            else:
                # 如果无法解析，尝试手动构建
                logger.warning("--- [PPTFiller]: Failed to parse JSON, using fallback")
                content_map = self._fallback_content_generation(placeholder_mapping, prompt)
            
            return content_map
            
        except Exception as e:
            logger.error(f"--- [PPTFiller]: Failed to generate content: {e}", exc_info=True)
            # 使用fallback
            return self._fallback_content_generation(placeholder_mapping, prompt)
    
    def _fallback_content_generation(
        self,
        placeholder_mapping: Dict[int, List[Dict[str, Any]]],
        prompt: str
    ) -> Dict[str, str]:
        """
        Fallback内容生成（如果LLM失败）
        
        Args:
            placeholder_mapping: 占位符映射
            prompt: 用户需求
            
        Returns:
            内容映射字典
        """
        content_map = {}
        for slide_idx, placeholders in placeholder_mapping.items():
            for placeholder in placeholders:
                key = f"slide_{slide_idx}_placeholder_{placeholder['placeholder_id']}"
                if placeholder.get("has_text"):
                    # 如果有现有文本，保留
                    content_map[key] = placeholder["text"]
                else:
                    # 生成占位文本
                    content_map[key] = f"[需要填充: {prompt[:50]}...]"
        
        return content_map
    
    def _fill_ppt(
        self,
        content_map: Dict[str, str],
        output_path: str,
        preserve_structure: bool = True,
        human_analysis: Optional[Dict[str, Any]] = None,
        content_strategy: Optional[Dict[str, Any]] = None
    ):
        """
        填充PPT内容
        
        Args:
            content_map: 内容映射字典
            output_path: 输出路径
            preserve_structure: 是否保持结构
        """
        logger.info("="*80)
        logger.info("--- [PPTFiller]: 开始填充PPT流程")
        logger.info("="*80)
        
        # 复制框架PPT
        from shutil import copy
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)
        copy(self.framework_path, output_path)
        logger.info(f"--- [PPTFiller]: 已复制框架PPT到: {output_path}")
        
        # 打开复制的PPT
        prs = Presentation(str(output_path))
        
        # 【日志探针1】检查原始PPT尺寸
        original_width_emu = prs.slide_width
        original_height_emu = prs.slide_height
        original_width_cm = float(original_width_emu) / 360000
        original_height_cm = float(original_height_emu) / 360000
        original_ratio = original_width_cm / original_height_cm
        logger.info(f"--- [PPTFiller]: 【尺寸检查】原始PPT尺寸:")
        logger.info(f"   宽度: {original_width_cm:.2f}cm ({original_width_emu} EMU)")
        logger.info(f"   高度: {original_height_cm:.2f}cm ({original_height_emu} EMU)")
        logger.info(f"   宽高比: {original_ratio:.2f}")
        logger.info(f"   16:9 = {16/9:.2f}, 4:3 = {4/3:.2f}")
        logger.info(f"   是否为16:9: {abs(original_ratio - 16/9) < 0.1}")
        logger.info(f"   是否为4:3: {abs(original_ratio - 4/3) < 0.1}")
        
        # 【修复1】强制设置为16:9
        target_width_cm = 33.867  # 16:9宽度
        target_height_cm = 19.05  # 16:9高度
        if abs(original_ratio - 16/9) > 0.1:
            logger.warning(f"--- [PPTFiller]: 【尺寸修复】检测到非16:9比例，正在转换为16:9...")
            prs.slide_width = Cm(target_width_cm)
            prs.slide_height = Cm(target_height_cm)
            new_ratio = target_width_cm / target_height_cm
            logger.info(f"--- [PPTFiller]: 【尺寸修复】已设置为16:9:")
            logger.info(f"   新宽度: {target_width_cm:.2f}cm")
            logger.info(f"   新高度: {target_height_cm:.2f}cm")
            logger.info(f"   新宽高比: {new_ratio:.2f} (目标: {16/9:.2f})")
        else:
            logger.info(f"--- [PPTFiller]: 【尺寸检查】PPT已经是16:9，无需修改")
        
        # 【日志探针2】检查设计规范应用
        logger.info(f"--- [PPTFiller]: 【设计规范】开始应用Ant Design设计规范...")
        logger.info(f"   主色: {ant_design_theme.colors.colorPrimary}")
        logger.info(f"   文本色: {ant_design_theme.colors.colorText}")
        logger.info(f"   字体族: {ant_design_theme.typography.fontFamily}")
        logger.info(f"   标题字号: {ant_design_theme.get_font_size_pt('h1')}pt")
        logger.info(f"   正文字号: {ant_design_theme.get_font_size_pt('base')}pt")
        
        # 构建样式策略（如果提供了分析结果）
        style_strategy = None
        if human_analysis and content_strategy:
            logger.info("--- [PPTFiller]: 【样式策略】构建智能样式策略...")
            style_strategy = self._build_style_strategy(human_analysis, content_strategy)
            logger.info(f"--- [PPTFiller]: 【样式策略】正式程度: {style_strategy.get('formality', '')}, 语调: {style_strategy.get('tone', '')}")
        
        # 填充每张幻灯片
        logger.info(f"--- [PPTFiller]: 【内容填充】开始填充 {len(prs.slides)} 张幻灯片...")
        for slide_idx, slide in enumerate(prs.slides):
            logger.info(f"--- [PPTFiller]: 【内容填充】处理幻灯片 {slide_idx + 1}/{len(prs.slides)}")
            placeholder_count = 0
            filled_count = 0
            
            for shape in slide.shapes:
                if shape.is_placeholder:
                    placeholder_id = shape.placeholder_format.idx
                    key = f"slide_{slide_idx}_placeholder_{placeholder_id}"
                    placeholder_count += 1
                    
                    logger.debug(f"--- [PPTFiller]: 【占位符】幻灯片{slide_idx}, 占位符{placeholder_id}, key={key}")
                    
                    if key in content_map and hasattr(shape, "text_frame"):
                        try:
                            # 【日志探针3】记录填充前状态
                            old_text = shape.text_frame.text[:50] if shape.text_frame.text else "(空)"
                            logger.debug(f"--- [PPTFiller]: 【填充前】占位符{placeholder_id}内容: {old_text}...")
                            
                            # 清除现有内容
                            shape.text_frame.clear()
                            
                            # 添加新内容
                            content = content_map[key]
                            logger.debug(f"--- [PPTFiller]: 【内容】占位符{placeholder_id}新内容长度: {len(content)}字符")
                            
                            if content:
                                # 处理多段落
                                paragraphs = content.split('\n')
                                logger.debug(f"--- [PPTFiller]: 【段落】占位符{placeholder_id}包含{len(paragraphs)}个段落")
                                
                                for i, para_text in enumerate(paragraphs):
                                    if i == 0:
                                        p = shape.text_frame.paragraphs[0]
                                        p.text = para_text
                                    else:
                                        p = shape.text_frame.add_paragraph()
                                        p.text = para_text
                                
                                # 【改进】应用智能样式（如果提供了分析结果）
                                # 注意：对整个shape应用一次，而不是对每个段落
                                if style_strategy:
                                    self._apply_smart_style(
                                        shape, placeholder_id, slide_idx,
                                        style_strategy, human_analysis, content_strategy
                                    )
                                else:
                                    # 使用原有方法（向后兼容）
                                    for para in shape.text_frame.paragraphs:
                                        self._apply_ant_design_style(para, placeholder_id, slide_idx)
                                
                                filled_count += 1
                                logger.info(f"--- [PPTFiller]: 【填充成功】幻灯片{slide_idx}, 占位符{placeholder_id}")
                            else:
                                logger.warning(f"--- [PPTFiller]: 【内容为空】占位符{placeholder_id}没有内容")
                        except Exception as e:
                            logger.error(f"--- [PPTFiller]: 【填充失败】占位符{placeholder_id}: {e}", exc_info=True)
                    else:
                        if key not in content_map:
                            logger.warning(f"--- [PPTFiller]: 【缺少内容】占位符{placeholder_id}在content_map中不存在 (key={key})")
                        if not hasattr(shape, "text_frame"):
                            logger.warning(f"--- [PPTFiller]: 【无文本框架】占位符{placeholder_id}没有text_frame属性")
            
            logger.info(f"--- [PPTFiller]: 【幻灯片完成】幻灯片{slide_idx}: {filled_count}/{placeholder_count}个占位符已填充")
        
        logger.info(f"--- [PPTFiller]: 【内容填充】所有幻灯片处理完成")
        
        # 【日志探针4】最终尺寸检查
        final_width_emu = prs.slide_width
        final_height_emu = prs.slide_height
        final_width_cm = float(final_width_emu) / 360000
        final_height_cm = float(final_height_emu) / 360000
        final_ratio = final_width_cm / final_height_cm
        logger.info(f"--- [PPTFiller]: 【最终检查】保存前PPT尺寸:")
        logger.info(f"   宽度: {final_width_cm:.2f}cm ({final_width_emu} EMU)")
        logger.info(f"   高度: {final_height_cm:.2f}cm ({final_height_emu} EMU)")
        logger.info(f"   宽高比: {final_ratio:.2f} (目标16:9={16/9:.2f})")
        logger.info(f"   是否为16:9: {abs(final_ratio - 16/9) < 0.1}")
        
        # 保存
        prs.save(str(output_path))
        logger.info(f"--- [PPTFiller]: 【保存完成】PPT已保存到: {output_path}")
        
        # 【日志探针5】验证保存后的文件
        saved_size = Path(output_path).stat().st_size
        logger.info(f"--- [PPTFiller]: 【文件验证】保存后文件大小: {saved_size:,} bytes ({saved_size/1024:.2f} KB)")
        logger.info("="*80)
        logger.info("--- [PPTFiller]: 填充PPT流程完成")
        logger.info("="*80)
    
    def _build_style_strategy(
        self,
        human_analysis: Dict[str, Any],
        content_strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        构建样式策略（充分利用所有6层分析结果）
        
        Args:
            human_analysis: 人类中心化分析结果
            content_strategy: 内容生成策略
            
        Returns:
            样式策略字典
        """
        # 【改进1】使用所有6层分析结果
        expression_style = human_analysis.get("layer_5_expression_style", {}).get("data", {})
        sections = human_analysis.get("layer_2_sections", {}).get("data", {})
        arguments = human_analysis.get("layer_3_arguments", {}).get("data", {})
        supporting_materials = human_analysis.get("layer_4_supporting_materials", {}).get("data", {})
        presentation_form = human_analysis.get("layer_6_presentation_form", {}).get("data", {})
        visual_style = content_strategy.get("expression_strategy", {}).get("visual_style", {})
        
        formality = expression_style.get("formality_level", "中性")
        tone = expression_style.get("tone", "中性")
        cultural_features = expression_style.get("cultural_features", [])
        
        # 【改进1.1】使用板块结构信息
        section_count = len(sections.get("sections", []))
        has_multiple_sections = section_count > 1
        
        # 【改进1.2】使用支撑材料信息
        has_data_points = len(supporting_materials.get("data_points", [])) > 0
        has_charts = len(supporting_materials.get("charts", [])) > 0
        has_case_studies = len(supporting_materials.get("case_studies", [])) > 0
        
        # 【改进1.3】使用呈现形式信息
        visual_hierarchy = presentation_form.get("visual_hierarchy", {})
        layout_style = presentation_form.get("layout_style", "standard")
        
        # 根据正式程度调整字号
        if formality == "正式":
            title_font_size = 40  # 更大，更正式
            body_font_size = 15
            subtitle_font_size = 24
        elif formality == "非正式":
            title_font_size = 36  # 稍小，更轻松
            body_font_size = 14
            subtitle_font_size = 22
        else:
            title_font_size = 38  # 标准
            body_font_size = 14
            subtitle_font_size = 24
        
        # 根据语调调整颜色
        if tone == "积极":
            primary_color = "#1890ff"  # Ant Design蓝色（积极）
            accent_color = "#52c41a"   # 绿色（成功）
            text_color = "#262626"     # 黑色
        elif tone == "谨慎":
            primary_color = "#fa8c16"  # 橙色（警告）
            accent_color = "#ff4d4f"    # 红色（错误）
            text_color = "#595959"     # 深灰色（更柔和）
        else:
            primary_color = "#1890ff"  # 标准蓝色
            accent_color = "#1890ff"
            text_color = "#262626"     # 标准黑色
        
        return {
            "typography": {
                "title_font_size": title_font_size,
                "subtitle_font_size": subtitle_font_size,
                "body_font_size": body_font_size,
                "font_family": visual_style.get("typography", {}).get("font_family", "Segoe UI")
            },
            "colors": {
                "primary": primary_color,
                "accent": accent_color,
                "text": text_color
            },
            "cultural_features": cultural_features,
            "formality": formality,
            "tone": tone,
            # 【改进1】新增：使用所有6层分析结果
            "sections": {
                "count": section_count,
                "has_multiple": has_multiple_sections
            },
            "supporting_materials": {
                "has_data_points": has_data_points,
                "has_charts": has_charts,
                "has_case_studies": has_case_studies
            },
            "presentation_form": {
                "visual_hierarchy": visual_hierarchy,
                "layout_style": layout_style
            }
        }
    
    def _determine_content_type(
        self,
        shape,
        placeholder_id: int,
        human_analysis: Optional[Dict[str, Any]]
    ) -> str:
        """
        确定内容类型
        
        Args:
            shape: PPT形状对象
            placeholder_id: 占位符ID
            human_analysis: 人类中心化分析结果
            
        Returns:
            内容类型字符串
        """
        import re
        
        # 获取占位符类型
        placeholder_type = ""
        if shape.is_placeholder:
            try:
                placeholder_type = str(shape.placeholder_format.type)
            except:
                pass
        
        # 获取文本内容
        text = ""
        if hasattr(shape, "text_frame"):
            text = shape.text_frame.text
        
        # 根据占位符类型判断
        if "CENTER_TITLE" in placeholder_type or "TITLE" in placeholder_type:
            return "title"
        elif "SUBTITLE" in placeholder_type:
            return "subtitle"
        elif "OBJECT" in placeholder_type or "BODY" in placeholder_type:
            # 检查内容是否包含数据或案例
            if "数据支撑" in text or re.search(r'\d+[%％]', text):
                return "data_highlight"
            elif "案例说明" in text or "案例" in text:
                return "case_study"
            elif "关键要点" in text or text.strip().startswith("•"):
                return "key_points"
            else:
                return "body"
        else:
            return "body"
    
    def _apply_smart_style(
        self,
        shape,
        placeholder_id: int,
        slide_idx: int,
        style_strategy: Dict[str, Any],
        human_analysis: Optional[Dict[str, Any]],
        content_strategy: Optional[Dict[str, Any]]
    ):
        """
        应用智能样式
        
        Args:
            shape: PPT形状对象
            placeholder_id: 占位符ID
            slide_idx: 幻灯片索引
            style_strategy: 样式策略
            human_analysis: 人类中心化分析结果
            content_strategy: 内容生成策略
        """
        # 1. 确定内容类型
        content_type = self._determine_content_type(shape, placeholder_id, human_analysis)
        logger.debug(f"--- [PPTFiller]: 【内容类型】占位符{placeholder_id}识别为: {content_type}")
        
        # 2. 根据内容类型应用样式
        if content_type == "title":
            self._apply_title_style(shape, style_strategy)
        elif content_type == "subtitle":
            self._apply_subtitle_style(shape, style_strategy)
        elif content_type == "data_highlight":
            self._apply_data_highlight_style(shape, style_strategy)
        elif content_type == "case_study":
            self._apply_case_study_style(shape, style_strategy)
        elif content_type == "key_points":
            self._apply_key_points_style(shape, style_strategy)
        else:
            self._apply_body_style(shape, style_strategy)
        
        # 3. 应用文化特征
        if "强调价值导向" in style_strategy.get("cultural_features", []):
            self._emphasize_value_propositions(shape, style_strategy)
        
        if "数据驱动表达" in style_strategy.get("cultural_features", []):
            self._emphasize_data_points(shape, style_strategy)
        
        # 【改进1】使用支撑材料信息突出数据
        supporting_materials = style_strategy.get("supporting_materials", {})
        if supporting_materials.get("has_data_points", False):
            self._emphasize_data_points(shape, style_strategy)
        
        # 【改进2】应用Ant Design间距系统
        self._apply_ant_design_spacing(shape, content_type)
        
        # 【改进2】应用Ant Design布局原则（增强视觉效果）
        self._apply_ant_design_layout(shape, content_type, style_strategy)
        
        # 【改进2.4】调整占位符位置（添加整体布局改进）
        self._adjust_placeholder_position(shape, content_type, slide_idx)
    
    def _hex_to_rgb(self, hex_color: str) -> RGBColor:
        """将hex颜色转换为RGBColor"""
        if hex_color.startswith('#'):
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            return RGBColor(r, g, b)
        return RGBColor(38, 38, 38)  # 默认黑色
    
    def _apply_title_style(self, shape, style_strategy: Dict[str, Any]):
        """应用标题样式"""
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                font = run.font
                font.name = style_strategy["typography"]["font_family"]
                font.size = Pt(style_strategy["typography"]["title_font_size"])
                font.bold = True
                font.color.rgb = self._hex_to_rgb(style_strategy["colors"]["primary"])
    
    def _apply_subtitle_style(self, shape, style_strategy: Dict[str, Any]):
        """应用副标题样式"""
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                font = run.font
                font.name = style_strategy["typography"]["font_family"]
                font.size = Pt(style_strategy["typography"]["subtitle_font_size"])
                font.bold = True
                font.color.rgb = self._hex_to_rgb(style_strategy["colors"]["text"])
    
    def _apply_body_style(self, shape, style_strategy: Dict[str, Any]):
        """应用正文样式"""
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                font = run.font
                font.name = style_strategy["typography"]["font_family"]
                font.size = Pt(style_strategy["typography"]["body_font_size"])
                font.bold = False
                font.color.rgb = self._hex_to_rgb(style_strategy["colors"]["text"])
    
    def _apply_data_highlight_style(self, shape, style_strategy: Dict[str, Any]):
        """应用数据高亮样式"""
        import re
        
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                text = run.text
                font = run.font
                font.name = style_strategy["typography"]["font_family"]
                
                # 如果是数据（包含数字和%），使用强调色
                if re.search(r'\d+[%％]|\d+\.\d+%', text):
                    font.size = Pt(style_strategy["typography"]["body_font_size"] + 2)  # 稍大
                    font.bold = True
                    font.color.rgb = self._hex_to_rgb(style_strategy["colors"]["accent"])
                else:
                    # 普通文本
                    font.size = Pt(style_strategy["typography"]["body_font_size"])
                    font.bold = False
                    font.color.rgb = self._hex_to_rgb(style_strategy["colors"]["text"])
    
    def _apply_case_study_style(self, shape, style_strategy: Dict[str, Any]):
        """应用案例样式"""
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                font = run.font
                font.name = style_strategy["typography"]["font_family"]
                font.size = Pt(style_strategy["typography"]["body_font_size"])
                font.italic = True  # 案例使用斜体
                font.color.rgb = self._hex_to_rgb(style_strategy["colors"]["text"])
    
    def _apply_key_points_style(self, shape, style_strategy: Dict[str, Any]):
        """应用关键要点样式"""
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                font = run.font
                font.name = style_strategy["typography"]["font_family"]
                font.size = Pt(style_strategy["typography"]["body_font_size"])
                font.bold = True  # 要点加粗
                font.color.rgb = self._hex_to_rgb(style_strategy["colors"]["text"])
    
    def _emphasize_value_propositions(self, shape, style_strategy: Dict[str, Any]):
        """突出价值主张"""
        import re
        
        value_keywords = ["降低", "提升", "加速", "优化", "改善", "增长", "提高"]
        
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                if any(kw in run.text for kw in value_keywords):
                    # 价值主张使用强调色和加粗
                    run.font.bold = True
                    run.font.color.rgb = self._hex_to_rgb(style_strategy["colors"]["accent"])
    
    def _emphasize_data_points(self, shape, style_strategy: Dict[str, Any]):
        """突出数据点"""
        import re
        
        for para in shape.text_frame.paragraphs:
            for run in para.runs:
                text = run.text
                
                # 如果是数据，使用强调样式
                if re.search(r'\d+[%％]|\d+\.\d+%', text):
                    run.font.bold = True
                    run.font.size = Pt(style_strategy["typography"]["body_font_size"] + 2)
                    run.font.color.rgb = self._hex_to_rgb(style_strategy["colors"]["accent"])
    
    def _apply_ant_design_spacing(self, shape, content_type: str):
        """应用Ant Design间距系统"""
        from ant_design_theme import ant_design_theme
        from pptx.util import Pt
        
        try:
            # 获取Ant Design间距（转换为pt）
            spacing_sm_pt = ant_design_theme.get_spacing_cm('sm') * 28.35  # cm转pt (1cm ≈ 28.35pt)
            spacing_md_pt = ant_design_theme.get_spacing_cm('md') * 28.35
            spacing_lg_pt = ant_design_theme.get_spacing_cm('lg') * 28.35
            
            # 应用段落间距
            for i, para in enumerate(shape.text_frame.paragraphs):
                # 检查是否有paragraph_format属性
                if not hasattr(para, 'paragraph_format'):
                    continue
                
                try:
                    # 段落后间距（根据内容类型调整）
                    if content_type == "title":
                        para.paragraph_format.space_after = Pt(0)  # 标题后无间距
                    elif content_type == "subtitle":
                        para.paragraph_format.space_after = Pt(spacing_sm_pt)  # 副标题后小间距
                    elif content_type in ["data_highlight", "case_study", "key_points"]:
                        para.paragraph_format.space_after = Pt(spacing_md_pt)  # 重要内容后中等间距
                    else:
                        para.paragraph_format.space_after = Pt(spacing_sm_pt)  # 正文后小间距
                    
                    # 段落前间距（第一个段落除外）
                    if i > 0:
                        if content_type == "title":
                            para.paragraph_format.space_before = Pt(spacing_lg_pt)  # 标题前大间距
                        else:
                            para.paragraph_format.space_before = Pt(0)  # 其他内容前无间距
                except Exception as e:
                    logger.debug(f"--- [PPTFiller]: 【间距】应用段落间距失败: {e}")
            
            logger.debug(f"--- [PPTFiller]: 【间距】已应用Ant Design间距系统到{content_type}")
        except Exception as e:
            logger.warning(f"--- [PPTFiller]: 【间距】应用Ant Design间距系统失败: {e}")
    
    def _apply_ant_design_layout(self, shape, content_type: str, style_strategy: Dict[str, Any]):
        """应用Ant Design布局原则（增强视觉效果）"""
        from ant_design_theme import ant_design_theme
        from pptx.util import Cm
        from pptx.enum.text import PP_ALIGN
        from pptx.enum.shapes import MSO_SHAPE
        
        # 【改进2.1】应用文本对齐（根据内容类型）
        try:
            if content_type == "title":
                for para in shape.text_frame.paragraphs:
                    para.alignment = PP_ALIGN.CENTER  # 标题居中
            elif content_type in ["data_highlight", "case_study", "key_points"]:
                for para in shape.text_frame.paragraphs:
                    para.alignment = PP_ALIGN.LEFT  # 数据和案例左对齐
            else:
                for para in shape.text_frame.paragraphs:
                    para.alignment = PP_ALIGN.LEFT  # 正文左对齐
        except Exception as e:
            logger.debug(f"--- [PPTFiller]: 【布局】应用对齐失败: {e}")
        
        # 【改进2.2】应用文本框架内边距（增强视觉效果）
        try:
            # 根据内容类型使用不同的内边距
            if content_type == "title":
                padding_cm = ant_design_theme.get_spacing_cm('lg')  # 24px = 更大间距
            elif content_type in ["data_highlight", "case_study", "key_points"]:
                padding_cm = ant_design_theme.get_spacing_cm('md')  # 16px = 中等间距
            else:
                padding_cm = ant_design_theme.get_spacing_cm('sm')  # 12px = 小间距
            
            # 应用内边距（通过调整文本框架的边距）
            text_frame = shape.text_frame
            text_frame.margin_left = Cm(padding_cm)
            text_frame.margin_right = Cm(padding_cm)
            text_frame.margin_top = Cm(padding_cm * 0.75)  # 上下间距稍大
            text_frame.margin_bottom = Cm(padding_cm * 0.75)
            
            logger.debug(f"--- [PPTFiller]: 【布局】已应用内边距: {padding_cm:.2f}cm ({content_type})")
        except Exception as e:
            logger.warning(f"--- [PPTFiller]: 【布局】应用内边距失败: {e}")
        
        # 【改进2.3】为所有内容类型添加背景色和边框（增强视觉效果）
        try:
            fill = shape.fill
            
            # 根据内容类型使用不同的背景色
            if content_type == "title":
                # 标题：使用主色背景（更明显）
                fill.solid()
                fill.fore_color.rgb = RGBColor(24, 144, 255)  # #1890ff 主色
                # 标题文字改为白色（在蓝色背景上）
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        run.font.color.rgb = RGBColor(255, 255, 255)  # 白色
            elif content_type in ["data_highlight", "case_study"]:
                # 数据和案例：使用浅灰背景
                fill.solid()
                fill.fore_color.rgb = RGBColor(240, 242, 245)  # #f0f2f5 浅灰
            elif content_type == "key_points":
                # 关键要点：使用极浅灰背景
                fill.solid()
                fill.fore_color.rgb = RGBColor(250, 250, 250)  # #fafafa 极浅灰
            else:
                # 正文：使用白色背景（保持原样）
                fill.solid()
                fill.fore_color.rgb = RGBColor(255, 255, 255)  # #ffffff 白色
            
            # 添加边框（除了标题）
            if content_type != "title":
                try:
                    line = shape.line
                    line.color.rgb = RGBColor(217, 217, 217)  # #d9d9d9 边框色
                    line.width = Pt(1)  # 1pt边框
                except Exception as e:
                    logger.debug(f"--- [PPTFiller]: 【布局】应用边框失败: {e}")
            
            logger.debug(f"--- [PPTFiller]: 【布局】已应用背景色和边框到{content_type}")
        except Exception as e:
            logger.warning(f"--- [PPTFiller]: 【布局】应用背景色失败: {e}")
        
        logger.debug(f"--- [PPTFiller]: 【布局】已应用Ant Design布局原则到{content_type}")
    
    def _adjust_placeholder_position(self, shape, content_type: str, slide_idx: int):
        """调整占位符位置（添加整体布局改进）"""
        from ant_design_theme import ant_design_theme
        from pptx.util import Cm
        
        try:
            # 获取Ant Design间距
            slide_padding_cm = ant_design_theme.get_spacing_cm('lg')  # 24px = 0.63cm
            
            # 调整占位符位置（添加幻灯片内边距）
            # 注意：这会影响所有占位符，所以需要谨慎
            # 我们只调整位置，不改变尺寸（保持原有布局）
            
            # 如果占位符太靠近边缘，向内移动
            current_left_cm = float(shape.left) / 360000
            current_top_cm = float(shape.top) / 360000
            
            # 如果左边距小于内边距，调整位置
            if current_left_cm < slide_padding_cm:
                shape.left = Cm(slide_padding_cm)
                logger.debug(f"--- [PPTFiller]: 【布局】调整占位符左边距: {current_left_cm:.2f}cm -> {slide_padding_cm:.2f}cm")
            
            # 如果上边距小于内边距，调整位置
            if current_top_cm < slide_padding_cm:
                shape.top = Cm(slide_padding_cm)
                logger.debug(f"--- [PPTFiller]: 【布局】调整占位符上边距: {current_top_cm:.2f}cm -> {slide_padding_cm:.2f}cm")
            
        except Exception as e:
            logger.debug(f"--- [PPTFiller]: 【布局】调整占位符位置失败: {e}")
    
    def _apply_ant_design_style(self, paragraph, placeholder_id: int, slide_idx: int):
        """
        应用Ant Design设计规范到段落
        
        Args:
            paragraph: PPT段落对象
            placeholder_id: 占位符ID
            slide_idx: 幻灯片索引
        """
        try:
            if not paragraph.runs:
                run = paragraph.add_run()
            else:
                run = paragraph.runs[0]
            
            font = run.font
            
            # 【修复3】应用Ant Design字体系统
            logger.debug(f"--- [PPTFiller]: 【字体应用】幻灯片{slide_idx}, 占位符{placeholder_id}")
            try:
                font.name = "Segoe UI"  # Windows系统字体
                logger.debug(f"--- [PPTFiller]: 【字体】设置为: Segoe UI")
            except Exception:
                try:
                    font.name = "Helvetica Neue"  # macOS系统字体
                    logger.debug(f"--- [PPTFiller]: 【字体】设置为: Helvetica Neue")
                except Exception:
                    try:
                        font.name = "微软雅黑"  # 中文字体fallback
                        logger.debug(f"--- [PPTFiller]: 【字体】设置为: 微软雅黑")
                    except Exception:
                        font.name = "Arial"  # 最终fallback
                        logger.debug(f"--- [PPTFiller]: 【字体】设置为: Arial (fallback)")
            
            # 【修复4】应用Ant Design字号系统
            # 根据占位符类型判断（通常placeholder_id=0是标题，1是内容）
            if placeholder_id == 0:
                # 标题
                font.size = Pt(ant_design_theme.get_font_size_pt('h1'))
                font.bold = True
                logger.debug(f"--- [PPTFiller]: 【字号】占位符{placeholder_id}设置为标题: {ant_design_theme.get_font_size_pt('h1')}pt, 加粗")
            else:
                # 正文
                font.size = Pt(ant_design_theme.get_font_size_pt('base'))
                font.bold = False
                logger.debug(f"--- [PPTFiller]: 【字号】占位符{placeholder_id}设置为正文: {ant_design_theme.get_font_size_pt('base')}pt")
            
            # 【修复5】应用Ant Design颜色系统
            try:
                # 解析颜色（从hex转换为RGB）
                text_color_hex = ant_design_theme.colors.colorText
                if text_color_hex.startswith('#'):
                    r = int(text_color_hex[1:3], 16)
                    g = int(text_color_hex[3:5], 16)
                    b = int(text_color_hex[5:7], 16)
                    font.color.rgb = RGBColor(r, g, b)
                    logger.debug(f"--- [PPTFiller]: 【颜色】设置为: {text_color_hex} (RGB: {r}, {g}, {b})")
            except Exception as e:
                logger.warning(f"--- [PPTFiller]: 【颜色应用失败】占位符{placeholder_id}: {e}")
            
        except Exception as e:
            logger.error(f"--- [PPTFiller]: 【样式应用失败】占位符{placeholder_id}: {e}", exc_info=True)
    
    async def _generate_content_by_sections(
        self,
        human_analysis: Dict[str, Any],
        content_strategy: Dict[str, Any],
        user_prompt: str,
        intelligent_data_points: Optional[List[Dict[str, Any]]] = None,
        intelligent_cases: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, str]:
        """
        逐板块生成内容（改进方案）
        
        Args:
            human_analysis: 人类中心化分析结果
            content_strategy: 内容生成策略
            user_prompt: 用户需求
            
        Returns:
            内容映射字典
        """
        content_map = {}
        section_strategies = content_strategy.get("section_strategies", [])
        
        logger.info(f"--- [PPTFiller]: Generating content for {len(section_strategies)} sections...")
        
        # 初始化润色器、展示策划器、布局规划器和颜色配置器
        content_polisher = ContentPolisher(self.llm_service)
        presentation_planner = PresentationPlanner(self.llm_service)
        layout_planner = LayoutPlanner(self.llm_service)
        from color_configurator import ColorConfigurator
        color_configurator = ColorConfigurator(self.llm_service)
        
        # 【新增】收集所有板块的润色结果、布局规划结果和颜色配置结果
        all_polished_slides = []
        all_presentation_plans = []
        all_layout_plans = []
        all_color_configs = []
        
        for idx, section_strategy in enumerate(section_strategies):
            logger.info(f"--- [PPTFiller]: Processing section {idx + 1}/{len(section_strategies)}: {section_strategy.get('theme', '')}")
            
            # 获取该板块相关的支撑材料
            section_slides = section_strategy.get("slides", [])
            section_data_points = []
            section_cases = []
            
            if intelligent_data_points:
                section_data_points = [
                    dp for dp in intelligent_data_points 
                    if dp.get("slide_index", -1) in section_slides
                ]
            
            if intelligent_cases:
                section_cases = [
                    c for c in intelligent_cases 
                    if c.get("slide_index", -1) in section_slides
                ]
            
            logger.info(f"--- [PPTFiller]: Section {idx + 1} 相关支撑材料: {len(section_data_points)}个数据点, {len(section_cases)}个案例")
            
            # 【新增】步骤0: 获取板块分析结果（用于润色）
            section_analysis = self._get_section_analysis(idx, human_analysis, section_strategy)
            
            # 【新增】步骤1: 内容润色 - 将文档内容润色成适合PPT展示的文案
            logger.info(f"--- [PPTFiller]: 【步骤1】内容润色 - 板块{idx + 1}...")
            polished_slides = await content_polisher.polish_section(
                section_analysis=section_analysis,
                section_index=idx
            )
            logger.info(f"--- [PPTFiller]: ✅ 润色完成，生成{len(polished_slides)}张幻灯片")
            
            # 【新增】步骤2: 展示策划 - 设计简洁明了的展示方式
            logger.info(f"--- [PPTFiller]: 【步骤2】展示策划 - 板块{idx + 1}...")
            presentation_plan = await presentation_planner.plan_presentation(
                polished_slides=polished_slides,
                section_theme=section_strategy.get('theme', '')
            )
            logger.info(f"--- [PPTFiller]: ✅ 展示策划完成，策划了{len(presentation_plan)}张幻灯片")
            
            # 【新增】步骤3: 布局规划 - 基于设计规范生成详细的布局说明
            logger.info(f"--- [PPTFiller]: 【步骤3】布局规划 - 板块{idx + 1}...")
            layout_plans = await layout_planner.plan_layout(
                polished_slides=polished_slides,
                presentation_plan=presentation_plan
            )
            logger.info(f"--- [PPTFiller]: ✅ 布局规划完成，规划了{len(layout_plans)}张幻灯片")
            
            # 【新增】步骤4: 颜色配置 - 为每个元素配置符合Ant Design规范的颜色方案
            logger.info(f"--- [PPTFiller]: 【步骤4】颜色配置 - 板块{idx + 1}...")
            color_configs = await color_configurator.configure_colors(
                polished_slides=polished_slides,
                presentation_plans=presentation_plan,
                layout_plans=layout_plans
            )
            logger.info(f"--- [PPTFiller]: ✅ 颜色配置完成，配置了{len(color_configs)}张幻灯片")
            
            # 【新增】收集润色结果、展示策划结果、布局规划结果和颜色配置结果
            # 【探针】记录板块内的slide_index分布
            logger.info(f"--- [PPTFiller]: 【探针】板块{idx + 1}的slide_index分布:")
            logger.info(f"--- [PPTFiller]:   polished_slides: {[s.get('slide_index', 0) for s in polished_slides]}")
            logger.info(f"--- [PPTFiller]:   layout_plans: {[l.get('slide_index', 0) for l in layout_plans]}")
            
            # 在合并前，调整slide_index为全局索引
            # 计算全局起始索引
            global_start_index = sum(len(all_polished_slides) for _ in range(idx)) if idx > 0 else 0
            global_start_index = len(all_polished_slides)  # 使用实际已收集的数量
            
            logger.info(f"--- [PPTFiller]: 【探针】板块{idx + 1}的全局起始索引: {global_start_index}")
            
            # 调整polished_slides的slide_index
            adjusted_polished_slides = []
            for slide in polished_slides:
                adjusted_slide = slide.copy()
                old_index = adjusted_slide.get('slide_index', 0)
                new_index = global_start_index + old_index
                adjusted_slide['slide_index'] = new_index
                adjusted_slide['section_index'] = idx  # 保留板块索引
                adjusted_polished_slides.append(adjusted_slide)
                logger.debug(f"--- [PPTFiller]:   调整polished_slide: {old_index} -> {new_index}")
            
            # 调整layout_plans的slide_index
            adjusted_layout_plans = []
            for plan in layout_plans:
                adjusted_plan = plan.copy()
                old_index = adjusted_plan.get('slide_index', 0)
                new_index = global_start_index + old_index
                adjusted_plan['slide_index'] = new_index
                adjusted_plan['section_index'] = idx  # 保留板块索引
                adjusted_layout_plans.append(adjusted_plan)
                logger.debug(f"--- [PPTFiller]:   调整layout_plan: {old_index} -> {new_index}")
            
            # 调整presentation_plans的slide_index
            adjusted_presentation_plans = []
            for plan in presentation_plan:
                adjusted_plan = plan.copy()
                old_index = adjusted_plan.get('slide_index', 0)
                new_index = global_start_index + old_index
                adjusted_plan['slide_index'] = new_index
                adjusted_plan['section_index'] = idx  # 保留板块索引
                adjusted_presentation_plans.append(adjusted_plan)
                logger.debug(f"--- [PPTFiller]:   调整presentation_plan: {old_index} -> {new_index}")
            
            # 调整color_configs的slide_index
            adjusted_color_configs = []
            for config in color_configs:
                adjusted_config = config.copy()
                old_index = adjusted_config.get('slide_index', 0)
                new_index = global_start_index + old_index
                adjusted_config['slide_index'] = new_index
                adjusted_config['section_index'] = idx  # 保留板块索引
                adjusted_color_configs.append(adjusted_config)
                logger.debug(f"--- [PPTFiller]:   调整color_config: {old_index} -> {new_index}")
            
            # 使用调整后的数据
            all_polished_slides.extend(adjusted_polished_slides)
            all_presentation_plans.extend(adjusted_presentation_plans)
            all_layout_plans.extend(adjusted_layout_plans)
            all_color_configs.extend(adjusted_color_configs)
            
            logger.info(f"--- [PPTFiller]: 【探针】合并后总数: polished_slides={len(all_polished_slides)}, layout_plans={len(all_layout_plans)}")
            
            # 1. 构建板块特定的生成提示词（包含支撑材料、润色结果、展示策划）
            section_prompt = self._build_section_prompt(
                section_strategy=section_strategy,
                overall_strategy=content_strategy.get("overall_strategy", {}),
                expression_strategy=content_strategy.get("expression_strategy", {}),
                user_prompt=user_prompt,
                human_analysis=human_analysis,
                section_strategies=section_strategies,
                data_points=section_data_points,
                cases=section_cases,
                polished_slides=polished_slides,
                presentation_plan=presentation_plan
            )
            
            # 2. 调用LLM生成板块内容（基于润色和展示策划结果）
            logger.info(f"--- [PPTFiller]: 【详细探针】调用LLM生成板块{idx + 1}内容...")
            logger.info(f"   提示词长度: {len(section_prompt)}字符")
            logger.info(f"   提示词预览: {section_prompt[:500]}...")
            
            section_content = await self._generate_section_content(section_prompt)
            
            logger.info(f"--- [PPTFiller]: 【详细探针】LLM生成结果:")
            logger.info(f"   返回类型: {type(section_content)}")
            if isinstance(section_content, dict):
                logger.info(f"   标题: {section_content.get('title', '')[:100]}...")
                logger.info(f"   内容长度: {len(section_content.get('content', ''))}字符")
                logger.info(f"   关键点数量: {len(section_content.get('key_points', []))}")
                logger.info(f"   数据高亮数量: {len(section_content.get('data_highlights', []))}")
                logger.info(f"   案例数量: {len(section_content.get('case_studies', []))}")
            else:
                logger.warning(f"   ⚠️ 返回格式异常: {section_content}")
            
            # 3. 结构化板块内容
            logger.info(f"--- [PPTFiller]: 【详细探针】结构化板块内容...")
            structured_content = self._structure_section_content(
                section_content,
                section_strategy
            )
            
            logger.info(f"--- [PPTFiller]: 【详细探针】结构化结果:")
            logger.info(f"   标题: {structured_content.get('title', '')[:100]}...")
            logger.info(f"   主要内容: {len(structured_content.get('main_content', ''))}字符")
            logger.info(f"   关键点: {len(structured_content.get('key_points', []))}个")
            if structured_content.get('key_points'):
                for i, kp in enumerate(structured_content['key_points'][:3]):
                    logger.info(f"     关键点{i+1}: {kp[:80]}...")
            
            # 4. 映射到PPT占位符
            section_slides = section_strategy.get("slides", [])
            logger.info(f"--- [PPTFiller]: 【探针】板块{idx + 1}映射到幻灯片: {section_slides}")
            section_content_map = self._map_to_placeholders(
                structured_content,
                section_slides,
                human_analysis
            )
            
            # 【探针】记录映射结果
            logger.info(f"--- [PPTFiller]: 【探针】板块{idx + 1}生成的内容映射:")
            for key, content in section_content_map.items():
                logger.info(f"   {key}: {len(content)}字符 - {content[:50]}...")
            
            # 5. 合并到总内容映射
            content_map.update(section_content_map)
            logger.info(f"--- [PPTFiller]: Section {idx + 1} completed, generated {len(section_content_map)} placeholders")
            logger.info(f"--- [PPTFiller]: 【探针】当前总内容映射项数: {len(content_map)}")
        
        # 【新增】返回内容映射、润色结果、布局规划结果和颜色配置结果
        return {
            'content_map': content_map,
            'polished_slides': all_polished_slides,
            'presentation_plans': all_presentation_plans,
            'layout_plans': all_layout_plans,
            'color_configs': all_color_configs
        }
    
    def _get_section_analysis(
        self,
        section_index: int,
        human_analysis: Dict[str, Any],
        section_strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        获取特定板块的分析结果（用于润色）
        
        Args:
            section_index: 板块索引
            human_analysis: 人类中心化分析结果
            section_strategy: 板块策略
            
        Returns:
            板块分析结果字典
        """
        sections = human_analysis.get("layer_2_sections", {}).get("data", {})
        section_list = sections.get("sections", [])
        
        # 查找对应板块
        section_data = None
        for section in section_list:
            if section.get("section_index", -1) == section_index:
                section_data = section
                break
        
        # 如果没有找到，使用板块策略中的信息
        if not section_data:
            section_data = {
                "section_index": section_index,
                "theme": section_strategy.get("theme", ""),
                "core_idea": section_strategy.get("core_idea", ""),
                "content_summary": section_strategy.get("content_summary", "")
            }
        
        # 获取该板块的论证逻辑
        arguments = human_analysis.get("layer_3_arguments", {}).get("data", {})
        argument_list = arguments.get("arguments", [])
        section_arguments = [
            arg for arg in argument_list 
            if arg.get("section_index", -1) == section_index
        ]
        
        return {
            "section_index": section_index,
            "theme": section_data.get("theme", ""),
            "core_idea": section_data.get("core_idea", ""),
            "content_summary": section_data.get("content_summary", ""),
            "arguments": section_arguments,
            "slides": section_strategy.get("slides", [])
        }
    
    def _build_section_prompt(
        self,
        section_strategy: Dict[str, Any],
        overall_strategy: Dict[str, Any],
        expression_strategy: Dict[str, Any],
        user_prompt: str,
        human_analysis: Dict[str, Any],
        section_strategies: List[Dict[str, Any]],
        data_points: Optional[List[Dict[str, Any]]] = None,
        cases: Optional[List[Dict[str, Any]]] = None,
        polished_slides: Optional[List[Dict[str, Any]]] = None,
        presentation_plan: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """构建板块特定的生成提示词"""
        
        section_idx = section_strategy.get("section_index", 0)
        approach = section_strategy.get("content_generation_approach", {})
        
        # 获取前后板块信息
        prev_section = section_strategies[section_idx - 1] if section_idx > 0 else None
        next_section = section_strategies[section_idx + 1] if section_idx < len(section_strategies) - 1 else None
        
        # 格式化证据点
        evidence_points = section_strategy.get("evidence_points", [])
        evidence_text = "\n".join([f"{i+1}. {point}" for i, point in enumerate(evidence_points[:5])]) if evidence_points else "无"
        
        prompt = f"""
【整体背景】
核心主题：{overall_strategy.get("core_theme", "")}
价值主张：{", ".join(overall_strategy.get("value_propositions", []))}
目标受众：{overall_strategy.get("target_audience", "")}
文档目的：{overall_strategy.get("purpose", "")}

【当前板块】
板块主题：{section_strategy.get("theme", "")}
核心思想：{section_strategy.get("core_idea", "")}
板块位置：第{section_idx + 1}个板块（共{len(section_strategies)}个）

【论证逻辑】
论证方式：{", ".join(section_strategy.get("argument_types", [])) if section_strategy.get("argument_types") else "通用论证"}
证据点：
{evidence_text}

【生成策略】
强调重点：{approach.get("emphasis", "核心观点")}
证据优先级：{", ".join(approach.get("evidence_priority", []))}
内容长度：{approach.get("length", "medium")}

【表达风格】
正式程度：{expression_strategy.get("language_style", {}).get("formality", "中性")}
语调：{expression_strategy.get("language_style", {}).get("tone", "中性")}
文化特征：{", ".join(expression_strategy.get("language_style", {}).get("cultural_features", []))}

【板块上下文】
前一个板块：{prev_section.get("theme", "无") if prev_section else "无"}
后一个板块：{next_section.get("theme", "无") if next_section else "无"}

【可用支撑材料】
{self._format_supporting_materials_for_prompt(data_points, cases)}

【润色结果】
{self._format_polished_slides_for_prompt(polished_slides) if polished_slides else "未进行润色"}

【展示策划】
{self._format_presentation_plan_for_prompt(presentation_plan) if presentation_plan else "未进行展示策划"}

【用户需求】
{user_prompt}

【生成要求 - 重要：这是PPT，不是发言稿！】
1. **标题**：简洁有力，体现核心思想，不超过15字
2. **正文（content字段）**：只放简洁概述（1-2句话，不超过50字），不要放长段落
3. **关键要点（key_points）**：必须是要点式列表，每个要点不超过30字，不要用完整句子
4. **数据**：优先使用上述"可用数据点"，如果有数据论证，突出显示数据（如"降低40-60%成本"）
5. **案例**：优先使用上述"可用案例"，如果有案例论证，简洁说明案例（要点式，不超过20字）
6. **逻辑**：与前一个板块有逻辑衔接，为后一个板块做铺垫
7. **风格**：符合{expression_strategy.get("language_style", {}).get("formality", "中性")}风格，语调{expression_strategy.get("language_style", {}).get("tone", "中性")}
8. **文化**：体现{", ".join(expression_strategy.get("language_style", {}).get("cultural_features", [])) if expression_strategy.get("language_style", {}).get("cultural_features") else "通用商业文化"}

【禁止事项】：
- ❌ 不要生成"各位同事"、"今天我将"等发言稿开场白
- ❌ 不要生成长段落描述，必须用要点列表
- ❌ 不要生成完整的句子，要用简洁的要点
- ❌ content字段不要放长段落，应该放简洁的概述（1-2句话），详细内容放在key_points中

【正确格式示例】：
{{
  "title": "技术产品商业化全链路AI解决方案",
  "content": "基于25年技术积累，形成完整的AI赋能解决方案体系",
  "key_points": [
    "降低运营成本40-60%",
    "提升转化效率20-35%",
    "三大核心系统：朋友云、BefriendsAI、数据中心"
  ],
  "data_highlights": ["降低运营成本40-60%", "提升转化效率20-35%"],
  "case_studies": []
}}

请生成该板块的内容（JSON格式）：
{{
  "title": "标题（不超过15字）",
  "content": "简洁概述（1-2句话，不超过50字）",
  "key_points": ["要点1（不超过30字）", "要点2（不超过30字）"],
  "data_highlights": ["数据1", "数据2"],
  "case_studies": ["案例1（不超过20字）", "案例2（不超过20字）"]
}}
"""
        return prompt
    
    async def _generate_section_content(self, section_prompt: str) -> Dict[str, Any]:
        """生成板块内容"""
        system_prompt = """你是一个专业的PPT内容创作助手，擅长生成符合中国商业汇报习惯的PPT内容。

【重要】PPT内容要求（不是发言稿！）：
1. **简洁性**：PPT是视觉辅助工具，内容必须简洁明了，每页不超过5-7个要点
2. **要点式**：使用要点列表（bullet points），而不是长段落描述
3. **标题**：标题要简洁有力，不超过15字，体现核心观点
4. **正文**：正文应该是要点列表，每个要点不超过30字，避免完整句子
5. **数据**：如果有数据，单独列出，突出显示（如"降低40-60%成本"）
6. **避免**：
   - ❌ 不要生成完整的发言稿或演讲稿
   - ❌ 不要使用"各位同事"、"今天我将"等开场白
   - ❌ 不要生成长段落描述
   - ❌ 不要使用完整的句子，要用要点式
7. **正确示例**：
   - ✅ "降低运营成本40-60%"
   - ✅ "提升转化效率20-35%"
   - ✅ "三大核心系统：朋友云、BefriendsAI、数据中心"
   - ❌ "各位管理层同事，今天我将向大家汇报..."（这是发言稿，不是PPT）

要求：
1. 理解板块的核心思想和论证逻辑
2. 根据生成策略组织内容，但必须是要点式，不是详细描述
3. 突出价值主张和关键数据
4. 保持逻辑清晰，有说服力
5. 符合表达风格和文化特征

输出必须是有效的JSON格式。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": section_prompt}
        ]
        
        try:
            logger.debug(f"--- [PPTFiller]: 【详细探针】调用LLM API...")
            logger.debug(f"   模型: {self.llm_service.model_name}")
            logger.debug(f"   Base URL: {self.llm_service.base_url}")
            logger.debug(f"   消息数量: {len(messages)}")
            logger.debug(f"   System消息长度: {len(messages[0].get('content', ''))}字符")
            logger.debug(f"   User消息长度: {len(messages[1].get('content', ''))}字符")
            
            response = await self.llm_service.chat_completion_async(
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            logger.debug(f"--- [PPTFiller]: 【详细探针】LLM API调用成功")
            logger.debug(f"   响应长度: {len(response)}字符")
            logger.debug(f"   响应预览: {response[:300]}...")
            
            # 解析JSON响应
            import json
            import re
            
            # 尝试提取JSON（支持多种格式）
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    parsed_json = json.loads(json_match.group(0))
                    logger.debug(f"--- [PPTFiller]: 【详细探针】JSON解析成功")
                    logger.debug(f"   解析后的键: {list(parsed_json.keys())}")
                    return parsed_json
                except json.JSONDecodeError as je:
                    logger.error(f"--- [PPTFiller]: JSON解析失败: {je}")
                    logger.error(f"   尝试解析的内容: {json_match.group(0)[:500]}...")
                    # 尝试修复常见的JSON问题
                    json_str = json_match.group(0)
                    # 移除可能的注释
                    json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)
                    try:
                        return json.loads(json_str)
                    except:
                        pass
            else:
                logger.warning("--- [PPTFiller]: 未找到JSON格式，使用fallback")
                logger.warning(f"   响应内容: {response[:500]}...")
            
            # Fallback: 尝试从响应中提取内容
            return {
                "title": "标题",
                "content": response[:200] if response else "",
                "key_points": [],
                "data_highlights": [],
                "case_studies": []
            }
        except Exception as e:
            logger.error(f"--- [PPTFiller]: Failed to generate section content: {e}", exc_info=True)
            logger.error(f"--- [PPTFiller]: 【详细探针】错误类型: {type(e).__name__}")
            logger.error(f"--- [PPTFiller]: 【详细探针】错误详情: {str(e)}")
            
            # 如果是API错误，记录更多信息
            if hasattr(e, 'response'):
                logger.error(f"--- [PPTFiller]: 【详细探针】API响应: {e.response}")
            if hasattr(e, 'status_code'):
                logger.error(f"--- [PPTFiller]: 【详细探针】HTTP状态码: {e.status_code}")
            
            return {
                "title": "标题",
                "content": "",
                "key_points": [],
                "data_highlights": [],
                "case_studies": []
            }
    
    def _structure_section_content(
        self,
        section_content: Dict[str, Any],
        section_strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """结构化板块内容"""
        structured = {
            "title": section_content.get("title", ""),
            "main_content": section_content.get("content", ""),
            "key_points": section_content.get("key_points", []),
            "data_highlights": section_content.get("data_highlights", []),
            "case_studies": section_content.get("case_studies", []),
            "section_index": section_strategy.get("section_index", 0),
            "slides": section_strategy.get("slides", [])
        }
        
        # 根据论证类型调整结构
        argument_types = section_strategy.get("argument_types", [])
        if "数据论证" in argument_types:
            structured["emphasis"] = "data"
            structured["data_formatted"] = self._format_data_highlights(
                structured["data_highlights"]
            )
        
        if "案例论证" in argument_types:
            structured["emphasis"] = "case"
            structured["cases_formatted"] = self._format_case_studies(
                structured["case_studies"]
            )
        
        return structured
    
    def _format_polished_slides_for_prompt(
        self,
        polished_slides: List[Dict[str, Any]]
    ) -> str:
        """
        格式化润色后的幻灯片用于提示词
        
        Args:
            polished_slides: 润色后的幻灯片列表
            
        Returns:
            格式化后的字符串
        """
        if not polished_slides:
            return "未进行润色"
        
        formatted = []
        for slide in polished_slides:
            slide_idx = slide.get('slide_index', 0)
            title = slide.get('title', '')
            content = slide.get('content', '')
            content_type = slide.get('content_type', '')
            
            formatted.append(f"幻灯片{slide_idx} ({content_type}):")
            if title:
                formatted.append(f"  标题: {title}")
            if content:
                # 限制长度
                content_preview = content[:200] + "..." if len(content) > 200 else content
                formatted.append(f"  内容: {content_preview}")
            
            # 如果有视觉元素详情
            visual_elements = slide.get('visual_elements_detail', [])
            if visual_elements:
                formatted.append(f"  视觉元素 ({len(visual_elements)}个):")
                for elem in visual_elements[:3]:  # 只显示前3个
                    elem_id = elem.get('element_id', '')
                    elem_type = elem.get('element_type', '')
                    elem_title = elem.get('title', '')
                    formatted.append(f"    - {elem_id} ({elem_type}): {elem_title}")
        
        return "\n".join(formatted)
    
    def _format_presentation_plan_for_prompt(
        self,
        presentation_plan: List[Dict[str, Any]]
    ) -> str:
        """
        格式化展示策划结果用于提示词
        
        Args:
            presentation_plan: 展示策划结果列表
            
        Returns:
            格式化后的字符串
        """
        if not presentation_plan:
            return "未进行展示策划"
        
        formatted = []
        for plan in presentation_plan:
            slide_idx = plan.get('slide_index', 0)
            layout_type = plan.get('layout_type', '')
            layout_desc = plan.get('layout_description', '')
            visual_guidance = plan.get('visual_guidance', {})
            
            formatted.append(f"幻灯片{slide_idx}:")
            formatted.append(f"  布局类型: {layout_type}")
            if layout_desc:
                formatted.append(f"  布局描述: {layout_desc[:150]}...")
            if visual_guidance:
                font_size = visual_guidance.get('font_size', '')
                alignment = visual_guidance.get('alignment', '')
                if font_size or alignment:
                    formatted.append(f"  视觉指导: 字号{font_size}, 对齐{alignment}")
        
        return "\n".join(formatted)
    
    def _format_data_highlights(self, data_highlights: List[str]) -> str:
        """格式化数据高亮"""
        if not data_highlights:
            return ""
        
        formatted = []
        for data in data_highlights:
            formatted.append(f"• {data}")
        
        return "\n".join(formatted)
    
    def _format_case_studies(self, case_studies: List[str]) -> str:
        """格式化案例说明"""
        if not case_studies:
            return ""
        
        formatted = []
        for case in case_studies:
            formatted.append(f"• {case}")
        
        return "\n".join(formatted)
    
    def _format_supporting_materials_for_prompt(
        self,
        data_points: Optional[List[Dict[str, Any]]],
        cases: Optional[List[Dict[str, Any]]]
    ) -> str:
        """
        格式化支撑材料用于提示词
        
        Args:
            data_points: 智能识别的数据点列表
            cases: 智能识别的案例列表
            
        Returns:
            格式化的支撑材料文本
        """
        parts = []
        
        # 格式化数据点
        if data_points:
            parts.append("【可用数据点】")
            for dp in data_points:
                data_text = f"- {dp.get('value', '')}"
                if dp.get('label'):
                    data_text += f" ({dp.get('label')})"
                if dp.get('context'):
                    data_text += f" - {dp.get('context')[:50]}"
                parts.append(data_text)
        else:
            parts.append("【可用数据点】无")
        
        # 格式化案例
        if cases:
            parts.append("\n【可用案例】")
            for case in cases:
                case_text = f"- {case.get('type', '案例')}"
                if case.get('company'):
                    case_text += f": {case.get('company')}"
                if case.get('result'):
                    case_text += f" - 结果: {case.get('result')}"
                if case.get('content'):
                    case_text += f" - {case.get('content')[:100]}"
                parts.append(case_text)
        else:
            parts.append("\n【可用案例】无")
        
        return "\n".join(parts)
    
    def _map_to_placeholders(
        self,
        structured_content: Dict[str, Any],
        slide_indices: List[int],
        human_analysis: Dict[str, Any]
    ) -> Dict[str, str]:
        """智能映射到PPT占位符（详细探针）"""
        content_map = {}
        
        logger.info("="*80)
        logger.info("--- [PPTFiller]: 【详细探针】内容映射到PPT占位符")
        logger.info("="*80)
        logger.info(f"   结构化内容:")
        logger.info(f"     标题: {structured_content.get('title', '')[:100]}...")
        logger.info(f"     主要内容长度: {len(structured_content.get('main_content', ''))}字符")
        logger.info(f"     关键点数量: {len(structured_content.get('key_points', []))}")
        logger.info(f"     数据高亮数量: {len(structured_content.get('data_highlights', []))}")
        logger.info(f"     案例数量: {len(structured_content.get('case_studies', []))}")
        logger.info(f"   目标幻灯片: {slide_indices}")
        
        # 获取所有幻灯片的占位符信息
        slides_data = human_analysis.get("layer_1_physical", {}).get("data", {})
        # 从原始结构获取占位符信息
        enhanced_parser = EnhancedPPTParser(str(self.framework_path))
        enhanced_structure = enhanced_parser.extract_structure_enhanced()
        
        logger.info(f"   框架PPT幻灯片数: {len(enhanced_structure.get('slides', []))}")
        
        for slide_idx in slide_indices:
            logger.info(f"\n   --- 处理幻灯片{slide_idx} ---")
            if slide_idx < len(enhanced_structure.get("slides", [])):
                # 使用框架PPT的占位符结构
                slide_data = enhanced_structure["slides"][slide_idx]
                placeholders = slide_data.get("placeholders", [])
                
                logger.info(f"     占位符数量: {len(placeholders)}")
                
                # 根据占位符类型分配内容
                for placeholder in placeholders:
                    placeholder_id = placeholder.get("placeholder_id", 0)
                    placeholder_type = placeholder.get("placeholder_type", "")
                    placeholder_key = f"slide_{slide_idx}_placeholder_{placeholder_id}"
                    
                    logger.info(f"     占位符{placeholder_id}:")
                    logger.info(f"       类型: {placeholder_type}")
                    logger.info(f"       键名: {placeholder_key}")
                    
                    if "TITLE" in placeholder_type or "CENTER_TITLE" in placeholder_type:
                        # 标题占位符
                        assigned_content = structured_content["title"]
                        content_map[placeholder_key] = assigned_content
                        logger.info(f"       → 分配标题内容: {assigned_content[:100]}...")
                    elif "OBJECT" in placeholder_type or "BODY" in placeholder_type or "SUBTITLE" in placeholder_type:
                        # 正文占位符
                        # 【改进】根据占位符ID和内容类型智能分配
                        # 如果有多个占位符，可以拆分不同类型的内容
                        placeholder_idx = placeholder_id
                        
                        if placeholder_idx == 1:
                            # 第一个正文占位符：优先显示关键要点
                            if structured_content.get("key_points"):
                                key_points_text = "\n".join([f"• {point}" for point in structured_content["key_points"]])
                                content_map[placeholder_key] = key_points_text
                                logger.info(f"       → 分配关键要点: {len(key_points_text)}字符, {len(structured_content['key_points'])}个要点")
                            else:
                                content = self._build_body_content(structured_content, placeholder_type)
                                content_map[placeholder_key] = content
                                logger.info(f"       → 分配正文内容: {len(content)}字符")
                        elif placeholder_idx == 2:
                            # 第二个正文占位符：显示数据高亮
                            if structured_content.get("data_highlights"):
                                data_text = "\n".join([f"📊 {data}" for data in structured_content["data_highlights"]])
                                content_map[placeholder_key] = data_text
                                logger.info(f"       → 分配数据高亮: {len(data_text)}字符")
                            elif structured_content.get("case_studies"):
                                case_text = "\n".join([f"💡 {case}" for case in structured_content["case_studies"]])
                                content_map[placeholder_key] = case_text
                                logger.info(f"       → 分配案例说明: {len(case_text)}字符")
                            else:
                                # 如果没有数据/案例，使用合并的body_content
                                content = self._build_body_content(structured_content, placeholder_type)
                                content_map[placeholder_key] = content
                                logger.info(f"       → 分配正文内容: {len(content)}字符")
                        else:
                            # 其他占位符：使用合并的body_content
                            content = self._build_body_content(structured_content, placeholder_type)
                            content_map[placeholder_key] = content
                            logger.info(f"       → 分配正文内容: {len(content)}字符")
                            logger.info(f"         内容预览: {content[:150]}...")
                    else:
                        # 其他占位符
                        assigned_content = structured_content["main_content"]
                        content_map[placeholder_key] = assigned_content
                        logger.info(f"       → 分配主要内容: {len(assigned_content)}字符")
                        logger.info(f"         内容预览: {assigned_content[:150]}...")
            else:
                # 【修复】对于超出框架PPT范围的幻灯片，使用默认占位符结构
                # 【改进】将不同类型的内容拆分成多个内容块，提升视觉层次
                logger.info(f"     幻灯片{slide_idx}超出框架PPT范围，使用默认占位符结构（拆分内容块）")
                
                # 标题占位符
                title_key = f"slide_{slide_idx}_placeholder_0"
                title_content = structured_content.get("title", "")
                if title_content:
                    content_map[title_key] = title_content
                    logger.info(f"       → 分配标题内容: {title_content[:100]}...")
                
                # 【改进】将内容拆分成多个块，而不是合并成一个
                placeholder_idx = 1
                
                # 1. 关键要点（如果有，单独一个块）
                if structured_content.get("key_points"):
                    key_points_text = "\n".join([f"• {point}" for point in structured_content["key_points"]])
                    key_points_key = f"slide_{slide_idx}_placeholder_{placeholder_idx}"
                    content_map[key_points_key] = key_points_text
                    logger.info(f"       → 分配关键要点块: {len(key_points_text)}字符, {len(structured_content['key_points'])}个要点")
                    placeholder_idx += 1
                
                # 2. 数据高亮（如果有，单独一个块）
                if structured_content.get("data_highlights"):
                    data_text = "\n".join([f"📊 {data}" for data in structured_content["data_highlights"]])
                    data_key = f"slide_{slide_idx}_placeholder_{placeholder_idx}"
                    content_map[data_key] = data_text
                    logger.info(f"       → 分配数据高亮块: {len(data_text)}字符, {len(structured_content['data_highlights'])}个数据")
                    placeholder_idx += 1
                
                # 3. 案例说明（如果有，单独一个块）
                if structured_content.get("case_studies"):
                    case_text = "\n".join([f"💡 {case}" for case in structured_content["case_studies"]])
                    case_key = f"slide_{slide_idx}_placeholder_{placeholder_idx}"
                    content_map[case_key] = case_text
                    logger.info(f"       → 分配案例说明块: {len(case_text)}字符, {len(structured_content['case_studies'])}个案例")
                    placeholder_idx += 1
                
                # 4. 主要内容（如果有且简短，作为概述）
                if structured_content.get("main_content") and len(structured_content["main_content"]) < 100:
                    main_key = f"slide_{slide_idx}_placeholder_{placeholder_idx}"
                    content_map[main_key] = structured_content["main_content"]
                    logger.info(f"       → 分配主要内容块: {len(structured_content['main_content'])}字符")
                    placeholder_idx += 1
                
                # 如果没有以上任何内容，使用合并的body_content作为后备
                if placeholder_idx == 1:  # 只有标题，没有其他内容
                    body_key = f"slide_{slide_idx}_placeholder_1"
                    body_content = self._build_body_content(structured_content, "OBJECT")
                    if body_content:
                        content_map[body_key] = body_content
                        logger.info(f"       → 分配正文内容（后备）: {len(body_content)}字符")
        
        logger.info(f"\n   映射完成，共生成{len(content_map)}个内容映射项")
        logger.info("="*80)
        
        return content_map
    
    def _build_body_content(
        self,
        structured_content: Dict[str, Any],
        placeholder_type: str
    ) -> str:
        """构建正文内容（要点式，不是发言稿）"""
        parts = []
        
        # 1. 关键要点（优先显示，这是PPT的主要内容）
        if structured_content.get("key_points"):
            for point in structured_content["key_points"]:
                parts.append(f"• {point}")
        
        # 2. 数据高亮（如果有，单独列出）
        if structured_content.get("data_highlights"):
            for data in structured_content["data_highlights"]:
                parts.append(f"📊 {data}")
        
        # 3. 案例说明（如果有，简洁列出）
        if structured_content.get("case_studies"):
            for case in structured_content["case_studies"]:
                parts.append(f"💡 {case}")
        
        # 4. 主要内容（如果有且简短，可以作为概述）
        # 但不要放长段落，因为那是发言稿风格
        if structured_content.get("main_content") and len(structured_content["main_content"]) < 100:
            # 只在内容简短时使用
            parts.insert(0, structured_content["main_content"])
        
        return "\n".join(parts) if parts else ""
    
    def _create_structure_from_docx_content(
        self,
        docx_content: str,
        framework_structure: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        从docx内容创建结构数据，用于人类中心化分析
        
        Args:
            docx_content: docx文档的文本内容
            framework_structure: 框架PPT的结构（用于获取幻灯片布局信息）
            
        Returns:
            结构数据字典，格式与EnhancedPPTParser的输出类似
        """
        # 将docx内容按段落分割
        paragraphs = [p.strip() for p in docx_content.split('\n') if p.strip()]
        
        # 【改进】识别标题和章节结构
        # 标题特征：短文本（<50字）、可能包含emoji、数字编号、关键词等
        headings = []
        for i, para in enumerate(paragraphs):
            # 判断是否为标题
            is_heading = False
            heading_level = 0
            
            # 特征1: 短文本（<50字）且可能是标题
            if len(para) < 50:
                # 特征2: 包含emoji（如💎、🚀）
                if any(ord(c) > 127 and c not in '，。、；：！？""''（）【】《》' for c in para[:10]):
                    is_heading = True
                    heading_level = 1
                # 特征3: 数字编号（如"1、"、"2、"、"一、"等）
                elif re.match(r'^[0-9一二三四五六七八九十]+[、.]', para):
                    is_heading = True
                    heading_level = 2
                # 特征4: 包含关键词（如"分析"、"战略"、"路线图"、"回顾"等）
                elif any(kw in para for kw in ['分析', '战略', '路线图', '回顾', '市场', '商业化', '技术', '产品', '文档', '启示', '规划', '能力', '路径']):
                    is_heading = True
                    heading_level = 1
                # 特征5: 主标题（如"技术产品商业化-文档"）
                elif '-' in para or '：' in para or ':' in para:
                    # 如果包含短横线或冒号，且长度较短，可能是标题
                    if len(para) < 30:
                        is_heading = True
                        heading_level = 1
            
            if is_heading:
                headings.append({
                    "index": i,
                    "text": para,
                    "level": heading_level
                })
        
        logger.info(f"--- [PPTFiller]: 识别到{len(headings)}个标题/章节")
        for h in headings[:15]:  # 显示前15个
            logger.info(f"   标题: {h['text'][:50]}")
        
        # 【改进】基于标题将内容分成多个板块，每个板块生成1-2张幻灯片
        slides = []
        framework_slides = framework_structure.get("slides", [])
        framework_placeholders = framework_slides[0].get("placeholders", []) if framework_slides else []
        
        if headings:
            # 基于标题分割内容
            for heading_idx, heading in enumerate(headings):
                start_para_idx = heading["index"]
                end_para_idx = headings[heading_idx + 1]["index"] if heading_idx + 1 < len(headings) else len(paragraphs)
                
                # 获取该板块的段落
                section_paragraphs = paragraphs[start_para_idx:end_para_idx]
                
                # 每个板块生成1-2张幻灯片（根据内容长度）
                # 如果内容超过200字，分成2张幻灯片
                section_text = ' '.join(section_paragraphs)
                num_slides_for_section = 2 if len(section_text) > 200 else 1
                
                paragraphs_per_slide = max(1, len(section_paragraphs) // num_slides_for_section)
                
                for slide_in_section in range(num_slides_for_section):
                    slide_start = slide_in_section * paragraphs_per_slide
                    slide_end = (slide_in_section + 1) * paragraphs_per_slide if slide_in_section < num_slides_for_section - 1 else len(section_paragraphs)
                    slide_paragraphs = section_paragraphs[slide_start:slide_end]
                    
                    # 第一张幻灯片包含标题
                    if slide_in_section == 0:
                        slide_paragraphs = [heading["text"]] + slide_paragraphs
                    
                    # 创建幻灯片结构
                    slide_data = {
                        "slide_index": len(slides),
                        "placeholders": framework_placeholders,
                        "shapes": []
                    }
                    
                    # 为每个段落创建一个shape
                    for para_idx, para_text in enumerate(slide_paragraphs):
                        shape_data = {
                            "shape_id": para_idx,
                            "text": para_text,
                            "shape_type": "paragraph",
                            "is_placeholder": False,
                            "format": {
                                "is_bold": para_idx == 0 and slide_in_section == 0,  # 标题加粗
                                "font_size_pt": 20 if para_idx == 0 and slide_in_section == 0 else 14
                            }
                        }
                        slide_data["shapes"].append(shape_data)
                    
                    slides.append(slide_data)
        else:
            # 如果没有识别到标题，使用原来的策略
            logger.warning("--- [PPTFiller]: 未识别到标题，使用简单分配策略")
            if framework_slides:
                paragraphs_per_slide = max(1, len(paragraphs) // len(framework_slides))
                
                for slide_idx, framework_slide in enumerate(framework_slides):
                    start_idx = slide_idx * paragraphs_per_slide
                    end_idx = (slide_idx + 1) * paragraphs_per_slide if slide_idx < len(framework_slides) - 1 else len(paragraphs)
                    slide_paragraphs = paragraphs[start_idx:end_idx]
                    
                    slide_data = {
                        "slide_index": slide_idx,
                        "placeholders": framework_slide.get("placeholders", []),
                        "shapes": []
                    }
                    
                    for para_idx, para_text in enumerate(slide_paragraphs):
                        shape_data = {
                            "shape_id": para_idx,
                            "text": para_text,
                            "shape_type": "paragraph",
                            "is_placeholder": False
                        }
                        slide_data["shapes"].append(shape_data)
                    
                    slides.append(slide_data)
            else:
                # 如果没有框架，创建一个简单的单幻灯片结构
                slide_data = {
                    "slide_index": 0,
                    "placeholders": [],
                    "shapes": []
                }
                for para_idx, para_text in enumerate(paragraphs):
                    shape_data = {
                        "shape_id": para_idx,
                        "text": para_text,
                        "shape_type": "paragraph",
                        "is_placeholder": False
                    }
                    slide_data["shapes"].append(shape_data)
                slides.append(slide_data)
        
        logger.info(f"--- [PPTFiller]: 基于docx结构生成了{len(slides)}张幻灯片结构（之前只有{len(framework_slides) if framework_slides else 1}张）")
        
        return {
            "slide_count": len(slides),
            "slides": slides
        }
    
    def _generate_output_path(self) -> str:
        """生成输出文件路径"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_name = f"{self.framework_path.stem}-filled-{timestamp}.pptx"
        output_path = self.framework_path.parent / output_name
        return str(output_path)


```


## File: ppt_generator.py

```python
"""
PPT生成器 - 核心组装功能
从FabricatorAgent中抽离的PPT组装核心功能，不依赖数据库和知识库
支持可选的Vinci图表生成集成
"""

import json
import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union

from loguru import logger
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Cm, Emu, Pt
from webcolors import hex_to_rgb

# 导入Ant Design主题
from ant_design_theme import ant_design_theme


# 辅助类，用于管理布局计算（使用统一单位）
class Box:
    def __init__(self, left, top, width, height):
        # 统一转换为 Cm 类型，确保运算兼容性
        def _to_cm(value):
            if isinstance(value, Cm):
                return value
            elif isinstance(value, (Pt, Emu)):
                return Cm(float(value) / 360000)  # Emu to cm
            elif isinstance(value, (int, float)):
                return Cm(value)
            else:
                return Cm(0)

        self.left = _to_cm(left)
        self.top = _to_cm(top)
        self.width = _to_cm(width)
        self.height = _to_cm(height)

    def _cm_to_float(self, cm_value):
        """将 Cm 对象转换为厘米数值"""
        if isinstance(cm_value, Cm):
            return float(cm_value) / 360000
        elif isinstance(cm_value, (int, float)):
            return float(cm_value)
        else:
            return 0.0


class PPTGenerator:
    """
    独立的PPT生成器
    根据VML计划和内容映射生成PPT文件
    支持可选的Vinci图表生成集成
    """

    def __init__(
        self,
        output_dir: Optional[Union[str, Path]] = None,
        vinci_integration: Optional[Any] = None
    ):
        """
        初始化PPT生成器
        
        Args:
            output_dir: PPT输出目录，默认为当前目录下的 ppt_outputs 文件夹
            vinci_integration: 可选的Vinci集成实例，用于生成图表
        """
        self.codename = "PPTGenerator"
        
        if output_dir is None:
            output_dir = Path.cwd() / "ppt_outputs"
        elif isinstance(output_dir, str):
            output_dir = Path(output_dir)
        
        self.PPT_OUTPUT_DIR = output_dir
        self.PPT_OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
        
        self._vinci_integration = vinci_integration
        if vinci_integration:
            logger.info(f"--- [{self.codename}]: Initialized with Vinci integration")
        else:
            logger.info(f"--- [{self.codename}]: Initialized without Vinci integration (chart generation disabled)")
        
        logger.info(f"--- [{self.codename}]: Output directory: {self.PPT_OUTPUT_DIR}")

    def _parse_unit(self, value_str: str, base_cm: float = 0, base_pt: float = 0) -> Union[Cm, Pt, Emu]:
        """解析并转换各种单位 (cm, px, pt, %) 到 python-pptx 的单位类型"""
        if isinstance(value_str, (int, float)):
            return Cm(value_str)

        value_str = str(value_str).lower().strip()

        try:
            if value_str.endswith('cm'):
                return Cm(float(value_str[:-2]))
            elif value_str.endswith('px'):
                px_value = float(value_str[:-2])
                return Cm(px_value * 2.54 / 96)
            elif value_str.endswith('pt'):
                return Pt(float(value_str[:-2]))
            elif value_str.endswith('%'):
                if base_cm > 0:
                    return Cm(base_cm * (float(value_str[:-1]) / 100.0))
                elif base_pt > 0:
                    return Pt(base_pt * (float(value_str[:-1]) / 100.0))
                return Cm(0)
            else:
                return Cm(float(value_str))
        except (ValueError, TypeError):
            logger.warning(f"--- [{self.codename}] Could not parse unit from '{value_str}'. Defaulting to 0.")
            return Cm(0)

    def _parse_color(self, color_str: str) -> Optional[dict[str, Any]]:
        """解析颜色字符串 (hex 或 rgba) 并返回包含 RGB 和 alpha 的字典"""
        if not color_str:
            return None

        try:
            # 处理 rgba 格式
            if color_str.startswith('rgba'):
                parts = [p.strip() for p in color_str[5:-1].split(',')]
                if len(parts) >= 3:
                    r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
                    a = float(parts[3]) if len(parts) > 3 else 1.0
                    return {"rgb": RGBColor(r, g, b), "alpha": a}

            # 处理 rgb 格式（无 alpha）
            if color_str.startswith('rgb'):
                parts = [p.strip() for p in color_str[4:-1].split(',')]
                if len(parts) >= 3:
                    r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
                    return {"rgb": RGBColor(r, g, b), "alpha": 1.0}

            # 处理 hex 格式
            if color_str.startswith('#'):
                rgb = hex_to_rgb(color_str)
                return {"rgb": RGBColor(rgb.red, rgb.green, rgb.blue), "alpha": 1.0}

            # 处理不带 # 的 hex
            if len(color_str) == 6 and all(c in '0123456789abcdef' for c in color_str.lower()):
                rgb = hex_to_rgb('#' + color_str)
                return {"rgb": RGBColor(rgb.red, rgb.green, rgb.blue), "alpha": 1.0}

        except Exception as e:
            logger.warning(f"--- [{self.codename}] Could not parse color '{color_str}'. Error: {e}")

        return None

    def _parse_shadow(self, shadow_str: str) -> Optional[dict[str, Any]]:
        """解析 CSS box-shadow 字符串，转换为 python-pptx 阴影参数"""
        if not shadow_str or shadow_str.lower() == 'none':
            return None

        try:
            first_shadow = shadow_str.split(',')[0].strip()
            color_match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)', first_shadow)
            if not color_match:
                return None

            r, g, b, a = color_match.groups()
            a = float(a) if a is not None else 1.0

            offset_matches = re.findall(r'(-?\d+(?:\.\d+)?)px', first_shadow)
            if len(offset_matches) < 2:
                return None

            offset_x = float(offset_matches[0])
            offset_y = float(offset_matches[1])
            blur_radius = float(offset_matches[2]) if len(offset_matches) > 2 else 0

            distance = Pt(abs(offset_y))
            direction = 270 if offset_y >= 0 else 90

            return {
                "color": RGBColor(int(r), int(g), int(b)),
                "transparency": 1.0 - a,
                "blur_radius": Pt(blur_radius),
                "distance": distance,
                "direction": direction
            }
        except Exception as e:
            logger.warning(f"--- [{self.codename}] Could not parse shadow '{shadow_str}'. Error: {e}")
        return None

    def _parse_vml(self, vml_code: str):
        """解析 VML 代码，如果失败则尝试修复或返回安全的 fallback"""
        try:
            return ET.fromstring(vml_code)
        except ET.ParseError as e:
            try:
                from xml.sax.saxutils import escape

                def escape_text_content(match):
                    attr_name = match.group(1)
                    content = match.group(2)
                    escaped_content = escape(content)
                    return f'{attr_name}="{escaped_content}"'

                fixed_vml = re.sub(r'(text)="([^"]*)"', escape_text_content, vml_code)

                if fixed_vml != vml_code:
                    logger.debug("--- [PPTGenerator] VML parse failed, attempting auto-fix...")
                    try:
                        result = ET.fromstring(fixed_vml)
                        logger.debug("--- [PPTGenerator] ✅ VML auto-fixed and parsed successfully!")
                        return result
                    except ET.ParseError:
                        logger.warning(f"--- [PPTGenerator] Auto-fix failed. Using fallback.")
            except Exception as fix_error:
                logger.warning(f"--- [PPTGenerator] Failed to fix VML: {fix_error}")

            logger.error(f"VML Parse Error: {e}. VML Code:\n{vml_code}")

            # 生成安全的 fallback VML
            from xml.sax.saxutils import escape
            error_msg = escape(str(e))
            try:
                fallback_vml = f'<Slide padding="1.5cm"><VStack><TextBox style="title" text="VML解析失败"/><TextBox style="body" text="错误: {error_msg}"/></VStack></Slide>'
                return ET.fromstring(fallback_vml)
            except ET.ParseError:
                logger.critical("Fallback VML also failed. Using minimal safe VML.")
                return ET.fromstring('<Slide padding="1.5cm"><VStack><TextBox style="title" text="VML解析失败"/></VStack></Slide>')

    def _render_element(self, slide, element, box: Box, content_map: dict):
        """渲染VML元素到PPT幻灯片"""
        tag = element.tag.lower()
        attrs = {k: v for k, v in element.attrib.items()}

        # 容器元素递归渲染
        if tag in ["vstack", "hstack", "stack"]:
            children = list(element)
            if not children:
                return

            direction = attrs.get("direction", "vertical").lower()
            if tag == "vstack":
                direction = "vertical"
            elif tag == "hstack":
                direction = "horizontal"

            gap_str = attrs.get("gap", "0.5cm")
            base_dim = box.width if direction == 'horizontal' else box.height
            base_dim_cm = box._cm_to_float(base_dim) if isinstance(base_dim, Cm) else float(base_dim)
            gap = self._parse_unit(gap_str, base_cm=base_dim_cm)

            if len(children) > 1:
                if isinstance(gap, Cm):
                    gap_cm = box._cm_to_float(gap)
                    total_gap_cm = gap_cm * (len(children) - 1)
                    total_gap = Cm(total_gap_cm)
                else:
                    total_gap = Cm(float(gap) * (len(children) - 1))
            else:
                total_gap = Cm(0)

            if direction == "vertical":
                total_gap_cm = box._cm_to_float(total_gap)
                box_height_cm = box._cm_to_float(box.height)
                available_height_cm = box_height_cm - total_gap_cm if len(children) > 1 else box_height_cm
                child_height_cm = available_height_cm / len(children) if children else 0
                child_height = Cm(child_height_cm)

                current_top = box.top
                gap_cm = box._cm_to_float(gap) if isinstance(gap, Cm) else float(gap)
                for child in children:
                    child_box = Box(box.left, current_top, box.width, child_height)
                    self._render_element(slide, child, child_box, content_map)
                    current_top_cm = box._cm_to_float(current_top) + child_height_cm + gap_cm
                    current_top = Cm(current_top_cm)
            else:  # horizontal
                total_gap_cm = box._cm_to_float(total_gap)
                box_width_cm = box._cm_to_float(box.width)
                available_width_cm = box_width_cm - total_gap_cm if len(children) > 1 else box_width_cm
                child_width_cm = available_width_cm / len(children) if children else 0
                child_width = Cm(child_width_cm)

                current_left = box.left
                gap_cm = box._cm_to_float(gap) if isinstance(gap, Cm) else float(gap)
                for child in children:
                    child_box = Box(current_left, box.top, child_width, box.height)
                    self._render_element(slide, child, child_box, content_map)
                    current_left_cm = box._cm_to_float(current_left) + child_width_cm + gap_cm
                    current_left = Cm(current_left_cm)
            return

        # 判断是否需要创建带样式的容器
        is_styled_container = (
            'background' in attrs or
            'border' in attrs or
            'shadows' in attrs or
            'shadow' in attrs or
            'borderRadius' in attrs or
            'borderradius' in attrs
        )

        # 1. 处理纯文本内容（无样式容器）
        if tag == "textbox" and not is_styled_container:
            text_ref = attrs.get("ref", "")
            if not text_ref:
                text = attrs.get("text", "内容缺失")
                logger.debug(f"--- [PPTGenerator] Rendering pure TextBox (fallback): text='{text[:50]}...'")
            else:
                text = content_map.get(text_ref, f"!!REF_NOT_FOUND: {text_ref}!!")
                logger.debug(f"--- [PPTGenerator] Rendering pure TextBox: ref='{text_ref}'")

            txBox = slide.shapes.add_textbox(box.left, box.top, box.width, box.height)
            tf = txBox.text_frame
            tf.clear()
            tf.word_wrap = True

            justify = attrs.get("justify", "top").lower()
            if justify == "center":
                tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            elif justify == "bottom":
                tf.vertical_anchor = MSO_ANCHOR.BOTTOM
            else:
                tf.vertical_anchor = MSO_ANCHOR.TOP

            p = tf.paragraphs[0]
            align = attrs.get("align", "left").lower()
            if align == "center":
                p.alignment = PP_ALIGN.CENTER
            elif align == "right":
                p.alignment = PP_ALIGN.RIGHT
            else:
                p.alignment = PP_ALIGN.LEFT

            p.text = str(text)

            try:
                if hasattr(txBox, 'line'):
                    txBox.line.fill.background()
            except Exception:
                pass

            try:
                if hasattr(txBox, 'fill'):
                    txBox.fill.background()
            except Exception:
                pass

            if not p.runs:
                run = p.add_run()
            else:
                run = p.runs[0]

            font = run.font
            # 使用Ant Design字体系统
            try:
                # Ant Design字体栈（优先系统字体）
                font.name = "Segoe UI"  # Windows系统字体
            except Exception:
                try:
                    font.name = "Helvetica Neue"  # macOS系统字体
                except Exception:
                    try:
                        font.name = "微软雅黑"  # 中文字体fallback
                    except Exception:
                        font.name = "Arial"  # 最终fallback

            if 'color' in attrs:
                font_color_info = self._parse_color(attrs['color'])
                if font_color_info:
                    font.color.rgb = font_color_info['rgb']

            if 'fontSize' in attrs:
                font_size = self._parse_unit(attrs['fontSize'], base_pt=100)
                if isinstance(font_size, Pt):
                    font.size = font_size
                else:
                    font.size = Pt(float(font_size) * 28.35)

            if 'fontWeight' in attrs:
                try:
                    weight = int(attrs['fontWeight'])
                    font.bold = weight >= 600
                except (ValueError, TypeError):
                    font.bold = attrs.get('fontWeight', '').lower() in ['bold', '700', '600']

            if 'fontSize' not in attrs and 'fontWeight' not in attrs:
                style_key = attrs.get("style", "body")
                if style_key == "title":
                    font.size = Pt(ant_design_theme.get_font_size_pt('h1'))
                    font.bold = True
                elif style_key == "subtitle":
                    font.size = Pt(ant_design_theme.get_font_size_pt('h3'))
                    font.bold = False
                else:
                    font.size = Pt(ant_design_theme.get_font_size_pt('base'))
                    font.bold = False

            return

        # 2. 处理纯图片内容（无样式容器）
        elif tag in ["imagebox", "image"] and not is_styled_container:
            img_ref = attrs.get("ref", "")
            img_path = content_map.get(img_ref)

            logger.info(f"--- [PPTGenerator] Rendering pure ImageBox: ref='{img_ref}', found_path='{img_path}'")

            if not img_path or not os.path.exists(img_path):
                logger.error(f"--- [PPTGenerator] CRITICAL: Image path not found: {img_path}")
                txBox = slide.shapes.add_textbox(box.left, box.top, box.width, box.height)
                txBox.text_frame.text = f"Image Load Error!\nRef: {img_ref}"
            else:
                width_str = attrs.get("width", "100%")
                height_str = attrs.get("height", "100%")

                box_width_cm = box._cm_to_float(box.width)
                box_height_cm = box._cm_to_float(box.height)
                img_width = self._parse_unit(width_str, base_cm=box_width_cm)
                img_height = self._parse_unit(height_str, base_cm=box_height_cm)

                try:
                    slide.shapes.add_picture(str(img_path), box.left, box.top, img_width, img_height)
                except Exception as e:
                    logger.error(f"--- [PPTGenerator] Failed to add picture: {e}", exc_info=True)
                    txBox = slide.shapes.add_textbox(box.left, box.top, box.width, box.height)
                    txBox.text_frame.text = f"Image Error: {img_ref}\n{str(e)}"

            return

        # 3. 处理带样式的容器
        shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if ('borderRadius' in attrs or 'borderradius' in attrs) else MSO_SHAPE.RECTANGLE
        shape = slide.shapes.add_shape(shape_type, box.left, box.top, box.width, box.height)

        if 'borderRadius' in attrs or 'borderradius' in attrs:
            try:
                radius_str = attrs.get('borderRadius') or attrs.get('borderradius', '')
                radius_px = float(re.sub(r'[a-zA-Z%]', '', str(radius_str)))
                box_height_cm = box._cm_to_float(box.height)
                adjustment = min(0.5, radius_px / 32.0)
                if shape_type == MSO_SHAPE.ROUNDED_RECTANGLE and len(shape.adjustments) > 0:
                    shape.adjustments[0] = adjustment
            except Exception as e:
                logger.warning(f"--- [PPTGenerator] Failed to apply custom borderRadius: {e}")

        fill = shape.fill
        line = shape.line
        fill.background()
        line.fill.background()

        if 'background' in attrs:
            color_info = self._parse_color(attrs['background'])
            if color_info:
                fill.solid()
                fill.fore_color.rgb = color_info['rgb']
                if color_info['alpha'] < 1.0:
                    fill.transparency = 1.0 - color_info['alpha']

        if 'shadows' in attrs or 'shadow' in attrs:
            shadow_params = self._parse_shadow(attrs.get('shadows') or attrs.get('shadow'))
            if shadow_params:
                try:
                    shadow = shape.shadow
                    shadow.inherit = False
                    shadow.style = 'outer'
                    shadow.blur_radius = shadow_params['blur_radius']
                    shadow.distance = shadow_params['distance']
                    shadow.direction = shadow_params['direction']
                    shadow.color.rgb = shadow_params['color']
                    shadow.transparency = shadow_params['transparency']
                except Exception as e:
                    logger.warning(f"--- [PPTGenerator] Could not apply shadow. Error: {e}")

        # 4. 处理文本内容（在带样式的容器中）
        if tag == "textbox":
            text_ref = attrs.get("ref", "")
            if not text_ref:
                text = attrs.get("text", "内容缺失")
                logger.debug(f"--- [PPTGenerator] Rendering TextBox (fallback): text='{text[:50]}...'")
            else:
                text = content_map.get(text_ref, f"!!REF_NOT_FOUND: {text_ref}!!")
                logger.debug(f"--- [PPTGenerator] Rendering TextBox: ref='{text_ref}'")

            tf = shape.text_frame
            tf.clear()
            tf.word_wrap = True

            justify = attrs.get("justify", "top").lower()
            if justify == "center":
                tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            elif justify == "bottom":
                tf.vertical_anchor = MSO_ANCHOR.BOTTOM
            else:
                tf.vertical_anchor = MSO_ANCHOR.TOP

            p = tf.paragraphs[0]
            align = attrs.get("align", "left").lower()
            if align == "center":
                p.alignment = PP_ALIGN.CENTER
            elif align == "right":
                p.alignment = PP_ALIGN.RIGHT
            else:
                p.alignment = PP_ALIGN.LEFT

            p.text = str(text)

            font = p.font
            # 使用Ant Design字体系统
            try:
                font.name = "Segoe UI"
            except Exception:
                try:
                    font.name = "Helvetica Neue"
                except Exception:
                    try:
                        font.name = "微软雅黑"
                    except Exception:
                        font.name = "Arial"

            if 'color' in attrs:
                font_color_info = self._parse_color(attrs['color'])
                if font_color_info:
                    font.color.rgb = font_color_info['rgb']

            if 'fontSize' in attrs:
                font_size = self._parse_unit(attrs['fontSize'], base_pt=100)
                if isinstance(font_size, Pt):
                    font.size = font_size
                else:
                    font.size = Pt(float(font_size) * 28.35)

            if 'fontWeight' in attrs:
                try:
                    weight = int(attrs['fontWeight'])
                    font.bold = weight >= 600
                except (ValueError, TypeError):
                    font.bold = attrs.get('fontWeight', '').lower() in ['bold', '700', '600']

            if 'fontSize' not in attrs and 'fontWeight' not in attrs:
                style_key = attrs.get("style", "body")
                if style_key == "title":
                    font.size = Pt(ant_design_theme.get_font_size_pt('h1'))
                    font.bold = True
                elif style_key == "subtitle":
                    font.size = Pt(ant_design_theme.get_font_size_pt('h3'))
                    font.bold = False
                else:
                    font.size = Pt(ant_design_theme.get_font_size_pt('base'))
                    font.bold = False

        # 5. 处理图片内容（在带样式的容器中）
        elif tag in ["imagebox", "image"]:
            img_ref = attrs.get("ref", "")
            img_path = content_map.get(img_ref)

            logger.info(f"--- [PPTGenerator] Rendering ImageBox/Image in styled container: ref='{img_ref}'")

            if not img_path or not os.path.exists(img_path):
                logger.error(f"--- [PPTGenerator] CRITICAL: Image path not found: {img_path}")
                shape.text_frame.text = f"Image Load Error!\nRef: {img_ref}"
            else:
                width_str = attrs.get("width", "100%")
                height_str = attrs.get("height", "100%")

                box_width_cm = box._cm_to_float(box.width)
                box_height_cm = box._cm_to_float(box.height)
                img_width = self._parse_unit(width_str, base_cm=box_width_cm)
                img_height = self._parse_unit(height_str, base_cm=box_height_cm)

                try:
                    fill.picture(str(img_path))
                    fill.tile = False
                except (AttributeError, Exception) as e:
                    logger.warning(f"--- [PPTGenerator] fill.picture() not available, using add_picture: {e}")
                    try:
                        pic_shape = slide.shapes.add_picture(str(img_path), box.left, box.top, img_width, img_height)
                        try:
                            shape.fill.background()
                            shape.line.fill.background()
                        except Exception:
                            pass
                    except Exception as e2:
                        logger.error(f"--- [PPTGenerator] Failed to add picture: {e2}", exc_info=True)
                        try:
                            shape.text_frame.text = f"Image Error: {img_ref}\n{str(e2)}"
                        except:
                            pass

    def assemble_slide_from_vml(self, slide, vml_code: str, content_map: dict):
        """从VML代码组装单张幻灯片"""
        root_element = self._parse_vml(vml_code)
        attrs = root_element.attrib

        if root_element.tag.lower() == "slide":
            try:
                slide_width = slide.part.package.presentation_part.presentation.slide_width
                slide_height = slide.part.package.presentation_part.presentation.slide_height
                if isinstance(slide_width, Cm):
                    slide_width_cm = float(slide_width)
                else:
                    slide_width_cm = float(slide_width) / 360000

                if isinstance(slide_height, Cm):
                    slide_height_cm = float(slide_height)
                else:
                    slide_height_cm = float(slide_height) / 360000
            except Exception as e:
                logger.warning(f"--- [PPTGenerator] Could not get slide dimensions: {e}. Using defaults.")
                slide_width_cm = 33.867
                slide_height_cm = 19.05

            # 使用Ant Design间距系统（默认padding）
            default_padding_cm = ant_design_theme.get_spacing_cm('lg')
            padding_str = attrs.get("padding", f"{default_padding_cm:.2f}cm")
            padding = self._parse_unit(padding_str, base_cm=slide_width_cm)
            if isinstance(padding, Cm):
                padding_cm = float(padding) / 360000
            else:
                padding_cm = float(padding)

            inner_box = Box(
                left=Cm(padding_cm),
                top=Cm(padding_cm),
                width=Cm(slide_width_cm - (padding_cm * 2)),
                height=Cm(slide_height_cm - (padding_cm * 2))
            )

            if 'background' in attrs:
                try:
                    color = self._parse_color(attrs['background'])
                    if color:
                        slide.background.fill.solid()
                        slide.background.fill.fore_color.rgb = color['rgb']
                except Exception as e:
                    logger.warning(f"--- [PPTGenerator] Could not apply slide background color. Error: {e}")

            for child in list(root_element):
                self._render_element(slide, child, inner_box, content_map)

    async def generate_ppt(
        self,
        project_name: str,
        vml_plan: list[dict],
        content_map: dict,
        template_path: Optional[Union[str, Path]] = None,
        chart_insights: Optional[list[dict]] = None
    ) -> dict:
        """
        根据VML计划生成PPT文件
        
        Args:
            project_name: 项目名称（用于文件名）
            vml_plan: VML计划列表，每个元素包含 'vml_code' 字段
            content_map: 内容映射字典，键是ref名称，值是实际内容（文本或图片路径）
            template_path: 可选的PPT模板路径
            chart_insights: 可选的图表洞察列表，如果提供且Vinci集成可用，会自动生成图表
            
        Returns:
            包含 'file_path' 的字典，如果失败则包含 'error'
        """
        logger.info(f"--- [{self.codename}]: Generating PPT from VML plan...")
        logger.info(f"VML Plan ({len(vml_plan)} slides)")
        logger.info(f"Content Map ({len(content_map)} items)")
        
        # 如果提供了图表洞察且Vinci集成可用，先生成图表
        if chart_insights and self._vinci_integration:
            logger.info(f"--- [{self.codename}]: Generating {len(chart_insights)} charts via Vinci...")
            try:
                chart_paths = await self._vinci_integration.generate_charts_from_insights(
                    chart_insights,
                    project_id=project_name
                )
                # 将生成的图表路径添加到content_map
                for insight_id, chart_path in chart_paths.items():
                    # 如果content_map中已经有这个ref，更新它；否则添加
                    if insight_id in content_map:
                        logger.info(f"--- [{self.codename}]: Updated chart path for '{insight_id}': {chart_path}")
                    content_map[insight_id] = chart_path
                logger.success(f"--- [{self.codename}]: Generated {len(chart_paths)} charts")
            except Exception as e:
                logger.error(f"--- [{self.codename}]: Failed to generate charts: {e}", exc_info=True)
                # 继续生成PPT，即使图表生成失败
        elif chart_insights and not self._vinci_integration:
            logger.warning(
                f"--- [{self.codename}]: Chart insights provided but Vinci integration not available. "
                "Charts will not be generated."
            )

        try:
            # 加载模板或创建空白演示文稿
            if template_path and Path(template_path).exists():
                prs = Presentation(str(template_path))
                logger.info(f"--- [{self.codename}]: Loaded template from: {template_path}")
            else:
                prs = Presentation()
                prs.slide_width = Cm(33.867)  # 16:9
                prs.slide_height = Cm(19.05)
                logger.info(f"--- [{self.codename}]: Using blank presentation")

            # 选择空白布局
            num_layouts = len(prs.slide_layouts)
            blank_layout = None
            min_placeholders = float('inf')

            for layout_idx in range(num_layouts):
                try:
                    test_layout = prs.slide_layouts[layout_idx]
                    placeholder_count = len(test_layout.placeholders)
                    if placeholder_count < min_placeholders:
                        min_placeholders = placeholder_count
                        blank_layout = test_layout
                    if placeholder_count == 0:
                        break
                except Exception:
                    continue

            if blank_layout is None:
                blank_layout = prs.slide_layouts[0]
                logger.warning(f"--- [{self.codename}] Could not find blank layout, using first layout")
            else:
                logger.info(f"--- [{self.codename}] Selected blank layout: {blank_layout.name} ({min_placeholders} placeholders)")

            # 处理每张幻灯片
            for i, slide_vml_data in enumerate(vml_plan):
                vml_code = slide_vml_data.get("vml_code", "")

                try:
                    slide = prs.slides.add_slide(blank_layout)
                except Exception as layout_error:
                    logger.warning(f"--- [{self.codename}] Failed to add slide: {layout_error}")
                    slide = prs.slides.add_slide(prs.slide_layouts[0])

                # 清除占位符
                from pptx.enum.shapes import MSO_SHAPE_TYPE
                for shape in slide.shapes:
                    if shape.shape_type == MSO_SHAPE_TYPE.PLACEHOLDER:
                        try:
                            if hasattr(shape, 'text_frame'):
                                shape.text_frame.clear()
                            if hasattr(shape, 'fill'):
                                try:
                                    shape.fill.background()
                                except:
                                    pass
                            if hasattr(shape, 'line'):
                                try:
                                    shape.line.fill.background()
                                except:
                                    pass
                        except Exception:
                            pass

                try:
                    self.assemble_slide_from_vml(slide, vml_code, content_map)
                except Exception as slide_error:
                    logger.error(f"--- [{self.codename}] Failed to render slide {i+1}: {slide_error}", exc_info=True)
                    try:
                        error_textbox = slide.shapes.add_textbox(Cm(2), Cm(2), Cm(10), Cm(2))
                        error_textbox.text_frame.text = f"幻灯片 {i+1} 渲染失败: {str(slide_error)[:100]}"
                    except:
                        pass

            # 保存文件
            safe_project_name = "".join(c for c in project_name if c.isalnum() or c in " -_").rstrip()
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            file_name = f"{safe_project_name}-{timestamp}.pptx"
            file_path = self.PPT_OUTPUT_DIR / file_name

            try:
                prs.save(str(file_path))

                if not file_path.exists():
                    raise FileNotFoundError(f"PPT file was not created: {file_path}")

                file_size = file_path.stat().st_size
                if file_size < 1000:
                    logger.warning(f"--- [{self.codename}] Generated PPT file is suspiciously small: {file_size} bytes")

                logger.success(f"--- [{self.codename}]: PPT file generated and saved to: {file_path} ({file_size} bytes)")
                return {"file_path": str(file_path), "file_size": file_size}
            except Exception as save_error:
                logger.error(f"--- [{self.codename}] Failed to save PPT file: {save_error}", exc_info=True)
                raise

        except Exception as e:
            error_msg = f"Failed to generate PPT: {e}"
            logger.error(f"--- [{self.codename}]: {error_msg}", exc_info=True)
            return {"error": error_msg}


```


## File: ppt_parser.py

```python
"""
PPT框架解析器
读取现有PPT文件，提取结构和布局信息
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from loguru import logger


class PPTParser:
    """
    PPT框架解析器
    从现有PPT文件中提取结构和内容信息
    """
    
    def __init__(self, ppt_path: str):
        """
        初始化PPT解析器
        
        Args:
            ppt_path: PPT文件路径
        """
        self.ppt_path = Path(ppt_path)
        if not self.ppt_path.exists():
            raise FileNotFoundError(f"PPT file not found: {ppt_path}")
        
        self.prs = Presentation(str(self.ppt_path))
        logger.info(f"--- [PPTParser]: Loaded PPT: {self.ppt_path}")
    
    def extract_structure(self) -> Dict[str, Any]:
        """
        提取PPT的结构信息
        
        Returns:
            包含幻灯片结构信息的字典
        """
        structure = {
            "slides": [],
            "slide_count": len(self.prs.slides),
            "slide_width": float(self.prs.slide_width) / 360000,  # 转换为cm
            "slide_height": float(self.prs.slide_height) / 360000
        }
        
        for idx, slide in enumerate(self.prs.slides):
            slide_info = {
                "slide_index": idx,
                "layout_name": slide.slide_layout.name if hasattr(slide.slide_layout, 'name') else "Unknown",
                "shapes": [],
                "placeholders": [],
                "text_content": []
            }
            
            # 提取所有形状信息
            for shape in slide.shapes:
                shape_info = self._extract_shape_info(shape, idx)
                if shape_info:
                    slide_info["shapes"].append(shape_info)
                    
                    # 如果是占位符，单独记录
                    if shape.is_placeholder:
                        slide_info["placeholders"].append(shape_info)
                    
                    # 如果有文本内容，记录
                    if shape_info.get("text"):
                        slide_info["text_content"].append({
                            "type": shape_info["type"],
                            "text": shape_info["text"],
                            "placeholder_id": shape_info.get("placeholder_id")
                        })
            
            structure["slides"].append(slide_info)
        
        logger.info(f"--- [PPTParser]: Extracted structure from {len(structure['slides'])} slides")
        return structure
    
    def _extract_shape_info(self, shape, slide_index: int) -> Optional[Dict[str, Any]]:
        """
        提取单个形状的信息
        
        Args:
            shape: PPT形状对象
            slide_index: 幻灯片索引
            
        Returns:
            形状信息字典
        """
        try:
            shape_info = {
                "type": self._get_shape_type(shape),
                "shape_id": shape.shape_id,
                "left": float(shape.left) / 360000,  # 转换为cm
                "top": float(shape.top) / 360000,
                "width": float(shape.width) / 360000,
                "height": float(shape.height) / 360000,
                "is_placeholder": shape.is_placeholder
            }
            
            # 如果是占位符，记录占位符信息
            if shape.is_placeholder:
                try:
                    shape_info["placeholder_id"] = shape.placeholder_format.idx
                    shape_info["placeholder_type"] = str(shape.placeholder_format.type)
                except:
                    pass
            
            # 提取文本内容
            if hasattr(shape, "text_frame"):
                text = shape.text_frame.text.strip()
                if text:
                    shape_info["text"] = text
                    shape_info["has_text"] = True
                else:
                    shape_info["has_text"] = False
                    shape_info["text"] = ""
            elif hasattr(shape, "text"):
                text = shape.text.strip()
                if text:
                    shape_info["text"] = text
                    shape_info["has_text"] = True
                else:
                    shape_info["has_text"] = False
                    shape_info["text"] = ""
            else:
                shape_info["has_text"] = False
                shape_info["text"] = ""
            
            # 提取图片信息
            if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                try:
                    shape_info["image_path"] = shape.image.filename if hasattr(shape.image, 'filename') else None
                except:
                    pass
            
            return shape_info
            
        except Exception as e:
            logger.warning(f"--- [PPTParser]: Failed to extract shape info: {e}")
            return None
    
    def _get_shape_type(self, shape) -> str:
        """获取形状类型名称"""
        try:
            shape_type = shape.shape_type
            type_names = {
                MSO_SHAPE_TYPE.AUTO_SHAPE: "auto_shape",
                MSO_SHAPE_TYPE.PLACEHOLDER: "placeholder",
                MSO_SHAPE_TYPE.PICTURE: "picture",
                MSO_SHAPE_TYPE.TEXT_BOX: "text_box",
                MSO_SHAPE_TYPE.GROUP: "group",
                MSO_SHAPE_TYPE.TABLE: "table",
                MSO_SHAPE_TYPE.MEDIA: "media"
            }
            return type_names.get(shape_type, "unknown")
        except:
            return "unknown"
    
    def extract_text_summary(self) -> str:
        """
        提取PPT的文本摘要，用于LLM理解框架内容
        
        Returns:
            文本摘要字符串
        """
        summary_parts = []
        summary_parts.append(f"PPT框架文档包含 {len(self.prs.slides)} 张幻灯片。\n")
        
        for idx, slide in enumerate(self.prs.slides):
            summary_parts.append(f"\n幻灯片 {idx + 1}:")
            
            # 提取所有文本内容
            texts = []
            for shape in slide.shapes:
                if hasattr(shape, "text_frame") and shape.text_frame.text.strip():
                    texts.append(shape.text_frame.text.strip())
                elif hasattr(shape, "text") and shape.text.strip():
                    texts.append(shape.text.strip())
            
            if texts:
                summary_parts.append(f"  内容: {' | '.join(texts)}")
            else:
                summary_parts.append(f"  内容: (空白占位符)")
            
            # 记录占位符信息
            placeholders = [s for s in slide.shapes if s.is_placeholder]
            if placeholders:
                summary_parts.append(f"  占位符数量: {len(placeholders)}")
        
        summary = "\n".join(summary_parts)
        logger.debug(f"--- [PPTParser]: Extracted text summary:\n{summary}")
        return summary
    
    def get_placeholder_mapping(self) -> Dict[int, List[Dict[str, Any]]]:
        """
        获取每张幻灯片的占位符映射
        
        Returns:
            字典，键是幻灯片索引，值是占位符信息列表
        """
        mapping = {}
        
        for idx, slide in enumerate(self.prs.slides):
            placeholders = []
            for shape in slide.shapes:
                if shape.is_placeholder:
                    placeholder_info = {
                        "placeholder_id": shape.placeholder_format.idx,
                        "placeholder_type": str(shape.placeholder_format.type),
                        "has_text": False,
                        "text": ""
                    }
                    
                    if hasattr(shape, "text_frame") and shape.text_frame.text.strip():
                        placeholder_info["has_text"] = True
                        placeholder_info["text"] = shape.text_frame.text.strip()
                    
                    placeholders.append(placeholder_info)
            
            if placeholders:
                mapping[idx] = placeholders
        
        return mapping


```


## File: presentation_planner.py

```python
"""
展示策划模块
为副总裁级别的汇报设计简洁明了的展示方式
"""

from typing import Dict, Any, List
from loguru import logger
from llm_service import LLMService
from presentation_schema import (
    PresentationProtocol,
    PresentationPlanSchema,
    VisualGuidanceSchema,
    LayoutType
)
import json
import re


class PresentationPlanner:
    """
    展示策划器
    为副总裁级别的汇报设计简洁明了的展示方式
    """
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        logger.info("--- [PresentationPlanner]: 初始化展示策划器")
    
    async def plan_presentation(
        self,
        polished_slides: List[Dict[str, Any]],
        section_theme: str
    ) -> List[Dict[str, Any]]:
        """
        为润色后的幻灯片设计展示方式
        
        Args:
            polished_slides: 润色后的幻灯片列表
            section_theme: 板块主题
            
        Returns:
            展示策划结果，每个元素包含：
            - slide_index: 幻灯片索引
            - layout_type: 布局类型（blank_center, table_with_summary, cards_with_data等）
            - layout_description: 布局描述
            - visual_guidance: 视觉指导（如何展示）
        """
        logger.info(f"--- [PresentationPlanner]: 策划板块展示方式: {section_theme}")
        
        # 获取Schema描述
        schema_desc = PresentationProtocol.get_schema_description()
        schema_json = json.dumps(schema_desc, ensure_ascii=False, indent=2)
        
        system_prompt = f"""你是中国职场的述职汇报专家，专门为副总裁级别的职场高管筹备述职内容，最擅长将高管整理的文稿大纲转换成适合呈现在ppt上的语言内容。

你具备强大的展示策划能力，能够为副总裁级别的汇报设计简洁明了（注意不是简单）的展示方式。

【重要】展示策划要求：
1. **简洁明了**：快速用分格、分点、分板块的方式展示核心观点
2. **视觉层次**：通过布局、字体大小、颜色等建立清晰的视觉层次
3. **信息密度**：每张幻灯片信息密度适中，不堆砌文字
4. **视觉元素**：合理使用空白、表格、图表、卡片等视觉元素
5. **高管汇报**：听取汇报的是更高层级的管理者，需要快速抓住核心观点

【输出Schema规范】：
请严格按照以下Schema规范输出JSON格式的结果。核心字段必须包含，扩展字段可放在metadata或custom_fields中。

{schema_json}

【关键说明】：
- 必须使用JSON格式输出，包含"presentation_plan"数组
- 每个plan必须包含：slide_index, layout_type, layout_description, visual_guidance
- layout_type可以是常用值（{', '.join([e.value for e in LayoutType])}），也可以自定义
- visual_guidance必须包含：font_size, font_weight, alignment
- 如果需要扩展信息，请放在metadata字段或visual_guidance.custom_fields中，使用snake_case命名"""
        
        # 构建幻灯片信息
        slides_info = []
        for slide in polished_slides:
            slide_info = f"""
幻灯片{slide.get('slide_index', 0)}：
- 标题：{slide.get('title', '')}
- 内容：{slide.get('content', '')}
- 内容类型：{slide.get('content_type', '')}
- 视觉元素需求：{json.dumps(slide.get('visual_elements', {}), ensure_ascii=False)}"""
            slides_info.append(slide_info)
        
        user_prompt = f"""请为以下润色后的幻灯片设计展示方式。

板块主题：{section_theme}

润色后的幻灯片：
{chr(10).join(slides_info)}

请按照以下要求进行展示策划：
1. 为每张幻灯片设计具体的展示方式
2. 考虑副总裁级别汇报的特点：简洁明了、快速抓住核心观点
3. 根据内容类型和视觉元素需求，设计合适的布局

【展示策划示例】：

幻灯片1（标题页）：
- 布局类型：blank_center（空白模板，页面正中间）
- 布局描述：页面正中间加粗、放大显示标题，其他区域留白
- 视觉指导：使用大号字体（76pt+），加粗，居中显示

幻灯片2（内容页，延续标题）：
- 布局类型：blank_center（空白模板，页面正中间）
- 布局描述：页面正中间加粗、放大显示内容，或者考虑与幻灯片1结合
- 视觉指导：使用大号字体（60pt+），加粗，居中显示

幻灯片3（数据页，需要表格/图表）：
- 布局类型：table_with_summary（表格+总结）
- 布局描述：将页面拆解成三页，每一页放置一个表格或图表，在图表下方或右侧放置1-3句总结性话术
- 视觉指导：表格/图表占页面60-70%，总结文字占30-40%，使用中等字体（28-32pt）

幻灯片4（效果页，需要卡片展示）：
- 布局类型：cards_with_data（卡片+数据）
- 布局描述：用三个圆角矩形分别包裹三个系统内容，在下方用居中的数字/文字展示提升数据
- 视觉指导：三个圆角矩形卡片横向排列，每个卡片内包含系统名称和描述，卡片下方居中显示数据（大号字体，加粗）

请以JSON格式输出展示策划结果：
{{
  "presentation_plan": [
    {{
      "slide_index": 幻灯片索引,
      "layout_type": "blank_center|table_with_summary|cards_with_data|split_content|...",
      "layout_description": "详细的布局描述",
      "visual_guidance": {{
        "font_size": "大号(76pt+)|中号(32-60pt)|小号(28pt以下)",
        "font_weight": "bold|normal",
        "alignment": "center|left|right",
        "spacing": "描述间距要求",
        "color_scheme": "描述配色方案",
        "other_notes": "其他视觉指导说明"
      }}
    }},
    ...
  ]
}}"""
        
        try:
            response = await self.llm_service.chat_completion_async(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # 解析JSON响应
            if isinstance(response, str):
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    raw_result = json.loads(json_match.group(0))
                else:
                    logger.warning("   无法从LLM响应中提取JSON，使用默认策划")
                    return self._default_plan(polished_slides)
            else:
                raw_result = response
            
            # 规范化LLM输出
            normalized_result = PresentationProtocol.normalize_llm_output(raw_result)
            presentation_plan = normalized_result.get("presentation_plan", [])
            
            # 验证每个plan
            validated_plans = []
            for plan in presentation_plan:
                if PresentationProtocol.validate_presentation_plan(plan):
                    validated_plans.append(plan)
                else:
                    logger.warning(f"   展示策划数据不符合Schema，跳过: {plan}")
            
            if not validated_plans:
                logger.warning("   没有有效的展示策划结果，使用默认策划")
                return self._default_plan(polished_slides)
            
            logger.info(f"   ✅ 展示策划完成，策划了{len(validated_plans)}张幻灯片")
            for plan in validated_plans:
                logger.info(f"      幻灯片{plan.get('slide_index', 0)}: {plan.get('layout_type', '')} - {plan.get('layout_description', '')[:50]}...")
            
            return validated_plans
        except Exception as e:
            logger.error(f"   ❌ 展示策划失败: {e}，使用默认策划", exc_info=True)
            return self._default_plan(polished_slides)
    
    def _default_plan(self, polished_slides: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """默认策划（回退方案）"""
        plans = []
        for slide in polished_slides:
            content_type = slide.get("content_type", "content_page")
            if content_type == "title_page":
                layout_type = "blank_center"
            elif content_type == "data_page":
                layout_type = "table_with_summary"
            elif content_type == "effect_page":
                layout_type = "cards_with_data"
            else:
                layout_type = "content_page"
            
            plans.append({
                "slide_index": slide.get("slide_index", 0),
                "layout_type": layout_type,
                "layout_description": f"默认{layout_type}布局",
                "visual_guidance": {
                    "font_size": "中号(32-60pt)",
                    "font_weight": "normal",
                    "alignment": "center",
                    "spacing": "默认间距",
                    "color_scheme": "默认配色",
                    "other_notes": ""
                }
            })
        return plans


```


## File: presentation_schema.py

```python
"""
PPT展示Schema定义
采用折中方案：核心字段固定 + 灵活扩展机制
"""

from typing import Dict, Any, List, Optional
from enum import Enum
import json
from loguru import logger


class ContentType(str, Enum):
    """内容类型枚举"""
    TITLE_PAGE = "title_page"
    CONTENT_PAGE = "content_page"
    DATA_PAGE = "data_page"
    EFFECT_PAGE = "effect_page"
    SUMMARY_PAGE = "summary_page"


class LayoutType(str, Enum):
    """布局类型枚举（常用布局）"""
    BLANK_CENTER = "blank_center"
    CARDS_WITH_DATA = "cards_with_data"
    SPLIT_CONTENT = "split_content"
    TIMELINE_HORIZONTAL = "timeline_horizontal"
    TABLE_WITH_SUMMARY = "table_with_summary"
    CARDS_GRID = "cards_grid"
    CHART_WITH_INSIGHT = "chart_with_insight"
    KEY_MESSAGE = "key_message"
    DUAL_WHEEL_CHART = "dual_wheel_chart"
    CHART_WITH_ANNOTATION = "chart_with_annotation"
    # 允许LLM动态扩展其他布局类型


class FontSize(str, Enum):
    """字体大小枚举"""
    LARGE = "large"  # 76pt+
    MEDIUM = "medium"  # 32-60pt
    SMALL = "small"  # 28pt以下


class FontWeight(str, Enum):
    """字体粗细枚举"""
    BOLD = "bold"
    NORMAL = "normal"


class Alignment(str, Enum):
    """对齐方式枚举"""
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"


class PolishedSlideSchema:
    """
    润色后的幻灯片Schema（核心字段固定）
    """
    
    def __init__(
        self,
        slide_index: int,
        title: str,
        content: str,
        content_type: str,
        visual_elements: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        初始化润色后的幻灯片Schema
        
        Args:
            slide_index: 幻灯片索引（在板块内的索引）
            title: 幻灯片标题
            content: 幻灯片核心内容
            content_type: 内容类型（使用ContentType枚举或字符串）
            visual_elements: 视觉元素需求（可选，灵活扩展）
            metadata: 元数据（可选，用于存储LLM动态生成的其他信息）
        """
        self.slide_index = slide_index
        self.title = title
        self.content = content
        self.content_type = content_type
        self.visual_elements = visual_elements or {}
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "slide_index": self.slide_index,
            "title": self.title,
            "content": self.content,
            "content_type": self.content_type,
            "visual_elements": self.visual_elements,
            "metadata": self.metadata
        }
        if self.visual_elements_detail:
            result["visual_elements_detail"] = self.visual_elements_detail
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PolishedSlideSchema":
        """从字典创建"""
        return cls(
            slide_index=data.get("slide_index", 0),
            title=data.get("title", ""),
            content=data.get("content", ""),
            content_type=data.get("content_type", ContentType.CONTENT_PAGE.value),
            visual_elements=data.get("visual_elements", {}),
            visual_elements_detail=data.get("visual_elements_detail", []),
            metadata=data.get("metadata", {})
        )


class VisualGuidanceSchema:
    """
    视觉指导Schema（核心字段固定）
    """
    
    def __init__(
        self,
        font_size: str,
        font_weight: str,
        alignment: str,
        spacing: Optional[str] = None,
        color_scheme: Optional[str] = None,
        other_notes: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None
    ):
        """
        初始化视觉指导Schema
        
        Args:
            font_size: 字体大小（使用FontSize枚举或字符串，如"大号(76pt+)"）
            font_weight: 字体粗细（使用FontWeight枚举或字符串）
            alignment: 对齐方式（使用Alignment枚举或字符串）
            spacing: 间距描述（可选）
            color_scheme: 配色方案描述（可选）
            other_notes: 其他说明（可选）
            custom_fields: 自定义字段（可选，用于LLM动态扩展）
        """
        self.font_size = font_size
        self.font_weight = font_weight
        self.alignment = alignment
        self.spacing = spacing
        self.color_scheme = color_scheme
        self.other_notes = other_notes
        self.custom_fields = custom_fields or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "font_size": self.font_size,
            "font_weight": self.font_weight,
            "alignment": self.alignment
        }
        if self.spacing:
            result["spacing"] = self.spacing
        if self.color_scheme:
            result["color_scheme"] = self.color_scheme
        if self.other_notes:
            result["other_notes"] = self.other_notes
        if self.custom_fields:
            result["custom_fields"] = self.custom_fields
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VisualGuidanceSchema":
        """从字典创建"""
        # 提取自定义字段（不在核心字段中的）
        core_fields = {"font_size", "font_weight", "alignment", "spacing", "color_scheme", "other_notes"}
        custom_fields = {k: v for k, v in data.items() if k not in core_fields}
        
        return cls(
            font_size=data.get("font_size", FontSize.MEDIUM.value),
            font_weight=data.get("font_weight", FontWeight.NORMAL.value),
            alignment=data.get("alignment", Alignment.LEFT.value),
            spacing=data.get("spacing"),
            color_scheme=data.get("color_scheme"),
            other_notes=data.get("other_notes"),
            custom_fields=custom_fields if custom_fields else None
        )


class PresentationPlanSchema:
    """
    展示策划Schema（核心字段固定）
    """
    
    def __init__(
        self,
        slide_index: int,
        layout_type: str,
        layout_description: str,
        visual_guidance: VisualGuidanceSchema,
        data_bindings: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        初始化展示策划Schema
        
        Args:
            slide_index: 幻灯片索引
            layout_type: 布局类型（使用LayoutType枚举或字符串，允许LLM动态扩展）
            layout_description: 布局描述
            visual_guidance: 视觉指导
            data_bindings: 数据绑定（可选，用于指定需要填充的数据、图表等）
            metadata: 元数据（可选，用于存储LLM动态生成的其他信息）
        """
        self.slide_index = slide_index
        self.layout_type = layout_type
        self.layout_description = layout_description
        self.visual_guidance = visual_guidance
        self.data_bindings = data_bindings or {}
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "slide_index": self.slide_index,
            "layout_type": self.layout_type,
            "layout_description": self.layout_description,
            "visual_guidance": self.visual_guidance.to_dict(),
            "data_bindings": self.data_bindings,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PresentationPlanSchema":
        """从字典创建"""
        return cls(
            slide_index=data.get("slide_index", 0),
            layout_type=data.get("layout_type", LayoutType.BLANK_CENTER.value),
            layout_description=data.get("layout_description", ""),
            visual_guidance=VisualGuidanceSchema.from_dict(data.get("visual_guidance", {})),
            data_bindings=data.get("data_bindings", {}),
            metadata=data.get("metadata", {})
        )


class PresentationProtocol:
    """
    PPT展示协议（用于LLM之间的通信）
    包含Schema版本和自描述信息
    """
    
    SCHEMA_VERSION = "1.0.0"
    
    @staticmethod
    def get_schema_description() -> Dict[str, Any]:
        """
        获取Schema描述（用于LLM理解）
        返回一个包含核心字段说明和扩展机制的描述
        """
        return {
            "schema_version": PresentationProtocol.SCHEMA_VERSION,
            "core_fields": {
                "polished_slide": {
                    "slide_index": "幻灯片索引（在板块内的索引，从0开始）",
                    "title": "幻灯片标题（简洁有力，不超过15字）",
                    "content": "幻灯片核心内容（1-2句话）",
                    "content_type": f"内容类型（固定值：{', '.join([e.value for e in ContentType])}）",
                    "visual_elements": "视觉元素需求（字典，可包含needs_table, needs_chart, needs_cards等）",
                    "visual_elements_detail": "视觉元素详细展开（数组，当有多个元素时，必须详细展开每个元素的具体内容，每个元素包含：element_index, element_id, element_type, title, content, data等。element_id格式：element_type_element_index，用于唯一标识，避免传参混淆）",
                    "metadata": "元数据（可选，用于存储扩展信息）"
                },
                "presentation_plan": {
                    "slide_index": "幻灯片索引（与polished_slide对应）",
                    "layout_type": f"布局类型（常用值：{', '.join([e.value for e in LayoutType])}，也可自定义）",
                    "layout_description": "详细的布局描述（文字说明）",
                    "visual_guidance": {
                        "font_size": f"字体大小（建议值：{', '.join([e.value for e in FontSize])}，也可用文字描述如'大号(76pt+)'）",
                        "font_weight": f"字体粗细（{', '.join([e.value for e in FontWeight])}）",
                        "alignment": f"对齐方式（{', '.join([e.value for e in Alignment])}）",
                        "spacing": "间距描述（可选，文字说明）",
                        "color_scheme": "配色方案描述（可选，文字说明）",
                        "other_notes": "其他视觉指导说明（可选）",
                        "custom_fields": "自定义字段（可选，字典形式，用于扩展）"
                    },
                    "data_bindings": "数据绑定（可选，用于指定需要填充的数据、图表等）",
                    "metadata": "元数据（可选，用于存储扩展信息）"
                }
            },
            "extension_mechanism": {
                "description": "LLM可以在以下位置添加自定义字段：",
                "locations": [
                    "polished_slide.metadata: 存储润色相关的扩展信息",
                    "polished_slide.visual_elements: 添加自定义视觉元素需求",
                    "presentation_plan.metadata: 存储策划相关的扩展信息",
                    "presentation_plan.visual_guidance.custom_fields: 添加自定义视觉指导字段",
                    "presentation_plan.data_bindings: 添加数据绑定信息"
                ],
                "naming_convention": "建议使用snake_case命名，如custom_field_name"
            },
            "example": {
                "polished_slide": {
                    "slide_index": 0,
                    "title": "技术产品概述",
                    "content": "展示三大技术产品体系的核心价值",
                    "content_type": "title_page",
                    "visual_elements": {
                        "needs_table": False,
                        "needs_chart": False,
                        "needs_cards": True,
                        "custom_visual_requirement": "需要品牌logo"
                    },
                    "visual_elements_detail": [
                        {
                            "element_index": 0,
                            "element_id": "value_card_0",
                            "element_type": "value_card",
                            "title": "降本",
                            "content": "运营成本降低40-60%",
                            "data": "40-60%",
                            "description": "通过自动化流程和智能优化，显著降低运营成本"
                        },
                        {
                            "element_index": 1,
                            "element_id": "value_card_1",
                            "element_type": "value_card",
                            "title": "增效",
                            "content": "转化效率提升20-35%",
                            "data": "20-35%",
                            "description": "通过AI技术提升转化效率"
                        },
                        {
                            "element_index": 2,
                            "element_id": "value_card_2",
                            "element_type": "value_card",
                            "title": "转型",
                            "content": "加速业务智能化转型",
                            "data": "智能化",
                            "description": "推动业务向智能化方向转型"
                        }
                    ],
                    "metadata": {
                        "priority": "high",
                        "estimated_duration": "30秒"
                    }
                },
                "presentation_plan": {
                    "slide_index": 0,
                    "layout_type": "blank_center",
                    "layout_description": "页面正中间加粗放大显示标题，其他区域留白",
                    "visual_guidance": {
                        "font_size": "large",
                        "font_weight": "bold",
                        "alignment": "center",
                        "spacing": "标题与副标题间距1.5倍行高",
                        "color_scheme": "深色标题+浅灰色副标题",
                        "custom_fields": {
                            "background_color": "#FFFFFF",
                            "title_color": "#1A1A1A"
                        }
                    },
                    "data_bindings": {},
                    "metadata": {
                        "layout_complexity": "simple",
                        "render_time_estimate": "2秒"
                    }
                }
            }
        }
    
    @staticmethod
    def validate_polished_slide(data: Dict[str, Any]) -> bool:
        """验证润色后的幻灯片数据是否符合Schema"""
        required_fields = ["slide_index", "title", "content", "content_type"]
        return all(field in data for field in required_fields)
    
    @staticmethod
    def validate_presentation_plan(data: Dict[str, Any]) -> bool:
        """验证展示策划数据是否符合Schema"""
        required_fields = ["slide_index", "layout_type", "layout_description", "visual_guidance"]
        if not all(field in data for field in required_fields):
            return False
        # 验证visual_guidance
        vg = data.get("visual_guidance", {})
        required_vg_fields = ["font_size", "font_weight", "alignment"]
        return all(field in vg for field in required_vg_fields)
    
    @staticmethod
    def _normalize_visual_elements_detail(elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        规范化视觉元素详细展开，确保每个元素都有element_id
        如果LLM没有提供element_id，自动生成：element_type_element_index
        这样可以避免多个相同类型元素在传参时混淆
        """
        normalized_elements = []
        for elem in elements:
            element_index = elem.get("element_index", 0)
            element_type = elem.get("element_type", "unknown")
            element_id = elem.get("element_id")
            
            # 如果没有element_id，自动生成（格式：element_type_element_index）
            if not element_id:
                element_id = f"{element_type}_{element_index}"
            
            normalized_elem = {
                "element_index": element_index,
                "element_id": element_id,  # 唯一标识，避免传参混淆
                "element_type": element_type,
                "title": elem.get("title", ""),
                "content": elem.get("content", ""),
                "data": elem.get("data"),
                "description": elem.get("description", "")
            }
            normalized_elements.append(normalized_elem)
        return normalized_elements
    
    @staticmethod
    def normalize_llm_output(llm_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        规范化LLM输出，确保符合Schema
        如果LLM使用了不同的字段名，尝试映射到标准字段
        """
        normalized = {}
        
        # 处理polished_slides
        if "polished_slides" in llm_output:
            polished_slides = []
            for slide in llm_output["polished_slides"]:
                # 字段名映射（处理LLM可能的变体）
                normalized_slide = {
                    "slide_index": slide.get("slide_index") or slide.get("index") or slide.get("slide_id", 0),
                    "title": slide.get("title") or slide.get("slide_title") or "",
                    "content": slide.get("content") or slide.get("content_text") or "",
                    "content_type": slide.get("content_type") or slide.get("type") or ContentType.CONTENT_PAGE.value,
                    "visual_elements": slide.get("visual_elements") or slide.get("visual") or {},
                    "visual_elements_detail": PresentationProtocol._normalize_visual_elements_detail(
                        slide.get("visual_elements_detail") or slide.get("visual_detail") or slide.get("elements_detail") or []
                    ),
                    "metadata": slide.get("metadata") or {}
                }
                polished_slides.append(normalized_slide)
            normalized["polished_slides"] = polished_slides
        
        # 处理presentation_plan
        if "presentation_plan" in llm_output:
            presentation_plan = []
            for plan in llm_output["presentation_plan"]:
                # 字段名映射
                vg = plan.get("visual_guidance") or plan.get("visual") or {}
                normalized_plan = {
                    "slide_index": plan.get("slide_index") or plan.get("index") or plan.get("slide_id", 0),
                    "layout_type": plan.get("layout_type") or plan.get("layout") or LayoutType.BLANK_CENTER.value,
                    "layout_description": plan.get("layout_description") or plan.get("description") or "",
                    "visual_guidance": {
                        "font_size": vg.get("font_size") or FontSize.MEDIUM.value,
                        "font_weight": vg.get("font_weight") or FontWeight.NORMAL.value,
                        "alignment": vg.get("alignment") or Alignment.LEFT.value,
                        "spacing": vg.get("spacing"),
                        "color_scheme": vg.get("color_scheme"),
                        "other_notes": vg.get("other_notes"),
                        "custom_fields": vg.get("custom_fields") or {}
                    },
                    "data_bindings": plan.get("data_bindings") or {},
                    "metadata": plan.get("metadata") or {}
                }
                presentation_plan.append(normalized_plan)
            normalized["presentation_plan"] = presentation_plan
        
        return normalized


```


## File: semantic_analyzer.py

```python
"""
语义分析器
识别内容语义、主题分类、逻辑关系
"""

from typing import List, Dict, Any
from loguru import logger
import re


class SemanticAnalyzer:
    """语义分析器 - 识别内容语义和逻辑关系"""
    
    def __init__(self, structure_data: Dict[str, Any]):
        """
        初始化语义分析器
        
        Args:
            structure_data: 增强的结构数据（包含格式信息）
        """
        self.structure = structure_data
        logger.info("--- [SemanticAnalyzer]: Initialized")
    
    def identify_semantic_blocks(self) -> List[Dict[str, Any]]:
        """
        识别语义块（标题-内容结构）
        
        Returns:
            语义块列表
        """
        blocks = []
        current_block = None
        
        for slide in self.structure["slides"]:
            for shape in slide["shapes"]:
                if shape.get("text") and shape.get("text").strip():
                    # 判断是否为标题
                    is_heading = self._is_heading(shape)
                    
                    if is_heading:
                        # 保存之前的块
                        if current_block:
                            blocks.append(current_block)
                        
                        # 开始新块
                        current_block = {
                            "heading": shape.get("text", ""),
                            "heading_level": self._get_heading_level(shape),
                            "heading_format": shape.get("format", {}),
                            "slide_index": slide["slide_index"],
                            "content": []
                        }
                    else:
                        # 添加到当前块的内容
                        if current_block:
                            current_block["content"].append({
                                "text": shape.get("text", ""),
                                "format": shape.get("format", {}),
                                "slide_index": slide["slide_index"]
                            })
                        else:
                            # 如果没有标题，创建一个匿名块
                            current_block = {
                                "heading": None,
                                "heading_level": 0,
                                "heading_format": {},
                                "slide_index": slide["slide_index"],
                                "content": [{
                                    "text": shape.get("text", ""),
                                    "format": shape.get("format", {}),
                                    "slide_index": slide["slide_index"]
                                }]
                            }
        
        # 保存最后一个块
        if current_block:
            blocks.append(current_block)
        
        logger.info(f"--- [SemanticAnalyzer]: Identified {len(blocks)} semantic blocks")
        return blocks
    
    def _is_heading(self, shape: Dict[str, Any]) -> bool:
        """
        判断是否为标题
        
        判断规则（多维度）:
        1. 字体大小 >= 20pt 且加粗
        2. 占位符类型包含 TITLE/HEADING
        3. 文本长度 < 50 且全加粗
        4. 包含编号模式（1. 2. 3.）
        """
        format_info = shape.get("format", {})
        text = shape.get("text", "")
        placeholder_type = shape.get("placeholder_type", "")
        
        # 检查1: 字体大小和加粗
        font_size = format_info.get("font_size_pt") or 0
        is_bold = format_info.get("is_bold", False)
        if font_size and font_size >= 20 and is_bold:
            return True
        
        # 检查2: 占位符类型
        is_title_type = any(keyword in placeholder_type for keyword in ["TITLE", "HEADING", "CENTER_TITLE"])
        if is_title_type:
            return True
        
        # 检查3: 文本长度和格式
        is_short = len(text) < 50
        if is_short and is_bold:
            return True
        
        # 检查4: 编号模式
        has_numbering = bool(re.match(r'^[\d一二三四五六七八九十]+[\.、]', text))
        if has_numbering:
            return True
        
        return False
    
    def _get_heading_level(self, shape: Dict[str, Any]) -> int:
        """
        获取标题级别
        
        Returns:
            标题级别（1-3）
        """
        format_info = shape.get("format", {})
        font_size = format_info.get("font_size_pt", 0)
        placeholder_type = shape.get("placeholder_type", "")
        
        # 根据字体大小判断
        if font_size >= 24:
            return 1
        elif font_size >= 18:
            return 2
        elif "CENTER_TITLE" in placeholder_type:
            return 1
        elif "TITLE" in placeholder_type:
            return 2
        else:
            return 3
    
    def identify_topics(self, blocks: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """
        识别主题
        
        Args:
            blocks: 语义块列表
            
        Returns:
            主题字典，键是主题名，值是相关块列表
        """
        topics = {}
        keywords_patterns = {
            "业务相关": ["业务", "销售", "客户", "市场", "产品", "商业化", "运营", "转化"],
            "技术相关": ["技术", "系统", "平台", "开发", "实现", "AI", "智能", "算法"],
            "数据相关": ["数据", "分析", "统计", "报表", "指标", "数据中心", "数据平台"]
        }
        
        for block in blocks:
            # 构建块文本（标题+内容预览）
            block_text = block["heading"] or ""
            if block["content"]:
                content_preview = " ".join([c["text"][:50] for c in block["content"][:3]])
                block_text += " " + content_preview
            
            # 匹配关键词
            for topic, keywords in keywords_patterns.items():
                if any(keyword in block_text for keyword in keywords):
                    if topic not in topics:
                        topics[topic] = []
                    topics[topic].append({
                        "heading": block["heading"],
                        "heading_level": block["heading_level"],
                        "content_preview": [c["text"][:50] for c in block["content"][:2]]
                    })
                    break
        
        logger.info(f"--- [SemanticAnalyzer]: Identified {len(topics)} topics")
        return topics
    
    def identify_logical_relations(self, blocks: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """
        识别逻辑关系
        
        Args:
            blocks: 语义块列表
            
        Returns:
            逻辑关系字典
        """
        relations = {
            "sequential": [],
            "hierarchical": [],
            "comparative": []
        }
        
        # 顺序关系：连续的块
        for i in range(len(blocks) - 1):
            relations["sequential"].append({
                "from": blocks[i]["heading"] or f"块{i+1}",
                "to": blocks[i+1]["heading"] or f"块{i+2}",
                "from_index": i,
                "to_index": i + 1
            })
        
        # 层级关系：基于标题级别
        for i, block in enumerate(blocks):
            if block["heading_level"] > 0:
                relations["hierarchical"].append({
                    "heading": block["heading"],
                    "level": block["heading_level"],
                    "sub_items": len(block["content"]),
                    "block_index": i
                })
        
        logger.info(f"--- [SemanticAnalyzer]: Identified {len(relations['sequential'])} sequential, {len(relations['hierarchical'])} hierarchical relations")
        return relations


```


## File: supporting_materials_analyzer.py

```python
"""
支撑材料分析器
使用LLM智能识别和理解支撑材料（数据点、案例等）
"""

from typing import List, Dict, Any, Optional
from loguru import logger
import json
import re

from llm_service import LLMService, create_llm_service


class SupportingMaterialsAnalyzer:
    """
    支撑材料分析器
    使用LLM智能识别和理解支撑材料
    """
    
    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        初始化支撑材料分析器
        
        Args:
            llm_service: LLM服务实例
        """
        self.llm_service = llm_service or create_llm_service()
        logger.info("--- [SupportingMaterialsAnalyzer]: 初始化支撑材料分析器")
    
    async def intelligently_identify_data_points(
        self,
        materials: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        智能识别数据点，理解其语义和上下文
        
        Args:
            materials: 从human_centered_analyzer提取的原始材料列表
            
        Returns:
            智能识别后的数据点列表
        """
        if not materials:
            return []
        
        logger.info(f"--- [SupportingMaterialsAnalyzer]: 开始智能识别{len(materials)}个数据点")
        
        # 收集所有数据点的文本和上下文
        data_texts = []
        for material in materials:
            data_texts.append({
                "data": material.get("data", ""),
                "context": material.get("context", ""),
                "slide_index": material.get("slide_index", 0)
            })
        
        # 构建LLM提示词
        prompt = f"""
你是一个专业的数据分析专家。请从以下数据点中提取和理解每个数据的完整信息。

数据点列表：
{json.dumps(data_texts, ensure_ascii=False, indent=2)}

要求：
1. 识别每个数据的类型（percentage百分比、number数值、ratio比率、range范围等）
2. 提取数据的单位（%、万、亿、元等）
3. 从上下文中提取数据的标签（如"成本降低"、"效率提升"等）
4. 判断数据的重要性（high/medium/low）
5. 识别数据之间的关系（如果有对比数据或趋势数据）
6. 提取数据的完整上下文

返回JSON格式：
{{
    "data_points": [
        {{
            "value": "40-60%",
            "type": "percentage_range",
            "unit": "%",
            "label": "成本降低",
            "context": "降低运营成本40-60%",
            "significance": "high",
            "comparison": null,
            "trend": null,
            "slide_index": 0
        }}
    ]
}}

只返回JSON，不要其他内容。
"""
        
        try:
            messages = [
                {"role": "system", "content": "你是一个专业的数据分析专家，擅长理解和提取数据的语义信息。"},
                {"role": "user", "content": prompt}
            ]
            response = await self.llm_service.chat_completion_async(messages=messages)
            
            # 解析JSON响应
            result = self._parse_json_response(response)
            data_points = result.get("data_points", [])
            
            logger.info(f"--- [SupportingMaterialsAnalyzer]: 成功识别{len(data_points)}个数据点")
            return data_points
            
        except Exception as e:
            logger.warning(f"--- [SupportingMaterialsAnalyzer]: LLM识别失败，使用基础识别: {e}")
            # Fallback到基础识别
            return self._basic_identify_data_points(materials)
    
    async def intelligently_identify_cases(
        self,
        materials: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        智能识别案例，理解其结构和价值
        
        Args:
            materials: 从human_centered_analyzer提取的原始材料列表
            
        Returns:
            智能识别后的案例列表
        """
        if not materials:
            return []
        
        logger.info(f"--- [SupportingMaterialsAnalyzer]: 开始智能识别{len(materials)}个案例")
        
        # 收集所有案例的文本和上下文
        case_texts = []
        for material in materials:
            case_texts.append({
                "content": material.get("content", ""),
                "slide_index": material.get("slide_index", 0)
            })
        
        # 构建LLM提示词
        prompt = f"""
你是一个专业的案例分析专家。请从以下案例文本中提取结构化信息。

案例列表：
{json.dumps(case_texts, ensure_ascii=False, indent=2)}

要求：
1. 识别案例类型（customer_case客户案例、project_case项目案例、success_story成功故事等）
2. 提取案例的关键信息：
   - 公司/组织名称（如果有）
   - 行业（如果有）
   - 挑战/问题（如果有）
   - 解决方案（如果有）
   - 结果/效果（如果有）
3. 提取案例的关键要点（3-5个）
4. 判断案例的重要性（high/medium/low）

返回JSON格式：
{{
    "cases": [
        {{
            "type": "customer_case",
            "company": "某直播公司",
            "industry": "直播",
            "challenge": "运营成本高",
            "solution": "使用AI解决方案",
            "result": "成本降低50%",
            "key_points": ["要点1", "要点2", "要点3"],
            "significance": "high",
            "slide_index": 0
        }}
    ]
}}

只返回JSON，不要其他内容。
"""
        
        try:
            messages = [
                {"role": "system", "content": "你是一个专业的案例分析专家，擅长提取和结构化案例信息。"},
                {"role": "user", "content": prompt}
            ]
            response = await self.llm_service.chat_completion_async(messages=messages)
            
            # 解析JSON响应
            result = self._parse_json_response(response)
            cases = result.get("cases", [])
            
            logger.info(f"--- [SupportingMaterialsAnalyzer]: 成功识别{len(cases)}个案例")
            return cases
            
        except Exception as e:
            logger.warning(f"--- [SupportingMaterialsAnalyzer]: LLM识别失败，使用基础识别: {e}")
            # Fallback到基础识别
            return self._basic_identify_cases(materials)
    
    async def identify_chartable_data(
        self,
        data_points: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        识别可以可视化的数据
        
        Args:
            data_points: 智能识别后的数据点列表
            
        Returns:
            可可视化的数据列表
        """
        if not data_points:
            return []
        
        logger.info(f"--- [SupportingMaterialsAnalyzer]: 开始识别可可视化数据")
        
        # 构建LLM提示词
        prompt = f"""
你是一个专业的数据可视化专家。请分析以下数据点，判断哪些适合生成图表。

数据点列表：
{json.dumps(data_points, ensure_ascii=False, indent=2)}

要求：
1. 识别适合可视化的数据（有对比、有趋势、有分类、有分布等）
2. 推荐图表类型（bar柱状图、line折线图、pie饼图、area面积图等）
3. 准备图表数据（结构化数据）
4. 推荐图表位置（slide_index和位置信息）

判断标准：
- 有多个数据点可以对比 → 柱状图
- 有时间序列数据 → 折线图
- 有比例关系 → 饼图
- 有分布数据 → 面积图

返回JSON格式：
{{
    "chartable_data": [
        {{
            "chart_type": "bar",
            "data": [
                {{"label": "成本降低", "value": 50}},
                {{"label": "效率提升", "value": 30}}
            ],
            "title": "成本降低和效率提升对比",
            "x_axis": "指标",
            "y_axis": "百分比(%)",
            "slide_index": 2,
            "recommended_position": {{
                "x": 10,
                "y": 5,
                "width": 15,
                "height": 8
            }}
        }}
    ]
}}

只返回JSON，不要其他内容。如果没有适合可视化的数据，返回空的chartable_data数组。
"""
        
        try:
            messages = [
                {"role": "system", "content": "你是一个专业的数据可视化专家，擅长判断数据是否适合可视化并推荐图表类型。"},
                {"role": "user", "content": prompt}
            ]
            response = await self.llm_service.chat_completion_async(messages=messages)
            
            # 解析JSON响应
            result = self._parse_json_response(response)
            chartable_data = result.get("chartable_data", [])
            
            logger.info(f"--- [SupportingMaterialsAnalyzer]: 识别出{len(chartable_data)}个可可视化数据")
            return chartable_data
            
        except Exception as e:
            logger.warning(f"--- [SupportingMaterialsAnalyzer]: LLM识别失败: {e}")
            return []
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        解析LLM的JSON响应
        
        Args:
            response: LLM响应文本
            
        Returns:
            解析后的JSON字典
        """
        try:
            # 尝试直接解析JSON
            return json.loads(response)
        except json.JSONDecodeError:
            # 尝试提取JSON部分
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                logger.error(f"--- [SupportingMaterialsAnalyzer]: 无法解析JSON响应: {response[:200]}")
                return {}
    
    def _basic_identify_data_points(
        self,
        materials: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        基础识别数据点（Fallback方法）
        
        Args:
            materials: 原始材料列表
            
        Returns:
            基础识别的数据点列表
        """
        data_points = []
        for material in materials:
            data = material.get("data", "")
            # 简单判断类型
            if "%" in data or "％" in data:
                data_type = "percentage"
                unit = "%"
            elif "万" in data:
                data_type = "number"
                unit = "万"
            elif "亿" in data:
                data_type = "number"
                unit = "亿"
            else:
                data_type = "number"
                unit = ""
            
            data_points.append({
                "value": data,
                "type": data_type,
                "unit": unit,
                "label": "",
                "context": material.get("context", ""),
                "significance": "medium",
                "comparison": None,
                "trend": None,
                "slide_index": material.get("slide_index", 0)
            })
        
        return data_points
    
    def _basic_identify_cases(
        self,
        materials: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        基础识别案例（Fallback方法）
        
        Args:
            materials: 原始材料列表
            
        Returns:
            基础识别的案例列表
        """
        cases = []
        for material in materials:
            cases.append({
                "type": "case",
                "company": "",
                "industry": "",
                "challenge": "",
                "solution": "",
                "result": "",
                "key_points": [],
                "significance": "medium",
                "slide_index": material.get("slide_index", 0),
                "content": material.get("content", "")
            })
        
        return cases


```


## File: test_canvas_generator.py

```python
#!/usr/bin/env python3
"""
测试画布生成器
使用Playwright验证HTML渲染效果
"""

import asyncio
from pathlib import Path
from html_canvas_generator import HTMLCanvasGenerator
from loguru import logger


async def test_canvas_generator():
    """测试画布生成器"""
    logger.info("="*80)
    logger.info("测试HTML画布生成器")
    logger.info("="*80)
    
    # 创建画布生成器
    generator = HTMLCanvasGenerator()
    
    # 定义测试元素（使用坐标系：左下角为原点）
    test_elements = [
        {
            'id': 'title-1',
            'type': 'title',
            'content': '技术产品概览与价值主张',
            'coordinates': {
                'left': 100,      # 距离左边缘100px
                'bottom': 900,    # 距离下边缘900px（即距离顶部约80px）
                'width': 800,
                'height': 80
            }
        },
        {
            'id': 'card-1',
            'type': 'card',
            'content': '降低运营成本40-60%',
            'coordinates': {
                'left': 100,
                'bottom': 700,
                'width': 300,
                'height': 150
            }
        },
        {
            'id': 'card-2',
            'type': 'card',
            'content': '提升转化效率20-35%',
            'coordinates': {
                'left': 450,
                'bottom': 700,
                'width': 300,
                'height': 150
            }
        },
        {
            'id': 'card-3',
            'type': 'card',
            'content': '加速业务智能化转型',
            'coordinates': {
                'left': 800,
                'bottom': 700,
                'width': 300,
                'height': 150
            }
        }
    ]
    
    # 生成HTML
    html_content = generator.create_canvas_html(
        elements=test_elements,
        show_grid=True
    )
    
    # 保存HTML文件
    output_file = Path("html_output/test_canvas.html")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html_content, encoding='utf-8')
    logger.info(f"✅ HTML文件已保存: {output_file}")
    
    # 使用Playwright验证渲染效果
    try:
        from playwright.async_api import async_playwright
        
        logger.info("--- 使用Playwright验证HTML渲染...")
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            
            # 加载HTML文件
            html_path = output_file.absolute().as_uri()
            await page.goto(html_path)
            
            # 等待页面加载
            await page.wait_for_load_state('networkidle')
            
            # 获取画布尺寸
            canvas = page.locator('#canvas')
            canvas_box = await canvas.bounding_box()
            logger.info(f"画布尺寸: {canvas_box['width']}px × {canvas_box['height']}px")
            
            # 检查元素位置
            for elem in test_elements:
                elem_id = elem['id']
                elem_locator = page.locator(f'#{elem_id}')
                if await elem_locator.count() > 0:
                    elem_box = await elem_locator.bounding_box()
                    logger.info(f"元素 {elem_id}:")
                    logger.info(f"  位置: left={elem_box['x']:.1f}px, top={elem_box['y']:.1f}px")
                    logger.info(f"  尺寸: width={elem_box['width']:.1f}px, height={elem_box['height']:.1f}px")
                else:
                    logger.warning(f"元素 {elem_id} 未找到")
            
            # 截图
            screenshot_path = Path("html_output/test_canvas_screenshot.png")
            await page.screenshot(path=str(screenshot_path), full_page=True)
            logger.info(f"✅ 截图已保存: {screenshot_path}")
            
            # 保持浏览器打开5秒以便查看
            await asyncio.sleep(5)
            await browser.close()
            
    except ImportError:
        logger.warning("Playwright未安装，跳过渲染验证")
        logger.info("安装命令: pip install playwright && playwright install chromium")
    except Exception as e:
        logger.error(f"Playwright验证失败: {e}", exc_info=True)
    
    logger.info("="*80)
    logger.info("测试完成")
    logger.info("="*80)


if __name__ == "__main__":
    asyncio.run(test_canvas_generator())


```


## File: verify_fixes.py

```python
#!/usr/bin/env python3
"""
验证修复效果的脚本
检查生成的PPT是否符合16:9和Ant Design规范
"""

from pptx import Presentation
from pptx.util import Pt
from pathlib import Path
import glob

def verify_ppt(ppt_path: str):
    """验证PPT文件"""
    print(f"\n{'='*80}")
    print(f"验证文件: {ppt_path}")
    print('='*80)
    
    prs = Presentation(ppt_path)
    
    # 1. 检查尺寸
    print("\n【1. 尺寸检查】")
    width_emu = prs.slide_width
    height_emu = prs.slide_height
    width_cm = float(width_emu) / 360000
    height_cm = float(height_emu) / 360000
    ratio = width_cm / height_cm
    is_16_9 = abs(ratio - 16/9) < 0.1
    
    print(f"  宽度: {width_cm:.2f}cm ({width_emu:,} EMU)")
    print(f"  高度: {height_cm:.2f}cm ({height_emu:,} EMU)")
    print(f"  宽高比: {ratio:.2f} (16:9={16/9:.2f})")
    print(f"  {'✅' if is_16_9 else '❌'} 是否为16:9: {is_16_9}")
    
    # 2. 检查设计规范
    print("\n【2. 设计规范检查】")
    if prs.slides:
        slide = prs.slides[0]
        placeholder_count = 0
        
        for shape in slide.shapes:
            if shape.is_placeholder and hasattr(shape, 'text_frame'):
                placeholder_count += 1
                print(f"\n  占位符 {placeholder_count}:")
                
                if shape.text_frame.paragraphs:
                    para = shape.text_frame.paragraphs[0]
                    if para.runs:
                        font = para.runs[0].font
                        
                        # 字体
                        font_name = font.name or "未设置"
                        print(f"    字体: {font_name}")
                        
                        # 字号（EMU转pt）
                        if font.size:
                            size_pt = float(font.size) / 12700
                            print(f"    字号: {size_pt:.0f}pt (EMU: {font.size:,})")
                            
                            # 验证字号是否符合规范
                            if placeholder_count == 1:
                                # 第一个占位符应该是标题（38pt）
                                is_correct = abs(size_pt - 38) < 1
                                print(f"    {'✅' if is_correct else '❌'} 标题字号检查: {is_correct} (期望38pt)")
                            else:
                                # 其他占位符应该是正文（14pt）
                                is_correct = abs(size_pt - 14) < 1
                                print(f"    {'✅' if is_correct else '❌'} 正文字号检查: {is_correct} (期望14pt)")
                        else:
                            print(f"    ❌ 字号: 未设置")
                        
                        # 加粗
                        print(f"    加粗: {font.bold}")
                        
                        # 颜色
                        if font.color and font.color.rgb:
                            rgb = font.color.rgb
                            # RGBColor对象可以转换为整数
                            try:
                                if hasattr(rgb, '__int__'):
                                    rgb_int = int(rgb)
                                    r = (rgb_int >> 16) & 0xFF
                                    g = (rgb_int >> 8) & 0xFF
                                    b = rgb_int & 0xFF
                                elif isinstance(rgb, int):
                                    r = (rgb >> 16) & 0xFF
                                    g = (rgb >> 8) & 0xFF
                                    b = rgb & 0xFF
                                else:
                                    # 尝试从字符串解析（格式可能是"262626"）
                                    rgb_str = str(rgb)
                                    if len(rgb_str) == 6 and rgb_str.isdigit():
                                        # 直接是hex字符串
                                        r = int(rgb_str[0:2], 16)
                                        g = int(rgb_str[2:4], 16)
                                        b = int(rgb_str[4:6], 16)
                                    else:
                                        r, g, b = 0, 0, 0
                            except Exception as e:
                                print(f"    颜色解析错误: {e}")
                                r, g, b = 0, 0, 0
                            
                            hex_color = f"#{r:02x}{g:02x}{b:02x}"
                            print(f"    颜色: RGB({r}, {g}, {b}) = {hex_color}")
                            
                            # 验证颜色是否符合规范（#262626）
                            expected_rgb = (38, 38, 38)
                            is_correct = (r, g, b) == expected_rgb
                            print(f"    {'✅' if is_correct else '❌'} 颜色检查: {is_correct} (期望#262626)")
                        else:
                            print(f"    ❌ 颜色: 未设置")
    
    # 3. 总结
    print("\n【3. 验证总结】")
    all_checks = [
        ("16:9尺寸", is_16_9),
    ]
    
    for check_name, check_result in all_checks:
        status = "✅ 通过" if check_result else "❌ 失败"
        print(f"  {check_name}: {status}")
    
    return is_16_9


if __name__ == "__main__":
    # 查找最新生成的PPT文件
    files = sorted(glob.glob('demo_filled-filled-*.pptx'))
    
    if not files:
        print("未找到生成的PPT文件")
        print("请先运行: python test_demo_framework.py")
    else:
        print(f"找到 {len(files)} 个生成的PPT文件")
        print("验证最新的文件...")
        
        latest = files[-1]
        verify_ppt(latest)
        
        print("\n" + "="*80)
        print("验证完成！")
        print("="*80)


```


## File: vinci_integration.py

```python
"""
图表生成集成模块（独立版本）
使用独立的ChartGenerator替代Vinci
"""

from pathlib import Path
from typing import Any, Optional

from loguru import logger

from chart_generator import ChartGenerator


class VinciIntegration:
    """
    图表生成集成类（独立版本）
    使用ChartGenerator生成图表，不依赖BeeWise项目
    """

    def __init__(self, chart_generator: Optional[ChartGenerator] = None, output_dir: Optional[Path] = None):
        """
        初始化图表生成集成
        
        Args:
            chart_generator: ChartGenerator实例，如果为None则创建新实例
            output_dir: 图表输出目录
        """
        if chart_generator is None:
            self._chart_generator = ChartGenerator(output_dir=output_dir)
        else:
            self._chart_generator = chart_generator
        
        logger.info("--- [VinciIntegration]: Initialized with ChartGenerator (standalone)")

    async def generate_chart_from_insight(
        self,
        insight_details: dict[str, Any],
        project_id: str = "fixer"
    ) -> dict[str, Any]:
        """
        从数据洞察生成图表
        
        Args:
            insight_details: 数据洞察字典，包含：
                - insightId 或 insight_id: 洞察ID
                - type: 图表类型（如 'bar_chart', 'pie_chart', 'line_chart', 'grouped_bar_chart'）
                - title: 图表标题
                - data: 数据列表
            project_id: 项目ID，用于组织输出目录
            
        Returns:
            包含 'chart_image_path' 和 'insight_id' 的字典，失败时包含 'error'
        """
        return self._chart_generator.generate_chart_from_insight(insight_details, project_id)

    async def generate_charts_from_insights(
        self,
        insights: list[dict[str, Any]],
        project_id: str = "fixer"
    ) -> dict[str, str]:
        """
        批量生成图表
        
        Args:
            insights: 数据洞察列表
            project_id: 项目ID
            
        Returns:
            图表路径映射字典，键是insight_id，值是图表路径
        """
        return await self._chart_generator.generate_charts_from_insights(insights, project_id)


def create_vinci_integration(
    chart_generator: Optional[ChartGenerator] = None,
    output_dir: Optional[Path] = None
) -> Optional[VinciIntegration]:
    """
    创建图表生成集成实例
    
    Args:
        chart_generator: ChartGenerator实例
        output_dir: 图表输出目录
        
    Returns:
        VinciIntegration实例
    """
    try:
        return VinciIntegration(chart_generator=chart_generator, output_dir=output_dir)
    except Exception as e:
        logger.error(f"--- [VinciIntegration] Failed to create integration: {e}", exc_info=True)
        return None

```


## File: web_chart_generator.py

```python
"""
基于无头浏览器的图表生成器
使用Playwright + AntV G2Plot渲染真实的web图表
"""

import json
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
from loguru import logger

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not installed. Install with: pip install playwright && playwright install chromium")

from ant_design_theme import ant_design_theme
from antv_chart_theme import antv_chart_theme


class WebChartGenerator:
    """
    基于无头浏览器的图表生成器
    使用Playwright渲染AntV G2Plot图表
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        初始化Web图表生成器
        
        Args:
            output_dir: 图表输出目录
        """
        if output_dir is None:
            output_dir = Path.cwd() / "charts"
        elif isinstance(output_dir, str):
            output_dir = Path(output_dir)
        
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True, parents=True)
        logger.info(f"--- [WebChartGenerator]: Output directory: {self.output_dir}")
        
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright is required for WebChartGenerator. "
                "Install with: pip install playwright && playwright install chromium"
            )
    
    def _generate_html_template(
        self,
        chart_type: str,
        data: List[Dict[str, Any]],
        config: Dict[str, Any]
    ) -> str:
        """
        生成包含AntV G2Plot图表的HTML模板
        
        Args:
            chart_type: 图表类型 (bar, line, pie, column)
            data: 数据列表
            config: 图表配置
            
        Returns:
            HTML字符串
        """
        # 转换数据为JavaScript格式
        data_json = json.dumps(data, ensure_ascii=False, indent=2)
        
        # 获取Ant Design/AntV配色
        colors = antv_chart_theme.get_default_colors()
        colors_json = json.dumps(colors)
        
        # 图表配置
        title = config.get('title', 'Chart')
        width = config.get('width', 800)
        height = config.get('height', 500)
        
        # 根据图表类型生成不同的G2Plot配置
        chart_config_js = self._generate_chart_config(chart_type, config)
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: {ant_design_theme.typography.fontFamily};
            background-color: {ant_design_theme.colors.colorBgBase};
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        #container {{
            width: {width}px;
            height: {height}px;
            background-color: {ant_design_theme.colors.colorBgContainer};
            border-radius: {ant_design_theme.borderRadius.borderRadius}px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            padding: 20px;
        }}
        .chart-title {{
            font-size: {ant_design_theme.typography.fontSizeLG}px;
            font-weight: {ant_design_theme.typography.fontWeightStrong};
            color: {ant_design_theme.colors.colorText};
            margin-bottom: 16px;
            text-align: center;
        }}
        #chart {{
            width: 100%;
            height: calc(100% - 50px);
        }}
    </style>
</head>
<body>
    <div id="container">
        <div class="chart-title">{title}</div>
        <div id="chart"></div>
    </div>
    
    <!-- AntV G2Plot CDN -->
    <script src="https://unpkg.com/@antv/g2plot@latest/dist/g2plot.min.js"></script>
    <script>
        const data = {data_json};
        const colors = {colors_json};
        
        // 图表配置
        const chartConfig = {{
            container: 'chart',
            data: data,
            {chart_config_js}
            theme: {{
                defaultColor: '{ant_design_theme.colors.colorPrimary}',
                styleSheet: {{
                    fontFamily: '{ant_design_theme.typography.fontFamily}',
                    fontSize: {ant_design_theme.typography.fontSize}
                }}
            }}
        }};
        
        // 创建图表
        let plot;
        const chartType = '{chart_type}';
        
        if (chartType === 'bar' || chartType === 'bar_chart') {{
            const {{ Bar }} = G2Plot;
            plot = new Bar(chartConfig);
        }} else if (chartType === 'line' || chartType === 'line_chart') {{
            const {{ Line }} = G2Plot;
            plot = new Line(chartConfig);
        }} else if (chartType === 'pie' || chartType === 'pie_chart') {{
            const {{ Pie }} = G2Plot;
            plot = new Pie(chartConfig);
        }} else if (chartType === 'column' || chartType === 'column_chart') {{
            const {{ Column }} = G2Plot;
            plot = new Column(chartConfig);
        }} else {{
            // 默认使用Bar
            const {{ Bar }} = G2Plot;
            plot = new Bar(chartConfig);
        }}
        
        plot.render();
        
        // 等待图表渲染完成
        setTimeout(() => {{
            console.log('Chart rendered');
        }}, 1000);
    </script>
</body>
</html>"""
        return html
    
    def _generate_chart_config(self, chart_type: str, config: Dict[str, Any]) -> str:
        """
        生成G2Plot图表配置的JavaScript代码
        
        Args:
            chart_type: 图表类型
            config: 配置字典
            
        Returns:
            JavaScript配置代码字符串
        """
        x_key = config.get('x_key', 'x')
        y_key = config.get('y_key', 'y')
        label_key = config.get('label_key', 'label')
        value_key = config.get('value_key', 'value')
        
        if chart_type in ['pie', 'pie_chart']:
            # 饼图配置
            return f"""
            angleField: '{value_key}',
            colorField: '{label_key}',
            color: colors,
            label: {{
                type: 'outer',
                content: '{{name}}: {{percentage}}'
            }},
            interactions: [{{ type: 'element-active' }}],
            """
        elif chart_type in ['bar', 'bar_chart', 'column', 'column_chart']:
            # 柱状图配置
            return f"""
            xField: '{x_key}',
            yField: '{y_key}',
            color: '{ant_design_theme.colors.colorPrimary}',
            label: {{
                position: 'top',
                style: {{
                    fill: '{ant_design_theme.colors.colorText}',
                    fontSize: {ant_design_theme.typography.fontSizeSM}
                }}
            }},
            """
        elif chart_type in ['line', 'line_chart']:
            # 折线图配置
            return f"""
            xField: '{x_key}',
            yField: '{y_key}',
            color: '{ant_design_theme.colors.colorPrimary}',
            point: {{
                size: 4,
                shape: 'circle',
                style: {{
                    fill: '{ant_design_theme.colors.colorPrimary}',
                    stroke: '{ant_design_theme.colors.colorBgBase}',
                    lineWidth: 2
                }}
            }},
            smooth: true,
            """
        else:
            # 默认配置
            return f"""
            xField: '{x_key}',
            yField: '{y_key}',
            color: '{ant_design_theme.colors.colorPrimary}',
            """
    
    async def _render_chart(
        self,
        html_content: str,
        output_path: Path,
        width: int = 800,
        height: int = 500
    ) -> str:
        """
        使用Playwright渲染HTML并截图
        
        Args:
            html_content: HTML内容
            output_path: 输出文件路径
            width: 视口宽度
            height: 视口高度
            
        Returns:
            保存的文件路径
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(
                viewport={'width': width + 40, 'height': height + 100}  # 留出padding
            )
            
            # 加载HTML内容
            await page.set_content(html_content, wait_until='networkidle')
            
            # 等待图表渲染（G2Plot需要时间渲染）
            await page.wait_for_timeout(2000)  # 等待2秒确保图表完全渲染
            
            # 截图
            await page.screenshot(
                path=str(output_path),
                full_page=False,
                clip={'x': 0, 'y': 0, 'width': width + 40, 'height': height + 100}
            )
            
            await browser.close()
        
        logger.info(f"--- [WebChartGenerator]: Chart saved to {output_path}")
        return str(output_path)
    
    async def generate_bar_chart_async(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Bar Chart",
        width: int = 800,
        height: int = 500
    ) -> str:
        """
        异步生成柱状图
        
        Args:
            data: 数据列表
            x_key: X轴数据键名
            y_key: Y轴数据键名
            title: 图表标题
            width: 图表宽度
            height: 图表高度
            
        Returns:
            保存的图表文件路径
        """
        config = {
            'title': title,
            'width': width,
            'height': height,
            'x_key': x_key,
            'y_key': y_key
        }
        
        html = self._generate_html_template('bar', data, config)
        filename = f"web_bar_chart_{title.replace(' ', '_')}.png"
        output_path = self.output_dir / filename
        
        return await self._render_chart(html, output_path, width, height)
    
    async def generate_line_chart_async(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Line Chart",
        width: int = 800,
        height: int = 500
    ) -> str:
        """
        异步生成折线图
        """
        config = {
            'title': title,
            'width': width,
            'height': height,
            'x_key': x_key,
            'y_key': y_key
        }
        
        html = self._generate_html_template('line', data, config)
        filename = f"web_line_chart_{title.replace(' ', '_')}.png"
        output_path = self.output_dir / filename
        
        return await self._render_chart(html, output_path, width, height)
    
    async def generate_pie_chart_async(
        self,
        data: List[Dict[str, Any]],
        label_key: str,
        value_key: str,
        title: str = "Pie Chart",
        width: int = 800,
        height: int = 500
    ) -> str:
        """
        异步生成饼图
        """
        config = {
            'title': title,
            'width': width,
            'height': height,
            'label_key': label_key,
            'value_key': value_key
        }
        
        html = self._generate_html_template('pie', data, config)
        filename = f"web_pie_chart_{title.replace(' ', '_')}.png"
        output_path = self.output_dir / filename
        
        return await self._render_chart(html, output_path, width, height)
    
    # 同步包装方法
    def generate_bar_chart(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Bar Chart",
        width: int = 800,
        height: int = 500
    ) -> str:
        """同步生成柱状图"""
        return asyncio.run(self.generate_bar_chart_async(data, x_key, y_key, title, width, height))
    
    def generate_line_chart(
        self,
        data: List[Dict[str, Any]],
        x_key: str,
        y_key: str,
        title: str = "Line Chart",
        width: int = 800,
        height: int = 500
    ) -> str:
        """同步生成折线图"""
        return asyncio.run(self.generate_line_chart_async(data, x_key, y_key, title, width, height))
    
    def generate_pie_chart(
        self,
        data: List[Dict[str, Any]],
        label_key: str,
        value_key: str,
        title: str = "Pie Chart",
        width: int = 800,
        height: int = 500
    ) -> str:
        """同步生成饼图"""
        return asyncio.run(self.generate_pie_chart_async(data, label_key, value_key, title, width, height))


```


## File: tests/test_browser_rendering_output.py

```python
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


```


## File: tests/test_browser_to_ppt_replicator.py

```python
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


```


## File: tests/test_demo_framework.py

```python
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


```


## File: tests/test_docx_to_ppt_full_flow.py

```python
#!/usr/bin/env python3
"""
完整流程测试：从Demo文档.docx生成PPT
使用Demo文档.docx的内容作为PPT的主要内容，运行完整流程
带详细探针和日志分析
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from loguru import logger
from docx import Document

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from ppt_filler import PPTFiller

# 配置日志系统
def setup_logging(log_file: str):
    """配置日志系统，同时输出到控制台和文件"""
    logger.remove()  # 移除默认处理器
    
    # 控制台输出（带颜色）
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="INFO"
    )
    
    # 文件输出（详细格式）
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="100 MB",
        retention="10 days"
    )
    
    return logger

def extract_docx_content(docx_path: str) -> Dict[str, Any]:
    """从docx文件中提取文本内容（详细探针）"""
    doc = Document(docx_path)
    content_parts = []
    detailed_info = {
        "paragraphs": [],
        "tables": [],
        "structure": []
    }
    
    print(f"\n{'='*80}")
    print("【详细探针】docx内容提取过程")
    print("="*80)
    
    # 提取段落
    print(f"\n📝 段落提取（共{len(doc.paragraphs)}个段落）:")
    for idx, para in enumerate(doc.paragraphs):
        para_text = para.text.strip()
        if para_text:
            style_name = para.style.name if para.style else "无样式"
            is_bold = any(run.bold for run in para.runs if run.bold)
            font_size = None
            for run in para.runs:
                if run.font.size:
                    font_size = run.font.size.pt
                    break
            
            para_info = {
                "index": idx,
                "text": para_text,
                "style": style_name,
                "is_bold": is_bold,
                "font_size": font_size,
                "length": len(para_text)
            }
            detailed_info["paragraphs"].append(para_info)
            
            print(f"   段落{idx}:")
            print(f"     文本: {para_text[:100]}{'...' if len(para_text) > 100 else ''}")
            print(f"     样式: {style_name}")
            print(f"     加粗: {is_bold}")
            print(f"     字号: {font_size}pt" if font_size else "     字号: 默认")
            print(f"     长度: {len(para_text)}字符")
            
            content_parts.append(para_text)
    
    # 提取表格
    print(f"\n📊 表格提取（共{len(doc.tables)}个表格）:")
    for idx, table in enumerate(doc.tables):
        table_rows = []
        table_info = {
            "index": idx,
            "rows": [],
            "columns": len(table.columns) if table.rows else 0
        }
        
        for row_idx, row in enumerate(table.rows):
            row_cells = []
            for cell in row.cells:
                cell_text = cell.text.strip()
                row_cells.append(cell_text)
            
            if any(cell for cell in row_cells):
                table_rows.append(" | ".join(row_cells))
                table_info["rows"].append({
                    "row_index": row_idx,
                    "cells": row_cells
                })
        
        if table_rows:
            table_content = "\n".join(table_rows)
            content_parts.append(table_content)
            detailed_info["tables"].append(table_info)
            
            print(f"   表格{idx}:")
            print(f"     行数: {len(table_info['rows'])}")
            print(f"     列数: {table_info['columns']}")
            print(f"     内容预览: {table_content[:200]}{'...' if len(table_content) > 200 else ''}")
    
    # 分析结构
    print(f"\n🔍 结构分析:")
    print(f"   总段落数: {len(detailed_info['paragraphs'])}")
    print(f"   总表格数: {len(detailed_info['tables'])}")
    print(f"   总内容块数: {len(content_parts)}")
    
    # 识别可能的标题和正文
    titles = []
    bodies = []
    for para_info in detailed_info["paragraphs"]:
        if para_info["is_bold"] or para_info["font_size"] and para_info["font_size"] > 12:
            titles.append(para_info)
        else:
            bodies.append(para_info)
    
    print(f"   可能的标题段落: {len(titles)}")
    print(f"   可能的正文段落: {len(bodies)}")
    
    detailed_info["structure"] = {
        "total_paragraphs": len(detailed_info["paragraphs"]),
        "total_tables": len(detailed_info["tables"]),
        "title_paragraphs": len(titles),
        "body_paragraphs": len(bodies)
    }
    
    return {
        "content": "\n\n".join(content_parts),
        "detailed_info": detailed_info
    }

async def test_docx_to_ppt_full_flow():
    """完整流程测试：从docx到PPT（带详细探针）"""
    
    print("\n" + "="*80)
    print("完整流程测试：从Demo文档.docx生成PPT（带详细探针）")
    print("="*80)
    
    # ========== 探针1: 文件检查 ==========
    print("\n" + "="*80)
    print("【探针1】文件检查")
    print("="*80)
    docx_path = Path("Demo文档.docx")
    framework_ppt = Path("demo_filled.pptx")
    
    if not docx_path.exists():
        print(f"❌ 未找到文件: {docx_path}")
        return
    print(f"✅ docx文件存在: {docx_path} ({docx_path.stat().st_size:,} bytes)")
    
    if not framework_ppt.exists():
        print(f"❌ 未找到框架PPT: {framework_ppt}")
        print("   将创建一个新的16:9框架PPT...")
        from create_framework_ppt import create_framework_ppt
        framework_ppt_str = create_framework_ppt()
        framework_ppt = Path(framework_ppt_str)
    print(f"✅ 框架PPT存在: {framework_ppt} ({framework_ppt.stat().st_size:,} bytes)")
    
    # 检查框架PPT的幻灯片数
    from pptx import Presentation
    prs = Presentation(str(framework_ppt))
    print(f"📊 框架PPT信息:")
    print(f"   幻灯片数: {len(prs.slides)}")
    total_placeholders = 0
    for i, slide in enumerate(prs.slides):
        placeholders = [s for s in slide.shapes if s.is_placeholder]
        total_placeholders += len(placeholders)
        print(f"   幻灯片{i}: {len(placeholders)}个占位符")
    print(f"   总占位符数: {total_placeholders}")
    
    # ========== 探针2: 提取docx内容（详细） ==========
    docx_result = extract_docx_content(str(docx_path))
    docx_content = docx_result["content"]
    docx_detailed = docx_result["detailed_info"]
    
    print(f"\n✅ 提取完成")
    print(f"   内容长度: {len(docx_content)} 字符")
    print(f"   段落数: {docx_detailed['structure']['total_paragraphs']}")
    print(f"   表格数: {docx_detailed['structure']['total_tables']}")
    print(f"   内容预览: {docx_content[:200]}...")
    
    # ========== 探针3: 初始化PPT填充器 ==========
    print("\n" + "="*80)
    print("【探针3】初始化PPT填充器（浏览器渲染模式）")
    print("="*80)
    filler = PPTFiller(
        str(framework_ppt),
        use_browser_rendering=True
    )
    print(f"✅ PPT填充器初始化完成")
    print(f"   框架路径: {filler.framework_path}")
    print(f"   浏览器渲染: {filler.use_browser_rendering}")
    print(f"   LLM服务: {'已初始化' if filler.llm_service else '未初始化'}")
    
    # ========== 探针4: 构建用户提示词 ==========
    print("\n" + "="*80)
    print("【探针4】构建生成提示词")
    print("="*80)
    user_prompt = f"""
基于以下文档内容，生成一份完整的PPT演示文稿：

【文档内容】
{docx_content}

【生成要求】
1. 保持文档的核心思想和主要观点
2. 将内容组织成清晰的板块结构
3. 突出关键数据和案例
4. 符合中国商业汇报习惯
5. 使用专业、正式的表达风格
6. 确保内容完整、逻辑清晰
7. 为所有幻灯片生成内容（框架PPT有{len(prs.slides)}张幻灯片）
"""
    print(f"✅ 提示词构建完成")
    print(f"   提示词长度: {len(user_prompt)} 字符")
    print(f"   包含docx内容: {len(docx_content)} 字符")
    
    # ========== 探针5: 执行完整流程 ==========
    print("\n" + "="*80)
    print("【探针5】执行完整流程：生成PPT")
    print("="*80)
    print("   这将执行以下完整流程：")
    print("   1. 提取框架结构（增强解析）")
    print("   2. 人类中心化分析（6层分析）")
    print("   3. 内容生成策略制定")
    print("   4. 智能识别支撑材料（数据点、案例）")
    print("   5. 逐板块内容生成（整合支撑材料）")
    print("     5.1 内容润色（ContentPolisher）")
    print("     5.2 展示策划（PresentationPlanner）")
    print("     5.3 布局规划（LayoutPlanner）【新增】")
    print("   6. HTML生成（基于布局规划，Ant Design规范 + 24栅格系统）【新增】")
    print("   7. 浏览器渲染（Playwright）")
    print("   8. 元素分析和提取（容器、文本）")
    print("   9. 复刻到PPT（坐标映射、24栅格系统）")
    print("   10. 图表生成和整合（如果有数据）")
    print("   11. 最终PPT保存")
    print("")
    
    # 保存日志到文件
    log_file = f"docx_to_ppt_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    print(f"📝 详细日志将保存到: {log_file}")
    print("")
    
    # 配置日志系统
    setup_logging(log_file)
    logger.info("="*80)
    logger.info("开始完整流程测试")
    logger.info("="*80)
    
    # 【探针】记录关键参数
    logger.info(f"【探针】测试参数:")
    logger.info(f"  - docx文件: {docx_path}")
    logger.info(f"  - 框架PPT: {framework_ppt}")
    logger.info(f"  - 提示词长度: {len(user_prompt)} 字符")
    logger.info(f"  - docx内容长度: {len(docx_content)} 字符")
    logger.info(f"  - 使用增强分析: True")
    logger.info(f"  - 使用浏览器渲染: {filler.use_browser_rendering}")
    logger.info(f"  - LLM服务: {'已初始化' if filler.llm_service else '未初始化'}")
    
    # 检查LLM服务
    if not filler.llm_service:
        logger.error("❌ LLM服务未初始化，无法继续测试")
        print("\n❌ 错误: LLM服务未初始化")
        print("   请确保设置了环境变量: CHAT_MODEL_API_KEY 或 OPENAI_API_KEY")
        return
    
    # 【新增】跳过PPT转换，仅生成HTML
    skip_ppt = True  # 设置为True以跳过HTML到PPT的转换，仅生成HTML文件
    logger.info(f"  - 跳过PPT转换: {skip_ppt} (仅生成HTML)")
    
    output_path = await filler.fill_from_prompt(
        user_prompt,
        output_path="docx_to_ppt_output.pptx",
        use_enhanced_analysis=True,  # 使用增强分析（人类中心化）
        skip_ppt_conversion=skip_ppt  # 跳过HTML到PPT的转换
    )
    
    logger.info("="*80)
    logger.info("完整流程执行完成")
    logger.info("="*80)
    
    # ========== 探针6: 验证输出结果 ==========
    print("\n" + "="*80)
    print("【探针6】验证输出结果")
    print("="*80)
    output_path_obj = Path(output_path)
    
    # 【新增】如果跳过PPT转换，验证HTML文件
    if skip_ppt:
        if output_path_obj.exists() and output_path_obj.is_dir():
            html_files = sorted(output_path_obj.glob("*.html"))
            print(f"✅ HTML输出目录存在: {output_path}")
            print(f"   HTML文件数量: {len(html_files)}")
            for html_file in html_files:
                file_size = html_file.stat().st_size
                print(f"   - {html_file.name}: {file_size:,} bytes ({file_size/1024:.2f} KB)")
            print(f"\n💡 提示: 请打开HTML文件查看效果（在浏览器中打开）")
        else:
            print(f"❌ HTML输出目录不存在: {output_path}")
    else:
        # 验证PPT内容
        if output_path_obj.exists() and output_path_obj.is_file():
            file_size = output_path_obj.stat().st_size
            print(f"✅ 输出文件存在: {output_path}")
            print(f"   文件大小: {file_size:,} bytes ({file_size/1024:.2f} KB)")
            
            # 验证PPT内容
            output_prs = Presentation(str(output_path))
            print(f"📊 输出PPT信息:")
            print(f"   幻灯片数: {len(output_prs.slides)}")
            print(f"   尺寸: {output_prs.slide_width/360000:.2f}cm × {output_prs.slide_height/360000:.2f}cm")
            print(f"   宽高比: {(output_prs.slide_width/output_prs.slide_height):.2f} (16:9 = {16/9:.2f})")
            
            # 检查每张幻灯片的内容
            for i, slide in enumerate(output_prs.slides):
                text_shapes = [s for s in slide.shapes if hasattr(s, 'text') and s.text.strip()]
                image_shapes = [s for s in slide.shapes if hasattr(s, 'image')]
                print(f"   幻灯片{i}:")
                print(f"     文本形状: {len(text_shapes)}")
                print(f"     图片形状: {len(image_shapes)}")
                if text_shapes:
                    print(f"     文本预览: {text_shapes[0].text[:50]}...")
        else:
            print(f"❌ 输出文件不存在: {output_path}")
    
    # ========== 探针7: 分析日志 ==========
    print("\n" + "="*80)
    print("【探针7】分析详细日志")
    print("="*80)
    analyze_log_file(log_file)
    
    # ========== 最终总结 ==========
    print("\n" + "="*80)
    print("✅ 完整流程测试完成！")
    print("="*80)
    print(f"\n📁 输出文件: {output_path}")
    print(f"📝 详细日志: {log_file}")
    
    print("\n" + "="*80)
    print("💡 提示: 请打开生成的PPT文件查看效果")
    print("="*80)

def analyze_log_file(log_file: str):
    """分析日志文件，提取关键信息"""
    log_path = Path(log_file)
    if not log_path.exists():
        print(f"❌ 日志文件不存在: {log_file}")
        return
    
    print(f"📊 分析日志文件: {log_file}")
    print(f"   文件大小: {log_path.stat().st_size:,} bytes")
    
    # 读取日志内容
    with open(log_file, 'r', encoding='utf-8') as f:
        log_lines = f.readlines()
    
    print(f"   总行数: {len(log_lines)}")
    
    # 分析关键阶段
    stages = {
        "人类中心化分析": 0,
        "内容生成策略": 0,
        "支撑材料识别": 0,
        "内容润色": 0,
        "展示策划": 0,
        "布局规划": 0,
        "HTML生成": 0,
        "浏览器渲染": 0,
        "PPT复刻": 0,
        "错误": 0,
        "警告": 0
    }
    
    # 统计各阶段出现次数
    for line in log_lines:
        line_lower = line.lower()
        if "人类中心化分析" in line or "human-centered" in line_lower:
            stages["人类中心化分析"] += 1
        if "内容生成策略" in line or "content strategy" in line_lower:
            stages["内容生成策略"] += 1
        if "支撑材料" in line or "supporting materials" in line_lower:
            stages["支撑材料识别"] += 1
        if "内容润色" in line or "polish" in line_lower or "润色" in line:
            stages["内容润色"] += 1
        if "展示策划" in line or "presentation plan" in line_lower or "展示策划" in line:
            stages["展示策划"] += 1
        if "布局规划" in line or "layout plan" in line_lower or "布局规划" in line:
            stages["布局规划"] += 1
        if "html生成" in line or "generate.*html" in line_lower or "generate_from_layout_plan" in line:
            stages["HTML生成"] += 1
        if "浏览器渲染" in line or "browser render" in line_lower:
            stages["浏览器渲染"] += 1
        if "复刻" in line or "replicate" in line_lower:
            stages["PPT复刻"] += 1
        if "error" in line_lower or "❌" in line or "失败" in line:
            stages["错误"] += 1
        if "warning" in line_lower or "⚠️" in line or "警告" in line:
            stages["警告"] += 1
    
    print(f"\n📈 各阶段统计:")
    for stage, count in stages.items():
        if count > 0:
            print(f"   {stage}: {count} 次")
    
    # 查找关键信息
    print(f"\n🔍 关键信息提取:")
    
    # 查找润色结果
    polished_count = 0
    for i, line in enumerate(log_lines):
        if "润色完成" in line or "polish.*完成" in line.lower():
            polished_count += 1
            if polished_count <= 3:  # 只显示前3个
                print(f"   ✅ 润色完成: {line.strip()}")
    
    # 查找布局规划结果
    layout_count = 0
    for i, line in enumerate(log_lines):
        if "布局规划完成" in line or "layout.*plan.*完成" in line.lower():
            layout_count += 1
            if layout_count <= 3:  # 只显示前3个
                print(f"   ✅ 布局规划完成: {line.strip()}")
    
    # 查找HTML生成方式
    html_method = None
    for line in log_lines:
        if "使用布局规划生成HTML" in line:
            html_method = "布局规划方式"
            break
        elif "使用内容映射生成HTML" in line:
            html_method = "内容映射方式"
            break
    
    if html_method:
        print(f"   📄 HTML生成方式: {html_method}")
    
    # 查找错误和警告
    errors = []
    warnings = []
    for i, line in enumerate(log_lines):
        if "error" in line.lower() or "❌" in line or "失败" in line:
            errors.append((i+1, line.strip()[:100]))
        if "warning" in line.lower() or "⚠️" in line or "警告" in line:
            warnings.append((i+1, line.strip()[:100]))
    
    if errors:
        print(f"\n❌ 发现 {len(errors)} 个错误:")
        for line_num, error_msg in errors[:5]:  # 只显示前5个
            print(f"   行{line_num}: {error_msg}")
    
    if warnings:
        print(f"\n⚠️ 发现 {len(warnings)} 个警告:")
        for line_num, warn_msg in warnings[:5]:  # 只显示前5个
            print(f"   行{line_num}: {warn_msg}")
    
    if not errors and not warnings:
        print(f"\n✅ 未发现错误或警告")

if __name__ == "__main__":
    asyncio.run(test_docx_to_ppt_full_flow())


```


## File: tests/test_fixer.py

```python
#!/usr/bin/env python3
"""
Fixer 测试脚本
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
                "title": "Fixer 测试演示",
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
    print("Fixer 测试套件")
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


```


## File: tests/test_llm_understand_demo_docx.py

```python
"""
测试LLM理解Demo文档.docx
使用新的简化prompt（只有背景和方向，没有强制限定）
"""

import asyncio
from pathlib import Path
from loguru import logger
import json

from llm_service import LLMService
from human_centered_analyzer import HumanCenteredAnalyzer
from enhanced_ppt_parser import EnhancedPPTParser


def extract_docx_content(docx_path: str) -> str:
    """从docx文件中提取文本内容"""
    try:
        from docx import Document
        
        doc = Document(docx_path)
        paragraphs = []
        
        # 提取段落文本
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                paragraphs.append(text)
        
        # 提取表格文本
        for table in doc.tables:
            for row in table.rows:
                row_texts = []
                for cell in row.cells:
                    cell_text = cell.text.strip()
                    if cell_text:
                        row_texts.append(cell_text)
                if row_texts:
                    paragraphs.append(" | ".join(row_texts))
        
        return "\n".join(paragraphs)
    except ImportError:
        logger.error("需要安装python-docx: pip install python-docx")
        return ""
    except Exception as e:
        logger.error(f"读取docx文件失败: {e}")
        return ""


async def test_llm_understand_demo_docx():
    """测试LLM理解Demo文档.docx"""
    logger.info("="*80)
    logger.info("测试：LLM理解Demo文档.docx（使用新的简化prompt）")
    logger.info("="*80)
    
    # 1. 读取Demo文档.docx
    docx_path = Path("Demo文档.docx")
    if not docx_path.exists():
        logger.error(f"文件不存在: {docx_path}")
        return
    
    logger.info(f"📄 读取文件: {docx_path}")
    docx_content = extract_docx_content(str(docx_path))
    logger.info(f"   文档长度: {len(docx_content)}字符")
    logger.info(f"   文档预览: {docx_content[:500]}...")
    
    # 2. 创建结构数据（用于HumanCenteredAnalyzer）
    # 使用一个简单的框架PPT结构作为基础
    framework_path = Path("demo_filled.pptx")
    if framework_path.exists():
        parser = EnhancedPPTParser(str(framework_path))
        framework_structure = parser.extract_structure_enhanced()
    else:
        # 如果没有框架PPT，创建一个基本结构
        framework_structure = {
            "slide_count": 1,
            "slide_width": 33.867,
            "slide_height": 19.05,
            "slides": [{
                "slide_index": 0,
                "shapes": [],
                "placeholders": []
            }]
        }
    
    # 3. 创建docx结构（模拟PPT结构，但使用docx内容）
    docx_structure = {
        "slide_count": 1,
        "slide_width": 33.867,
        "slide_height": 19.05,
        "slides": [{
            "slide_index": 0,
            "shapes": [{
                "shape_id": i,
                "text": para,
                "format": {}
            } for i, para in enumerate(docx_content.split('\n') if docx_content else [])],
            "placeholders": []
        }]
    }
    
    # 4. 初始化LLM服务和HumanCenteredAnalyzer
    logger.info("🤖 初始化LLM服务...")
    llm_service = LLMService()
    
    logger.info("📊 初始化HumanCenteredAnalyzer...")
    analyzer = HumanCenteredAnalyzer(
        structure_data=docx_structure,
        raw_text=docx_content,
        llm_service=llm_service
    )
    
    # 5. 执行分析
    logger.info("🔍 开始LLM理解分析...")
    logger.info("   使用新的简化prompt：")
    logger.info("   - 背景：中国职场的述职汇报专家，专门为副总裁级别的职场高管筹备述职内容")
    logger.info("   - 方向：先通读了解核心思想 → 再细分板块拆解 → 然后深入探寻每个板块")
    logger.info("")
    
    try:
        human_analysis = await analyzer.analyze_all()
        
        # 6. 输出分析结果到文档
        output_path = Path("LLM_理解_Demo文档_分析结果.md")
        logger.info(f"📝 输出分析结果到: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# LLM理解Demo文档.docx - 分析结果\n\n")
            f.write("## 📋 说明\n\n")
            f.write("本文档是使用新的简化prompt（只有背景和方向，没有强制限定）对Demo文档.docx进行理解的结果。\n\n")
            f.write("**Prompt特点**：\n")
            f.write("- ✅ 背景：中国职场的述职汇报专家，专门为副总裁级别的职场高管筹备述职内容\n")
            f.write("- ✅ 方向：先通读了解核心思想 → 再细分板块拆解 → 然后深入探寻每个板块\n")
            f.write("- ✅ 没有强制限定和格式要求，让LLM自由理解\n\n")
            f.write("---\n\n")
            
            # 第1层：通读理解
            f.write("## 第1层：通读理解\n\n")
            layer1 = human_analysis.get("layer_1_overall_understanding", {}).get("data", {})
            f.write(f"### 核心主题\n\n{layer1.get('core_theme', '未识别')}\n\n")
            f.write(f"### 核心思想\n\n{layer1.get('core_idea', '未识别')}\n\n")
            f.write(f"### 文档目的\n\n{layer1.get('purpose', '未识别')}\n\n")
            f.write(f"### 目标受众\n\n{layer1.get('target_audience', '未识别')}\n\n")
            f.write(f"### 核心价值主张\n\n")
            for i, vp in enumerate(layer1.get('value_propositions', []), 1):
                f.write(f"{i}. {vp}\n")
            f.write("\n")
            f.write(f"### 关键短语\n\n")
            for i, phrase in enumerate(layer1.get('key_phrases', [])[:10], 1):
                f.write(f"{i}. {phrase}\n")
            f.write("\n")
            f.write(f"### 统计信息\n\n")
            f.write(f"- 文档总长度: {layer1.get('text_length', 0)}字符\n")
            f.write(f"- 幻灯片数: {layer1.get('total_slides', 0)}\n\n")
            f.write("---\n\n")
            
            # 第2层：板块拆分
            f.write("## 第2层：板块拆分\n\n")
            layer2 = human_analysis.get("layer_2_sections", {}).get("data", {})
            f.write(f"### 板块总数\n\n{layer2.get('total_sections', 0)}个板块\n\n")
            f.write(f"### 各板块详情\n\n")
            for section in layer2.get('sections', []):
                f.write(f"#### 板块{section.get('section_index', 0)}: {section.get('theme', '未命名')}\n\n")
                f.write(f"**核心思想**: {section.get('core_idea', '未识别')}\n\n")
                f.write(f"**内容摘要**: {section.get('content_summary', '无')}\n\n")
                f.write(f"**涉及幻灯片**: {', '.join(map(str, section.get('slides', [])))}\n\n")
            f.write("---\n\n")
            
            # 【新增】润色结果
            f.write("## 润色结果\n\n")
            f.write("### 说明\n\n")
            f.write("以下是对各板块内容进行PPT展示层面润色的结果，将文档内容润色成适合PPT展示的文案。\n\n")
            
            # 为每个板块进行润色（这里需要调用ContentPolisher）
            from content_polisher import ContentPolisher
            from presentation_planner import PresentationPlanner
            from layout_planner import LayoutPlanner
            
            content_polisher = ContentPolisher(llm_service)
            presentation_planner = PresentationPlanner(llm_service)
            layout_planner = LayoutPlanner(llm_service)
            
            for section in layer2.get('sections', []):
                section_idx = section.get('section_index', 0)
                section_analysis = {
                    "theme": section.get('theme', ''),
                    "core_idea": section.get('core_idea', ''),
                    "content_summary": section.get('content_summary', '')
                }
                
                # 获取论证信息
                layer3 = human_analysis.get("layer_3_arguments", {}).get("data", {})
                arguments = layer3.get('arguments', [])
                if section_idx < len(arguments):
                    arg = arguments[section_idx]
                    section_analysis.update({
                        "core_content": arg.get('core_content', ''),
                        "specific_arguments": arg.get('specific_arguments', []),
                        "core_evidence": arg.get('core_evidence', []),
                        "data_points": arg.get('data_points', [])
                    })
                
                f.write(f"#### 板块{section_idx}: {section.get('theme', '未命名')}\n\n")
                
                try:
                    # 润色
                    polished_slides = await content_polisher.polish_section(
                        section_analysis=section_analysis,
                        section_index=section_idx
                    )
                    
                    f.write(f"**润色后的幻灯片**（共{len(polished_slides)}张）:\n\n")
                    for slide in polished_slides:
                        f.write(f"**幻灯片{slide.get('slide_index', 0)}**: {slide.get('title', '')}\n")
                        f.write(f"- 内容: {slide.get('content', '')}\n")
                        f.write(f"- 内容类型: {slide.get('content_type', '')}\n")
                        visual = slide.get('visual_elements', {})
                        if visual.get('needs_table') or visual.get('needs_chart') or visual.get('needs_cards'):
                            f.write(f"- 视觉元素: {visual.get('notes', '需要视觉元素')}\n")
                        # 详细展开视觉元素
                        visual_detail = slide.get('visual_elements_detail', [])
                        if visual_detail:
                            f.write(f"- 视觉元素详细展开（共{len(visual_detail)}个元素）:\n")
                            for elem in visual_detail:
                                element_id = elem.get('element_id', f"{elem.get('element_type', 'unknown')}_{elem.get('element_index', 0)}")
                                f.write(f"  * 元素{elem.get('element_index', 0)} (ID: {element_id}, 类型: {elem.get('element_type', 'unknown')}): {elem.get('title', '无标题')}\n")
                                if elem.get('content'):
                                    f.write(f"    - 内容: {elem.get('content', '')}\n")
                                if elem.get('data'):
                                    f.write(f"    - 数据: {elem.get('data', '')}\n")
                                if elem.get('description'):
                                    f.write(f"    - 说明: {elem.get('description', '')}\n")
                        f.write("\n")
                    
                    # 展示策划
                    presentation_plan = await presentation_planner.plan_presentation(
                        polished_slides=polished_slides,
                        section_theme=section.get('theme', '')
                    )
                    
                    f.write(f"**展示策划**（共{len(presentation_plan)}张）:\n\n")
                    for plan in presentation_plan:
                        f.write(f"**幻灯片{plan.get('slide_index', 0)}**:\n")
                        f.write(f"- 布局类型: {plan.get('layout_type', '')}\n")
                        f.write(f"- 布局描述: {plan.get('layout_description', '')}\n")
                        guidance = plan.get('visual_guidance', {})
                        if guidance:
                            f.write(f"- 视觉指导:\n")
                            f.write(f"  - 字体大小: {guidance.get('font_size', '')}\n")
                            f.write(f"  - 字体粗细: {guidance.get('font_weight', '')}\n")
                            f.write(f"  - 对齐方式: {guidance.get('alignment', '')}\n")
                            f.write(f"  - 间距: {guidance.get('spacing', '')}\n")
                            f.write(f"  - 配色: {guidance.get('color_scheme', '')}\n")
                            if guidance.get('other_notes'):
                                f.write(f"  - 其他说明: {guidance.get('other_notes', '')}\n")
                        f.write("\n")
                    
                    # 布局规划
                    layout_plans = await layout_planner.plan_layout(
                        polished_slides=polished_slides,
                        presentation_plan=presentation_plan
                    )
                    
                    f.write("*********** 布局规划（新增） ***********\n\n")
                    f.write(f"**布局规划**（共{len(layout_plans)}张）:\n\n")
                    for layout_plan in layout_plans:
                        slide_idx = layout_plan.get('slide_index', 0)
                        plan_data = layout_plan.get('layout_plan', {})
                        f.write(f"**幻灯片{slide_idx}**:\n")
                        f.write(f"- 整体布局结构: {plan_data.get('overall_structure', '')}\n\n")
                        
                        # 元素位置
                        element_positions = plan_data.get('element_positions', [])
                        if element_positions:
                            f.write(f"- 元素位置（共{len(element_positions)}个元素）:\n")
                            for elem_pos in element_positions:
                                f.write(f"  * {elem_pos.get('element_id', '')} ({elem_pos.get('element_type', '')}):\n")
                                f.write(f"    - 位置: {elem_pos.get('position_description', '')}\n")
                                f.write(f"    - 尺寸: {elem_pos.get('size_description', '')}\n")
                                f.write(f"    - 对齐: {elem_pos.get('alignment', '')}\n")
                                spacing = elem_pos.get('spacing', {})
                                if spacing:
                                    f.write(f"    - 间距: 上{elem_pos.get('spacing', {}).get('margin_top', '')}, 下{elem_pos.get('spacing', {}).get('margin_bottom', '')}, 左{elem_pos.get('spacing', {}).get('margin_left', '')}, 右{elem_pos.get('spacing', {}).get('margin_right', '')}\n")
                            f.write("\n")
                        
                        # 元素间距
                        element_spacing = plan_data.get('element_spacing', {})
                        if element_spacing:
                            f.write(f"- 元素间距:\n")
                            f.write(f"  - 元素之间: {element_spacing.get('between_elements', '')}\n")
                            f.write(f"  - 内边距: {element_spacing.get('internal_padding', '')}\n\n")
                        
                        # 视觉层次
                        visual_hierarchy = plan_data.get('visual_hierarchy', '')
                        if visual_hierarchy:
                            f.write(f"- 视觉层次: {visual_hierarchy}\n\n")
                        
                        # 设计规范
                        design_specs = plan_data.get('design_specifications', '')
                        if design_specs:
                            f.write(f"- 设计规范: {design_specs}\n\n")
                    
                    f.write("*********** 布局规划结束 ***********\n\n")
                    
                except Exception as e:
                    logger.error(f"板块{section_idx}润色/策划失败: {e}", exc_info=True)
                    f.write(f"*润色/策划失败: {e}*\n\n")
            
            f.write("---\n\n")
            
            # 第3层：论证逻辑
            f.write("## 第3层：论证逻辑\n\n")
            layer3 = human_analysis.get("layer_3_arguments", {}).get("data", {})
            f.write(f"### 有论证的板块数\n\n{layer3.get('total_sections_with_arguments', 0)}个板块\n\n")
            f.write(f"### 各板块论证详情\n\n")
            for arg in layer3.get('arguments', []):
                f.write(f"#### 板块{arg.get('section_index', 0)}: {arg.get('section_theme', '未命名')}\n\n")
                f.write(f"**核心内容**: {arg.get('core_content', '未识别')}\n\n")
                f.write(f"**核心思想**: {arg.get('core_idea', '未识别')}\n\n")
                f.write(f"**具体论点**:\n")
                for i, point in enumerate(arg.get('specific_arguments', []), 1):
                    f.write(f"{i}. {point}\n")
                f.write("\n")
                f.write(f"**核心论据**:\n")
                for i, evidence in enumerate(arg.get('core_evidence', []), 1):
                    f.write(f"{i}. {evidence}\n")
                f.write("\n")
                f.write(f"**数据点**:\n")
                for i, data in enumerate(arg.get('data_points', []), 1):
                    f.write(f"{i}. {data}\n")
                f.write("\n")
                f.write(f"**论证类型**: {', '.join(arg.get('argument_types', []))}\n\n")
            f.write("---\n\n")
            
            # 第4层：支撑材料
            f.write("## 第4层：支撑材料\n\n")
            layer4 = human_analysis.get("layer_4_supporting_materials", {}).get("data", {})
            f.write(f"### 数据点总数\n\n{layer4.get('total_data_points', 0)}个\n\n")
            f.write(f"### 案例总数\n\n{layer4.get('total_cases', 0)}个\n\n")
            materials = layer4.get('materials', {})
            if materials.get('data_points'):
                f.write(f"### 数据点详情\n\n")
                for i, dp in enumerate(materials.get('data_points', [])[:10], 1):
                    f.write(f"{i}. {dp.get('data', '')} (上下文: {dp.get('context', '')})\n")
                f.write("\n")
            if materials.get('cases'):
                f.write(f"### 案例详情\n\n")
                for i, case in enumerate(materials.get('cases', [])[:10], 1):
                    f.write(f"{i}. {case.get('content', '')}\n")
                f.write("\n")
            f.write("---\n\n")
            
            # 第5层：表达风格
            f.write("## 第5层：表达风格\n\n")
            layer5 = human_analysis.get("layer_5_expression_style", {}).get("data", {})
            f.write(f"### 正式程度\n\n{layer5.get('formality_level', '未识别')}\n\n")
            f.write(f"### 语调\n\n{layer5.get('tone', '未识别')}\n\n")
            f.write(f"### 文化特征\n\n")
            for feature in layer5.get('cultural_features', []):
                f.write(f"- {feature}\n")
            f.write("\n")
            f.write(f"### 数字使用\n\n{layer5.get('use_of_numbers', 0)}次\n\n")
            f.write(f"### 表情符号使用\n\n{layer5.get('use_of_emojis', 0)}次\n\n")
            f.write("---\n\n")
            
            # 第6层：呈现形式
            f.write("## 第6层：呈现形式\n\n")
            layer6 = human_analysis.get("layer_6_presentation_form", {}).get("data", {})
            layout = layer6.get('layout_style', {})
            f.write(f"### 布局风格\n\n")
            f.write(f"- 宽高比: {layout.get('aspect_ratio', '未识别')}\n")
            f.write(f"- 宽度: {layout.get('width_cm', 0)}cm\n")
            f.write(f"- 高度: {layout.get('height_cm', 0)}cm\n\n")
            typography = layer6.get('typography', {})
            f.write(f"### 字体排版\n\n")
            f.write(f"- 字体大小: {', '.join(map(str, typography.get('font_sizes', [])))}\n")
            f.write(f"- 字体名称: {', '.join(typography.get('font_names', []))}\n")
            f.write(f"- 加粗使用: {typography.get('bold_usage_count', 0)}次\n\n")
            f.write("---\n\n")
            
            # 原始JSON（用于调试）
            f.write("## 原始JSON数据（用于调试）\n\n")
            f.write("```json\n")
            f.write(json.dumps(human_analysis, indent=2, ensure_ascii=False))
            f.write("\n```\n")
        
        logger.info(f"✅ 分析结果已保存到: {output_path}")
        logger.info(f"   文件大小: {output_path.stat().st_size}字节")
        
    except Exception as e:
        logger.error(f"❌ 分析失败: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(test_llm_understand_demo_docx())


```


## File: tests/test_single_slide_layout.py

```python
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

from html_generator import HTMLGenerator
from html_canvas_generator import HTMLCanvasGenerator
from loguru import logger
from datetime import datetime


def create_test_data():
    """创建测试数据（支持CSS-First新架构）"""
    
    # 【CSS-First 新架构】LLM 生成的 HTML 代码
    # 【颜色修复】：大标题使用深黑色（--ant-text-color-heading），而不是主色
    llm_html_code = """
    <div class="slide-container" style="display: flex; flex-direction: column; height: 100vh; padding: 40px; background: var(--ant-bg-color-layout);">
      <header style="margin-bottom: 60px; border-left: 12px solid var(--ant-color-primary); padding-left: 24px;">
        <h1 data-ppt-element="true" data-ppt-element-id="title_text_0" data-ppt-element-type="title"
            style="font-size: 48px; font-weight: 600; color: var(--ant-text-color-heading); text-align: left; margin: 0; line-height: 1;">
          核心价值主张
        </h1>
      </header>
      <main style="flex: 1; display: flex; gap: 24px; align-items: stretch;">
        <div class="ant-card" data-ppt-element="true" data-ppt-element-id="value_card_0" data-ppt-element-type="card"
             style="flex: 1; background: var(--ant-bg-color-container); padding: 40px 32px; border-radius: var(--ant-border-radius-base); box-shadow: var(--ant-box-shadow); border-top: 6px solid #1677FF; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <h3 style="margin: 0 0 24px 0; font-size: 32px; font-weight: 700; color: var(--ant-text-color-heading); text-align: center;">成本降低</h3>
          <p style="margin: 0; font-size: 18px; color: var(--ant-text-color-body); line-height: 1.8; text-align: center;">降低运营成本40-60%</p>
        </div>
        <div class="ant-card" data-ppt-element="true" data-ppt-element-id="value_card_1" data-ppt-element-type="card"
             style="flex: 1; background: var(--ant-bg-color-container); padding: 40px 32px; border-radius: var(--ant-border-radius-base); box-shadow: var(--ant-box-shadow); border-top: 6px solid #52C41A; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <h3 style="margin: 0 0 24px 0; font-size: 32px; font-weight: 700; color: var(--ant-text-color-heading); text-align: center;">效率提升</h3>
          <p style="margin: 0; font-size: 18px; color: var(--ant-text-color-body); line-height: 1.8; text-align: center;">提升转化效率20-35%</p>
        </div>
        <div class="ant-card" data-ppt-element="true" data-ppt-element-id="value_card_2" data-ppt-element-type="card"
             style="flex: 1; background: var(--ant-bg-color-container); padding: 40px 32px; border-radius: var(--ant-border-radius-base); box-shadow: var(--ant-box-shadow); border-top: 6px solid #FA8C16; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <h3 style="margin: 0 0 24px 0; font-size: 32px; font-weight: 700; color: var(--ant-text-color-heading); text-align: center;">智能转型</h3>
          <p style="margin: 0; font-size: 18px; color: var(--ant-text-color-body); line-height: 1.8; text-align: center;">加速业务智能化转型</p>
        </div>
      </main>
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


```


## File: browser_to_ppt_replicator/__init__.py

```python
"""
浏览器到PPT复刻器
将浏览器渲染的Ant Design/AntV组件一比一复刻到PPT
"""

from .browser_renderer import BrowserRenderer
from .element_analyzer import ElementAnalyzer
from .coordinate_mapper import CoordinateMapper
from .container_extractor import ContainerExtractor
from .text_extractor import TextExtractor
from .ppt_replicator import PPTReplicator
from .replicator import BrowserToPPTReplicator

__all__ = [
    'BrowserRenderer',
    'ElementAnalyzer',
    'CoordinateMapper',
    'ContainerExtractor',
    'TextExtractor',
    'PPTReplicator',
    'BrowserToPPTReplicator',
]


```


## File: browser_to_ppt_replicator/browser_renderer.py

```python
"""
浏览器渲染器
使用Playwright渲染HTML内容（Ant Design组件）
"""

from typing import Optional
from pathlib import Path
from loguru import logger

try:
    from playwright.async_api import async_playwright, Page, Browser
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    logger.warning("Playwright not installed. Install with: pip install playwright && playwright install chromium")


class BrowserRenderer:
    """
    浏览器渲染器
    使用Playwright渲染HTML内容，支持Ant Design/AntV组件
    """
    
    # 16:9画布尺寸
    CANVAS_WIDTH = 1920
    CANVAS_HEIGHT = 1080
    
    def __init__(self):
        """初始化浏览器渲染器"""
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright is required. "
                "Install with: pip install playwright && playwright install chromium"
            )
        self.browser: Optional[Browser] = None
        logger.info("--- [BrowserRenderer]: Initialized")
    
    async def render_html(self, html_content: str) -> Page:
        """
        渲染HTML内容
        
        Args:
            html_content: HTML内容字符串
            
        Returns:
            Playwright Page对象
        """
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(headless=True)
        
        page = await self.browser.new_page(
            viewport={
                'width': self.CANVAS_WIDTH,
                'height': self.CANVAS_HEIGHT
            }
        )
        
        # 加载HTML内容
        await page.set_content(html_content, wait_until='networkidle')
        
        # 等待页面完全渲染（Ant Design组件可能需要时间）
        await page.wait_for_timeout(1000)
        
        logger.info(f"--- [BrowserRenderer]: HTML rendered (viewport: {self.CANVAS_WIDTH}x{self.CANVAS_HEIGHT})")
        return page
    
    async def render_html_file(self, html_file_path: Path) -> Page:
        """
        从文件渲染HTML
        
        Args:
            html_file_path: HTML文件路径
            
        Returns:
            Playwright Page对象
        """
        html_content = html_file_path.read_text(encoding='utf-8')
        return await self.render_html(html_content)
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            self.browser = None
            logger.info("--- [BrowserRenderer]: Browser closed")
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()


```


## File: browser_to_ppt_replicator/container_extractor.py

```python
"""
容器提取器
截图容器元素并保存为PNG
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from playwright.async_api import ElementHandle
from loguru import logger


class ContainerExtractor:
    """
    容器提取器
    截图容器元素并保存为PNG文件
    """
    
    def __init__(self, output_dir: Path):
        """
        初始化容器提取器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.container_count = 0
        logger.info(f"--- [ContainerExtractor]: Initialized, output_dir: {self.output_dir}")
    
    async def extract_container(
        self,
        container_info: Dict[str, Any],
        container_index: int,
        hide_text: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        提取容器（截图）
        
        【新架构原则】：混合渲染法
        - 如果 hide_text=True：隐藏文字后截图（用于混合渲染，文字单独插入）
        - 如果 hide_text=False：直接截图（文字包含在图片中）
        
        Args:
            container_info: 容器信息（来自ElementAnalyzer）
            container_index: 容器索引
            hide_text: 是否隐藏文字后截图（默认True，用于混合渲染）
            
        Returns:
            容器提取结果，包含图片路径和位置信息
        """
        try:
            element: ElementHandle = container_info['element']
            page = element.page if hasattr(element, 'page') else None
            
            # 生成文件名
            filename = f"container_{container_index:03d}.png"
            output_path = self.output_dir / filename
            
            # 【混合渲染法】：隐藏文字后截图
            if hide_text and page:
                try:
                    # 获取元素选择器
                    element_id = await element.get_attribute('id')
                    selector = f"#{element_id}" if element_id else None
                    
                    if selector:
                        # 临时隐藏文字
                        await page.evaluate(f"""
                            (selector) => {{
                                const el = document.querySelector(selector);
                                if (el) {{
                                    el.setAttribute('data-original-color', el.style.color || '');
                                    el.style.color = 'transparent';
                                    const children = el.querySelectorAll('*');
                                    children.forEach(child => {{
                                        child.setAttribute('data-original-color', child.style.color || '');
                                        child.style.color = 'transparent';
                                    }});
                                }}
                            }}
                        """, selector)
                        
                        # 等待样式应用
                        await page.wait_for_timeout(100)
                        
                        # 截图（包含阴影，透明背景）
                        await element.screenshot(
                            path=str(output_path),
                            omit_background=True  # 透明背景，保留圆角
                        )
                        
                        # 恢复文字
                        await page.evaluate(f"""
                            (selector) => {{
                                const el = document.querySelector(selector);
                                if (el) {{
                                    const originalColor = el.getAttribute('data-original-color');
                                    if (originalColor) {{
                                        el.style.color = originalColor;
                                    }}
                                    const children = el.querySelectorAll('*');
                                    children.forEach(child => {{
                                        const childOriginalColor = child.getAttribute('data-original-color');
                                        if (childOriginalColor) {{
                                            child.style.color = childOriginalColor;
                                        }}
                                    }});
                                }}
                            }}
                        """, selector)
                        
                        logger.debug(f"--- [ContainerExtractor]: 【混合渲染】容器截图完成（文字已隐藏）: {filename}")
                    else:
                        # 如果没有选择器，直接截图
                        await element.screenshot(path=str(output_path))
                        logger.debug(f"--- [ContainerExtractor]: 容器截图完成（无选择器，直接截图）: {filename}")
                except Exception as e:
                    logger.warning(f"--- [ContainerExtractor]: 隐藏文字失败，使用直接截图: {e}")
                    await element.screenshot(path=str(output_path))
            else:
                # 直接截图（文字包含在图片中）
                await element.screenshot(path=str(output_path))
                logger.debug(f"--- [ContainerExtractor]: 容器截图完成（文字包含）: {filename}")
            
            return {
                'image_path': str(output_path),
                'position': container_info['position'],
                'size': container_info['size'],
                'style': container_info.get('style', {}),
                'z_index': container_info.get('z_index', 0),
                'hide_text': hide_text  # 记录是否隐藏了文字
            }
        except Exception as e:
            logger.warning(f"--- [ContainerExtractor]: Failed to extract container {container_index}: {e}")
            return None
    
    async def extract_all_containers(
        self,
        containers: list[Dict[str, Any]],
        hide_text: bool = True
    ) -> List[Dict[str, Any]]:
        """
        提取所有容器
        
        【新架构原则】：支持混合渲染法
        - hide_text=True：隐藏文字后截图（容器用图片，文字单独插入）
        - hide_text=False：直接截图（文字包含在图片中）
        
        Args:
            containers: 容器信息列表
            hide_text: 是否隐藏文字后截图（默认True）
            
        Returns:
            提取结果列表
        """
        logger.info(f"--- [ContainerExtractor]: Extracting {len(containers)} containers (hide_text={hide_text})...")
        
        # 按z-index排序（从后往前，先处理底层）
        sorted_containers = sorted(containers, key=lambda c: c.get('z_index', 0))
        
        extracted = []
        for idx, container in enumerate(sorted_containers):
            result = await self.extract_container(container, idx, hide_text=hide_text)
            if result:
                extracted.append(result)
        
        logger.info(f"--- [ContainerExtractor]: Extracted {len(extracted)} containers")
        return extracted


```


## File: browser_to_ppt_replicator/coordinate_mapper.py

```python
"""
坐标映射器 - 24栅格系统
将浏览器坐标映射到PPT坐标
"""

from typing import Tuple, Dict
from pptx.util import Cm
from loguru import logger


class CoordinateMapper:
    """
    坐标映射器 - 24栅格系统
    
    浏览器端：1920px × 1080px (16:9)
    PPT端：33.867cm × 19.05cm (16:9)
    栅格系统：24列 × 13.5行（保持16:9比例）
    
    注意：HTML中有24px的padding，需要从坐标中减去
    """
    
    # 浏览器端尺寸
    BROWSER_WIDTH = 1920
    BROWSER_HEIGHT = 1080
    GRID_COLUMNS = 24
    GRID_ROWS = 13.5  # 1080 / 80 = 13.5 (保持16:9比例)
    
    # HTML Padding（与HTML生成器保持一致）
    HTML_PADDING = 24  # px
    
    # PPT端尺寸（16:9）
    PPT_WIDTH_CM = 33.867
    PPT_HEIGHT_CM = 19.05
    
    # 实际内容区域（减去padding）
    CONTENT_WIDTH = BROWSER_WIDTH - 2 * HTML_PADDING  # 1872px
    CONTENT_HEIGHT = BROWSER_HEIGHT - 2 * HTML_PADDING  # 1032px
    
    # PPT内容区域（等比例）
    PPT_CONTENT_WIDTH_CM = PPT_WIDTH_CM - 2 * (HTML_PADDING * PPT_WIDTH_CM / BROWSER_WIDTH)  # ≈ 33.02cm
    PPT_CONTENT_HEIGHT_CM = PPT_HEIGHT_CM - 2 * (HTML_PADDING * PPT_HEIGHT_CM / BROWSER_HEIGHT)  # ≈ 18.20cm
    
    # 栅格单元尺寸（基于内容区域）
    BROWSER_CELL_WIDTH = CONTENT_WIDTH / GRID_COLUMNS  # ≈ 78px
    BROWSER_CELL_HEIGHT = CONTENT_HEIGHT / GRID_ROWS   # ≈ 76.4px
    
    PPT_CELL_WIDTH_CM = PPT_CONTENT_WIDTH_CM / GRID_COLUMNS  # ≈ 1.38cm
    PPT_CELL_HEIGHT_CM = PPT_CONTENT_HEIGHT_CM / GRID_ROWS   # ≈ 1.35cm
    
    def browser_to_ppt(self, browser_x: float, browser_y: float) -> Tuple[float, float]:
        """
        浏览器坐标转PPT坐标（cm）
        
        Args:
            browser_x: 浏览器X坐标（px，相对于body）
            browser_y: 浏览器Y坐标（px，相对于body）
            
        Returns:
            (ppt_x, ppt_y) 单位：cm
        """
        # 【重要】减去HTML padding，得到相对于内容区域的坐标
        # 如果坐标在padding内，设为0（元素可能从padding边缘开始）
        content_x = max(0, browser_x - self.HTML_PADDING)
        content_y = max(0, browser_y - self.HTML_PADDING)
        
        # 映射到PPT内容区域
        ppt_x = (content_x / self.CONTENT_WIDTH) * self.PPT_CONTENT_WIDTH_CM
        ppt_y = (content_y / self.CONTENT_HEIGHT) * self.PPT_CONTENT_HEIGHT_CM
        
        logger.info(f"--- [CoordinateMapper]: 坐标映射")
        logger.info(f"    浏览器坐标: ({browser_x:.1f}px, {browser_y:.1f}px)")
        logger.info(f"    减去padding: ({browser_x - self.HTML_PADDING:.1f}px, {browser_y - self.HTML_PADDING:.1f}px)")
        logger.info(f"    内容区域坐标: ({content_x:.1f}px, {content_y:.1f}px)")
        logger.info(f"    内容区域尺寸: {self.CONTENT_WIDTH}px × {self.CONTENT_HEIGHT}px")
        logger.info(f"    PPT内容区域尺寸: {self.PPT_CONTENT_WIDTH_CM:.2f}cm × {self.PPT_CONTENT_HEIGHT_CM:.2f}cm")
        logger.info(f"    PPT坐标: ({ppt_x:.2f}cm, {ppt_y:.2f}cm)")
        logger.info(f"    比例: x={content_x/self.CONTENT_WIDTH:.4f}, y={content_y/self.CONTENT_HEIGHT:.4f}")
        
        return ppt_x, ppt_y
    
    def browser_size_to_ppt(self, browser_width: float, browser_height: float) -> Tuple[float, float]:
        """
        浏览器尺寸转PPT尺寸（cm）
        
        Args:
            browser_width: 浏览器宽度（px）
            browser_height: 浏览器高度（px）
            
        Returns:
            (ppt_width, ppt_height) 单位：cm
        """
        # 尺寸直接按比例映射（不需要减去padding）
        ppt_width = (browser_width / self.CONTENT_WIDTH) * self.PPT_CONTENT_WIDTH_CM
        ppt_height = (browser_height / self.CONTENT_HEIGHT) * self.PPT_CONTENT_HEIGHT_CM
        
        logger.info(f"--- [CoordinateMapper]: 尺寸映射")
        logger.info(f"    浏览器尺寸: {browser_width:.1f}px × {browser_height:.1f}px")
        logger.info(f"    内容区域尺寸: {self.CONTENT_WIDTH}px × {self.CONTENT_HEIGHT}px")
        logger.info(f"    PPT内容区域尺寸: {self.PPT_CONTENT_WIDTH_CM:.2f}cm × {self.PPT_CONTENT_HEIGHT_CM:.2f}cm")
        logger.info(f"    PPT尺寸: {ppt_width:.2f}cm × {ppt_height:.2f}cm")
        logger.info(f"    比例: w={browser_width/self.CONTENT_WIDTH:.4f}, h={browser_height/self.CONTENT_HEIGHT:.4f}")
        
        return ppt_width, ppt_height
    
    def browser_to_grid(self, browser_x: float, browser_y: float) -> Tuple[int, int]:
        """
        浏览器坐标转栅格坐标
        
        Args:
            browser_x: 浏览器X坐标（px）
            browser_y: 浏览器Y坐标（px）
            
        Returns:
            (grid_x, grid_y) 栅格坐标（0-23列，0-12行）
        """
        grid_x = int(browser_x / self.BROWSER_CELL_WIDTH)
        grid_y = int(browser_y / self.BROWSER_CELL_HEIGHT)
        
        # 限制在有效范围内
        grid_x = max(0, min(grid_x, self.GRID_COLUMNS - 1))
        grid_y = max(0, min(grid_y, int(self.GRID_ROWS) - 1))
        
        return grid_x, grid_y
    
    def grid_to_ppt(self, grid_x: int, grid_y: int, span_x: int = 1, span_y: int = 1) -> Dict[str, float]:
        """
        栅格坐标转PPT位置和尺寸
        
        Args:
            grid_x: 栅格X坐标（0-23）
            grid_y: 栅格Y坐标（0-12）
            span_x: 横向跨度（占几个栅格）
            span_y: 纵向跨度（占几个栅格）
            
        Returns:
            {'left': cm, 'top': cm, 'width': cm, 'height': cm}
        """
        return {
            'left': grid_x * self.PPT_CELL_WIDTH_CM,
            'top': grid_y * self.PPT_CELL_HEIGHT_CM,
            'width': span_x * self.PPT_CELL_WIDTH_CM,
            'height': span_y * self.PPT_CELL_HEIGHT_CM
        }
    
    def calculate_grid_span(self, browser_width: float, browser_height: float) -> Tuple[int, int]:
        """
        计算浏览器尺寸对应的栅格跨度
        
        Args:
            browser_width: 浏览器宽度（px）
            browser_height: 浏览器高度（px）
            
        Returns:
            (span_x, span_y) 栅格跨度
        """
        span_x = max(1, int(browser_width / self.BROWSER_CELL_WIDTH))
        span_y = max(1, int(browser_height / self.BROWSER_CELL_HEIGHT))
        return span_x, span_y


```


## File: browser_to_ppt_replicator/element_analyzer.py

```python
"""
元素分析器
识别和分析浏览器页面中的容器和文本元素
"""

from typing import List, Dict, Any, Optional
from playwright.async_api import Page, ElementHandle
from loguru import logger


class ElementAnalyzer:
    """
    元素分析器
    识别容器元素（Card、div等）和文本元素（Typography等）
    """
    
    # 容器元素选择器（按优先级）
    CONTAINER_SELECTORS = [
        '.card',               # 通用card类
        '[class*="card"]',     # 包含card的类名
        'div.card',            # div.card
        'section',             # HTML5 section
        'div[style*="background"]',  # 有背景色的div
        'div[style*="border"]',      # 有边框的div
    ]
    
    # 文本元素选择器
    TEXT_SELECTORS = [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',  # 标题
        'p',                                   # 段落
        '.ant-typography',                     # Ant Design Typography
        '[class*="typography"]',               # 包含typography的类名
        'span',                                # 行内文本
        'li',                                  # 列表项
    ]
    
    def __init__(self):
        """初始化元素分析器"""
        logger.info("--- [ElementAnalyzer]: Initialized")
    
    async def analyze_elements(self, page: Page) -> Dict[str, List[Dict[str, Any]]]:
        """
        分析页面元素
        
        Args:
            page: Playwright Page对象
            
        Returns:
            {
                'containers': [容器信息列表],
                'texts': [文本信息列表]
            }
        """
        logger.info("--- [ElementAnalyzer]: Analyzing page elements...")
        
        # 识别容器元素
        containers = await self._identify_containers(page)
        logger.info(f"--- [ElementAnalyzer]: Found {len(containers)} container elements")
        
        # 识别文本元素
        texts = await self._identify_texts(page)
        logger.info(f"--- [ElementAnalyzer]: Found {len(texts)} text elements")
        
        return {
            'containers': containers,
            'texts': texts
        }
    
    async def _identify_containers(self, page: Page) -> List[Dict[str, Any]]:
        """识别容器元素"""
        containers = []
        
        # 尝试所有容器选择器
        for selector in self.CONTAINER_SELECTORS:
            try:
                elements = await page.query_selector_all(selector)
                for elem in elements:
                    # 检查是否已经有父容器包含此元素
                    if not await self._is_nested_in_containers(elem, containers, page):
                        container_info = await self._extract_container_info(elem)
                        if container_info:
                            containers.append(container_info)
            except Exception as e:
                logger.debug(f"--- [ElementAnalyzer]: Selector '{selector}' failed: {e}")
        
        # 去重（基于位置和尺寸）
        containers = self._deduplicate_containers(containers)
        
        return containers
    
    async def _identify_texts(self, page: Page) -> List[Dict[str, Any]]:
        """识别文本元素"""
        texts = []
        
        # 尝试所有文本选择器
        for selector in self.TEXT_SELECTORS:
            try:
                elements = await page.query_selector_all(selector)
                for elem in elements:
                    text_info = await self._extract_text_info(elem)
                    if text_info and text_info.get('text', '').strip():
                        texts.append(text_info)
            except Exception as e:
                logger.debug(f"--- [ElementAnalyzer]: Selector '{selector}' failed: {e}")
        
        # 去重（基于位置）
        texts = self._deduplicate_texts(texts)
        
        return texts
    
    async def _extract_container_info(self, element: ElementHandle) -> Optional[Dict[str, Any]]:
        """提取容器元素信息"""
        try:
            # 获取位置和尺寸
            # 【重要】bounding_box()返回的坐标是相对于viewport的
            # 由于我们的HTML结构是 body > .canvas (padding: 24px) > .container > elements
            # 而viewport = body（没有滚动），所以坐标已经是相对于body的
            # 但是，元素的实际位置需要考虑canvas的padding
            box = await element.bounding_box()
            if not box:
                return None
            
            # 【修复】获取元素相对于body的实际位置
            # 使用getBoundingClientRect() + scrollX/Y获取相对于body的准确坐标
            # 这对于CSS Grid布局更准确
            try:
                rect_info = await element.evaluate("""
                    el => {
                        const rect = el.getBoundingClientRect();
                        // 获取body的位置（相对于viewport）
                        const bodyRect = document.body.getBoundingClientRect();
                        // 计算元素相对于body的位置
                        // 需要考虑scrollX/Y（虽然我们的页面没有滚动，但为了准确性还是加上）
                        return {
                            x: rect.left - bodyRect.left + window.scrollX,
                            y: rect.top - bodyRect.top + window.scrollY,
                            width: rect.width,
                            height: rect.height
                        };
                    }
                """)
                # 使用getBoundingClientRect计算的位置（相对于body）
                box['x'] = rect_info['x']
                box['y'] = rect_info['y']
                box['width'] = rect_info['width']
                box['height'] = rect_info['height']
                logger.debug(f"--- [ElementAnalyzer]: 使用getBoundingClientRect获取位置: ({box['x']:.1f}, {box['y']:.1f})")
            except Exception as e:
                logger.warning(f"--- [ElementAnalyzer]: Failed to get getBoundingClientRect position, using bounding_box: {e}")
                # 如果获取失败，使用bounding_box（相对于viewport）
                # 由于我们的页面没有滚动，viewport = body，所以可以直接使用
                pass
            
            # 获取样式
            style = await element.evaluate("""
                el => ({
                    backgroundColor: window.getComputedStyle(el).backgroundColor,
                    borderRadius: window.getComputedStyle(el).borderRadius,
                    border: window.getComputedStyle(el).border,
                    borderWidth: window.getComputedStyle(el).borderWidth,
                    borderColor: window.getComputedStyle(el).borderColor,
                    boxShadow: window.getComputedStyle(el).boxShadow,
                    padding: window.getComputedStyle(el).padding,
                    margin: window.getComputedStyle(el).margin,
                    zIndex: window.getComputedStyle(el).zIndex,
                })
            """)
            
            # 检查是否有可见的背景或边框（才认为是容器）
            has_background = (
                style['backgroundColor'] and 
                style['backgroundColor'] not in ['rgba(0, 0, 0, 0)', 'transparent']
            )
            has_border = (
                style['border'] and 
                style['border'] != '0px none rgb(0, 0, 0)'
            )
            
            if not (has_background or has_border):
                return None
            
            # 解析z-index
            z_index_str = style.get('zIndex', '0') or '0'
            try:
                z_index = int(z_index_str) if z_index_str != 'auto' else 0
            except:
                z_index = 0
            
            return {
                'element': element,
                'type': 'container',
                'position': {'x': box['x'], 'y': box['y']},
                'size': {'width': box['width'], 'height': box['height']},
                'style': style,
                'z_index': z_index
            }
        except Exception as e:
            logger.debug(f"--- [ElementAnalyzer]: Failed to extract container info: {e}")
            return None
    
    async def _extract_text_info(self, element: ElementHandle) -> Optional[Dict[str, Any]]:
        """提取文本元素信息"""
        try:
            # 获取文本内容
            text = await element.inner_text()
            if not text or not text.strip():
                return None
            
            # 获取位置和尺寸
            # 【重要】bounding_box()返回的坐标是相对于viewport的
            # 使用getBoundingClientRect() + scrollX/Y获取相对于body的准确坐标
            # 这对于CSS Grid布局更准确
            box = await element.bounding_box()
            if not box:
                return None
            
            # 【修复】获取元素相对于body的实际位置
            try:
                rect_info = await element.evaluate("""
                    el => {
                        const rect = el.getBoundingClientRect();
                        // 获取body的位置（相对于viewport）
                        const bodyRect = document.body.getBoundingClientRect();
                        // 计算元素相对于body的位置
                        // 需要考虑scrollX/Y（虽然我们的页面没有滚动，但为了准确性还是加上）
                        return {
                            x: rect.left - bodyRect.left + window.scrollX,
                            y: rect.top - bodyRect.top + window.scrollY,
                            width: rect.width,
                            height: rect.height
                        };
                    }
                """)
                # 使用getBoundingClientRect计算的位置（相对于body）
                box['x'] = rect_info['x']
                box['y'] = rect_info['y']
                box['width'] = rect_info['width']
                box['height'] = rect_info['height']
                logger.debug(f"--- [ElementAnalyzer]: 使用getBoundingClientRect获取文本位置: ({box['x']:.1f}, {box['y']:.1f})")
            except Exception as e:
                logger.warning(f"--- [ElementAnalyzer]: Failed to get getBoundingClientRect position, using bounding_box: {e}")
                # 如果获取失败，使用bounding_box（相对于viewport）
                # 由于我们的页面没有滚动，viewport = body，所以可以直接使用
                pass
            
            # 获取样式
            style = await element.evaluate("""
                el => ({
                    fontSize: window.getComputedStyle(el).fontSize,
                    fontFamily: window.getComputedStyle(el).fontFamily,
                    fontWeight: window.getComputedStyle(el).fontWeight,
                    color: window.getComputedStyle(el).color,
                    textAlign: window.getComputedStyle(el).textAlign,
                    lineHeight: window.getComputedStyle(el).lineHeight,
                    letterSpacing: window.getComputedStyle(el).letterSpacing,
                })
            """)
            
            return {
                'element': element,
                'type': 'text',
                'text': text.strip(),
                'position': {'x': box['x'], 'y': box['y']},
                'size': {'width': box['width'], 'height': box['height']},
                'style': style
            }
        except Exception as e:
            logger.debug(f"--- [ElementAnalyzer]: Failed to extract text info: {e}")
            return None
    
    async def _is_nested_in_containers(self, element: ElementHandle, containers: List[Dict], page: Page) -> bool:
        """检查元素是否嵌套在已有容器中"""
        try:
            elem_box = await element.bounding_box()
            if not elem_box:
                return False
            
            for container in containers:
                container_pos = container['position']
                container_size = container['size']
                
                # 检查元素是否在容器内
                if (elem_box['x'] >= container_pos['x'] and
                    elem_box['y'] >= container_pos['y'] and
                    elem_box['x'] + elem_box['width'] <= container_pos['x'] + container_size['width'] and
                    elem_box['y'] + elem_box['height'] <= container_pos['y'] + container_size['height']):
                    return True
            
            return False
        except:
            return False
    
    def _deduplicate_containers(self, containers: List[Dict]) -> List[Dict]:
        """去重容器（基于位置和尺寸）"""
        seen = set()
        unique = []
        
        for container in containers:
            pos = container['position']
            size = container['size']
            key = (int(pos['x']), int(pos['y']), int(size['width']), int(size['height']))
            
            if key not in seen:
                seen.add(key)
                unique.append(container)
        
        return unique
    
    def _deduplicate_texts(self, texts: List[Dict]) -> List[Dict]:
        """去重文本（基于位置和内容）"""
        seen = set()
        unique = []
        
        for text in texts:
            pos = text['position']
            content = text['text']
            key = (int(pos['x']), int(pos['y']), content[:50])  # 只取前50字符
            
            if key not in seen:
                seen.add(key)
                unique.append(text)
        
        return unique


```


## File: browser_to_ppt_replicator/hybrid_renderer.py

```python
"""
混合渲染器（Hybrid Renderer）
实现"容器用图片，内容用原生文本"的混合渲染方案

核心原则：
1. LLM 负责"定性"（审美和结构）- 生成流式布局 HTML
2. 浏览器负责"定量"（精确计算和渲染）- 计算坐标并截图
3. PPT 负责"组装"（图片背景 + 可编辑文本）
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
from loguru import logger

try:
    from playwright.async_api import Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False


class HybridRenderer:
    """
    混合渲染器
    
    工作流程：
    1. 加载流式布局 HTML（Flex/Grid）
    2. 等待浏览器渲染完成
    3. 提取所有元素的坐标和样式
    4. 为卡片元素截图（隐藏文字，保留样式）
    5. 返回元素信息和截图路径
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        初始化混合渲染器
        
        Args:
            output_dir: 截图输出目录
        """
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "Playwright is required. "
                "Install with: pip install playwright && playwright install chromium"
            )
        
        self.output_dir = output_dir or Path("replicated_outputs/containers")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"--- [HybridRenderer]: Initialized (output_dir: {self.output_dir})")
    
    async def extract_layout_data(self, page: Page) -> Dict[str, Any]:
        """
        从浏览器页面提取布局数据
        
        核心逻辑：
        - 识别所有带有 data-ppt-element 属性的元素
        - 提取坐标、样式、内容
        - 为卡片元素准备截图
        
        Args:
            page: Playwright Page 对象
            
        Returns:
            {
                'elements': [
                    {
                        'id': 'element_id',
                        'type': 'card|title|text',
                        'content': '文本内容',
                        'position': {'x': 100, 'y': 200},
                        'size': {'width': 300, 'height': 200},
                        'style': {
                            'color': '#000',
                            'fontSize': '16px',
                            'backgroundColor': '#fff'
                        },
                        'screenshot_path': 'path/to/screenshot.png'  # 仅卡片有
                    }
                ]
            }
        """
        logger.info("--- [HybridRenderer]: 开始提取布局数据...")
        
        # 等待页面完全渲染
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(500)  # 额外等待 CSS 动画和布局稳定
        
        # 提取所有标记的元素
        elements_data = await page.evaluate("""
            () => {
                const results = [];
                
                // 查找所有带有 data-ppt-element 属性的元素
                // 如果没有，则查找 .ppt-element 类名的元素
                const elements = document.querySelectorAll('[data-ppt-element], .ppt-element');
                
                elements.forEach(el => {
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    
                    // 提取基本信息
                    const elementData = {
                        id: el.id || el.getAttribute('data-ppt-element-id') || '',
                        type: el.getAttribute('data-ppt-element-type') || 
                              el.className.match(/element-(card|title|text)/)?.[1] || 'text',
                        content: el.innerText || el.textContent || '',
                        position: {
                            x: rect.left + window.scrollX,
                            y: rect.top + window.scrollY
                        },
                        size: {
                            width: rect.width,
                            height: rect.height
                        },
                        style: {
                            color: style.color,
                            fontSize: style.fontSize,
                            fontWeight: style.fontWeight,
                            fontFamily: style.fontFamily,
                            backgroundColor: style.backgroundColor,
                            textAlign: style.textAlign,
                            lineHeight: style.lineHeight
                        },
                        // 用于截图的选择器
                        selector: el.id ? `#${el.id}` : 
                                 el.className ? `.${el.className.split(' ')[0]}` : null
                    };
                    
                    results.push(elementData);
                });
                
                return results;
            }
        """)
        
        logger.info(f"--- [HybridRenderer]: 找到 {len(elements_data)} 个元素")
        
        # 为卡片元素截图（隐藏文字，保留样式）
        for elem in elements_data:
            if elem['type'] == 'card' and elem.get('selector'):
                screenshot_path = await self._screenshot_card_without_text(
                    page, elem, len(elements_data)
                )
                if screenshot_path:
                    elem['screenshot_path'] = str(screenshot_path)
        
        return {
            'elements': elements_data
        }
    
    async def _screenshot_card_without_text(
        self, 
        page: Page, 
        element_data: Dict[str, Any],
        total_elements: int
    ) -> Optional[Path]:
        """
        为卡片元素截图（隐藏文字，保留样式）
        
        策略：
        1. 临时隐藏文字（color: transparent）
        2. 截图（包含阴影和圆角）
        3. 恢复文字
        
        Args:
            page: Playwright Page 对象
            element_data: 元素数据
            total_elements: 总元素数量（用于生成唯一文件名）
            
        Returns:
            截图文件路径
        """
        element_id = element_data.get('id', '')
        selector = element_data.get('selector')
        
        if not selector:
            logger.warning(f"--- [HybridRenderer]: 元素 {element_id} 没有选择器，跳过截图")
            return None
        
        try:
            # 生成唯一文件名
            screenshot_filename = f"card_{element_id}_{total_elements}.png"
            screenshot_path = self.output_dir / screenshot_filename
            
            # 临时隐藏文字，保留样式
            await page.evaluate(f"""
                (selector) => {{
                    const el = document.querySelector(selector);
                    if (el) {{
                        // 保存原始颜色
                        el.setAttribute('data-original-color', el.style.color || '');
                        // 隐藏文字
                        el.style.color = 'transparent';
                        // 确保子元素文字也隐藏
                        const children = el.querySelectorAll('*');
                        children.forEach(child => {{
                            child.setAttribute('data-original-color', child.style.color || '');
                            child.style.color = 'transparent';
                        }});
                    }}
                }}
            """, selector)
            
            # 等待样式应用
            await page.wait_for_timeout(100)
            
            # 截图（包含阴影，需要稍微扩大截图区域）
            # 计算包含阴影的区域（通常阴影向外扩展 8-12px）
            shadow_padding = 12
            x = max(0, element_data['position']['x'] - shadow_padding)
            y = max(0, element_data['position']['y'] - shadow_padding)
            width = element_data['size']['width'] + shadow_padding * 2
            height = element_data['size']['height'] + shadow_padding * 2
            
            await page.locator(selector).screenshot(
                path=str(screenshot_path),
                omit_background=True  # 透明背景，保留圆角
            )
            
            # 恢复文字
            await page.evaluate(f"""
                (selector) => {{
                    const el = document.querySelector(selector);
                    if (el) {{
                        const originalColor = el.getAttribute('data-original-color');
                        if (originalColor) {{
                            el.style.color = originalColor;
                        }}
                        const children = el.querySelectorAll('*');
                        children.forEach(child => {{
                            const childOriginalColor = child.getAttribute('data-original-color');
                            if (childOriginalColor) {{
                                child.style.color = childOriginalColor;
                            }}
                        }});
                    }}
                }}
            """, selector)
            
            logger.info(f"--- [HybridRenderer]: ✅ 卡片截图完成: {screenshot_path}")
            return screenshot_path
            
        except Exception as e:
            logger.error(f"--- [HybridRenderer]: ❌ 卡片截图失败 {element_id}: {e}", exc_info=True)
            return None


```


## File: browser_to_ppt_replicator/ppt_replicator.py

```python
"""
PPT复刻器
将浏览器渲染结果复刻到PPT
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from pptx import Presentation
from pptx.util import Cm, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from loguru import logger

from .coordinate_mapper import CoordinateMapper


class PPTReplicator:
    """
    PPT复刻器
    将容器图片和文本插入到PPT的相同位置
    """
    
    def __init__(self, coordinate_mapper: CoordinateMapper, output_path: Optional[Path] = None, prs: Optional[Presentation] = None):
        """
        初始化PPT复刻器
        
        Args:
            coordinate_mapper: 坐标映射器
            output_path: 输出PPT路径
            prs: 现有的Presentation对象（如果提供，使用它而不是创建新的）
        """
        self.mapper = coordinate_mapper
        
        if prs is not None:
            # 使用现有的Presentation对象（用于多张幻灯片）
            self.prs = prs
        else:
            # 创建新的Presentation对象
            self.prs = Presentation()
            # 设置16:9尺寸
            self.prs.slide_width = Cm(coordinate_mapper.PPT_WIDTH_CM)
            self.prs.slide_height = Cm(coordinate_mapper.PPT_HEIGHT_CM)
        
        self.output_path = output_path
        logger.info(f"--- [PPTReplicator]: Initialized (size: {coordinate_mapper.PPT_WIDTH_CM}cm x {coordinate_mapper.PPT_HEIGHT_CM}cm)")
    
    def replicate_slide(
        self,
        containers: List[Dict[str, Any]],
        texts: List[Dict[str, Any]],
        use_hybrid_rendering: bool = True
    ) -> None:
        """
        复刻一张幻灯片
        
        【新架构原则】：混合渲染法
        - 容器用图片（浏览器截图，保留完美样式）
        - 内容用原生文本（保证可编辑性）
        
        Args:
            containers: 容器列表（包含图片路径和位置）
            texts: 文本列表（包含内容和样式）
            use_hybrid_rendering: 是否使用混合渲染（默认True）
        """
        logger.info(f"--- [PPTReplicator]: Replicating slide with {len(containers)} containers and {len(texts)} texts")
        logger.info(f"--- [PPTReplicator]: 使用混合渲染: {use_hybrid_rendering}")
        
        # 创建空白幻灯片
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])  # 空白布局
        
        if use_hybrid_rendering:
            # 【混合渲染法】：容器用图片，文本用原生
            # 1. 插入容器图片（底层，按z-index从后往前）
            sorted_containers = sorted(containers, key=lambda c: c.get('z_index', 0))
            logger.info(f"--- [PPTReplicator]: 【混合渲染】插入{len(sorted_containers)}个容器图片（作为背景）")
            for container in sorted_containers:
                self._insert_container_image(slide, container)
            
            # 2. 插入文本（顶层，可编辑）
            # 对于卡片内的文本，需要根据容器位置计算文本位置
            logger.info(f"--- [PPTReplicator]: 【混合渲染】插入{len(texts)}个文本元素（可编辑）")
            for text in texts:
                # 检查文本是否在容器内
                text_in_container = False
                container_for_text = None
                
                text_x = text['position']['x']
                text_y = text['position']['y']
                text_w = text['size']['width']
                text_h = text['size']['height']
                
                for container in sorted_containers:
                    cont_x = container['position']['x']
                    cont_y = container['position']['y']
                    cont_w = container['size']['width']
                    cont_h = container['size']['height']
                    
                    # 检查文本是否在容器内（允许小范围重叠）
                    if (text_x >= cont_x - 10 and text_y >= cont_y - 10 and
                        text_x + text_w <= cont_x + cont_w + 10 and
                        text_y + text_h <= cont_y + cont_h + 10):
                        text_in_container = True
                        container_for_text = container
                        break
                
                if text_in_container and container_for_text:
                    # 文本在容器内：在容器上方插入文本（可编辑）
                    # 注意：容器图片已经包含了样式，文本只需要内容
                    self._insert_text_on_container(slide, text, container_for_text)
                else:
                    # 文本不在容器内：独立插入
                    self._insert_text(slide, text)
        else:
            # 【旧方法】：只插入容器图片，文本已包含在图片中
            sorted_containers = sorted(containers, key=lambda c: c.get('z_index', 0))
            logger.info(f"--- [PPTReplicator]: 插入{len(sorted_containers)}个容器图片（文本已包含在容器图片中）")
            for container in sorted_containers:
                self._insert_container_image(slide, container)
            
            # 只插入不在容器内的文本
            texts_to_insert = []
            for text in texts:
                text_in_container = False
                text_x = text['position']['x']
                text_y = text['position']['y']
                text_w = text['size']['width']
                text_h = text['size']['height']
                
                for container in sorted_containers:
                    cont_x = container['position']['x']
                    cont_y = container['position']['y']
                    cont_w = container['size']['width']
                    cont_h = container['size']['height']
                    
                    if (text_x >= cont_x - 10 and text_y >= cont_y - 10 and
                        text_x + text_w <= cont_x + cont_w + 10 and
                        text_y + text_h <= cont_y + cont_h + 10):
                        text_in_container = True
                        break
                
                if not text_in_container:
                    texts_to_insert.append(text)
            
            if texts_to_insert:
                logger.info(f"--- [PPTReplicator]: 插入{len(texts_to_insert)}个独立文本元素")
                for text in texts_to_insert:
                    self._insert_text(slide, text)
        
        logger.info("--- [PPTReplicator]: Slide replicated")
    
    def _insert_container_image(self, slide, container: Dict[str, Any]):
        """插入容器图片"""
        try:
            image_path = container['image_path']
            if not Path(image_path).exists():
                logger.warning(f"--- [PPTReplicator]: Image not found: {image_path}")
                return
            
            # 转换坐标
            browser_x = container['position']['x']
            browser_y = container['position']['y']
            browser_w = container['size']['width']
            browser_h = container['size']['height']
            
            ppt_x, ppt_y = self.mapper.browser_to_ppt(browser_x, browser_y)
            ppt_width, ppt_height = self.mapper.browser_size_to_ppt(browser_w, browser_h)
            
            # 【日志探针】记录插入信息
            logger.info(f"--- [PPTReplicator]: 【容器图片】")
            logger.info(f"    浏览器位置: ({browser_x:.1f}px, {browser_y:.1f}px)")
            logger.info(f"    浏览器尺寸: {browser_w:.1f}px × {browser_h:.1f}px")
            logger.info(f"    PPT位置: ({ppt_x:.2f}cm, {ppt_y:.2f}cm)")
            logger.info(f"    PPT尺寸: {ppt_width:.2f}cm × {ppt_height:.2f}cm")
            logger.info(f"    覆盖区域: x=[{ppt_x:.2f}, {ppt_x+ppt_width:.2f}], y=[{ppt_y:.2f}, {ppt_y+ppt_height:.2f}]")
            
            # 检查是否超出边界
            if ppt_x < 0 or ppt_y < 0:
                logger.warning(f"--- [PPTReplicator]: ⚠️ 位置超出边界 (x={ppt_x:.2f}, y={ppt_y:.2f})")
            if ppt_x + ppt_width > self.mapper.PPT_WIDTH_CM or ppt_y + ppt_height > self.mapper.PPT_HEIGHT_CM:
                logger.warning(f"--- [PPTReplicator]: ⚠️ 尺寸超出边界")
            
            # 插入图片
            slide.shapes.add_picture(
                image_path,
                Cm(ppt_x),
                Cm(ppt_y),
                Cm(ppt_width),
                Cm(ppt_height)
            )
            
            logger.debug(f"--- [PPTReplicator]: Inserted container image at ({ppt_x:.2f}cm, {ppt_y:.2f}cm)")
        except Exception as e:
            logger.warning(f"--- [PPTReplicator]: Failed to insert container image: {e}")
            import traceback
            logger.debug(traceback.format_exc())
    
    def _insert_text_on_container(
        self, 
        slide, 
        text: Dict[str, Any], 
        container: Dict[str, Any]
    ):
        """
        在容器上方插入文本（混合渲染法）
        
        文本位置相对于容器，需要考虑容器的内边距
        
        Args:
            slide: PPT 幻灯片对象
            text: 文本信息
            container: 容器信息
        """
        try:
            # 计算文本相对于容器的位置
            # 假设容器有 24px 内边距（padding-lg）
            container_padding = 24  # px
            
            # 文本在浏览器中的绝对位置
            text_x = text['position']['x']
            text_y = text['position']['y']
            text_w = text['size']['width']
            text_h = text['size']['height']
            
            # 容器在浏览器中的绝对位置
            cont_x = container['position']['x']
            cont_y = container['position']['y']
            
            # 转换坐标
            ppt_x, ppt_y = self.mapper.browser_to_ppt(text_x, text_y)
            ppt_width, ppt_height = self.mapper.browser_size_to_ppt(text_w, text_h)
            
            logger.info(f"--- [PPTReplicator]: 【混合渲染】在容器上方插入文本")
            logger.info(f"    文本浏览器位置: ({text_x:.1f}px, {text_y:.1f}px)")
            logger.info(f"    容器浏览器位置: ({cont_x:.1f}px, {cont_y:.1f}px)")
            logger.info(f"    PPT位置: ({ppt_x:.2f}cm, {ppt_y:.2f}cm)")
            
            # 插入文本框（可编辑）
            textbox = slide.shapes.add_textbox(
                Cm(ppt_x),
                Cm(ppt_y),
                Cm(ppt_width),
                Cm(ppt_height)
            )
            
            # 设置文本内容
            tf = textbox.text_frame
            tf.text = text.get('content', '')
            tf.word_wrap = True
            
            # 设置文本样式
            if tf.paragraphs:
                para = tf.paragraphs[0]
                text_style = text.get('style', {})
                
                # 对齐方式
                text_align = text_style.get('textAlign', 'left')
                if text_align == 'center':
                    para.alignment = PP_ALIGN.CENTER
                elif text_align == 'right':
                    para.alignment = PP_ALIGN.RIGHT
                else:
                    para.alignment = PP_ALIGN.LEFT
                
                if para.runs:
                    run = para.runs[0]
                    # 字号（从px转换为pt）
                    font_size_str = text_style.get('fontSize', '14px')
                    font_size_pt = self._px_to_pt(font_size_str)
                    run.font.size = Pt(font_size_pt)
                    
                    # 字重
                    font_weight = text_style.get('fontWeight', '400')
                    run.font.bold = (font_weight == '600' or font_weight == '700' or font_weight == 'bold')
                    
                    # 颜色
                    color_str = text_style.get('color', '#000000')
                    run.font.color.rgb = self._parse_color(color_str)
            
            logger.debug(f"--- [PPTReplicator]: Inserted text on container at ({ppt_x:.2f}cm, {ppt_y:.2f}cm)")
        except Exception as e:
            logger.warning(f"--- [PPTReplicator]: Failed to insert text on container: {e}")
            import traceback
            logger.debug(traceback.format_exc())
    
    def _insert_text(self, slide, text: Dict[str, Any]):
        """插入文本"""
        try:
            browser_x = text['position']['x']
            browser_y = text['position']['y']
            browser_w = text['size']['width']
            browser_h = text['size']['height']
            
            # 转换坐标
            ppt_x, ppt_y = self.mapper.browser_to_ppt(browser_x, browser_y)
            ppt_width, ppt_height = self.mapper.browser_size_to_ppt(browser_w, browser_h)
            
            # 【日志探针】记录插入信息
            logger.info(f"--- [PPTReplicator]: 【文本】")
            logger.info(f"    浏览器位置: ({browser_x:.1f}px, {browser_y:.1f}px)")
            logger.info(f"    浏览器尺寸: {browser_w:.1f}px × {browser_h:.1f}px")
            logger.info(f"    PPT位置: ({ppt_x:.2f}cm, {ppt_y:.2f}cm)")
            logger.info(f"    PPT尺寸: {ppt_width:.2f}cm × {ppt_height:.2f}cm")
            logger.info(f"    文本内容: {text['text'][:50]}...")
            logger.info(f"    覆盖区域: x=[{ppt_x:.2f}, {ppt_x+ppt_width:.2f}], y=[{ppt_y:.2f}, {ppt_y+ppt_height:.2f}]")
            
            # 检查是否超出边界
            if ppt_x < 0 or ppt_y < 0:
                logger.warning(f"--- [PPTReplicator]: ⚠️ 位置超出边界 (x={ppt_x:.2f}, y={ppt_y:.2f})")
            if ppt_x + ppt_width > self.mapper.PPT_WIDTH_CM or ppt_y + ppt_height > self.mapper.PPT_HEIGHT_CM:
                logger.warning(f"--- [PPTReplicator]: ⚠️ 尺寸超出边界")
            
            # 创建文本框
            textbox = slide.shapes.add_textbox(
                Cm(ppt_x),
                Cm(ppt_y),
                Cm(ppt_width),
                Cm(ppt_height)
            )
            
            # 设置文本
            text_frame = textbox.text_frame
            text_frame.text = text['text']
            text_frame.word_wrap = True
            
            # 应用样式
            style = text['style']
            para = text_frame.paragraphs[0]
            run = para.runs[0]
            
            # 字体
            run.font.name = style.get('font_family', 'Arial')
            run.font.size = Pt(style.get('font_size_pt', 14))
            run.font.bold = style.get('is_bold', False)
            
            # 颜色
            color_hex = style.get('color_hex', '#000000')
            run.font.color.rgb = self._hex_to_rgb(color_hex)
            
            # 对齐方式
            text_align = style.get('text_align', 'left')
            if text_align == 'center':
                para.alignment = PP_ALIGN.CENTER
            elif text_align == 'right':
                para.alignment = PP_ALIGN.RIGHT
            else:
                para.alignment = PP_ALIGN.LEFT
            
            logger.debug(f"--- [PPTReplicator]: Inserted text at ({ppt_x:.2f}cm, {ppt_y:.2f}cm): {text['text'][:30]}...")
        except Exception as e:
            logger.warning(f"--- [PPTReplicator]: Failed to insert text: {e}")
            import traceback
            logger.debug(traceback.format_exc())
    
    def _hex_to_rgb(self, hex_color: str) -> RGBColor:
        """将hex颜色转换为RGBColor"""
        try:
            if hex_color.startswith('#'):
                r = int(hex_color[1:3], 16)
                g = int(hex_color[3:5], 16)
                b = int(hex_color[5:7], 16)
                return RGBColor(r, g, b)
        except:
            pass
        return RGBColor(0, 0, 0)  # 默认黑色
    
    def save(self, output_path: Optional[Path] = None) -> Path:
        """
        保存PPT
        
        Args:
            output_path: 输出路径（如果未提供，使用初始化时的路径）
            
        Returns:
            保存的文件路径
        """
        if output_path is None:
            output_path = self.output_path
        
        if output_path is None:
            from datetime import datetime
            output_path = Path(f"replicated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.prs.save(str(output_path))
        logger.info(f"--- [PPTReplicator]: PPT saved to {output_path}")
        return output_path


```


## File: browser_to_ppt_replicator/replicator.py

```python
"""
浏览器到PPT复刻器 - 主入口
整合所有模块，实现完整的复刻流程
"""

from pathlib import Path
from typing import Optional, Dict, Any
from loguru import logger

from .browser_renderer import BrowserRenderer
from .element_analyzer import ElementAnalyzer
from .coordinate_mapper import CoordinateMapper
from .container_extractor import ContainerExtractor
from .text_extractor import TextExtractor
from .ppt_replicator import PPTReplicator


class BrowserToPPTReplicator:
    """
    浏览器到PPT复刻器
    将浏览器渲染的Ant Design/AntV组件一比一复刻到PPT
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        初始化复刻器
        
        Args:
            output_dir: 输出目录（容器图片和PPT文件）
        """
        if output_dir is None:
            output_dir = Path.cwd() / "replicated_outputs"
        else:
            output_dir = Path(output_dir)
        
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建子目录
        self.containers_dir = self.output_dir / "containers"
        self.containers_dir.mkdir(exist_ok=True)
        
        # 初始化组件
        self.coordinate_mapper = CoordinateMapper()
        self.element_analyzer = ElementAnalyzer()
        self.container_extractor = ContainerExtractor(self.containers_dir)
        self.text_extractor = TextExtractor()
        
        logger.info(f"--- [BrowserToPPTReplicator]: Initialized, output_dir: {self.output_dir}")
    
    async def replicate(
        self,
        html_content: str,
        output_ppt_path: Optional[Path] = None
    ) -> Path:
        """
        复刻HTML内容到PPT
        
        Args:
            html_content: HTML内容字符串（包含Ant Design组件）
            output_ppt_path: 输出PPT路径
            
        Returns:
            生成的PPT文件路径
        """
        logger.info("="*80)
        logger.info("--- [BrowserToPPTReplicator]: Starting replication process...")
        logger.info("="*80)
        
        # 1. 浏览器渲染
        logger.info("--- [Step 1/5]: Rendering HTML in browser...")
        browser_renderer = BrowserRenderer()
        page = await browser_renderer.render_html(html_content)
        
        try:
            # 2. 分析元素
            logger.info("--- [Step 2/5]: Analyzing page elements...")
            elements = await self.element_analyzer.analyze_elements(page)
            containers_info = elements['containers']
            texts_info = elements['texts']
            
            # 3. 提取容器（截图）
            # 【新架构原则】：使用混合渲染法，隐藏文字后截图
            logger.info("--- [Step 3/5]: Extracting containers (screenshots with hybrid rendering)...")
            containers = await self.container_extractor.extract_all_containers(
                containers_info, 
                hide_text=True  # 隐藏文字，用于混合渲染
            )
            
            # 4. 提取文本
            logger.info("--- [Step 4/5]: Extracting texts...")
            texts = await self.text_extractor.extract_all_texts(texts_info)
            
            # 5. 复刻到PPT（使用混合渲染法）
            logger.info("--- [Step 5/5]: Replicating to PPT (Hybrid Rendering)...")
            ppt_replicator = PPTReplicator(self.coordinate_mapper, output_ppt_path)
            ppt_replicator.replicate_slide(
                containers, 
                texts,
                use_hybrid_rendering=True  # 使用混合渲染：容器用图片，文本用原生
            )
            
            # 保存PPT
            output_path = ppt_replicator.save(output_ppt_path)
            
            logger.info("="*80)
            logger.info(f"--- [BrowserToPPTReplicator]: Replication completed!")
            logger.info(f"    Output PPT: {output_path}")
            logger.info(f"    Containers: {len(containers)}")
            logger.info(f"    Texts: {len(texts)}")
            logger.info("="*80)
            
            return output_path
            
        finally:
            # 关闭浏览器
            await browser_renderer.close()
    
    async def replicate_from_file(
        self,
        html_file_path: Path,
        output_ppt_path: Optional[Path] = None
    ) -> Path:
        """
        从HTML文件复刻到PPT
        
        Args:
            html_file_path: HTML文件路径
            output_ppt_path: 输出PPT路径
            
        Returns:
            生成的PPT文件路径
        """
        html_content = Path(html_file_path).read_text(encoding='utf-8')
        return await self.replicate(html_content, output_ppt_path)


```


## File: browser_to_ppt_replicator/text_extractor.py

```python
"""
文本提取器
提取文本元素的内容和样式信息
"""

from typing import Dict, Any, List, Optional
from loguru import logger
import re


class TextExtractor:
    """
    文本提取器
    提取文本内容、字体、大小、颜色等样式信息
    """
    
    def __init__(self):
        """初始化文本提取器"""
        logger.info("--- [TextExtractor]: Initialized")
    
    async def extract_text(self, text_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        提取文本信息
        
        Args:
            text_info: 文本信息（来自ElementAnalyzer）
            
        Returns:
            提取的文本信息，包含内容和样式
        """
        try:
            style = text_info.get('style', {})
            
            # 解析字体大小（从px转换为pt）
            font_size_pt = self._parse_font_size(style.get('fontSize', '14px'))
            
            # 解析颜色（从rgb/rgba转换为hex）
            color_hex = self._parse_color(style.get('color', '#000000'))
            
            # 解析字重
            font_weight = style.get('fontWeight', '400')
            is_bold = font_weight in ['bold', '600', '700', '800', '900']
            
            # 解析对齐方式
            text_align = style.get('textAlign', 'left')
            
            return {
                'text': text_info.get('text', ''),
                'position': text_info.get('position', {}),
                'size': text_info.get('size', {}),
                'style': {
                    'font_family': style.get('fontFamily', 'Arial'),
                    'font_size_pt': font_size_pt,
                    'color_hex': color_hex,
                    'is_bold': is_bold,
                    'text_align': text_align,
                    'line_height': style.get('lineHeight', '1.5'),
                }
            }
        except Exception as e:
            logger.warning(f"--- [TextExtractor]: Failed to extract text: {e}")
            return None
    
    async def extract_all_texts(self, texts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        提取所有文本
        
        Args:
            texts: 文本信息列表
            
        Returns:
            提取结果列表
        """
        logger.info(f"--- [TextExtractor]: Extracting {len(texts)} text elements...")
        
        extracted = []
        for text_info in texts:
            result = await self.extract_text(text_info)
            if result:
                extracted.append(result)
        
        logger.info(f"--- [TextExtractor]: Extracted {len(extracted)} text elements")
        return extracted
    
    def _parse_font_size(self, font_size_str: str) -> int:
        """
        解析字体大小（px转pt）
        
        Args:
            font_size_str: 字体大小字符串，如 "14px", "1.2em"
            
        Returns:
            字体大小（pt）
        """
        try:
            # 提取数字
            match = re.search(r'([\d.]+)', font_size_str)
            if match:
                size_value = float(match.group(1))
                
                # 如果是px，直接转换为pt（1px ≈ 0.75pt，但PPT中通常直接使用px值）
                if 'px' in font_size_str:
                    return int(size_value)
                # 如果是em，假设基础字体是14px
                elif 'em' in font_size_str:
                    return int(size_value * 14)
                else:
                    return int(size_value)
        except:
            pass
        
        return 14  # 默认值
    
    def _parse_color(self, color_str: str) -> str:
        """
        解析颜色（rgb/rgba转hex）
        
        Args:
            color_str: 颜色字符串，如 "rgb(24, 144, 255)", "rgba(0,0,0,0.85)", "#1890ff"
            
        Returns:
            hex颜色字符串，如 "#1890ff"
        """
        try:
            # 如果是hex格式，直接返回
            if color_str.startswith('#'):
                return color_str
            
            # 解析rgb/rgba
            rgb_match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', color_str)
            if rgb_match:
                r = int(rgb_match.group(1))
                g = int(rgb_match.group(2))
                b = int(rgb_match.group(3))
                return f"#{r:02x}{g:02x}{b:02x}"
        except:
            pass
        
        return "#000000"  # 默认黑色


```
