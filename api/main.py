from fastapi import FastAPI
from pydantic import BaseModel
from src.services.memory import load_memory
from src.graph import app as research_app
from typing import Dict, Any

app = FastAPI(
    title="DeepResearch AI",
    version="1.0.0"
)

class ResearchRequest(BaseModel):
    query: str


class ResearchResponse(BaseModel):
    query: str
    report: str
    critique: Dict[str, Any]


@app.get("/")
async def read_root():
    return {"message": "Welcome to DeepResearch AI!"}


@app.post("/research", response_model=ResearchResponse)
async def perform_research(request: ResearchRequest):

    result = research_app.invoke({"query": request.query})

    return {
        "query": request.query,
        "report": result["report"],
        "critique": result["critique"]
    }

@app.get("/memory")
async def get_memory():
    return load_memory()