"""
Editor Agent: Responsible for synthesis, coherence, and document refinement.
"""

from typing import Dict, Any, List, Optional
from src.agents.base_agent import BaseAgent
from src.config import config


class EditorAgent(BaseAgent):
    """Agent specialized in editing and synthesizing research documents."""
    
    def __init__(self, llm=None, tools=None, memory=None):
        super().__init__(
            name="editor",
            role="Editor-in-Chief",
            llm=llm,
            tools=tools,
            memory=memory
        )
        self.agent_config = config.get_agent_config("editor")
        self.synthesis_mode = self.agent_config.get("synthesis_mode", "comprehensive")
    
    def _get_role_description(self) -> str:
        return """synthesize research content, ensure coherence across sections,
        improve clarity and structure, integrate feedback from reviewers,
        and produce a polished, publication-ready research document."""
    
    def edit(
        self,
        content: str,
        feedback: Optional[str] = None,
        original_topic: str = "",
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Edit and synthesize research content.
        
        Args:
            content: The content to edit
            feedback: Review feedback to incorporate
            original_topic: The original research topic
            context: Additional context
        
        Returns:
            Edited content with improvements
        """
        edit_prompt = f"""Edit and synthesize the following research content on: "{original_topic}"

Original Content:
---
{content}
---

{f"Review Feedback to Incorporate:\n---\n{feedback}\n---\n" if feedback else ""}

Please:
1. **Synthesize** the content into a coherent, well-structured document
2. **Improve clarity** and readability
3. **Ensure consistency** in terminology and style
4. **Integrate feedback** from reviewers (if provided)
5. **Enhance structure** with clear sections and transitions
6. **Verify citations** are properly formatted
7. **Maintain accuracy** while improving presentation

Synthesis mode: {self.synthesis_mode}

Provide the improved, synthesized version of the research document."""
        
        result = self.process(edit_prompt, context)
        
        # Track changes
        result["changes_made"] = self._identify_changes(content, result["output"])
        result["improvement_score"] = self._calculate_improvement(content, result["output"])
        
        return result
    
    def _identify_changes(self, original: str, edited: str) -> List[str]:
        """Identify key changes made during editing."""
        changes = []
        
        # Simple heuristic-based change detection
        if len(edited) > len(original) * 1.1:
            changes.append("Content expanded significantly")
        elif len(edited) < len(original) * 0.9:
            changes.append("Content condensed")
        
        # Check for structural improvements
        if edited.count("\n\n") > original.count("\n\n"):
            changes.append("Improved paragraph structure")
        
        if "##" in edited and "##" not in original:
            changes.append("Added section headers")
        
        return changes if changes else ["General improvements and refinements"]
    
    def _calculate_improvement(self, original: str, edited: str) -> float:
        """Calculate improvement score."""
        # Simple heuristic: longer, more structured = better
        improvement = 0.5
        
        if len(edited) > len(original):
            improvement += 0.1
        
        if edited.count("\n") > original.count("\n") * 1.2:
            improvement += 0.1
        
        # Check for better structure
        structure_indicators = ["##", "###", "**", "*"]
        edited_structure = sum(1 for ind in structure_indicators if ind in edited)
        original_structure = sum(1 for ind in structure_indicators if ind in original)
        
        if edited_structure > original_structure:
            improvement += 0.1
        
        return min(improvement, 1.0)
    
    def _calculate_confidence(self, output: str) -> float:
        """Calculate confidence based on editing quality."""
        base_confidence = super()._calculate_confidence(output)
        
        # Higher confidence for well-structured outputs
        if "##" in output or "**" in output:
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)

