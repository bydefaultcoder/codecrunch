"""
Configuration management for the AI Research Lab Simulator.
Allows easy model swapping without code changes.
"""

import os
import yaml
from typing import Dict, Any, List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class LLMConfig(BaseSettings):
    """LLM configuration from environment variables."""
    provider: str = os.getenv("LLM_PROVIDER", "openai")
    model: str = os.getenv("LLM_MODEL", "gpt-4-turbo-preview")
    api_key: str = os.getenv("LLM_API_KEY", "")
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    max_tokens: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    
    class Config:
        env_file = ".env"


class Config:
    """Main configuration class."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.llm_config = LLMConfig()
        self._load_yaml_config()
    
    def _load_yaml_config(self):
        """Load YAML configuration file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.yaml_config = yaml.safe_load(f)
        else:
            self.yaml_config = {}
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration."""
        # Use appropriate API key based on provider
        provider = self.llm_config.provider.lower()
        if provider == "anthropic":
            api_key = self.llm_config.anthropic_api_key or self.llm_config.api_key
        else:
            api_key = self.llm_config.api_key
        
        return {
            "provider": self.llm_config.provider,
            "model": self.llm_config.model,
            "api_key": api_key,
            "anthropic_api_key": self.llm_config.anthropic_api_key,
            "temperature": self.llm_config.temperature,
            "max_tokens": self.llm_config.max_tokens,
        }
    
    def get_enabled_agents(self) -> List[str]:
        """Get list of enabled agents."""
        return self.yaml_config.get("agents", {}).get("enabled", [
            "researcher", "reviewer", "editor", "fact_checker"
        ])
    
    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Get configuration for a specific agent."""
        return self.yaml_config.get("agents", {}).get(agent_name, {})
    
    def get_pipeline_config(self) -> Dict[str, Any]:
        """Get pipeline configuration."""
        return self.yaml_config.get("pipeline", {
            "max_iterations": 5,
            "convergence_threshold": 0.85,
        })
    
    def get_memory_config(self) -> Dict[str, Any]:
        """Get memory configuration."""
        return self.yaml_config.get("memory", {
            "type": "conversation_buffer",
            "max_context_length": 10000,
        })
    
    def get_evaluation_config(self) -> Dict[str, Any]:
        """Get evaluation configuration."""
        return self.yaml_config.get("evaluation", {})


# Global config instance
config = Config()

