"""
Configuration management for the AI Research Lab Simulator.
Uses OpenAI as the single LLM provider.
"""

import os
import yaml
from typing import Dict, Any, List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class LLMConfig(BaseSettings):
    """LLM configuration from environment variables."""
    api_key: str = ""
    model: str = "gpt-4o-mini"  # Default model
    temperature: float = 0.7
    max_tokens: int = 2000
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",  # Ignore extra env vars
    }
    
    def __init__(self, **kwargs):
        # Override with direct env vars
        super().__init__(**kwargs)
        # Get values from environment
        if not self.api_key:
            self.api_key = os.getenv("OPENAI_API_KEY", "") or os.getenv("LLM_API_KEY", "")
        if not self.model or self.model == "gpt-4o-mini":
            self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        try:
            self.temperature = float(os.getenv("LLM_TEMPERATURE", str(self.temperature)))
            self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", str(self.max_tokens)))
        except (ValueError, TypeError):
            pass


class Config:
    """Main configuration class."""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.llm_config = LLMConfig()
        self._load_yaml_config()
        self._pipeline_config_cache = None  # Cache for pipeline config
    
    def _load_yaml_config(self):
        """Load YAML configuration file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.yaml_config = yaml.safe_load(f)
        else:
            self.yaml_config = {}
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration."""
        return {
            "api_key": self.llm_config.api_key,
            "model": self.llm_config.model,
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
        if self._pipeline_config_cache is not None:
            return self._pipeline_config_cache
        
        pipeline_config = self.yaml_config.get("pipeline", {})
        
        # Ensure numeric types from environment variables
        default_config = {
            "max_iterations": 5,
            "convergence_threshold": 0.85,
        }
        
        # Merge and convert types
        result = default_config.copy()
        result.update(pipeline_config)
        
        # Convert string values to proper types
        if "convergence_threshold" in result:
            try:
                result["convergence_threshold"] = float(result["convergence_threshold"])
            except (ValueError, TypeError):
                result["convergence_threshold"] = 0.85
        
        if "max_iterations" in result:
            try:
                result["max_iterations"] = int(result["max_iterations"])
            except (ValueError, TypeError):
                result["max_iterations"] = 5
        
        self._pipeline_config_cache = result
        return result
    
    @property
    def pipeline_config(self) -> Dict[str, Any]:
        """Property access to pipeline config for UI compatibility."""
        return self.get_pipeline_config()
    
    def update_pipeline_config(self, key: str, value: Any):
        """Update pipeline config value."""
        config = self.get_pipeline_config()
        config[key] = value
        self._pipeline_config_cache = config
    
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
