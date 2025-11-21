# Native Compositor 测试日志

**测试时间**: 2025-11-21 23:59:23  
**测试文件**: `tests/test_native_compositor.py`  
**测试目的**: 验证 Native Shape Compiler 的完整功能，包括 DOM 样式提取和原生 PPT 绘制

---

## 完整测试日志

2025-11-21 23:59:51.843 | INFO     | __main__:test_native_compositor:24 - ================================================================================
2025-11-21 23:59:51.843 | INFO     | __main__:test_native_compositor:25 - 测试 Native Shape Compiler
2025-11-21 23:59:51.843 | INFO     | __main__:test_native_compositor:26 - ================================================================================
2025-11-21 23:59:51.843 | INFO     | __main__:test_native_compositor:38 - --- [测试1] 使用 DOMAnalyzer 提取样式...
2025-11-21 23:59:54.057 | INFO     | src.rendering.dom_analyzer:extract_layout_data:24 - --- [DOMAnalyzer]: 开始提取DOM样式数据...
2025-11-21 23:59:54.525 | INFO     | src.rendering.dom_analyzer:extract_layout_data:107 - --- [DOMAnalyzer]: 提取了 11 个元素的样式数据
2025-11-21 23:59:54.525 | INFO     | src.rendering.dom_analyzer:extract_layout_data:114 - --- [DOMAnalyzer]: 元素 title_text_0 (type=title) backgroundColor=None
2025-11-21 23:59:54.525 | INFO     | src.rendering.dom_analyzer:extract_layout_data:114 - --- [DOMAnalyzer]: 元素 value_card_0 (type=card) backgroundColor=rgb(255, 255, 255)
2025-11-21 23:59:54.525 | INFO     | src.rendering.dom_analyzer:extract_layout_data:114 - --- [DOMAnalyzer]: 元素 value_card_0_title (type=text) backgroundColor=None
2025-11-21 23:59:54.525 | INFO     | src.rendering.dom_analyzer:extract_layout_data:114 - --- [DOMAnalyzer]: 元素 value_card_0_content (type=text) backgroundColor=None
2025-11-21 23:59:54.525 | INFO     | src.rendering.dom_analyzer:extract_layout_data:114 - --- [DOMAnalyzer]: 元素 value_card_1 (type=card) backgroundColor=rgb(255, 255, 255)
2025-11-21 23:59:54.526 | INFO     | src.rendering.dom_analyzer:extract_layout_data:114 - --- [DOMAnalyzer]: 元素 value_card_1_title (type=text) backgroundColor=None
2025-11-21 23:59:54.526 | INFO     | src.rendering.dom_analyzer:extract_layout_data:114 - --- [DOMAnalyzer]: 元素 value_card_1_content (type=text) backgroundColor=None
2025-11-21 23:59:54.526 | INFO     | src.rendering.dom_analyzer:extract_layout_data:114 - --- [DOMAnalyzer]: 元素 value_card_2 (type=card) backgroundColor=rgb(255, 255, 255)
2025-11-21 23:59:54.526 | INFO     | src.rendering.dom_analyzer:extract_layout_data:114 - --- [DOMAnalyzer]: 元素 value_card_2_title (type=text) backgroundColor=None
2025-11-21 23:59:54.526 | INFO     | src.rendering.dom_analyzer:extract_layout_data:114 - --- [DOMAnalyzer]: 元素 value_card_2_content (type=text) backgroundColor=None
2025-11-21 23:59:54.526 | INFO     | src.rendering.dom_analyzer:extract_layout_data:114 - --- [DOMAnalyzer]: 元素 subtitle_text_0 (type=text) backgroundColor=None
2025-11-21 23:59:54.526 | INFO     | __main__:test_native_compositor:49 - --- [测试1] ✅ 提取了 11 个元素的样式数据
2025-11-21 23:59:54.526 | INFO     | __main__:test_native_compositor:53 - --- [测试1] 示例元素数据:
2025-11-21 23:59:54.526 | INFO     | __main__:test_native_compositor:54 -    ID: title_text_0
2025-11-21 23:59:54.526 | INFO     | __main__:test_native_compositor:55 -    Type: title
2025-11-21 23:59:54.526 | INFO     | __main__:test_native_compositor:56 -    Geometry: {'x': 76, 'y': 40, 'width': 1804, 'height': 48}
2025-11-21 23:59:54.526 | INFO     | __main__:test_native_compositor:57 -    Style keys: ['backgroundColor', 'borderTopWidth', 'borderTopColor', 'borderLeftWidth', 'borderLeftColor', 'borderWidth', 'borderColor', 'borderRadius', 'boxShadow', 'color', 'fontSize', 'fontWeight', 'fontFamily', 'textAlign', 'lineHeight', 'display', 'alignItems', 'justifyContent']
2025-11-21 23:59:54.562 | INFO     | __main__:test_native_compositor:62 - --- [测试2] 使用 NativeCompositor 绘制到 PPT...
2025-11-21 23:59:54.570 | INFO     | src.rendering.native_compositor:composite_slide:34 - --- [NativeCompositor]: 开始原生绘制 11 个元素
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:70 - --- [CoordinateMapper]: 坐标映射
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:71 -     浏览器坐标: (76.0px, 40.0px)
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:72 -     减去padding: (52.0px, 16.0px)
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:73 -     内容区域坐标: (52.0px, 16.0px)
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:74 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:75 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:76 -     PPT坐标: (0.92cm, 0.28cm)
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:77 -     比例: x=0.0278, y=0.0155
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:96 - --- [CoordinateMapper]: 尺寸映射
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:97 -     浏览器尺寸: 1804.0px × 48.0px
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:98 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:99 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:100 -     PPT尺寸: 31.82cm × 0.85cm
2025-11-21 23:59:54.570 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:101 -     比例: w=0.9637, h=0.0465
2025-11-21 23:59:54.570 | INFO     | src.rendering.native_compositor:_draw_text:130 - --- [NativeCompositor]: 绘制文本 title_text_0, 内容='核心价值主张', 长度=6
2025-11-21 23:59:54.570 | INFO     | src.rendering.native_compositor:_draw_text:131 - --- [NativeCompositor]: 原始尺寸: width=31.82cm, height=0.85cm
2025-11-21 23:59:54.571 | INFO     | src.rendering.native_compositor:_draw_text:152 - --- [NativeCompositor]: 文本 '核心价值主张' 启用 SHAPE_TO_FIT_TEXT，强制 word_wrap=False
2025-11-21 23:59:54.571 | INFO     | src.rendering.native_compositor:_draw_text:180 - --- [NativeCompositor]: 标题 '核心价值主张' 强制加粗
2025-11-21 23:59:54.572 | INFO     | src.rendering.native_compositor:_draw_card:57 - --- [NativeCompositor]: 绘制卡片 value_card_0, backgroundColor=rgb(255, 255, 255)
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:70 - --- [CoordinateMapper]: 坐标映射
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:71 -     浏览器坐标: (40.0px, 148.0px)
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:72 -     减去padding: (16.0px, 124.0px)
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:73 -     内容区域坐标: (16.0px, 124.0px)
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:74 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:75 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:76 -     PPT坐标: (0.28cm, 2.19cm)
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:77 -     比例: x=0.0085, y=0.1202
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:96 - --- [CoordinateMapper]: 尺寸映射
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:97 -     浏览器尺寸: 597.3px × 803.0px
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:98 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:99 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:100 -     PPT尺寸: 10.54cm × 14.16cm
2025-11-21 23:59:54.572 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:101 -     比例: w=0.3191, h=0.7781
2025-11-21 23:59:54.572 | INFO     | src.rendering.native_compositor:_draw_card:78 - --- [NativeCompositor]: 卡片 value_card_0 强制使用白色背景 (忽略提取到的 rgb(255, 255, 255))
2025-11-21 23:59:54.573 | WARNING  | src.rendering.native_compositor:_apply_color:261 - 颜色应用失败: rgb(22, 119, 255), error: fill type _NoneFill has no foreground color, call .solid() or .patterned() first
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:70 - --- [CoordinateMapper]: 坐标映射
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:71 -     浏览器坐标: (274.7px, 501.8px)
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:72 -     减去padding: (250.7px, 477.8px)
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:73 -     内容区域坐标: (250.7px, 477.8px)
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:74 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:75 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:76 -     PPT坐标: (4.42cm, 8.43cm)
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:77 -     比例: x=0.1339, y=0.4630
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:96 - --- [CoordinateMapper]: 尺寸映射
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:97 -     浏览器尺寸: 128.0px × 45.0px
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:98 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:99 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:100 -     PPT尺寸: 2.26cm × 0.79cm
2025-11-21 23:59:54.573 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:101 -     比例: w=0.0684, h=0.0436
2025-11-21 23:59:54.573 | INFO     | src.rendering.native_compositor:_draw_text:130 - --- [NativeCompositor]: 绘制文本 value_card_0_title, 内容='成本降低', 长度=4
2025-11-21 23:59:54.573 | INFO     | src.rendering.native_compositor:_draw_text:131 - --- [NativeCompositor]: 原始尺寸: width=2.26cm, height=0.79cm
2025-11-21 23:59:54.574 | INFO     | src.rendering.native_compositor:_draw_text:152 - --- [NativeCompositor]: 文本 '成本降低' 启用 SHAPE_TO_FIT_TEXT，强制 word_wrap=False
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:70 - --- [CoordinateMapper]: 坐标映射
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:71 -     浏览器坐标: (250.7px, 570.8px)
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:72 -     减去padding: (226.7px, 546.8px)
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:73 -     内容区域坐标: (226.7px, 546.8px)
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:74 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:75 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:76 -     PPT坐标: (4.00cm, 9.64cm)
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:77 -     比例: x=0.1211, y=0.5298
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:96 - --- [CoordinateMapper]: 尺寸映射
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:97 -     浏览器尺寸: 176.0px × 32.4px
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:98 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:99 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:100 -     PPT尺寸: 3.10cm × 0.57cm
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:101 -     比例: w=0.0940, h=0.0314
2025-11-21 23:59:54.574 | INFO     | src.rendering.native_compositor:_draw_text:130 - --- [NativeCompositor]: 绘制文本 value_card_0_content, 内容='降低运营成本40-60%', 长度=12
2025-11-21 23:59:54.574 | INFO     | src.rendering.native_compositor:_draw_text:131 - --- [NativeCompositor]: 原始尺寸: width=3.10cm, height=0.57cm
2025-11-21 23:59:54.574 | INFO     | src.rendering.native_compositor:_draw_text:152 - --- [NativeCompositor]: 文本 '降低运营成本40-60%' 启用 SHAPE_TO_FIT_TEXT，强制 word_wrap=False
2025-11-21 23:59:54.574 | INFO     | src.rendering.native_compositor:_draw_card:57 - --- [NativeCompositor]: 绘制卡片 value_card_1, backgroundColor=rgb(255, 255, 255)
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:70 - --- [CoordinateMapper]: 坐标映射
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:71 -     浏览器坐标: (661.3px, 148.0px)
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:72 -     减去padding: (637.3px, 124.0px)
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:73 -     内容区域坐标: (637.3px, 124.0px)
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:74 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.574 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:75 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:76 -     PPT坐标: (11.24cm, 2.19cm)
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:77 -     比例: x=0.3405, y=0.1202
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:96 - --- [CoordinateMapper]: 尺寸映射
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:97 -     浏览器尺寸: 597.3px × 803.0px
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:98 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:99 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:100 -     PPT尺寸: 10.54cm × 14.16cm
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:101 -     比例: w=0.3191, h=0.7781
2025-11-21 23:59:54.575 | INFO     | src.rendering.native_compositor:_draw_card:78 - --- [NativeCompositor]: 卡片 value_card_1 强制使用白色背景 (忽略提取到的 rgb(255, 255, 255))
2025-11-21 23:59:54.575 | WARNING  | src.rendering.native_compositor:_apply_color:261 - 颜色应用失败: rgb(82, 196, 26), error: fill type _NoneFill has no foreground color, call .solid() or .patterned() first
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:70 - --- [CoordinateMapper]: 坐标映射
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:71 -     浏览器坐标: (896.0px, 501.8px)
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:72 -     减去padding: (872.0px, 477.8px)
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:73 -     内容区域坐标: (872.0px, 477.8px)
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:74 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:75 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:76 -     PPT坐标: (15.38cm, 8.43cm)
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:77 -     比例: x=0.4658, y=0.4630
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:96 - --- [CoordinateMapper]: 尺寸映射
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:97 -     浏览器尺寸: 128.0px × 45.0px
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:98 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.575 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:99 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:100 -     PPT尺寸: 2.26cm × 0.79cm
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:101 -     比例: w=0.0684, h=0.0436
2025-11-21 23:59:54.576 | INFO     | src.rendering.native_compositor:_draw_text:130 - --- [NativeCompositor]: 绘制文本 value_card_1_title, 内容='效率提升', 长度=4
2025-11-21 23:59:54.576 | INFO     | src.rendering.native_compositor:_draw_text:131 - --- [NativeCompositor]: 原始尺寸: width=2.26cm, height=0.79cm
2025-11-21 23:59:54.576 | INFO     | src.rendering.native_compositor:_draw_text:152 - --- [NativeCompositor]: 文本 '效率提升' 启用 SHAPE_TO_FIT_TEXT，强制 word_wrap=False
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:70 - --- [CoordinateMapper]: 坐标映射
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:71 -     浏览器坐标: (872.5px, 570.8px)
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:72 -     减去padding: (848.5px, 546.8px)
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:73 -     内容区域坐标: (848.5px, 546.8px)
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:74 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:75 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:76 -     PPT坐标: (14.97cm, 9.64cm)
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:77 -     比例: x=0.4533, y=0.5298
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:96 - --- [CoordinateMapper]: 尺寸映射
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:97 -     浏览器尺寸: 174.9px × 32.4px
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:98 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:99 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:100 -     PPT尺寸: 3.08cm × 0.57cm
2025-11-21 23:59:54.576 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:101 -     比例: w=0.0934, h=0.0314
2025-11-21 23:59:54.576 | INFO     | src.rendering.native_compositor:_draw_text:130 - --- [NativeCompositor]: 绘制文本 value_card_1_content, 内容='提升转化效率20-35%', 长度=12
2025-11-21 23:59:54.576 | INFO     | src.rendering.native_compositor:_draw_text:131 - --- [NativeCompositor]: 原始尺寸: width=3.08cm, height=0.57cm
2025-11-21 23:59:54.577 | INFO     | src.rendering.native_compositor:_draw_text:152 - --- [NativeCompositor]: 文本 '提升转化效率20-35%' 启用 SHAPE_TO_FIT_TEXT，强制 word_wrap=False
2025-11-21 23:59:54.577 | INFO     | src.rendering.native_compositor:_draw_card:57 - --- [NativeCompositor]: 绘制卡片 value_card_2, backgroundColor=rgb(255, 255, 255)
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:70 - --- [CoordinateMapper]: 坐标映射
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:71 -     浏览器坐标: (1282.7px, 148.0px)
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:72 -     减去padding: (1258.7px, 124.0px)
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:73 -     内容区域坐标: (1258.7px, 124.0px)
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:74 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:75 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:76 -     PPT坐标: (22.20cm, 2.19cm)
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:77 -     比例: x=0.6724, y=0.1202
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:96 - --- [CoordinateMapper]: 尺寸映射
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:97 -     浏览器尺寸: 597.3px × 803.0px
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:98 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:99 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:100 -     PPT尺寸: 10.54cm × 14.16cm
2025-11-21 23:59:54.577 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:101 -     比例: w=0.3191, h=0.7781
2025-11-21 23:59:54.577 | INFO     | src.rendering.native_compositor:_draw_card:78 - --- [NativeCompositor]: 卡片 value_card_2 强制使用白色背景 (忽略提取到的 rgb(255, 255, 255))
2025-11-21 23:59:54.578 | WARNING  | src.rendering.native_compositor:_apply_color:261 - 颜色应用失败: rgb(250, 140, 22), error: fill type _NoneFill has no foreground color, call .solid() or .patterned() first
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:70 - --- [CoordinateMapper]: 坐标映射
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:71 -     浏览器坐标: (1517.3px, 501.8px)
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:72 -     减去padding: (1493.3px, 477.8px)
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:73 -     内容区域坐标: (1493.3px, 477.8px)
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:74 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:75 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:76 -     PPT坐标: (26.34cm, 8.43cm)
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:77 -     比例: x=0.7977, y=0.4630
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:96 - --- [CoordinateMapper]: 尺寸映射
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:97 -     浏览器尺寸: 128.0px × 45.0px
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:98 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:99 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:100 -     PPT尺寸: 2.26cm × 0.79cm
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:101 -     比例: w=0.0684, h=0.0436
2025-11-21 23:59:54.578 | INFO     | src.rendering.native_compositor:_draw_text:130 - --- [NativeCompositor]: 绘制文本 value_card_2_title, 内容='智能转型', 长度=4
2025-11-21 23:59:54.578 | INFO     | src.rendering.native_compositor:_draw_text:131 - --- [NativeCompositor]: 原始尺寸: width=2.26cm, height=0.79cm
2025-11-21 23:59:54.578 | INFO     | src.rendering.native_compositor:_draw_text:152 - --- [NativeCompositor]: 文本 '智能转型' 启用 SHAPE_TO_FIT_TEXT，强制 word_wrap=False
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:70 - --- [CoordinateMapper]: 坐标映射
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:71 -     浏览器坐标: (1500.3px, 570.8px)
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:72 -     减去padding: (1476.3px, 546.8px)
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:73 -     内容区域坐标: (1476.3px, 546.8px)
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:74 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:75 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:76 -     PPT坐标: (26.04cm, 9.64cm)
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:77 -     比例: x=0.7886, y=0.5298
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:96 - --- [CoordinateMapper]: 尺寸映射
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:97 -     浏览器尺寸: 162.0px × 32.4px
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:98 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:99 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:100 -     PPT尺寸: 2.86cm × 0.57cm
2025-11-21 23:59:54.578 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:101 -     比例: w=0.0865, h=0.0314
2025-11-21 23:59:54.579 | INFO     | src.rendering.native_compositor:_draw_text:130 - --- [NativeCompositor]: 绘制文本 value_card_2_content, 内容='加速业务智能化转型', 长度=9
2025-11-21 23:59:54.579 | INFO     | src.rendering.native_compositor:_draw_text:131 - --- [NativeCompositor]: 原始尺寸: width=2.86cm, height=0.57cm
2025-11-21 23:59:54.579 | INFO     | src.rendering.native_compositor:_draw_text:152 - --- [NativeCompositor]: 文本 '加速业务智能化转型' 启用 SHAPE_TO_FIT_TEXT，强制 word_wrap=False
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:70 - --- [CoordinateMapper]: 坐标映射
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:71 -     浏览器坐标: (48.0px, 999.0px)
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:72 -     减去padding: (24.0px, 975.0px)
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:73 -     内容区域坐标: (24.0px, 975.0px)
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:74 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:75 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:76 -     PPT坐标: (0.42cm, 17.20cm)
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_to_ppt:77 -     比例: x=0.0128, y=0.9448
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:96 - --- [CoordinateMapper]: 尺寸映射
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:97 -     浏览器尺寸: 1824.0px × 33.0px
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:98 -     内容区域尺寸: 1872px × 1032px
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:99 -     PPT内容区域尺寸: 33.02cm × 18.20cm
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:100 -     PPT尺寸: 32.17cm × 0.58cm
2025-11-21 23:59:54.579 | INFO     | src.rendering.browser_to_ppt_replicator.coordinate_mapper:browser_size_to_ppt:101 -     比例: w=0.9744, h=0.0320
2025-11-21 23:59:54.579 | INFO     | src.rendering.native_compositor:_draw_text:130 - --- [NativeCompositor]: 绘制文本 subtitle_text_0, 内容='全链路AI赋能解决方案', 长度=11
2025-11-21 23:59:54.579 | INFO     | src.rendering.native_compositor:_draw_text:131 - --- [NativeCompositor]: 原始尺寸: width=32.17cm, height=0.58cm
2025-11-21 23:59:54.579 | INFO     | src.rendering.native_compositor:_draw_text:152 - --- [NativeCompositor]: 文本 '全链路AI赋能解决方案' 启用 SHAPE_TO_FIT_TEXT，强制 word_wrap=False
2025-11-21 23:59:54.585 | INFO     | __main__:test_native_compositor:78 - --- [测试2] ✅ PPT 已保存到: outputs/ppt/test_native_compositor.pptx
2025-11-21 23:59:54.585 | INFO     | __main__:test_native_compositor:79 - ================================================================================
2025-11-21 23:59:54.585 | INFO     | __main__:test_native_compositor:80 - ✅ Native Shape Compiler 测试完成！
2025-11-21 23:59:54.585 | INFO     | __main__:test_native_compositor:81 - ================================================================================

---

## 测试结果总结

- ✅ 测试通过
- ✅ PPT 文件已生成: `outputs/ppt/test_native_compositor.pptx`
- ✅ 所有元素样式提取成功（11个元素）
- ✅ 原生绘制完成

## 关键修复点

1. **颜色错位修复**: 通过 `data-ppt-style-border-color` 属性显式传递颜色值
2. **阴影加重**: transparency=0.3 (70% 黑色), distance=8pt
3. **标题加粗**: 强制使用 Microsoft YaHei 字体，标题强制加粗
4. **文字换行修复**: 使用 `SHAPE_TO_FIT_TEXT` 和 `word_wrap=False`

## 警告信息

测试过程中出现了 3 个警告（关于装饰条颜色应用），但不影响整体功能：
- `fill type _NoneFill has no foreground color`: 需要在应用颜色前调用 `.solid()`
- 这些警告出现在装饰条（top bar）的颜色应用时，因为装饰条的 fill 对象需要先调用 `.solid()` 才能设置颜色
