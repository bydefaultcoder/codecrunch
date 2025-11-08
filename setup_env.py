"""
Helper script to create .env file from template.
"""

import shutil
from pathlib import Path

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print(".env file already exists. Skipping creation.")
        return
    
    # Create .env.example content
    env_content = """# LLM Configuration - Change these to swap models
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
LLM_API_KEY=your-api-key-here
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# Alternative providers (uncomment to use)
# LLM_PROVIDER=anthropic
# LLM_MODEL=claude-3-opus-20240229
# ANTHROPIC_API_KEY=your-api-key-here

# LangSmith (optional, for monitoring)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key-here

# Research Pipeline Configuration
MAX_ITERATIONS=5
CONVERGENCE_THRESHOLD=0.85
ENABLE_FACT_CHECKING=true
ENABLE_BIAS_DETECTION=true
"""
    
    # Write .env.example
    with open(env_example, "w") as f:
        f.write(env_content)
    print(f"Created {env_example}")
    
    # Copy to .env
    with open(env_file, "w") as f:
        f.write(env_content)
    print(f"Created {env_file}")
    print("\n⚠️  Please edit .env and add your API keys!")

if __name__ == "__main__":
    create_env_file()

