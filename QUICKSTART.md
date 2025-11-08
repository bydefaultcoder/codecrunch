# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Environment

Run the setup script to create your `.env` file:

```bash
python setup_env.py
```

Then edit `.env` and add your API key:

```env
LLM_API_KEY=your-actual-api-key-here
```

### Step 3: Run Your First Research

#### Option A: Command Line

```bash
python -m src.main "Quantum Computing Applications"
```

#### Option B: Web UI

```bash
streamlit run ui/app.py
```

Open your browser to `http://localhost:8501`

## 📝 Example Usage

### Basic Research

```bash
python -m src.main "Machine Learning in Healthcare" --output research_output.json
```

### With Requirements

```bash
python -m src.main "Climate Change Solutions" --requirements "Focus on renewable energy, include recent studies from 2023-2024"
```

### Text Output Format

```bash
python -m src.main "AI Ethics" --format text --output research.txt
```

## 🔧 Configuration

### Change LLM Model

Edit `.env`:

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
# or
LLM_MODEL=gpt-3.5-turbo
```

### Adjust Pipeline Settings

Edit `config.yaml`:

```yaml
pipeline:
  max_iterations: 3  # Reduce for faster results
  convergence_threshold: 0.80  # Lower threshold
```

### Enable/Disable Agents

Edit `config.yaml`:

```yaml
agents:
  enabled:
    - researcher
    - reviewer
    - editor
    # - fact_checker  # Comment out to disable
```

## 🐛 Troubleshooting

### "API key not found" error

- Make sure `.env` file exists
- Check that `LLM_API_KEY` is set correctly
- No quotes needed around the key value

### Import errors

```bash
pip install --upgrade langchain langchain-openai langgraph
```

### Memory issues

Reduce `max_iterations` in `config.yaml` or `.env`

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize agents in `src/agents/`
- Add new agents following the base agent pattern
- Integrate real search APIs for better research

## 💡 Tips

1. **Start Simple**: Use default settings first, then customize
2. **Monitor Costs**: Each iteration uses API calls - watch your usage
3. **Iterate**: Adjust convergence threshold based on your needs
4. **Extend**: Add custom tools to agents for specialized tasks

