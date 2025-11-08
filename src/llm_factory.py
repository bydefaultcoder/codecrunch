"""
LLM Factory for creating language models based on configuration.
Uses OpenAI as the single LLM provider.
"""

from typing import Optional
from langchain_core.language_models import BaseChatModel
from src.config import config


def create_llm(
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    model_name: Optional[str] = None
) -> BaseChatModel:
    """
    Create an OpenAI LLM instance based on configuration.
    
    Args:
        temperature: Override temperature from config
        max_tokens: Override max_tokens from config
        model_name: Override model name from config
    
    Returns:
        BaseChatModel instance (ChatOpenAI)
    """
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        raise ImportError("langchain-openai not installed. Install with: pip install langchain-openai")
    
    llm_config = config.get_llm_config()
    
    # Use overrides if provided, otherwise use config
    temp = temperature if temperature is not None else llm_config["temperature"]
    tokens = max_tokens if max_tokens is not None else llm_config["max_tokens"]
    model = model_name if model_name is not None else llm_config["model"]
    api_key = llm_config["api_key"] or None
    
    if not api_key:
        raise ValueError(
            "OpenAI API key is not set. Please set OPENAI_API_KEY or LLM_API_KEY in your .env file.\n"
            "Run 'python test_api_keys.py' to verify your configuration."
        )
    
    return ChatOpenAI(
        model=model,
        temperature=temp,
        max_tokens=tokens,
        api_key=api_key,
        timeout=60.0,  # 60 second timeout
        max_retries=2,  # Retry up to 2 times
    )

