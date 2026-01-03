from langchain_core.messages import HumanMessage
from helper import execute_tools
from graph import app

def run_agent(question: str):
    responses = app.invoke(
        [HumanMessage(content=question)],
        config={"recursion_limit": 50}
    )

    # Save the graph visualization
    try:
        # Use draw_png if pygraphviz is installed, or draw_mermaid_png if not
        # Trying a slightly more robust way to get png data
        png_data = app.get_graph().draw_png()
        with open("reflexion_agent/graph.png", "wb") as f:
            f.write(png_data)
        print("--- Graph saved as 'reflexion_agent/graph.png' ---")
    except Exception as e:
        # Fallback if dependencies are missing
        print(f"--- Notice: Could not save graph visualization: {e} ---")

    results = []
    # Collect all tool responses in reverse order
    for msg in reversed(responses):
        if getattr(msg, 'tool_calls', None):
            for tool_call in msg.tool_calls:
                args = tool_call.get('args', {})
                answer = args.get('answer')
                if answer:
                    reflection = args.get('reflection', {})
                    references = args.get('references', [])
                    results.append({
                        "answer": answer, 
                        "reflection": reflection,
                        "references": references
                    })

    if results:
        # Show only the last (final) answer with its references
        final_res = results[0]
        print("\n--- Final Answer ---")
        print(final_res["answer"])
        
        if final_res["references"]:
            print("\nReferences:")
            for ref in final_res["references"]:
                print(f"- {ref}")
        print("-" * 50)
    else:
        print("No results found.")

if __name__ == "__main__":
    question = """I'm pre-diabetic and need to lower my blood sugar, and I have heart issues.
    What breakfast foods should I eat and avoid"""
    run_agent(question)
