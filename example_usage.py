"""
Example usage of the AI Research Lab Simulator.
"""

from src.pipeline.orchestrator import ResearchPipeline
import json


def example_basic_research():
    """Basic research example."""
    print("=" * 60)
    print("Example 1: Basic Research")
    print("=" * 60)
    
    pipeline = ResearchPipeline()
    
    result = pipeline.run(
        topic="The Impact of Artificial Intelligence on Education",
        user_requirements="Focus on recent developments and include case studies"
    )
    
    print(f"\n📄 Document Preview:")
    print(result["document"][:500] + "...")
    print(f"\n📊 Scores: {json.dumps(result['scores'], indent=2)}")
    print(f"🔄 Iterations: {result['iterations']}")
    print(f"✅ Converged: {result['converged']}")


def example_custom_config():
    """Example with custom configuration."""
    print("\n" + "=" * 60)
    print("Example 2: Custom Configuration")
    print("=" * 60)
    
    # Modify config before creating pipeline
    from src.config import config
    config.pipeline_config["max_iterations"] = 3
    config.pipeline_config["convergence_threshold"] = 0.80
    
    pipeline = ResearchPipeline()
    
    result = pipeline.run(
        topic="Sustainable Energy Solutions",
        user_requirements="Compare solar and wind energy"
    )
    
    print(f"\n📄 Document Length: {len(result['document'])} characters")
    print(f"📊 Overall Score: {result['scores'].get('overall_score', 0):.2f}")
    print(f"🔄 Iterations: {result['iterations']}")
    print(f"🤖 Agent Interactions: {len(result['agent_interactions'])}")


def example_save_results():
    """Example saving results to file."""
    print("\n" + "=" * 60)
    print("Example 3: Save Results")
    print("=" * 60)
    
    pipeline = ResearchPipeline()
    
    result = pipeline.run(
        topic="Quantum Computing Breakthroughs",
        user_requirements="Focus on 2024 developments"
    )
    
    # Save to JSON
    with open("example_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print("✅ Results saved to example_output.json")
    
    # Save document only
    with open("example_document.txt", "w", encoding="utf-8") as f:
        f.write(f"Research Topic: {result['topic']}\n")
        f.write("=" * 60 + "\n\n")
        f.write(result["document"])
    
    print("✅ Document saved to example_document.txt")


if __name__ == "__main__":
    print("🔬 AI Research Lab Simulator - Examples\n")
    
    # Uncomment the example you want to run:
    
    # example_basic_research()
    # example_custom_config()
    # example_save_results()
    
    print("\n💡 Uncomment examples in example_usage.py to run them!")
    print("💡 Make sure you have set up your .env file with API keys first!")

