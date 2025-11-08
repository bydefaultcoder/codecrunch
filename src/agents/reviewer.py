"""
Reviewer Agent: Responsible for methodological critique and quality assessment.
"""

from typing import Dict, Any, List, Optional
from src.agents.base_agent import BaseAgent
from src.config import config


class ReviewerAgent(BaseAgent):
    """Agent specialized in reviewing and critiquing research content."""
    
    def __init__(self, llm=None, tools=None, memory=None):
        super().__init__(
            name="reviewer",
            role="Peer Reviewer",
            llm=llm,
            tools=tools,
            memory=memory
        )
        self.agent_config = config.get_agent_config("reviewer")
        self.strictness = self.agent_config.get("strictness", 0.8)
    
    def _get_role_description(self) -> str:
        return """review research content for methodological rigor, logical coherence,
        clarity, and adherence to academic standards. Provide constructive feedback
        and identify areas for improvement."""
    
    def review(self, content: str, original_topic: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Review research content.
        
        Args:
            content: The content to review
            original_topic: The original research topic
            context: Additional context
        
        Returns:
            Review feedback with scores and recommendations
        """
        check_methodology = self.agent_config.get("check_methodology", True)
        check_coherence = self.agent_config.get("check_coherence", True)
        
        review_prompt = f"""Review the following research content on the topic: "{original_topic}"

Content to review:
---
{content}
---

Please provide a comprehensive review covering:
1. **Methodological Quality**: {"Assess the research methodology, data sources, and analytical approach." if check_methodology else "Skip methodology check."}
2. **Logical Coherence**: {"Evaluate the logical flow, argument structure, and consistency." if check_coherence else "Skip coherence check."}
3. **Clarity and Presentation**: Assess writing clarity, organization, and readability.
4. **Completeness**: Identify missing information or underdeveloped sections.
5. **Citations and Sources**: Evaluate the quality and relevance of citations.

Provide:
- Overall quality score (0-1)
- Specific strengths
- Specific weaknesses
- Detailed recommendations for improvement
- Priority areas that need revision

Be thorough but constructive. Strictness level: {self.strictness}"""
        
        result = self.process(review_prompt, context)
        
        # Parse review scores
        scores = self._extract_scores(result["output"])
        result["scores"] = scores
        result["overall_score"] = scores.get("overall", 0.7)
        
        return result
    
    def _extract_scores(self, review_text: str) -> Dict[str, float]:
        """Extract quality scores from review text."""
        scores = {}
        
        # Try to extract numeric scores from text
        import re
        score_patterns = [
            r"overall.*?score.*?([0-9.]+)",
            r"quality.*?score.*?([0-9.]+)",
            r"score.*?:.*?([0-9.]+)",
        ]
        
        for pattern in score_patterns:
            matches = re.findall(pattern, review_text, re.IGNORECASE)
            if matches:
                try:
                    scores["overall"] = float(matches[0])
                    break
                except ValueError:
                    pass
        
        # Default scores if not found
        if "overall" not in scores:
            # Heuristic: longer, more detailed reviews = higher score
            if len(review_text) > 500:
                scores["overall"] = 0.75
            elif len(review_text) > 200:
                scores["overall"] = 0.65
            else:
                scores["overall"] = 0.55
        
        return scores
    
    def _calculate_confidence(self, output: str) -> float:
        """Calculate confidence based on review thoroughness."""
        base_confidence = super()._calculate_confidence(output)
        
        # Boost if review contains specific recommendations
        if "recommendation" in output.lower() or "improvement" in output.lower():
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)

