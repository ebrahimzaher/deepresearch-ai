from langgraph.graph import StateGraph, END
from .state import State
from .nodes import planner_node, researcher_node, writer_node, critic_node, summarizer_node

workflow = StateGraph(State)
workflow.add_node("summarizer", summarizer_node)
workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("critic", critic_node)

workflow.set_entry_point("summarizer")

workflow.add_edge("summarizer", "planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "critic")
workflow.add_edge("critic", END)

app = workflow.compile()