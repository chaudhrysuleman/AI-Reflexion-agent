

from langgraph.graph import MessageGraph
from helper import respond_node, execute_tools, revisor_node, event_loop

graph=MessageGraph()

graph.add_node("respond", respond_node)
graph.add_node("execute_tools", execute_tools)
graph.add_node("revisor", revisor_node)

graph.add_edge("respond", "execute_tools")
graph.add_edge("execute_tools", "revisor")

graph.add_conditional_edges("revisor", event_loop)
graph.set_entry_point("respond")

app = graph.compile()