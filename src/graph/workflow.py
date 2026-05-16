from langgraph.graph import StateGraph, END
from .state import State
from .nodes import planner_node, researcher_node, writer_node, critic_node

workflow = StateGraph(State)
workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("critic", critic_node)

workflow.set_entry_point("planner")

workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "critic")
workflow.add_edge("critic", END)

app = workflow.compile()