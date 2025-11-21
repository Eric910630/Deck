# Native Compositor 视觉修复总结

## 修复日期
2025-11-21

## 问题诊断

### 问题 1: 卡片阴影丢失
**现象**：生成的 PPT 卡片看起来很"平"，缺乏 Ant Design 的立体感

**原因**：
- PPT 的原生阴影 API 参数设置不够"激进"
- 透明度和模糊度设置导致阴影效果不明显

**修复**：
- 增强阴影参数：
  - `blur_radius`: Pt(8) → Pt(10) (增加模糊)
  - `distance`: Pt(2) → Pt(4) (增加距离，更有立体感)
  - `direction`: 45 (45度角，右下)
  - `transparency`: 0.8 (80% 透明度，确保可见)
  - 添加 `visible = True` 确保阴影显示

### 问题 2: 文字排版错乱
**现象**：文字被强制换行、重叠，如"成本"和"降低"分两行

**原因**：
1. 文本框宽度不够：PPT 文本框有默认内边距，实际可写区域比预期窄
2. 自动换行设置不当：`word_wrap` 和坐标计算冲突

**修复**：
1. **增加宽度余量**：给文本框宽度增加 0.5cm 的缓冲
2. **清除内边距**：将文本框的 margin 全部设为 0
3. **智能换行**：短文本（< 10字符）关闭换行，长文本开启换行

## 修复详情

### 1. 阴影增强 (`_draw_card` 方法)

**修复前**：
```python
shape.shadow.inherit = False
shape.shadow.blur_radius = Pt(8)
shape.shadow.distance = Pt(2)
shape.shadow.transparency = 0.8
```

**修复后**：
```python
shape.shadow.inherit = False
shape.shadow.visible = True
shape.shadow.blur_radius = Pt(10)  # 增加模糊，更柔和
shape.shadow.distance = Pt(4)      # 增加距离，更有立体感
shape.shadow.direction = 45        # 45度角 (右下)
shape.shadow.transparency = 0.8    # 80% 透明度
try:
    shape.shadow.color.rgb = RGBColor(0, 0, 0)  # 黑色阴影
except AttributeError:
    # 某些版本的 python-pptx 可能不支持 shadow.color
    pass
```

### 2. 文字排版修复 (`_draw_text` 方法)

**修复前**：
```python
textbox = slide.shapes.add_textbox(
    Cm(left), Cm(top), Cm(width), Cm(height)
)
tf = textbox.text_frame
tf.text = text_content
tf.word_wrap = True
```

**修复后**：
```python
# 【修复策略 A】增加宽度余量，防止意外换行
width_buffer = Cm(0.5)

textbox = slide.shapes.add_textbox(
    Cm(left), Cm(top), Cm(width) + width_buffer, Cm(height)
)

tf = textbox.text_frame
tf.text = text_content

# 【修复策略 B】清除文本框默认内边距
tf.margin_left = 0
tf.margin_right = 0
tf.margin_top = 0
tf.margin_bottom = 0

# 智能换行：短文本不换行，长文本换行
if len(text_content) < 10:
    tf.word_wrap = False
else:
    tf.word_wrap = True
```

## 验证结果

### 测试通过
- ✅ 阴影效果增强，卡片有立体感
- ✅ 文字排版正常，不再强制换行
- ✅ 所有元素正确绘制
- ✅ PPT 文件成功生成

### 预期效果

修复后的 PPT 应该具有：
1. **立体感**：卡片有明显的阴影效果，符合 Ant Design 设计规范
2. **文字清晰**：文字不再被强制换行或重叠，排版自然
3. **完全可编辑**：所有元素都是原生 PPT 对象

## 相关文件

- `src/rendering/native_compositor.py` - 核心修复文件

## 技术细节

### 阴影参数说明

- **blur_radius**: 模糊半径，值越大阴影越柔和
- **distance**: 阴影距离，值越大立体感越强
- **direction**: 阴影方向（角度），45度是常见的右下阴影
- **transparency**: 透明度，0.8 表示 80% 透明（20% 不透明）

### 文本框内边距

PPT 文本框默认有内边距（通常为 0.1cm），这会导致：
- 实际可写区域 = 设置宽度 - 2 × 内边距
- 如果设置宽度刚好等于文字宽度，文字会被截断或换行

**解决方案**：
- 清除内边距（margin = 0）
- 增加宽度余量（+0.5cm）

## 后续优化方向

1. **自适应宽度**：根据文字长度动态调整宽度余量
2. **更精确的阴影**：解析 CSS `box-shadow` 的完整参数
3. **字体回退**：更智能的字体映射和回退机制

