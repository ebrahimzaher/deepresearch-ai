from fastapi import FastAPI
from pydantic import BaseModel
from src.services.memory import load_memory
from src.graph import app as research_app
from src.agents import revision_agent, critic_agent
from typing import Dict, Any, Optional, List

app = FastAPI(
    title="DeepResearch AI",
    version="2.0.0"
)

# --- Request Models ---

class ResearchRequest(BaseModel):
    query: str

class RevisionRequest(BaseModel):
    query: str
    report: str
    user_feedback: str
    research_data: List[Any]
    source_index: Dict[str, Any]
    revision_count: int = 0


# --- Response Models ---

class ResearchResponse(BaseModel):
    query: str
    report: str
    critique: Dict[str, Any]
    source_index: Optional[Dict[str, Any]] = None
    research_data: Optional[List[Any]] = None
    revision_count: int = 0

class RevisionResponse(BaseModel):
    report: str
    critique: Dict[str, Any]
    revision_count: int


# --- Endpoints ---

@app.get("/")
async def read_root():
    return {"message": "Welcome to DeepResearch AI!"}


@app.post("/research", response_model=ResearchResponse)
async def perform_research(request: ResearchRequest):

    result = research_app.invoke({"query": request.query})

    return {
        "query": request.query,
        "report": result["report"],
        "critique": result["critique"],
        "source_index": result.get("source_index", {}),
        "research_data": result.get("research", []),
        "revision_count": result.get("revision_count", 0)
    }


@app.post("/revise", response_model=RevisionResponse)
async def revise_report(request: RevisionRequest):
    """Human-in-the-Loop: user rejects report and provides feedback for revision."""
    
    new_revision_count = request.revision_count + 1

    # Run revision writer with user feedback
    revised_report = revision_agent(
        query=request.query,
        original_report=request.report,
        critique_feedback=request.user_feedback,
        research_data=request.research_data,
        source_index=request.source_index
    )

    # Run critic on the revised report
    new_critique = critic_agent(revised_report)

    return {
        "report": revised_report,
        "critique": new_critique,
        "revision_count": new_revision_count
    }


@app.get("/memory")
async def get_memory():
    return load_memory()