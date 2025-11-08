"""
Researcher Agent: Responsible for knowledge acquisition and content generation.
"""

from typing import Dict, Any, List, Optional
from langchain.tools import Tool
from langchain_community.vectorstores import Chroma
try:
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    from langchain_community.embeddings import OpenAIEmbeddings
from src.agents.base_agent import BaseAgent
from src.config import config


class ResearcherAgent(BaseAgent):
    """Agent specialized in research and knowledge acquisition."""
    
    def __init__(self, llm=None, tools=None, memory=None):
        super().__init__(
            name="researcher",
            role="Research Specialist",
            llm=llm,
            tools=tools or self._create_tools(),
            memory=memory
        )
        self.agent_config = config.get_agent_config("researcher")
        self.vector_store = None
        self._initialize_retrieval()
    
    def _get_role_description(self) -> str:
        return """conduct research on given topics, gather information from multiple sources,
        synthesize findings, and generate well-structured research content with proper citations."""
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the researcher agent."""
        tools = []
        
        # Web search tool (placeholder - would need actual implementation)
        web_search = Tool(
            name="web_search",
            description="Search the web for information about a topic",
            func=self._web_search,
        )
        tools.append(web_search)
        
        # Document retrieval tool
        if self.vector_store:
            retrieval_tool = Tool(
                name="retrieve_documents",
                description="Retrieve relevant documents from knowledge base",
                func=self._retrieve_documents,
            )
            tools.append(retrieval_tool)
        
        return tools
    
    def _initialize_retrieval(self):
        """Initialize retrieval system for RAG."""
        try:
            embeddings = OpenAIEmbeddings()
            # In a real implementation, you'd load existing vector store or create one
            # For now, we'll create an empty one
            self.vector_store = Chroma(
                embedding_function=embeddings,
                persist_directory="./chroma_db"
            )
        except Exception as e:
            print(f"Warning: Could not initialize vector store: {e}")
            self.vector_store = None
    
    def _web_search(self, query: str) -> str:
        """Placeholder for web search functionality."""
        # In production, integrate with actual search API (Tavily, Serper, etc.)
        return f"[Web search results for: {query}] - This is a placeholder. Integrate with actual search API."
    
    def _retrieve_documents(self, query: str) -> str:
        """Retrieve relevant documents from knowledge base."""
        if not self.vector_store:
            return "No knowledge base available."
        
        try:
            docs = self.vector_store.similarity_search(
                query,
                k=self.agent_config.get("retrieval_top_k", 5)
            )
            return "\n\n".join([doc.page_content for doc in docs])
        except Exception as e:
            return f"Error retrieving documents: {e}"
    
    def research(self, topic: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Conduct research on a topic.
        
        Args:
            topic: Research topic
            context: Additional context from other agents
        
        Returns:
            Research findings with sources
        """
        prompt = f"""Conduct comprehensive research on the following topic:
        
Topic: {topic}

Please provide:
1. A detailed overview of the topic
2. Key findings and insights
3. Relevant sources and citations
4. Areas that need further investigation

Format your response as a structured research document section."""
        
        result = self.process(prompt, context)
        
        # Extract sources (in a real implementation, parse from output)
        sources = self._extract_sources(result["output"])
        result["sources"] = sources
        
        return result
    
    def _extract_sources(self, text: str) -> List[str]:
        """Extract source citations from text."""
        # Simple extraction - in production, use more sophisticated parsing
        sources = []
        lines = text.split("\n")
        for line in lines:
            if "source:" in line.lower() or "reference:" in line.lower():
                sources.append(line.strip())
        return sources if sources else ["[Sources to be added]"]
    
    def _calculate_confidence(self, output: str) -> float:
        """Calculate confidence based on research quality."""
        base_confidence = super()._calculate_confidence(output)
        
        # Boost confidence if sources are present
        if "source" in output.lower() or "citation" in output.lower():
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)

