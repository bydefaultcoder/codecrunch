"""
Main entry point for the AI Research Lab Simulator.
"""

import argparse
import json
from src.pipeline.orchestrator import ResearchPipeline


def main():
    """Main function to run the research pipeline."""
    parser = argparse.ArgumentParser(
        description="AI Research Lab Simulator - Multi-agent LLM research pipeline"
    )
    parser.add_argument(
        "topic",
        type=str,
        help="Research topic to investigate"
    )
    parser.add_argument(
        "--requirements",
        type=str,
        default=None,
        help="Additional user requirements"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output.json",
        help="Output file path (default: output.json)"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "text"],
        default="json",
        help="Output format (default: json)"
    )
    
    args = parser.parse_args()
    
    print(f"🔬 Starting AI Research Lab Simulator")
    print(f"📝 Topic: {args.topic}")
    print(f"{'='*60}\n")
    
    # Initialize pipeline
    pipeline = ResearchPipeline()
    
    # Run pipeline
    print("🚀 Running research pipeline...\n")
    result = pipeline.run(
        topic=args.topic,
        user_requirements=args.requirements
    )
    
    # Output results
    if args.format == "json":
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Results saved to {args.output}")
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(f"Research Topic: {result['topic']}\n")
            f.write("="*60 + "\n\n")
            f.write(result['document'])
            f.write("\n\n" + "="*60 + "\n")
            f.write(f"Iterations: {result['iterations']}\n")
            f.write(f"Converged: {result['converged']}\n")
            f.write(f"Scores: {json.dumps(result['scores'], indent=2)}\n")
        print(f"\n✅ Results saved to {args.output}")
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"   Iterations: {result['iterations']}")
    print(f"   Converged: {result['converged']}")
    print(f"   Overall Score: {result['scores'].get('overall_score', 0):.2f}")
    print(f"   Agent Interactions: {len(result['agent_interactions'])}")


if __name__ == "__main__":
    main()

