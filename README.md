---
title: DeepResearch AI
emoji: 🧠
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
short_description: Stateful multi-agent AI research system with LangGraph
tags:
  - ai
  - research
  - langgraph
  - langchain
  - fastapi
  - streamlit
  - groq
pinned: false
---

<div align="center">

# 🧠 DeepResearch AI

**A stateful multi-agent research system that automates complex research workflows using LLM-powered planning, real-time web retrieval, and reflection-based evaluation.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.2-FF6B6B?style=flat)](https://langchain-ai.github.io/langgraph/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.57-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Spaces-FFD21E?style=flat)](https://huggingface.co/spaces/ebrahimzaher/deepresearch-ai-demo)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

[**🚀 Live Demo**](https://huggingface.co/spaces/ebrahimzaher/deepresearch-ai-demo) · [**📖 API Docs**](https://huggingface.co/spaces/ebrahimzaher/deepresearch-ai-demo/api/docs) · [**🐛 Report Bug**](https://github.com/ebrahimzaher/deepresearch-ai/issues)

</div>

---

## Overview

DeepResearch AI is a production-ready multi-agent research pipeline built on **LangGraph**. Given a research topic, the system autonomously decomposes it into subtopics, retrieves live web content, synthesizes a structured report with inline citations, and evaluates it through a Critic agent — automatically triggering revisions when quality falls below a threshold.

The final report is presented through an interactive **Streamlit** frontend backed by a **FastAPI** REST API, with full support for **Human-in-the-Loop (HITL)** approval and PDF export.

---

## Features

| Feature | Description |
|---|---|
| 🗂️ **Query Decomposition** | Planner agent breaks complex queries into focused research subtopics |
| 🌐 **Real-Time Web Retrieval** | Tavily Search API fetches live, relevant sources per subtopic |
| 📝 **Citation-Aware Reports** | Inline `[1]`, `[2]` citations linked to a structured Sources section |
| 🔄 **Reflection & Auto-Revision** | Critic scores reports 1–10; scores below 7 trigger automatic revision (max 2 cycles) |
| 🤝 **Human-in-the-Loop** | Users approve or reject reports with custom feedback for further revision |
| 🧠 **Context Summarization** | Maintains research continuity across consecutive queries |
| 📊 **Critic Dashboard** | Score, strengths, weaknesses, citation quality, and revision suggestions |
| 📄 **PDF Export** | Unicode-safe PDF generation via ReportLab |
| 💾 **Persistent Memory** | Research history saved locally across sessions |
| 🐳 **Docker Ready** | Single-command deployment with Docker Compose |

---

## Architecture

The system is orchestrated as a **LangGraph state machine** with conditional routing and a reflection loop:

```
User Query
    │
    ▼
┌─────────────────┐
│ Summarizer Agent│  ← Maintains research context across sessions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Planner Agent  │  ← Decomposes query into research subtopics
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Research Agent  │  ← Real-time web retrieval + citation indexing
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Writer Agent   │  ← Synthesizes structured report with inline citations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Critic Agent   │  ← Scores report (1–10), identifies gaps
└────┬────────────┘
     │
     ├── score < 7 AND revisions < 2  ──► Revision Agent ──► Critic (loop)
     │
     └── score ≥ 7 OR max revisions reached
              │
              ▼
        Return to User
         (Approve / Reject with Feedback)
                  │
                  └── Rejected ──► /revise API ──► Revision ──► Critic
```

---

## Agent Pipeline

### 1. Summarizer Agent
Analyzes conversation history and generates a concise context summary before each research session. Prevents redundant research across consecutive queries.

### 2. Planner Agent
Decomposes the user's query into focused, non-overlapping subtopics using structured Pydantic output. Acts as the research blueprint for downstream agents.

### 3. Research Agent
Performs real-time web retrieval via Tavily Search API per subtopic. Builds a **global source index** — each source receives a unique citation number `[1]`, `[2]`, etc. — and annotates content chunks for downstream traceability.

### 4. Writer Agent
Synthesizes all retrieved content into a structured markdown report. Embeds **inline citations** throughout and appends a formatted **Sources** section with titles and URLs.

### 5. Critic Agent
Evaluates the report across four dimensions:
- **Clarity & Completeness** — overall depth and coverage
- **Technical Depth** — accuracy and specificity
- **Citation Quality** — inline citations and sources section presence
- **Revision Suggestions** — concrete, actionable improvements

Returns a structured JSON evaluation with a numeric score. Scores below **7/10** trigger automatic revision.

### 6. Revision Agent
Activated by the Critic (automatic) or the user (HITL). Receives the original report, critic/user feedback, and the full research dataset, then produces an improved version while preserving structure and citations.

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.10+ |
| Agent Orchestration | LangGraph + LangChain | 1.2 / 1.3 |
| LLM Provider | Groq API | — |
| Web Retrieval | Tavily Search API | 0.7 |
| Backend | FastAPI + Uvicorn | 0.136 / 0.47 |
| Frontend | Streamlit | 1.57 |
| PDF Generation | ReportLab | 4.5 |
| Data Validation | Pydantic | — |
| Containerization | Docker + Docker Compose | — |

---

## API Reference

### `POST /research`
Runs the full multi-agent research pipeline.

**Request**
```json
{ "query": "Future of AI agents in software engineering" }
```

**Response**
```json
{
  "query": "Future of AI agents in software engineering",
  "report": "# AI-Enhanced Software Development\n\n...",
  "critique": {
    "score": 8,
    "strengths": ["Comprehensive coverage", "Well-structured sections"],
    "weaknesses": ["Lacks real-world case studies"],
    "missing_topics": ["Cost analysis", "Vendor lock-in risks"],
    "citation_quality": {
      "has_inline_citations": true,
      "has_sources_section": true,
      "notes": "All major claims are properly cited."
    },
    "revision_suggestions": ["Add case studies", "Include cost analysis"],
    "final_verdict": "Strong report with minor gaps."
  },
  "source_index": {
    "1": { "title": "AI Agents Overview", "url": "https://example.com/ai-agents" }
  },
  "revision_count": 1
}
```

### `POST /revise`
Triggers a Human-in-the-Loop revision with custom user feedback.

### `GET /memory`
Returns the full research history from persistent local storage.

Interactive API documentation: **`/docs`** (Swagger UI)

---

## Quickstart

### Option 1 — Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/ebrahimzaher/deepresearch-ai.git
cd deepresearch-ai

# 2. Configure environment variables
cp .env.example .env
# Edit .env and add your API keys:
# GROQ_API_KEY=your_groq_api_key
# TAVILY_API_KEY=your_tavily_api_key

# 3. Build and run
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend (Streamlit) | http://localhost:8501 |
| Backend (FastAPI) | http://localhost:8080 |
| API Documentation | http://localhost:8080/docs |

---

### Option 2 — Local Setup

```bash
# 1. Clone and create virtual environment
git clone https://github.com/ebrahimzaher/deepresearch-ai.git
cd deepresearch-ai
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate
# Activate (Windows)
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables
# Create a .env file with:
# GROQ_API_KEY=your_groq_api_key
# TAVILY_API_KEY=your_tavily_api_key

# 4. Start the backend
uvicorn api.main:app --reload --port 8000

# 5. Start the frontend (in a new terminal)
streamlit run frontend/app.py
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | API key from [console.groq.com](https://console.groq.com) |
| `TAVILY_API_KEY` | ✅ | API key from [app.tavily.com](https://app.tavily.com) |
| `BACKEND_URL` | ⚙️ | Backend URL for the frontend (default: `http://localhost:8000`) |

---

## Project Structure

```
deepresearch-ai/
├── api/
│   └── main.py              # FastAPI application & endpoints
├── frontend/
│   └── app.py               # Streamlit UI
├── src/
│   ├── agents/              # Individual agent implementations
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   ├── writer.py
│   │   ├── critic.py
│   │   ├── revision.py
│   │   └── summarizer.py
│   ├── graph/               # LangGraph workflow
│   │   ├── workflow.py      # Graph definition & compilation
│   │   ├── nodes.py         # Node functions
│   │   └── state.py         # Shared state schema
│   ├── prompts/             # Agent prompt templates
│   └── services/            # Shared utilities (memory, search)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── start.sh                 # Container startup script
```

---

## Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Built by [Ebrahim Zaher](https://github.com/ebrahimzaher)**

⭐ Star this repo if you find it useful!

</div>
