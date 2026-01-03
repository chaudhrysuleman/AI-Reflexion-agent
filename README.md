# Reflexion Agent

This project implements a **Reflexion Agent** using [LangGraph](https://github.com/langchain-ai/langgraph). The agent is designed to provide high-quality, evidence-based answers to health and nutrition questions by iteratively critiquing and refining its own responses.

## Key Features

- **Iterative Refinement**: The agent doesn't just provide a single answer. It critiques its own drafts, identifies missing information, and performs additional research to improve the quality of the final response.
- **Evidence-Based**: Integrated with [Tavily Search](https://tavily.com/) to fetch the latest research and peer-reviewed citations.
- **Structured Output**: Uses Pydantic models to ensure the output includes clear answers, self-reflections, and full URL references.
- **Medical Persona**: Configured with an elite medical researcher persona for clinical precision and objective analysis.
- **Graph Visualization**: Automatically saves the agentic workflow visualization as `graph.png`.

## Project Structure

- `reflexion_agent.py`: The main entry point to run the agent.
- `graph.py`: Defines the LangGraph workflow structure (nodes and edges).
- `helper.py`: Contains node functions for responding, executing tools, and the iteration loop.
- `model.py`: Pydantic data models for structured tool calls and responses.
- `prompt_template.py`: Optimized system prompts and instructions for the agent.
- `llm_setup.py`: Centralized configuration for the LLM (GPT-4o-mini) and search tools.

## Setup

1. **Environment Variables**: Create a `.env` file in the root directory with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

2. **Install Dependencies**:
   ```bash
   pip install langgraph langchain-openai langchain-community tavily-python python-dotenv
   ```
   *Note: If you want to save the graph visualization, you may need `pygraphviz` and the `graphviz` system library.*

## How to Run

Execute the main script:
```bash
python reflexion_agent/reflexion_agent.py
```

The script will:
1. Initialize the workflow with a health-related question.
2. Execute multiple rounds of research and self-reflection.
3. Print the final refined answer along with a list of references.
4. Save the workflow graph as `graph.png`.
