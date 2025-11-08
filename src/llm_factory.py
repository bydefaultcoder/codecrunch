"""
LLM Factory for creating language models based on configuration.
Allows easy swapping of models without code changes.
"""

from typing import Any, Optional
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_core.language_models import BaseChatModel
from src.config import config


def create_llm(
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    model_name: Optional[str] = None
) -> BaseChatModel:
    """
    Create an LLM instance based on configuration.
    
    Args:
        temperature: Override temperature from config
        max_tokens: Override max_tokens from config
        model_name: Override model name from config
    
    Returns:
        BaseChatModel instance
    """
    llm_config = config.get_llm_config()
    provider = llm_config["provider"].lower()
    
    # Use overrides if provided, otherwise use config
    temp = temperature if temperature is not None else llm_config["temperature"]
    tokens = max_tokens if max_tokens is not None else llm_config["max_tokens"]
    model = model_name if model_name is not None else llm_config["model"]
    
    if provider == "openai":
        return ChatOpenAI(
            model=model,
            temperature=temp,
            max_tokens=tokens,
            api_key=llm_config["api_key"] or None,
        )
    elif provider == "anthropic":
        try:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=model,
                temperature=temp,
                max_tokens=tokens,
                api_key=llm_config["api_key"] or None,
            )
        except ImportError:
            raise ImportError("langchain-anthropic not installed. Install with: pip install langchain-anthropic")
    elif provider == "local" or provider == "ollama":
        return Ollama(
            model=model,
            temperature=temp,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
    
    return ChatOpenAI(
        model=model,
        temperature=temp,
        max_tokens=tokens,
    )

