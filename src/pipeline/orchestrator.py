"""
Main orchestrator for the multi-agent research pipeline using LangGraph.
"""

from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from src.pipeline.state import ResearchState
from src.agents import (
    ResearcherAgent,
    ReviewerAgent,
    EditorAgent,
    FactCheckerAgent
)
from src.config import config
from src.evaluation import Evaluator


class ResearchPipeline:
    """Main pipeline orchestrator for multi-agent research."""
    
    def __init__(self):
        self.config = config
        self.pipeline_config = config.get_pipeline_config()
        self.enabled_agents = config.get_enabled_agents()
        
        # Initialize agents
        self.agents = {}
        self._initialize_agents()
        
        # Initialize evaluator
        self.evaluator = Evaluator()
        
        # Build graph
        self.graph = self._build_graph()
    
    def _initialize_agents(self):
        """Initialize all enabled agents."""
        if "researcher" in self.enabled_agents:
            self.agents["researcher"] = ResearcherAgent()
        
        if "reviewer" in self.enabled_agents:
            self.agents["reviewer"] = ReviewerAgent()
        
        if "editor" in self.enabled_agents:
            self.agents["editor"] = EditorAgent()
        
        if "fact_checker" in self.enabled_agents:
            self.agents["fact_checker"] = FactCheckerAgent()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(ResearchState)
        
        # Add nodes for each agent
        if "researcher" in self.agents:
            workflow.add_node("researcher", self._researcher_node)
        
        if "fact_checker" in self.agents:
            workflow.add_node("fact_checker", self._fact_checker_node)
        
        if "reviewer" in self.agents:
            workflow.add_node("reviewer", self._reviewer_node)
        
        if "editor" in self.agents:
            workflow.add_node("editor", self._editor_node)
        
        # Add evaluation node
        workflow.add_node("evaluator", self._evaluator_node)
        
        # Set entry point
        workflow.set_entry_point("researcher")
        
        # Add edges
        if "researcher" in self.agents and "fact_checker" in self.agents:
            workflow.add_edge("researcher", "fact_checker")
        elif "researcher" in self.agents:
            workflow.add_edge("researcher", "reviewer" if "reviewer" in self.agents else "editor")
        
        if "fact_checker" in self.agents:
            next_node = "reviewer" if "reviewer" in self.agents else "editor"
            workflow.add_edge("fact_checker", next_node)
        
        if "reviewer" in self.agents:
            workflow.add_edge("reviewer", "editor")
        
        if "editor" in self.agents:
            workflow.add_edge("editor", "evaluator")
        else:
            workflow.add_edge("reviewer" if "reviewer" in self.agents else "fact_checker", "evaluator")
        
        # Add conditional edge for convergence check
        workflow.add_conditional_edges(
            "evaluator",
            self._should_continue,
            {
                "continue": "researcher" if "researcher" in self.agents else "editor",
                "end": END
            }
        )
        
        # Compile with memory
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)
    
    def _researcher_node(self, state: ResearchState) -> ResearchState:
        """Researcher agent node."""
        researcher = self.agents["researcher"]
        
        result = researcher.research(
            topic=state["topic"],
            context={"requirements": state.get("user_requirements")}
        )
        
        state["researcher_output"] = result
        state["current_content"] = result["output"]
        state["sources"] = result.get("sources", [])
        
        # Update history
        state["agent_interactions"].append({
            "agent": "researcher",
            "iteration": state["iteration"],
            "output": result["output"][:200] + "..." if len(result["output"]) > 200 else result["output"]
        })
        
        return state
    
    def _fact_checker_node(self, state: ResearchState) -> ResearchState:
        """Fact-checker agent node."""
        fact_checker = self.agents["fact_checker"]
        
        result = fact_checker.fact_check(
            content=state["current_content"],
            sources=state.get("sources", [])
        )
        
        state["fact_checker_output"] = result
        state["scores"]["factual_accuracy"] = result.get("factual_accuracy", 0.8)
        
        # Update history
        state["agent_interactions"].append({
            "agent": "fact_checker",
            "iteration": state["iteration"],
            "factual_accuracy": result.get("factual_accuracy", 0.8)
        })
        
        return state
    
    def _reviewer_node(self, state: ResearchState) -> ResearchState:
        """Reviewer agent node."""
        reviewer = self.agents["reviewer"]
        
        result = reviewer.review(
            content=state["current_content"],
            original_topic=state["topic"],
            context={
                "fact_checker_output": state.get("fact_checker_output"),
            }
        )
        
        state["reviewer_output"] = result
        state["scores"]["review_score"] = result.get("overall_score", 0.7)
        state["feedback_history"].append(result["output"])
        
        # Update history
        state["agent_interactions"].append({
            "agent": "reviewer",
            "iteration": state["iteration"],
            "score": result.get("overall_score", 0.7)
        })
        
        return state
    
    def _editor_node(self, state: ResearchState) -> ResearchState:
        """Editor agent node."""
        editor = self.agents["editor"]
        
        feedback = None
        if state.get("reviewer_output"):
            feedback = state["reviewer_output"]["output"]
        
        result = editor.edit(
            content=state["current_content"],
            feedback=feedback,
            original_topic=state["topic"],
            context={
                "fact_checker_output": state.get("fact_checker_output"),
                "reviewer_output": state.get("reviewer_output"),
            }
        )
        
        state["previous_content"] = state["current_content"]
        state["current_content"] = result["output"]
        state["editor_output"] = result
        
        # Update history
        state["agent_interactions"].append({
            "agent": "editor",
            "iteration": state["iteration"],
            "improvement_score": result.get("improvement_score", 0.7)
        })
        
        return state
    
    def _evaluator_node(self, state: ResearchState) -> ResearchState:
        """Evaluation node."""
        state["iteration"] += 1
        
        # Calculate convergence score
        scores = self.evaluator.evaluate(
            content=state["current_content"],
            previous_content=state.get("previous_content"),
            topic=state["topic"]
        )
        
        state["scores"].update(scores)
        state["convergence_score"] = scores.get("overall_score", 0.7)
        
        # Check convergence
        threshold = self.pipeline_config.get("convergence_threshold", 0.85)
        max_iter = self.pipeline_config.get("max_iterations", 5)
        
        state["converged"] = (
            state["convergence_score"] >= threshold or
            state["iteration"] >= max_iter
        )
        
        return state
    
    def _should_continue(self, state: ResearchState) -> str:
        """Determine if the pipeline should continue or end."""
        if state["converged"]:
            return "end"
        return "continue"
    
    def run(
        self,
        topic: str,
        user_requirements: Optional[str] = None,
        thread_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Run the research pipeline.
        
        Args:
            topic: Research topic
            user_requirements: Additional user requirements
            thread_id: Thread ID for state management
        
        Returns:
            Final research document and metadata
        """
        # Initialize state
        initial_state: ResearchState = {
            "topic": topic,
            "user_requirements": user_requirements,
            "current_content": "",
            "previous_content": None,
            "researcher_output": None,
            "fact_checker_output": None,
            "reviewer_output": None,
            "editor_output": None,
            "iteration": 0,
            "max_iterations": self.pipeline_config.get("max_iterations", 5),
            "convergence_score": 0.0,
            "converged": False,
            "conversation_history": [],
            "agent_interactions": [],
            "scores": {},
            "feedback_history": [],
            "sources": [],
            "citations": [],
        }
        
        # Run the graph
        graph_config = {"configurable": {"thread_id": thread_id}}
        final_state = initial_state
        
        # Stream through the graph execution
        for state_update in self.graph.stream(initial_state, graph_config):
            # Update final_state with the latest state
            if isinstance(state_update, dict):
                # Get state from the last updated node
                for node_name, node_state in state_update.items():
                    final_state = node_state
            else:
                final_state = state_update
        
        return {
            "topic": topic,
            "document": final_state.get("current_content", ""),
            "sources": final_state.get("sources", []),
            "scores": final_state.get("scores", {}),
            "iterations": final_state.get("iteration", 0),
            "converged": final_state.get("converged", False),
            "agent_interactions": final_state.get("agent_interactions", []),
            "feedback_history": final_state.get("feedback_history", []),
        }

