"""
Evaluation system for assessing research document quality.
"""

from typing import Dict, Any, Optional
from src.config import config


class Evaluator:
    """Evaluates research documents across multiple dimensions."""
    
    def __init__(self):
        self.eval_config = config.get_evaluation_config()
        self.metrics = self.eval_config.get("metrics", [
            "factual_accuracy",
            "logical_coherence",
            "linguistic_clarity"
        ])
        self.weights = self.eval_config.get("weights", {
            "factual_accuracy": 0.4,
            "logical_coherence": 0.3,
            "linguistic_clarity": 0.3,
        })
    
    def evaluate(
        self,
        content: str,
        previous_content: Optional[str] = None,
        topic: str = ""
    ) -> Dict[str, float]:
        """
        Evaluate research content.
        
        Args:
            content: Current content to evaluate
            previous_content: Previous version for comparison
            topic: Research topic
        
        Returns:
            Dictionary of scores
        """
        scores = {}
        
        # Factual accuracy (placeholder - would use fact-checker results)
        scores["factual_accuracy"] = self._evaluate_factual_accuracy(content)
        
        # Logical coherence
        scores["logical_coherence"] = self._evaluate_coherence(content)
        
        # Linguistic clarity
        scores["linguistic_clarity"] = self._evaluate_clarity(content)
        
        # Calculate overall score
        overall = sum(
            scores.get(metric, 0.7) * self.weights.get(metric, 0.33)
            for metric in self.metrics
        )
        scores["overall_score"] = overall
        
        # Improvement score (if previous content exists)
        if previous_content:
            scores["improvement"] = self._calculate_improvement(
                previous_content,
                content
            )
        
        return scores
    
    def _evaluate_factual_accuracy(self, content: str) -> float:
        """Evaluate factual accuracy (simplified heuristic)."""
        # In production, this would use fact-checker results
        # For now, use heuristics
        
        # Positive indicators
        positive_indicators = [
            "according to",
            "research shows",
            "studies indicate",
            "source:",
            "citation",
            "reference"
        ]
        
        positive_count = sum(1 for ind in positive_indicators if ind.lower() in content.lower())
        
        # Negative indicators
        negative_indicators = [
            "might be",
            "possibly",
            "uncertain",
            "unclear"
        ]
        
        negative_count = sum(1 for ind in negative_indicators if ind.lower() in content.lower())
        
        # Base score
        base_score = 0.7
        
        # Adjust based on indicators
        if positive_count > 3:
            base_score += 0.15
        elif positive_count > 1:
            base_score += 0.1
        
        if negative_count > 2:
            base_score -= 0.1
        
        return min(max(base_score, 0.0), 1.0)
    
    def _evaluate_coherence(self, content: str) -> float:
        """Evaluate logical coherence."""
        # Heuristic: check for structure and flow
        
        # Check for structure
        has_structure = any(marker in content for marker in ["##", "###", "**", "*"])
        
        # Check length (too short = low coherence)
        word_count = len(content.split())
        
        # Check for transitions
        transitions = [
            "however", "therefore", "furthermore", "moreover",
            "in addition", "consequently", "thus", "hence"
        ]
        transition_count = sum(1 for t in transitions if t.lower() in content.lower())
        
        base_score = 0.6
        
        if has_structure:
            base_score += 0.15
        
        if word_count > 200:
            base_score += 0.1
        elif word_count < 50:
            base_score -= 0.2
        
        if transition_count > 2:
            base_score += 0.1
        
        return min(max(base_score, 0.0), 1.0)
    
    def _evaluate_clarity(self, content: str) -> float:
        """Evaluate linguistic clarity."""
        # Heuristic: check for clarity indicators
        
        # Check sentence length (very long sentences = unclear)
        sentences = content.split(".")
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        # Check for jargon (simplified)
        clarity_indicators = [
            "in other words",
            "specifically",
            "for example",
            "that is"
        ]
        clarity_count = sum(1 for ind in clarity_indicators if ind.lower() in content.lower())
        
        base_score = 0.7
        
        # Penalize very long sentences
        if avg_sentence_length > 25:
            base_score -= 0.15
        elif avg_sentence_length < 10:
            base_score += 0.1
        
        # Reward clarity indicators
        if clarity_count > 1:
            base_score += 0.1
        
        return min(max(base_score, 0.0), 1.0)
    
    def _calculate_improvement(self, previous: str, current: str) -> float:
        """Calculate improvement score between versions."""
        # Simple heuristic: compare lengths and structure
        
        prev_score = (
            len(previous) * 0.3 +
            previous.count("\n") * 10 +
            (1 if "##" in previous else 0) * 50
        )
        
        curr_score = (
            len(current) * 0.3 +
            current.count("\n") * 10 +
            (1 if "##" in current else 0) * 50
        )
        
        if prev_score == 0:
            return 1.0
        
        improvement = (curr_score - prev_score) / max(prev_score, 1)
        return min(max(improvement, 0.0), 1.0)

