# AI Research Lab Simulator

A multi-agent LLM research pipeline that uses specialized AI agents to collaboratively produce, review, and refine research documents through iterative, collaborative reasoning cycles.

## 🎯 Overview

This system implements an autonomous research collective where multiple language model agents operate as specialized roles:
- **Researcher**: Knowledge acquisition and content generation
- **Fact-Checker**: Claim verification and citation validation
- **Reviewer**: Methodological critique and quality assessment
- **Editor**: Synthesis, coherence, and document refinement

The system performs multi-turn, reflexive collaboration (not linear chaining) where agents autonomously plan, negotiate, and resolve inconsistencies.

## ✨ Features

- **Multi-Agent Architecture**: Specialized agents with distinct roles
- **Iterative Refinement**: Feedback-driven improvement loops
- **Verification & Evaluation**: Cross-agent fact-checking and consistency scoring
- **Information Retrieval**: RAG-based knowledge acquisition
- **Autonomous Coordination**: Decentralized control via message passing
- **Easy Model Swapping**: Configuration-based LLM management
- **Simple UI**: Streamlit interface for input and visualization

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd codecrunch
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Configuration

The system uses a configuration layer that allows easy model swapping:

- **Environment Variables** (`.env`): LLM provider, model, API keys
- **YAML Config** (`config.yaml`): Agent settings, pipeline parameters

To swap models, simply update the `.env` file:
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
LLM_API_KEY=your-key-here
```

### Usage

#### Command Line Interface

```bash
python -m src.main "Your Research Topic" --requirements "Focus on recent developments"
```

Options:
- `--requirements`: Additional user requirements
- `--output`: Output file path (default: output.json)
- `--format`: Output format: json or text

#### Web UI

```bash
streamlit run ui/app.py
```

Then open your browser to `http://localhost:8501`

## 📁 Project Structure

```
codecrunch/
├── src/
│   ├── agents/           # Agent implementations
│   │   ├── base_agent.py
│   │   ├── researcher.py
│   │   ├── reviewer.py
│   │   ├── editor.py
│   │   └── fact_checker.py
│   ├── pipeline/         # Orchestration
│   │   ├── state.py
│   │   └── orchestrator.py
│   ├── config.py         # Configuration management
│   ├── llm_factory.py    # LLM creation
│   ├── evaluation.py     # Quality evaluation
│   └── main.py          # CLI entry point
├── ui/
│   └── app.py           # Streamlit UI
├── config.yaml          # Pipeline configuration
├── .env.example         # Environment template
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## 🔧 Architecture

### Agent Roles

1. **Researcher Agent**
   - Conducts research on topics
   - Gathers information from multiple sources
   - Generates structured research content
   - Provides citations

2. **Fact-Checker Agent**
   - Verifies factual claims
   - Validates citations
   - Checks for inconsistencies
   - Provides accuracy scores

3. **Reviewer Agent**
   - Critiques methodology
   - Evaluates logical coherence
   - Assesses clarity and completeness
   - Provides improvement recommendations

4. **Editor Agent**
   - Synthesizes content
   - Ensures coherence across sections
   - Integrates feedback
   - Produces polished documents

### Pipeline Flow

```
User Input → Researcher → Fact-Checker → Reviewer → Editor → Evaluator
                                                              ↓
                                                         Converged?
                                                              ↓
                                                         Yes → End
                                                         No → Loop back
```

### State Management

The pipeline uses LangGraph for state management, tracking:
- Current and previous content versions
- Agent outputs and interactions
- Iteration count and convergence scores
- Evaluation metrics
- Conversation history

## 🎛️ Configuration

### Environment Variables

```env
# LLM Configuration
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview
LLM_API_KEY=your-api-key
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# Pipeline Settings
MAX_ITERATIONS=5
CONVERGENCE_THRESHOLD=0.85
```

### YAML Configuration

Edit `config.yaml` to:
- Enable/disable specific agents
- Configure agent parameters
- Adjust evaluation weights
- Set memory settings

## 📊 Evaluation Metrics

The system evaluates documents across multiple dimensions:
- **Factual Accuracy**: Verification of claims and citations
- **Logical Coherence**: Structure and flow
- **Linguistic Clarity**: Readability and presentation
- **Overall Score**: Weighted combination of metrics

## 🔄 Iterative Refinement

The pipeline runs multiple iterations until:
1. Convergence threshold is met (default: 0.85)
2. Maximum iterations reached (default: 5)

Each iteration:
1. Agents collaborate to improve content
2. Evaluator assesses quality
3. System decides whether to continue or end

## 🛠️ Extending the System

### Adding New Agents

1. Create a new agent class in `src/agents/`:
```python
from src.agents.base_agent import BaseAgent

class NewAgent(BaseAgent):
    def _get_role_description(self) -> str:
        return "Description of agent role"
```

2. Add to `config.yaml`:
```yaml
agents:
  enabled:
    - new_agent
  new_agent:
    # Configuration
```

3. Add node to orchestrator in `src/pipeline/orchestrator.py`

### Custom Tools

Agents can use custom tools for specialized tasks:
- Web search APIs
- Database queries
- External APIs
- Custom functions

## 🐛 Troubleshooting

### API Key Issues
- Ensure `.env` file exists and contains valid API keys
- Check that `LLM_API_KEY` is set correctly

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### Memory Issues
- Reduce `max_iterations` in config
- Lower `max_context_length` in memory config

## 📝 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines]

## 📧 Contact

[Add contact information]

---

**Note**: This is a research prototype. For production use, consider:
- Implementing actual web search APIs
- Adding proper citation validation
- Enhancing bias detection
- Implementing persistent storage
- Adding authentication and rate limiting

