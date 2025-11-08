"""
Base agent class for all specialized agents in the research pipeline.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
try:
    from langchain.agents import AgentExecutor, create_openai_tools_agent
except ImportError:
    # Fallback for LangChain 0.3.0 - agents might be in different location
    try:
        from langchain.agents import AgentExecutor
        from langchain.agents.openai_tools import create_openai_tools_agent
    except ImportError:
        AgentExecutor = None
        create_openai_tools_agent = None

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
try:
    from langchain.memory import ConversationBufferMemory
except ImportError:
    from langchain_core.chat_history import InMemoryChatMessageHistory
    ConversationBufferMemory = None  # Will handle this
from src.llm_factory import create_llm
from src.config import config


class BaseAgent(ABC):
    """Base class for all research agents."""
    
    def __init__(
        self,
        name: str,
        role: str,
        llm: Optional[BaseChatModel] = None,
        tools: Optional[List] = None,
        memory: Optional[ConversationBufferMemory] = None
    ):
        self.name = name
        self.role = role
        self.llm = llm or create_llm()
        self.tools = tools or []
        
        # Initialize memory
        if memory:
            self.memory = memory
        elif ConversationBufferMemory:
            self.memory = ConversationBufferMemory(
                return_messages=True,
                memory_key="chat_history"
            )
        else:
            # Fallback: simple list-based memory
            self.memory = type('Memory', (), {
                'chat_memory': type('ChatMemory', (), {
                    'messages': [],
                    'add_user_message': lambda self, msg: self.messages.append(HumanMessage(content=msg)),
                    'add_ai_message': lambda self, msg: self.messages.append(AIMessage(content=msg)),
                })()
            })()
        
        self.conversation_history: List[BaseMessage] = []
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent."""
        return f"""You are a {self.role} in an AI research lab.
Your role is to {self._get_role_description()}.
Be thorough, accurate, and collaborative with other agents."""
    
    @abstractmethod
    def _get_role_description(self) -> str:
        """Return a description of this agent's role."""
        pass
    
    def get_prompt_template(self) -> ChatPromptTemplate:
        """Get the prompt template for this agent."""
        return ChatPromptTemplate.from_messages([
            ("system", self.get_system_prompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
    
    def process(self, input_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process input and return response.
        
        Args:
            input_text: The input text to process
            context: Additional context from other agents
        
        Returns:
            Dictionary with 'output', 'sources', 'confidence', etc.
        """
        # Add context to input if provided
        if context:
            input_text = self._format_input_with_context(input_text, context)
        
        # Create agent if tools are available and agent creation is supported
        if self.tools and AgentExecutor and create_openai_tools_agent:
            try:
                agent = create_openai_tools_agent(self.llm, self.tools, self.get_prompt_template())
                agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
                response = agent_executor.invoke({
                    "input": input_text,
                    "chat_history": getattr(self.memory, 'chat_memory', type('', (), {'messages': []})()).messages,
                })
                output = response.get("output", "")
            except Exception as e:
                # Check if it's a connection error
                error_msg = str(e)
                if "Connection" in error_msg or "APIConnectionError" in str(type(e).__name__):
                    raise ConnectionError(
                        f"Failed to connect to OpenAI API. Please check:\n"
                        f"1. Your internet connection\n"
                        f"2. Your API key is set correctly (check .env file)\n"
                        f"3. OpenAI API service is accessible\n"
                        f"4. Firewall/proxy settings\n\n"
                        f"Original error: {error_msg}"
                    ) from e
                # Fallback to simple LLM call if agent creation fails (non-connection errors)
                try:
                    messages = getattr(self.memory, 'chat_memory', type('', (), {'messages': []})()).messages + [HumanMessage(content=input_text)]
                    response = self.llm.invoke(messages)
                    output = response.content
                except Exception as api_error:
                    # Handle API connection errors in fallback
                    error_msg = str(api_error)
                    if "Connection" in error_msg or "APIConnectionError" in str(type(api_error).__name__):
                        raise ConnectionError(
                            f"Failed to connect to OpenAI API. Please check:\n"
                            f"1. Your internet connection\n"
                            f"2. Your API key is set correctly (check .env file)\n"
                            f"3. OpenAI API service is accessible\n"
                            f"4. Firewall/proxy settings\n\n"
                            f"Original error: {error_msg}"
                        ) from api_error
                    elif "API key" in error_msg or "authentication" in error_msg.lower():
                        raise ValueError(
                            f"API authentication failed. Please check your API key in .env file.\n"
                            f"Run 'python test_api_keys.py' to verify your API key.\n\n"
                            f"Original error: {error_msg}"
                        ) from api_error
                    else:
                        raise RuntimeError(
                            f"LLM API call failed: {error_msg}\n"
                            f"Please check your API configuration and try again."
                        ) from api_error
        else:
            # Simple LLM call without tools
            memory_messages = getattr(self.memory, 'chat_memory', type('', (), {'messages': []})()).messages
            messages = memory_messages + [HumanMessage(content=input_text)]
            try:
                response = self.llm.invoke(messages)
                output = response.content
            except Exception as api_error:
                # Handle API connection errors gracefully
                error_msg = str(api_error)
                if "Connection" in error_msg or "APIConnectionError" in str(type(api_error).__name__):
                    raise ConnectionError(
                        f"Failed to connect to OpenAI API. Please check:\n"
                        f"1. Your internet connection\n"
                        f"2. Your API key is set correctly (check .env file)\n"
                        f"3. OpenAI API service is accessible\n"
                        f"4. Firewall/proxy settings\n\n"
                        f"Original error: {error_msg}"
                    ) from api_error
                elif "API key" in error_msg or "authentication" in error_msg.lower():
                    raise ValueError(
                        f"API authentication failed. Please check your API key in .env file.\n"
                        f"Run 'python test_api_keys.py' to verify your API key.\n\n"
                        f"Original error: {error_msg}"
                    ) from api_error
                else:
                    raise RuntimeError(
                        f"LLM API call failed: {error_msg}\n"
                        f"Please check your API configuration and try again."
                    ) from api_error
        
        # Update memory
        try:
            if hasattr(self.memory, 'chat_memory'):
                if hasattr(self.memory.chat_memory, 'add_user_message'):
                    self.memory.chat_memory.add_user_message(input_text)
                    self.memory.chat_memory.add_ai_message(output)
                elif hasattr(self.memory.chat_memory, 'messages'):
                    self.memory.chat_memory.messages.append(HumanMessage(content=input_text))
                    self.memory.chat_memory.messages.append(AIMessage(content=output))
        except Exception:
            pass  # Memory update failed, continue anyway
        
        self.conversation_history.append(HumanMessage(content=input_text))
        self.conversation_history.append(AIMessage(content=output))
        
        return {
            "agent": self.name,
            "output": output,
            "confidence": self._calculate_confidence(output),
            "metadata": self._extract_metadata(output),
        }
    
    def _format_input_with_context(self, input_text: str, context: Dict[str, Any]) -> str:
        """Format input with additional context."""
        context_str = "\n\nAdditional Context:\n"
        for key, value in context.items():
            context_str += f"{key}: {value}\n"
        return f"{input_text}\n\n{context_str}"
    
    def _calculate_confidence(self, output: str) -> float:
        """Calculate confidence score for the output."""
        # Simple heuristic: longer, more structured outputs = higher confidence
        if len(output) < 50:
            return 0.5
        elif len(output) < 200:
            return 0.7
        else:
            return 0.85
    
    def _extract_metadata(self, output: str) -> Dict[str, Any]:
        """Extract metadata from the output."""
        return {
            "length": len(output),
            "word_count": len(output.split()),
        }
    
    def get_conversation_history(self) -> List[BaseMessage]:
        """Get the conversation history."""
        return self.conversation_history
    
    def clear_memory(self):
        """Clear agent memory."""
        self.memory.clear()
        self.conversation_history = []

