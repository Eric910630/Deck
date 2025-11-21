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

