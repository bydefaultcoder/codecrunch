"""
Base agent class for all specialized agents in the research pipeline.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
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
        self.memory = memory or ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
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
        
        # Create agent if tools are available
        if self.tools:
            agent = create_openai_tools_agent(self.llm, self.tools, self.get_prompt_template())
            agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
            response = agent_executor.invoke({
                "input": input_text,
                "chat_history": self.memory.chat_memory.messages,
            })
            output = response.get("output", "")
        else:
            # Simple LLM call without tools
            messages = self.memory.chat_memory.messages + [HumanMessage(content=input_text)]
            response = self.llm.invoke(messages)
            output = response.content
        
        # Update memory
        self.memory.chat_memory.add_user_message(input_text)
        self.memory.chat_memory.add_ai_message(output)
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

