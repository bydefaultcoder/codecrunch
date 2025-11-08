"""
Streamlit UI for the AI Research Lab Simulator.
"""

import streamlit as st
import json
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline.orchestrator import ResearchPipeline


def main():
    st.set_page_config(
        page_title="AI Research Lab Simulator",
        page_icon="🔬",
        layout="wide"
    )
    
    st.title("🔬 AI Research Lab Simulator")
    st.markdown("**Multi-agent LLM research pipeline for autonomous research document generation**")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.markdown("Configure your research pipeline settings here.")
        
        # Topic input
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g., Quantum Computing Applications in Cryptography",
            help="Enter the research topic you want to investigate"
        )
        
        requirements = st.text_area(
            "Additional Requirements (Optional)",
            placeholder="e.g., Focus on recent developments, include case studies",
            help="Any specific requirements for the research"
        )
        
        max_iterations = st.slider(
            "Max Iterations",
            min_value=1,
            max_value=10,
            value=5,
            help="Maximum number of refinement iterations"
        )
        
        convergence_threshold = st.slider(
            "Convergence Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.85,
            step=0.05,
            help="Quality threshold for convergence"
        )
        
        if st.button("🚀 Start Research", type="primary"):
            if not topic:
                st.error("Please enter a research topic")
                return
            
            # Store in session state
            st.session_state.topic = topic
            st.session_state.requirements = requirements
            st.session_state.max_iterations = max_iterations
            st.session_state.convergence_threshold = convergence_threshold
            st.session_state.run_pipeline = True
    
    # Main content area
    if "run_pipeline" in st.session_state and st.session_state.run_pipeline:
        run_pipeline_ui()
    else:
        show_welcome()


def show_welcome():
    """Show welcome screen."""
    st.markdown("""
    ### Welcome to the AI Research Lab Simulator
    
    This system uses multiple specialized AI agents to collaboratively produce research documents:
    
    - **Researcher**: Gathers information and generates content
    - **Fact-Checker**: Verifies claims and validates citations
    - **Reviewer**: Critiques methodology and quality
    - **Editor**: Synthesizes and refines the document
    
    **How to use:**
    1. Enter a research topic in the sidebar
    2. Optionally add specific requirements
    3. Configure iteration and convergence settings
    4. Click "Start Research" to begin
    
    The system will run multiple iterations, with agents collaborating to improve the document
    until it meets the quality threshold or reaches the maximum iterations.
    """)


def run_pipeline_ui():
    """Run the pipeline and show results."""
    topic = st.session_state.topic
    requirements = st.session_state.requirements
    max_iterations = st.session_state.max_iterations
    convergence_threshold = st.session_state.convergence_threshold
    
    # Update config
    from src.config import config
    config.update_pipeline_config("max_iterations", max_iterations)
    config.update_pipeline_config("convergence_threshold", convergence_threshold)
    
    # Initialize pipeline
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = ResearchPipeline()
    
    pipeline = st.session_state.pipeline
    
    # Progress tracking
    progress_placeholder = st.empty()
    status_placeholder = st.empty()
    
    # Run pipeline
    with st.spinner("Running research pipeline..."):
        progress_placeholder.progress(0)
        status_placeholder.info(f"🔬 Researching: {topic}")
        
        try:
            # Validate API key before running
            from src.config import config as cfg
            llm_config = cfg.get_llm_config()
            if not llm_config.get("api_key"):
                st.error("❌ **OpenAI API key is not configured**")
                st.info("💡 Please set `OPENAI_API_KEY` in your `.env` file.\n\nRun `python test_api_keys.py` to verify your API key.")
                return
            
            result = pipeline.run(
                topic=topic,
                user_requirements=requirements if requirements else None
            )
            
            progress_placeholder.progress(1.0)
            status_placeholder.success("✅ Research complete!")
        except ConnectionError as e:
            progress_placeholder.empty()
            status_placeholder.error("❌ **Connection Error**")
            st.error(str(e))
            st.info("💡 **Troubleshooting tips:**\n"
                   "1. Check your internet connection\n"
                   "2. Verify your API key is correct\n"
                   "3. Check if OpenAI API is accessible\n"
                   "4. Review firewall/proxy settings")
            return
        except ValueError as e:
            progress_placeholder.empty()
            status_placeholder.error("❌ **Configuration Error**")
            st.error(str(e))
            return
        except Exception as e:
            progress_placeholder.empty()
            status_placeholder.error("❌ **Error**")
            st.error(f"An error occurred: {str(e)}")
            st.info("💡 Run `python test_api_keys.py` to verify your API configuration.")
            return
    
    # Display results
    st.header("📄 Research Document")
    st.markdown(result["document"])
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Iterations", result["iterations"])
    
    with col2:
        st.metric("Converged", "Yes" if result["converged"] else "No")
    
    with col3:
        overall_score = result["scores"].get("overall_score", 0)
        st.metric("Overall Score", f"{overall_score:.2f}")
    
    with col4:
        st.metric("Interactions", len(result["agent_interactions"]))
    
    # Detailed scores
    with st.expander("📊 Detailed Scores"):
        scores = result["scores"]
        for metric, score in scores.items():
            st.progress(score, text=f"{metric.replace('_', ' ').title()}: {score:.2f}")
    
    # Agent interactions
    with st.expander("🤖 Agent Interactions"):
        for interaction in result["agent_interactions"]:
            st.markdown(f"""
            **{interaction['agent'].title()}** (Iteration {interaction['iteration']})
            - {interaction.get('output', interaction.get('score', 'N/A'))}
            """)
    
    # Sources
    if result.get("sources"):
        with st.expander("📚 Sources"):
            for source in result["sources"]:
                st.markdown(f"- {source}")
    
    # Feedback history
    if result.get("feedback_history"):
        with st.expander("💬 Feedback History"):
            for i, feedback in enumerate(result["feedback_history"], 1):
                st.markdown(f"**Feedback {i}:**\n{feedback}")
    
    # Reset button
    if st.button("🔄 Start New Research"):
        for key in list(st.session_state.keys()):
            if key != "pipeline":
                del st.session_state[key]
        st.rerun()


if __name__ == "__main__":
    main()

