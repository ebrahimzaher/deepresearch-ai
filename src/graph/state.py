from typing import TypedDict

class State(TypedDict):
    query: str
    plan: dict
    research: dict
    report: str