# AI Research Lab Simulator - Complete Project Documentation

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture & Design](#architecture--design)
3. [Development Journey](#development-journey)
4. [Technical Implementation](#technical-implementation)
5. [Issues Fixed](#issues-fixed)
6. [Configuration](#configuration)
7. [Usage Guide](#usage-guide)
8. [Project Structure](#project-structure)
9. [Dependencies](#dependencies)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

The **AI Research Lab Simulator** is a multi-agent LLM research pipeline that uses specialized AI agents to collaboratively produce, review, and refine research documents through iterative, collaborative reasoning cycles.

### Key Features

- **Multi-Agent Architecture**: Four specialized agents (Researcher, Fact-Checker, Reviewer, Editor) working collaboratively
- **Iterative Refinement**: Feedback-driven improvement loops until convergence
- **Verification & Evaluation**: Cross-agent fact-checking and consistency scoring
- **Information Retrieval**: RAG-based knowledge acquisition (optional vector store)
- **Autonomous Coordination**: Decentralized control via LangGraph state management
- **Easy Model Swapping**: Configuration-based LLM management (OpenAI)
- **User-Friendly UI**: Streamlit interface for input and visualization
- **Robust Error Handling**: Comprehensive error handling with user-friendly messages

### Technology Stack

- **Language**: Python 3.8+
- **LLM Framework**: LangChain 0.3.0, LangGraph 0.2.20
- **LLM Provider**: OpenAI (GPT-4o-mini)
- **UI Framework**: Streamlit
- **State Management**: LangGraph with MemorySaver
- **Configuration**: Pydantic Settings, YAML, Environment Variables

---

## 🏗️ Architecture & Design

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│  ┌──────────────┐              ┌──────────────┐            │
│  │  Streamlit   │              │  CLI (main)  │            │
│  │     UI       │              │              │            │
│  └──────┬───────┘              └──────┬───────┘            │
└─────────┼──────────────────────────────┼───────────────────┘
          │                              │
          └──────────────┬───────────────┘
                         │
          ┌──────────────▼───────────────┐
          │   Research Pipeline          │
          │   (Orchestrator)             │
          └──────────────┬───────────────┘
                         │
          ┌──────────────┼───────────────┐
          │              │               │
    ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
    │ Researcher │  │Fact-Check │  │ Reviewer │
    │   Agent   │  │   Agent   │  │   Agent   │
    └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
          │              │               │
          └──────────────┼───────────────┘
                         │
                   ┌─────▼─────┐
                   │  Editor   │
                   │   Agent   │
                   └─────┬─────┘
                         │
                   ┌─────▼─────┐
                   │ Evaluator │
                   └─────┬─────┘
                         │
          ┌──────────────┴───────────────┐
          │   Convergence Check          │
          │   (Continue or End)         │
          └──────────────────────────────┘
```

### Agent Roles

#### 1. Researcher Agent
- **Purpose**: Knowledge acquisition and content generation
- **Responsibilities**:
  - Conducts comprehensive research on topics
  - Gathers information from multiple sources
  - Generates structured research content
  - Provides citations and references
- **Tools**: Web search (placeholder), Document retrieval (optional vector store)
- **Location**: `src/agents/researcher.py`

#### 2. Fact-Checker Agent
- **Purpose**: Claim verification and citation validation
- **Responsibilities**:
  - Verifies factual claims in the document
  - Validates citations and references
  - Checks for inconsistencies
  - Provides accuracy scores
- **Location**: `src/agents/fact_checker.py`

#### 3. Reviewer Agent
- **Purpose**: Methodological critique and quality assessment
- **Responsibilities**:
  - Critiques methodology and approach
  - Evaluates logical coherence
  - Assesses clarity and completeness
  - Provides improvement recommendations
- **Location**: `src/agents/reviewer.py`

#### 4. Editor Agent
- **Purpose**: Synthesis, coherence, and document refinement
- **Responsibilities**:
  - Synthesizes content from all agents
  - Ensures coherence across sections
  - Integrates feedback from other agents
  - Produces polished final documents
- **Location**: `src/agents/editor.py`

### Pipeline Flow

```
User Input
    │
    ▼
[Researcher] → Generates initial research content
    │
    ▼
[Fact-Checker] → Verifies claims and citations
    │
    ▼
[Reviewer] → Critiques and provides feedback
    │
    ▼
[Editor] → Synthesizes and refines document
    │
    ▼
[Evaluator] → Calculates convergence score
    │
    ├─→ Score >= Threshold → [END] → Return final document
    │
    └─→ Score < Threshold → Loop back to Researcher
         (up to max_iterations)
```

### State Management

The pipeline uses **LangGraph** for state management, tracking:

- **Current Content**: Latest version of the research document
- **Previous Content**: Previous iteration for comparison
- **Topic**: Research topic
- **Requirements**: User-specified requirements
- **Iteration Count**: Current iteration number
- **Convergence Score**: Quality score (0-1)
- **Scores**: Detailed evaluation metrics
- **Agent Interactions**: History of all agent outputs
- **Conversation History**: Full conversation log
- **Converged**: Boolean flag indicating completion

---

## 🛣️ Development Journey

### Initial Setup

The project was built from scratch to implement a multi-agent research pipeline. Key milestones:

1. **Project Structure**: Created modular architecture with separate agent classes
2. **LangChain Integration**: Integrated LangChain 0.3.0 and LangGraph for orchestration
3. **Configuration System**: Built flexible configuration using Pydantic and YAML
4. **UI Development**: Created Streamlit interface for user interaction
5. **Error Handling**: Implemented comprehensive error handling throughout

### Challenges Encountered

#### 1. Dependency Conflicts
- **Issue**: Pydantic version conflicts with LangChain 0.3.0
- **Solution**: Updated to `pydantic>=2.7.4,<3.0.0` to match LangChain requirements
- **Issue**: Tiktoken version conflicts
- **Solution**: Updated to `tiktoken>=0.7,<1` for compatibility

#### 2. LangChain API Changes
- **Issue**: `Tool` class moved in LangChain 0.3.0
- **Solution**: Updated to use `StructuredTool` from `langchain_core.tools` with proper `args_schema`

#### 3. Type Conversion Errors
- **Issue**: `convergence_threshold` read as string instead of float
- **Solution**: Added type conversion in `get_pipeline_config()` and orchestrator

#### 4. Attribute Errors
- **Issue**: UI accessing `config.pipeline_config` as attribute (it was a method)
- **Solution**: Added `@property pipeline_config` and `update_pipeline_config()` method

#### 5. API Connection Errors
- **Issue**: Unhandled `APIConnectionError` causing crashes
- **Solution**: Added comprehensive error handling with user-friendly messages, timeout, and retry logic

#### 6. Deprecation Warnings
- **Issue**: ChromaDB deprecation warnings
- **Solution**: Disabled optional vector store feature (can be re-enabled later)

---

## 🔧 Technical Implementation

### Core Components

#### 1. Configuration Management (`src/config.py`)

**LLMConfig Class**:
- Uses Pydantic `BaseSettings` for environment variable management
- Supports `OPENAI_API_KEY` or `LLM_API_KEY`
- Configurable model, temperature, max_tokens
- Automatic type conversion and validation

**Config Class**:
- Loads YAML configuration
- Manages agent configurations
- Pipeline settings with type safety
- Caching for performance

**Key Methods**:
- `get_llm_config()`: Returns LLM configuration dictionary
- `get_pipeline_config()`: Returns pipeline settings with type conversion
- `get_enabled_agents()`: Returns list of active agents
- `get_agent_config(agent_name)`: Returns agent-specific settings
- `pipeline_config` (property): Direct access for UI compatibility
- `update_pipeline_config(key, value)`: Update config values

#### 2. LLM Factory (`src/llm_factory.py`)

**Purpose**: Centralized LLM instance creation

**Features**:
- Creates `ChatOpenAI` instances based on configuration
- Validates API key before creation
- Configurable timeout (60 seconds) and retries (2 attempts)
- Supports parameter overrides

**Usage**:
```python
from src.llm_factory import create_llm

llm = create_llm(
    temperature=0.7,
    max_tokens=2000,
    model_name="gpt-4o-mini"
)
```

#### 3. Base Agent (`src/agents/base_agent.py`)

**Purpose**: Abstract base class for all agents

**Features**:
- Common LLM interaction logic
- Memory management (ConversationBufferMemory or fallback)
- Tool integration support
- Error handling for API calls
- Context formatting

**Key Methods**:
- `process(input_text, context)`: Main processing method
- `_format_input_with_context()`: Adds context to prompts
- `get_prompt_template()`: Returns agent-specific prompt

**Error Handling**:
- Catches `APIConnectionError` and provides troubleshooting tips
- Distinguishes between connection, authentication, and other errors
- Falls back gracefully when agent executor fails

#### 4. Pipeline Orchestrator (`src/pipeline/orchestrator.py`)

**Purpose**: Coordinates agent execution using LangGraph

**Features**:
- Builds dynamic graph based on enabled agents
- Manages state transitions
- Handles convergence checking
- Tracks iterations and scores

**Graph Structure**:
- Nodes: One per agent + evaluator
- Edges: Sequential flow between agents
- Conditional edges: Convergence check after evaluator

**Key Methods**:
- `run(topic, user_requirements)`: Main execution method
- `_build_graph()`: Constructs LangGraph workflow
- `_should_continue()`: Determines if pipeline should continue
- Node methods: `_researcher_node()`, `_fact_checker_node()`, etc.

#### 5. Evaluation System (`src/evaluation.py`)

**Purpose**: Assesses document quality and convergence

**Metrics**:
- **Factual Accuracy**: Verification of claims
- **Logical Coherence**: Structure and flow
- **Linguistic Clarity**: Readability
- **Overall Score**: Weighted combination

**Convergence**:
- Compares current vs. previous content
- Calculates improvement delta
- Returns scores and convergence status

#### 6. User Interface (`ui/app.py`)

**Features**:
- Streamlit-based web interface
- Topic and requirements input
- Configuration sidebar
- Progress tracking
- Results display with metrics
- Error handling with helpful messages

**Components**:
- Main input form
- Configuration panel (max iterations, convergence threshold)
- Progress indicators
- Results display (document, metrics, scores)
- Error messages with troubleshooting tips

---

## 🐛 Issues Fixed

### 1. Dependency Conflicts

**Problem**: 
```
ERROR: Cannot install pydantic==2.5.0 and langchain 0.3.0 because these package versions have conflicting dependencies.
```

**Solution**:
- Updated `requirements.txt`:
  - `pydantic>=2.7.4,<3.0.0` (compatible with LangChain 0.3.0)
  - `tiktoken>=0.7,<1` (compatible with langchain-openai)

**Files Modified**: `requirements.txt`

### 2. LangChain Tool API Changes

**Problem**:
```
ImportError: cannot import name 'Tool' from 'langchain.tools'
```

**Solution**:
- Updated to use `StructuredTool` from `langchain_core.tools`
- Added Pydantic `BaseModel` schemas for tool arguments (`args_schema`)
- Added fallback imports for compatibility

**Files Modified**: 
- `src/agents/researcher.py`
- `src/agents/base_agent.py`

### 3. Type Conversion Error

**Problem**:
```
TypeError: '>=' not supported between instances of 'float' and 'str'
```

**Solution**:
- Added type conversion in `get_pipeline_config()`:
  - Converts `convergence_threshold` to float
  - Converts `max_iterations` to int
- Added safety checks in orchestrator node

**Files Modified**:
- `src/config.py`
- `src/pipeline/orchestrator.py`

### 4. AttributeError in UI

**Problem**:
```
AttributeError: 'Config' object has no attribute 'pipeline_config'
```

**Solution**:
- Added `@property pipeline_config` to Config class
- Added `update_pipeline_config(key, value)` method
- Updated UI to use update method

**Files Modified**:
- `src/config.py`
- `ui/app.py`

### 5. API Connection Errors

**Problem**:
```
openai.APIConnectionError: Connection error
```

**Solution**:
- Added comprehensive error handling in `base_agent.py`
- Added API key validation in `llm_factory.py`
- Added timeout and retry logic
- Added user-friendly error messages in UI
- Added pre-flight API key check

**Files Modified**:
- `src/agents/base_agent.py`
- `src/llm_factory.py`
- `ui/app.py`

### 6. ChromaDB Deprecation Warnings

**Problem**:
```
LangChainDeprecationWarning: The class Chroma was deprecated...
```

**Solution**:
- Disabled vector store initialization (optional feature)
- Commented out ChromaDB code with instructions for re-enabling
- Made it clear this is optional functionality

**Files Modified**:
- `src/agents/researcher.py`
- `requirements.txt` (commented out chromadb)

---

## ⚙️ Configuration

### Environment Variables (`.env`)

Create a `.env` file in the project root:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-api-key-here
# OR
LLM_API_KEY=your-api-key-here

# Optional: Override defaults
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# Pipeline Settings (optional)
MAX_ITERATIONS=5
CONVERGENCE_THRESHOLD=0.85
```

### YAML Configuration (`config.yaml`)

```yaml
# Agent Configuration
agents:
  enabled:
    - researcher
    - fact_checker
    - reviewer
    - editor
  
  researcher:
    retrieval_top_k: 5
    # Additional agent-specific settings
  
  fact_checker:
    # Fact-checker settings
  
  reviewer:
    # Reviewer settings
  
  editor:
    # Editor settings

# Pipeline Configuration
pipeline:
  max_iterations: 5
  convergence_threshold: 0.85

# Memory Configuration
memory:
  type: conversation_buffer
  max_context_length: 4000
```

### Testing API Keys

Run the test script to verify your configuration:

```bash
python test_api_keys.py
```

This will:
- Check if API key is set
- Test connection to OpenAI API
- Verify model access
- Display helpful error messages if issues found

---

## 📖 Usage Guide

### Command Line Interface

**Basic Usage**:
```bash
python -m src.main "Your Research Topic"
```

**With Requirements**:
```bash
python -m src.main "Quantum Computing" --requirements "Focus on recent developments in 2024"
```

**Output Options**:
```bash
# JSON output (default)
python -m src.main "Topic" --output results.json --format json

# Text output
python -m src.main "Topic" --output results.txt --format text
```

**Arguments**:
- `topic` (required): Research topic
- `--requirements` (optional): Additional user requirements
- `--output` (optional): Output file path (default: `output.json`)
- `--format` (optional): Output format - `json` or `text` (default: `json`)

### Web UI

**Start the UI**:
```bash
streamlit run ui/app.py
```

**Access**: Open your browser to `http://localhost:8501`

**UI Features**:
1. **Input Section**:
   - Research topic input
   - Requirements text area
   - Run button

2. **Configuration Sidebar**:
   - Max iterations slider
   - Convergence threshold slider
   - Agent enable/disable toggles

3. **Results Display**:
   - Research document
   - Metrics (iterations, convergence, scores)
   - Agent interactions
   - Evaluation scores breakdown

4. **Error Handling**:
   - Pre-flight API key validation
   - Connection error messages with troubleshooting tips
   - Configuration error notifications

### Example Workflow

1. **Start UI**: `streamlit run ui/app.py`
2. **Enter Topic**: "Machine Learning in Healthcare"
3. **Add Requirements**: "Focus on recent applications and ethical considerations"
4. **Configure**: Set max iterations to 3, threshold to 0.8
5. **Run**: Click "Run Research Pipeline"
6. **Monitor**: Watch progress indicators
7. **Review**: Examine results, scores, and agent interactions

---

## 📁 Project Structure

```
codecrunch/
├── src/
│   ├── __init__.py
│   ├── main.py                 # CLI entry point
│   ├── config.py               # Configuration management
│   ├── llm_factory.py          # LLM instance creation
│   ├── evaluation.py           # Quality evaluation
│   │
│   ├── agents/                 # Agent implementations
│   │   ├── __init__.py
│   │   ├── base_agent.py      # Base class for all agents
│   │   ├── researcher.py      # Research agent
│   │   ├── fact_checker.py    # Fact-checking agent
│   │   ├── reviewer.py        # Review agent
│   │   └── editor.py          # Editing agent
│   │
│   └── pipeline/              # Pipeline orchestration
│       ├── __init__.py
│       ├── state.py           # State definitions
│       └── orchestrator.py   # Main orchestrator
│
├── ui/
│   └── app.py                 # Streamlit UI
│
├── config.yaml                # Pipeline configuration
├── requirements.txt           # Python dependencies
├── test_api_keys.py          # API key testing script
├── .env                       # Environment variables (create this)
├── .env.example              # Environment template
│
├── README.md                  # Basic project README
├── QUICKSTART.md             # Quick start guide
├── QUICK_INSTALL.md          # Installation guide
└── PROJECT_DOCUMENTATION.md  # This file
```

### Key Files Explained

- **`src/main.py`**: Command-line interface entry point
- **`src/config.py`**: Centralized configuration management
- **`src/llm_factory.py`**: Factory for creating LLM instances
- **`src/agents/base_agent.py`**: Base class with common agent functionality
- **`src/pipeline/orchestrator.py`**: LangGraph-based pipeline orchestration
- **`ui/app.py`**: Streamlit web interface
- **`config.yaml`**: YAML-based configuration
- **`test_api_keys.py`**: Utility to test API configuration

---

## 📦 Dependencies

### Core Dependencies

```txt
# LangChain Ecosystem
langchain==0.3.0
langchain-openai==0.2.0
langchain-community==0.3.0
langgraph==0.2.20
langsmith==0.1.137

# Configuration & Settings
pydantic>=2.7.4,<3.0.0
pydantic-settings>=2.1.0
python-dotenv>=1.0.0

# Utilities
tiktoken>=0.7,<1

# Web Framework
streamlit>=1.28.0
fastapi>=0.104.1
uvicorn>=0.24.0

# Data & Visualization
networkx>=3.2.1
matplotlib>=3.8.2
plotly>=5.18.0

# Optional: Vector Store (commented out)
# chromadb>=0.4.18
# langchain-chroma>=0.1.0
```

### Installation

```bash
# Create virtual environment (recommended)
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Version Compatibility

- **Python**: 3.8+
- **LangChain**: 0.3.0 (pinned for stability)
- **Pydantic**: 2.7.4+ (required by LangChain 0.3.0)
- **OpenAI API**: Latest (via langchain-openai)

---

## 🔍 Troubleshooting

### Common Issues

#### 1. API Key Not Working

**Symptoms**:
- `ValueError: OpenAI API key is not set`
- `API authentication failed`

**Solutions**:
1. Check `.env` file exists in project root
2. Verify `OPENAI_API_KEY` or `LLM_API_KEY` is set
3. Run `python test_api_keys.py` to verify
4. Ensure no extra spaces or quotes around API key

#### 2. Connection Errors

**Symptoms**:
- `openai.APIConnectionError: Connection error`
- Timeout errors

**Solutions**:
1. Check internet connection
2. Verify OpenAI API is accessible
3. Check firewall/proxy settings
4. Try increasing timeout in `llm_factory.py`
5. Verify API key has sufficient credits

#### 3. Import Errors

**Symptoms**:
- `ModuleNotFoundError: No module named 'langchain'`
- Import errors for various packages

**Solutions**:
1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python version: `python --version` (should be 3.8+)
4. Try upgrading pip: `pip install --upgrade pip`

#### 4. Type Errors

**Symptoms**:
- `TypeError: '>=' not supported between instances of 'float' and 'str'`

**Solutions**:
- This should be fixed, but if it occurs:
  1. Check `config.yaml` values are numeric
  2. Verify environment variables are properly formatted
  3. Clear config cache if using custom config

#### 5. Deprecation Warnings

**Symptoms**:
- `LangChainDeprecationWarning` messages

**Solutions**:
- Most warnings are handled
- ChromaDB warnings are suppressed (feature disabled)
- Update LangChain if new warnings appear

### Getting Help

1. **Check Logs**: Review error messages carefully
2. **Test API**: Run `python test_api_keys.py`
3. **Verify Config**: Check `.env` and `config.yaml`
4. **Check Dependencies**: Ensure all packages installed
5. **Review Documentation**: Check this file and README.md

---

## 🚀 Future Enhancements

### Potential Improvements

1. **Web Search Integration**:
   - Integrate actual web search APIs (SerpAPI, Tavily, etc.)
   - Replace placeholder search functionality

2. **Vector Store**:
   - Re-enable ChromaDB with updated imports
   - Add document ingestion pipeline
   - Implement RAG retrieval

3. **Additional Agents**:
   - Summarizer agent
   - Translator agent
   - Citation formatter agent

4. **Enhanced Evaluation**:
   - More sophisticated scoring metrics
   - Bias detection
   - Citation validation

5. **Persistence**:
   - Database storage for research documents
   - History tracking
   - Export to various formats (PDF, Markdown, etc.)

6. **Performance**:
   - Parallel agent execution
   - Caching mechanisms
   - Optimized prompt engineering

7. **UI Enhancements**:
   - Real-time streaming of agent outputs
   - Interactive visualization of agent interactions
   - Export functionality

---

## 📝 Summary

This project implements a sophisticated multi-agent research pipeline that:

✅ **Works**: All core functionality implemented and tested  
✅ **Robust**: Comprehensive error handling and validation  
✅ **Flexible**: Easy configuration and model swapping  
✅ **User-Friendly**: Both CLI and web UI interfaces  
✅ **Maintainable**: Clean code structure and documentation  

The system successfully demonstrates:
- Multi-agent collaboration
- Iterative refinement
- Quality evaluation
- State management
- Error resilience

**Status**: ✅ **Production Ready** (for research/prototype use)

---

## 📧 Support

For issues, questions, or contributions:
1. Review this documentation
2. Check error messages and logs
3. Verify configuration
4. Test API keys
5. Review code comments

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Project**: AI Research Lab Simulator  
**Status**: Complete and Functional

