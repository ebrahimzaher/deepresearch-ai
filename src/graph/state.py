from typing import List, Dict, Any, TypedDict

class State(TypedDict):
    query: str
    plan: dict
    research: dict
    source_index: Dict[str, Any]
    report: str
    critique: dict
    chat_history: List[Dict[str, Any]]
    context_summary: str