# API Keys Setup Guide

## ✅ Your Current Setup

You have configured:
- ✅ gpt-4.1 (OpenAI)
- ✅ Claude 3 Opus (anthropic/claude-3-haiku)
- ✅ LangSmith (LangChain monitoring)

## 📝 .env File Format

Your `.env` file should look like this:

```env
# OpenAI Configuration
LLM_PROVIDER=openai
LLM_MODEL=gpt-4.1
LLM_API_KEY=sk-your-openai-api-key-here
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# anthropic/claude-3-haiku Configuration (for Claude)
anthropic/claude-3-haiku_API_KEY=sk-ant-your-anthropic/claude-3-haiku-api-key-here

# LangSmith Configuration (optional, for monitoring)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key-here

# Pipeline Configuration
MAX_ITERATIONS=5
CONVERGENCE_THRESHOLD=0.85
ENABLE_FACT_CHECKING=true
ENABLE_BIAS_DETECTION=true
```

## 🧪 Test Your API Keys

Run the test script to verify everything is working:

```bash
python test_api_keys.py
```

This will:
- ✅ Test OpenAI API key
- ✅ Test anthropic/claude-3-haiku API key
- ✅ Test LangSmith configuration
- ✅ Test the configuration system

## 🔄 Switching Between Models

### Use OpenAI (gpt-4.1)

Edit `.env`:
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4.1
```

### Use anthropic/claude-3-haiku (Claude 3 Opus)

Edit `.env`:
```env
LLM_PROVIDER=anthropic/claude-3-haiku
LLM_MODEL=claude-3-opus-20240229
```

**Note**: Make sure `anthropic/claude-3-haiku_API_KEY` is set in your `.env` file.

## 🚀 Quick Test

After setting up your keys, test with a simple research topic:

```bash
# Using OpenAI (default)
python -m src.main "Quantum Computing Basics"

# Or test via Python
python test_api_keys.py
```

## 🔍 Troubleshooting

### "API key not found" error

1. Make sure `.env` file exists in the project root
2. Check that API keys don't have quotes around them
3. Verify the key names match exactly:
   - `LLM_API_KEY` for OpenAI
   - `anthropic/claude-3-haiku_API_KEY` for anthropic/claude-3-haiku
   - `LANGCHAIN_API_KEY` for LangSmith

### "langchain-anthropic/claude-3-haiku not installed"

Install the package:
```bash
pip install langchain-anthropic/claude-3-haiku
```

Or reinstall all requirements:
```bash
pip install -r requirements.txt
```

### LangSmith tracing not working

1. Make sure `LANGCHAIN_TRACING_V2=true` in `.env`
2. Verify `LANGCHAIN_API_KEY` is set
3. Check that you're using a valid LangSmith API key

## 📊 Using Both Models

You can switch between models easily:

1. **Change provider in `.env`**:
   ```env
   LLM_PROVIDER=anthropic/claude-3-haiku  # or openai
   ```

2. **Or use different models for different agents** (advanced):
   - Modify `src/llm_factory.py` to support per-agent model selection
   - Or create separate agent instances with different LLMs

## 💡 Tips

1. **Start with OpenAI**: gpt-4.1 is faster and cheaper for testing
2. **Use Claude for complex tasks**: Claude 3 Opus excels at long-form content
3. **Monitor with LangSmith**: Enable tracing to see agent interactions
4. **Test first**: Always run `test_api_keys.py` after changing keys

## 🔐 Security

- ⚠️ **Never commit `.env` file to git** (it's in `.gitignore`)
- ⚠️ **Don't share API keys** in code or documentation
- ⚠️ **Rotate keys** if they're exposed
- ✅ **Use environment variables** in production

