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

