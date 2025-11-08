"""
State management for the research pipeline.
"""

from typing import Dict, Any, List, Optional, TypedDict
from langchain_core.messages import BaseMessage


class ResearchState(TypedDict):
    """State structure for the research pipeline."""
    # Input
    topic: str
    user_requirements: Optional[str]
    
    # Content
    current_content: str
    previous_content: Optional[str]
    
    # Agent outputs
    researcher_output: Optional[Dict[str, Any]]
    fact_checker_output: Optional[Dict[str, Any]]
    reviewer_output: Optional[Dict[str, Any]]
    editor_output: Optional[Dict[str, Any]]
    
    # Metadata
    iteration: int
    max_iterations: int
    convergence_score: float
    converged: bool
    
    # History
    conversation_history: List[BaseMessage]
    agent_interactions: List[Dict[str, Any]]
    
    # Evaluation
    scores: Dict[str, float]
    feedback_history: List[str]
    
    # Sources
    sources: List[str]
    citations: List[str]

