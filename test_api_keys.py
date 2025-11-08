"""
Test script to verify API keys are configured correctly.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def test_openai_key():
    """Test OpenAI API key."""
    print("=" * 60)
    print("Testing OpenAI API Key (GPT-4-turbo-preview)")
    print("=" * 60)
    
    api_key = os.getenv("LLM_API_KEY", "")
    
    if not api_key or api_key == "your-api-key-here":
        print("❌ OpenAI API key not set or using placeholder")
        return False
    
    try:
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            api_key=api_key,
            temperature=0.7,
            max_tokens=100
        )
        
        response = llm.invoke("Say 'API key works!' if you can read this.")
        print(f"✅ OpenAI API key is valid!")
        print(f"   Response: {response.content[:100]}")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API key test failed: {e}")
        return False


def test_anthropic_key():
    """Test Anthropic API key."""
    print("\n" + "=" * 60)
    print("Testing Anthropic API Key (Claude 3 Opus)")
    print("=" * 60)
    
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    
    if not api_key or api_key == "your-api-key-here":
        print("❌ Anthropic API key not set or using placeholder")
        return False
    
    try:
        from langchain_anthropic import ChatAnthropic
        
        llm = ChatAnthropic(
            model="claude-3-opus-20240229",
            api_key=api_key,
            temperature=0.7,
            max_tokens=100
        )
        
        response = llm.invoke("Say 'API key works!' if you can read this.")
        print(f"✅ Anthropic API key is valid!")
        print(f"   Response: {response.content[:100]}")
        return True
        
    except ImportError:
        print("❌ langchain-anthropic not installed")
        print("   Install with: pip install langchain-anthropic")
        return False
    except Exception as e:
        print(f"❌ Anthropic API key test failed: {e}")
        return False


def test_langsmith_key():
    """Test LangSmith API key."""
    print("\n" + "=" * 60)
    print("Testing LangSmith API Key")
    print("=" * 60)
    
    api_key = os.getenv("LANGCHAIN_API_KEY", "")
    tracing_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    
    if not tracing_enabled:
        print("⚠️  LangSmith tracing is disabled (LANGCHAIN_TRACING_V2=false)")
        print("   This is optional - tracing will be disabled")
        return None
    
    if not api_key or api_key == "your-langsmith-key-here":
        print("⚠️  LangSmith API key not set or using placeholder")
        print("   This is optional - tracing will be disabled")
        return None
    
    print("✅ LangSmith configuration looks good!")
    print("   Tracing will be enabled when running the pipeline")
    return True


def test_configuration():
    """Test the configuration system."""
    print("\n" + "=" * 60)
    print("Testing Configuration System")
    print("=" * 60)
    
    try:
        from src.config import config
        
        llm_config = config.get_llm_config()
        print(f"✅ Configuration loaded successfully")
        print(f"   Provider: {llm_config['provider']}")
        print(f"   Model: {llm_config['model']}")
        print(f"   Temperature: {llm_config['temperature']}")
        print(f"   Max Tokens: {llm_config['max_tokens']}")
        
        # Test LLM factory
        from src.llm_factory import create_llm
        llm = create_llm()
        print(f"✅ LLM factory created model: {type(llm).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("🔬 AI Research Lab Simulator - API Key Test\n")
    
    results = {
        "OpenAI": test_openai_key(),
        "Anthropic": test_anthropic_key(),
        "LangSmith": test_langsmith_key(),
        "Configuration": test_configuration(),
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for service, result in results.items():
        if result is True:
            print(f"✅ {service}: PASSED")
        elif result is False:
            print(f"❌ {service}: FAILED")
        else:
            print(f"⚠️  {service}: OPTIONAL (not configured)")
    
    print("\n" + "=" * 60)
    
    # Check if at least one LLM provider works
    if results["OpenAI"] or results["Anthropic"]:
        print("✅ At least one LLM provider is configured correctly!")
        print("   You can now run the research pipeline.")
        print("\n   Try: python -m src.main 'Your Research Topic'")
    else:
        print("❌ No LLM providers are configured correctly.")
        print("   Please check your .env file and API keys.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()

