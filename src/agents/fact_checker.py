"""
Fact-Checker Agent: Responsible for verifying claims and validating citations.
"""

from typing import Dict, Any, List, Optional
from src.agents.base_agent import BaseAgent
from src.config import config


class FactCheckerAgent(BaseAgent):
    """Agent specialized in fact-checking and citation validation."""
    
    def __init__(self, llm=None, tools=None, memory=None):
        super().__init__(
            name="fact_checker",
            role="Fact-Checker",
            llm=llm,
            tools=tools,
            memory=memory
        )
        self.agent_config = config.get_agent_config("fact_checker")
        self.cross_reference = self.agent_config.get("cross_reference", True)
    
    def _get_role_description(self) -> str:
        return """verify factual claims, validate citations, check for inconsistencies,
        and ensure the research content is accurate and well-supported by evidence."""
    
    def fact_check(
        self,
        content: str,
        sources: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Fact-check research content.
        
        Args:
            content: The content to fact-check
            sources: List of sources to validate
            context: Additional context
        
        Returns:
            Fact-checking results with verified claims and issues
        """
        fact_check_prompt = f"""Fact-check the following research content:

Content:
---
{content}
---

{f"Sources to validate:\n{chr(10).join(f'- {s}' for s in sources)}\n" if sources else ""}

Please:
1. **Identify factual claims** in the content
2. **Verify each claim** against available sources and general knowledge
3. **Check for inconsistencies** or contradictions
4. **Validate citations** - ensure they support the claims made
5. **Flag unsupported claims** that lack evidence
6. **Identify potential errors** or misleading statements

Cross-reference mode: {"Enabled" if self.cross_reference else "Disabled"}

Provide:
- List of verified claims (with confidence scores)
- List of unverified or questionable claims
- Citation validation results
- Any inconsistencies found
- Overall factual accuracy score (0-1)"""
        
        result = self.process(fact_check_prompt, context)
        
        # Parse fact-checking results
        verification_results = self._parse_verification_results(result["output"])
        result["verified_claims"] = verification_results.get("verified", [])
        result["questionable_claims"] = verification_results.get("questionable", [])
        result["factual_accuracy"] = verification_results.get("accuracy_score", 0.8)
        
        return result
    
    def _parse_verification_results(self, text: str) -> Dict[str, Any]:
        """Parse fact-checking results from text."""
        results = {
            "verified": [],
            "questionable": [],
            "accuracy_score": 0.8
        }
        
        # Simple parsing - in production, use more sophisticated NLP
        lines = text.split("\n")
        current_section = None
        
        for line in lines:
            line_lower = line.lower()
            if "verified" in line_lower or "confirmed" in line_lower:
                current_section = "verified"
            elif "questionable" in line_lower or "unverified" in line_lower:
                current_section = "questionable"
            elif "accuracy" in line_lower and "score" in line_lower:
                # Try to extract score
                import re
                score_match = re.search(r"([0-9.]+)", line)
                if score_match:
                    try:
                        results["accuracy_score"] = float(score_match.group(1))
                    except ValueError:
                        pass
            
            if current_section and line.strip() and not line.strip().startswith("-"):
                if len(line.strip()) > 20:  # Likely a claim
                    results[current_section].append(line.strip())
        
        return results
    
    def validate_citations(self, content: str, citations: List[str]) -> Dict[str, Any]:
        """
        Validate citations in the content.
        
        Args:
            content: The content with citations
            citations: List of citations to validate
        
        Returns:
            Citation validation results
        """
        validation_prompt = f"""Validate the following citations in the research content:

Content:
---
{content}
---

Citations to validate:
{chr(10).join(f'- {c}' for c in citations)}

Check:
1. Are citations properly formatted?
2. Do citations appear in the content where claims are made?
3. Are citations relevant to the claims they support?
4. Are there missing citations for major claims?

Provide validation results for each citation."""
        
        result = self.process(validation_prompt)
        
        return {
            "validated_citations": citations,  # Simplified
            "validation_results": result["output"],
            "citation_score": 0.85  # Placeholder
        }
    
    def _calculate_confidence(self, output: str) -> float:
        """Calculate confidence based on fact-checking thoroughness."""
        base_confidence = super()._calculate_confidence(output)
        
        # Higher confidence if specific claims are identified
        if "claim" in output.lower() or "verified" in output.lower():
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)

