import json
from typing import List
from langgraph.graph import END
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage, HumanMessage
from llm_setup import llm, tavily_tool
from model import AnswerQuestion, ReviseAnswer
from prompt_template import prompt_template, revise_instructions

# Max iterations for the event loop
MAX_ITERATIONS = 2

# Chains
initial_chain = prompt_template.partial(first_instruction="Provide a detailed ~250 word answer") | llm.bind_tools(tools=[AnswerQuestion], tool_choice="required")
revisor_prompt = prompt_template.partial(first_instruction=revise_instructions)
revisor_chain = revisor_prompt | llm.bind_tools(tools=[ReviseAnswer], tool_choice="required")

def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
    last_ai_message = state[-1]
    tool_messages = []
    
    if not hasattr(last_ai_message, "tool_calls") or not last_ai_message.tool_calls:
        print("--- No tool calls found in last message ---")
        return []

    for tool_call in last_ai_message.tool_calls:
        tool_name = tool_call["name"]
        call_id = tool_call["id"]
        print(f"--- Executing tool: {tool_name} (ID: {call_id}) ---")
        
        query_results = {}
        if tool_name.lower() in ["answerquestion", "reviseanswer"]:
            search_queries = tool_call["args"].get("search_queries", [])
            for query in search_queries:
                print(f"--- Searching for: {query} ---")
                try:
                    full_results = tavily_tool.invoke(query)
                    # Extract and truncate content to save tokens
                    short_results = []
                    for r in full_results[:2]:  # Limit to top 2 results per query
                        short_results.append({
                            "url": r.get("url"),
                            "content": r.get("content", "")[:1000] # Truncate content
                        })
                    query_results[query] = short_results
                except Exception as e:
                    print(f"--- Search failed for '{query}': {e} ---")
                    query_results[query] = f"Error: {e}"
        else:
            print(f"--- Warning: Unexpected tool call '{tool_name}' ---")
            query_results["error"] = f"Tool '{tool_name}' not supported."

        tool_messages.append(ToolMessage(
            content=json.dumps(query_results),
            tool_call_id=call_id)
        )
    return tool_messages

def event_loop(state: List[BaseMessage]) -> str:
    last_message = state[-1]
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        print("--- No tool calls found, ending workflow ---")
        return END

    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    if count_tool_visits >= MAX_ITERATIONS:
        print(f"--- Reached MAX_ITERATIONS ({MAX_ITERATIONS}), ending workflow ---")
        return END
    
    print(f"--- Continuing to execute_tools (Iteration: {count_tool_visits}) ---")
    return "execute_tools"

def respond_node(state):
    return initial_chain.invoke({"messages": state})

def revisor_node(state):
    return revisor_chain.invoke({"messages": state})