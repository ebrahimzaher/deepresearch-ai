# 🧠 DeepResearch AI

A stateful multi-agent AI research system that automates complex research workflows using LLM-powered planning, real-time web retrieval, AI-generated report synthesis, reflection-based evaluation, conditional agent routing, human-in-the-loop revision, and API-based orchestration.

Built with Python, LangChain, LangGraph, Groq LLMs, FastAPI, Streamlit, and Tavily Search API.

---

## 🚀 Features

- Autonomous query decomposition using AI planning agents
- Real-time web retrieval with Tavily Search API
- AI-generated structured markdown research reports
- **Citation-aware generation** — inline `[1]`, `[2]` citations linked to source URLs
- **Conditional agent routing & reflection loops** — automatic revision when critic score < 7 (max 2 auto-revisions)
- **Human-in-the-Loop (HITL)** — user approves or rejects reports with custom feedback for revision
- PDF export with Unicode-safe rendering
- Reflection / Critic agent for structured report evaluation (including citation quality & revision suggestions)
- Context summarization agent to maintain research history/continuity
- Stateful multi-agent orchestration with LangGraph
- Shared workflow state across all agents (including source index & revision tracking)
- Structured outputs using Pydantic
- FastAPI backend with production-style REST API (`/research` + `/revise`)
- Interactive API documentation via Swagger UI
- Streamlit frontend with critic score dashboard, citation quality metrics, and HITL approval UI
- Modular and scalable agent architecture
- Persistent local memory storage (`history.json`) across sessions
- Research history sidebar with previous report loading
- Automatic report saving to `reports/` folder with timestamps
- Docker + Docker Compose containerized deployment
- Configurable backend URL via environment variables

---

## 🏗️ Architecture

The system operates as a LangGraph-powered state-based multi-agent workflow exposed through a FastAPI backend and a Streamlit frontend.

```text
                ┌─────────────────┐
                │   User Query    │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Streamlit Front │◄──(Loads History)──┐
                └────────┬────────┘                    │
                         ↓                             │
                ┌─────────────────┐                    │
                │  FastAPI Layer  │                    │
                └────────┬────────┘                    │
                         ↓                             │
                ┌─────────────────┐                    │
                │ Summarizer Agent│                    │
                └────────┬────────┘                    │
                         ↓                             │
                ┌─────────────────┐                    │
                │ Planner Agent   │                    │
                └────────┬────────┘                    │
                         ↓                             │
                ┌─────────────────┐                    │
                │ Research Agent  │                    │
                └────────┬────────┘                    │
                         ↓                             │
                ┌─────────────────┐                    │
                │  Writer Agent   │                    │
                └────────┬────────┘                    │
                         ↓                             │
                ┌─────────────────┐            ┌───────┴───────┐
           ┌───►│  Critic Agent   ├───────────►│ Local Memory  │
           │    └────────┬────────┘            │(history.json) │
           │             │                     └───────────────┘
           │    ┌────────┴───────┐
           │    │  Score < 7 ?   │
           │    └──┬──────────┬──┘
           │   Yes │          │ No
           │       ↓          ↓
           │  ┌──────────┐  ┌────────────────┐
           └──│ Revision │  │ Return to User │
              │  Agent   │  │  (Approve?)    │
              └──────────┘  └──┬──────────┬──┘
                            Yes│          │No + Feedback
                               ↓          ↓
                          ┌────────┐  ┌──────────┐
                          │  Done  │  │ /revise  │──► Revision ──► Critic
                          └────────┘  └──────────┘
```

---

## ⚡ LangGraph Workflow

The system uses LangGraph to orchestrate agent execution through a shared state-based workflow with **conditional routing**.

Each agent operates as an independent node:

- **Summarizer Node** — summarizes previous conversation/search history to maintain research context
- **Planner Node** — decomposes the query into focused research subtopics
- **Research Node** — retrieves real-time web content per subtopic
- **Writer Node** — synthesizes findings into a structured markdown report
- **Critic Node** — evaluates the report and returns structured JSON feedback
- **Revision Node** — improves the report based on critic feedback (triggered conditionally)

### Conditional Routing & Reflection Loop

After the Critic evaluates the report:
- If `score < 7` and `revision_count < 2` → the workflow automatically routes to the **Revision Node**, which improves the report and sends it back to the Critic for re-evaluation
- If `score >= 7` or max revisions reached → the report is finalized and returned to the user

### Human-in-the-Loop (HITL)

After the automatic loop completes, the user can:
- **✅ Approve** the report — finalizes it
- **❌ Reject** with custom feedback (e.g., "Add more details about security risks") — triggers a revision via the `/revise` API endpoint, then re-evaluates with the Critic

---

## 🤖 Agents

### 1. Summarizer Agent
- Uses `gpt-oss-120b` via Groq to analyze previous conversation history and the user's new query
- Generates a concise summary of the core research context to maintain query continuity
- Prevents redundant research across consecutive queries

### 2. Planner Agent
- Uses `gpt-oss-120b` via Groq for intelligent task planning
- Breaks complex user queries into focused research topics
- Generates structured outputs for downstream agents using Pydantic schemas

### 3. Research Agent
- Performs real-time web retrieval using Tavily Search API
- Collects relevant articles, URLs, and research snippets
- Builds a **global source index** assigning each source a unique citation number `[1]`, `[2]`, etc.
- Annotates each content chunk with its citation number for downstream traceability
- Organizes retrieved information by topic for downstream synthesis

### 4. Writer Agent
- Synthesizes retrieved information into structured markdown reports
- Embeds **inline citations** (`[1]`, `[2]`, etc.) throughout the report to attribute claims to their sources
- Appends a **Sources section** at the end listing all cited sources with titles and URLs
- Highlights emerging technologies, trends, and key insights
- Produces concise, readable, and professional AI-generated research summaries

### 5. Critic Agent
- Evaluates generated reports for clarity, completeness, technical depth, and **citation quality**
- Assesses whether inline citations are present and whether a Sources section is included
- Returns a numeric score, strengths, weaknesses, missing topics, citation quality, **revision suggestions**, and a final verdict
- A score below 7 triggers automatic revision (up to 2 times)
- Outputs structured JSON using Pydantic schemas

### 6. Revision Agent
- Activated when the Critic scores a report below 7, or when the user requests a revision via HITL
- Takes the original report + critic feedback (or user feedback) + research data
- Produces an improved version while preserving structure and citations
- Sends the revised report back to the Critic for re-evaluation

---

## 🖥️ Streamlit Frontend

The interactive frontend (`frontend/app.py`) connects to the FastAPI backend and provides:

- Research topic input area
- Live report rendering in markdown with clickable citation links
- **PDF export** — downloadable, Unicode-safe report via ReportLab
- Critic score metric display
- Strengths / Weaknesses side-by-side columns
- **Citation Quality** dashboard — inline citations and sources section status
- **Revision Suggestions** from the Critic
- Missing topics and final verdict sections
- **Human-in-the-Loop UI** — Approve / Reject buttons with feedback text input
- Revision counter badge showing how many revisions occurred

---

## 🌐 FastAPI Backend

### Available Endpoints

#### Root
```http
GET /
```

#### Research
```http
POST /research
```

#### Revise (Human-in-the-Loop)
```http
POST /revise
```

#### Memory (History)
```http
GET /memory
```

#### Example Research Request

```json
{
  "query": "Future of AI agents in software engineering"
}
```

#### Example Research Response

```json
{
  "query": "Future of AI agents in software engineering",
  "report": "# AI Enhanced Software Development...\n\n## Sources\n[1] Source Title — https://example.com\n...",
  "critique": {
    "score": 8,
    "strengths": ["Comprehensive coverage", "Well structured"],
    "weaknesses": ["Lacks case studies"],
    "missing_topics": ["Cost analysis", "Vendor lock-in risks"],
    "citation_quality": {
      "has_inline_citations": true,
      "has_sources_section": true,
      "notes": "All major claims are properly cited."
    },
    "revision_suggestions": ["Add real-world case studies", "Include cost analysis section"],
    "final_verdict": "Strong report with minor gaps."
  },
  "source_index": {
    "1": { "title": "AI Agents Overview", "url": "https://example.com/ai-agents" },
    "2": { "title": "Future of Software Engineering", "url": "https://example.com/future-se" }
  },
  "research_data": ["..."],
  "revision_count": 0
}
```

#### Example Revision Request

```json
{
  "query": "Future of AI agents in software engineering",
  "report": "# AI Enhanced Software Development...",
  "user_feedback": "Add more details about security risks",
  "research_data": ["..."],
  "source_index": { "1": { "title": "...", "url": "..." } },
  "revision_count": 0
}
```

#### Example Revision Response

```json
{
  "report": "# AI Enhanced Software Development (Revised)...",
  "critique": {
    "score": 9,
    "strengths": ["Comprehensive coverage", "Security risks addressed"],
    "weaknesses": [],
    "revision_suggestions": [],
    "final_verdict": "Excellent report after revision."
  },
  "revision_count": 1
}
```

Interactive API docs available at:

```
http://localhost:8080/docs
```

---

## 🐳 Docker Setup (Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/ebrahimzaher/deepresearch-ai.git
cd deepresearch-ai
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

*Note: The frontend uses the `BACKEND_URL` environment variable to connect to the backend API. In the Docker setup, this is automatically configured to `http://backend:8000` via `docker-compose.yml`.*

### 3. Build and Run

```bash
docker-compose up --build
```

### 4. Access the App

| Service  | URL                          |
|----------|------------------------------|
| Frontend | http://localhost:8501        |
| Backend  | http://localhost:8080        |
| API Docs | http://localhost:8080/docs   |

Generated reports are saved to the `reports/` folder in the project root.

### `.dockerignore`

```
venv
__pycache__
.env
.git
reports
```

---

## ⚙️ Local Setup (Without Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/ebrahimzaher/deepresearch-ai.git
cd deepresearch-ai
```

### 2. Create a Virtual Environment

**Linux / macOS**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 5. Run the FastAPI Backend

```bash
uvicorn api.main:app --reload
```

### 6. Run the Streamlit Frontend

```bash
streamlit run frontend/app.py
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Agent Orchestration | LangGraph, LangChain |
| LLM Provider | Groq API (`gpt-oss-120b`) |
| Web Retrieval | Tavily Search API |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| PDF Generation | ReportLab |
| Data Validation | Pydantic |
| Containerization | Docker + Docker Compose |

---

## 📌 Example Workflow

**Input query:**
```
Future of AI agents in software engineering
```

**Planner output (subtopics):**
- AI-driven code generation & synthesis
- Automated debugging and testing
- AI-assisted software architecture
- Human-AI collaboration models
- Ethical, security & bias considerations

**Final output:**

A fully structured markdown research report containing an introduction, per-topic research sections with inline citations `[1]`, `[2]`, key technology insights, a conclusion, and a **Sources** section listing all referenced URLs — plus a structured critic evaluation with score, strengths, weaknesses, citation quality assessment, revision suggestions, and verdict. If the critic scores the report below 7, it is automatically revised (up to 2 times). The user can then **approve** or **reject with feedback** for further human-guided revision. Exportable as a PDF.

---

## 🔜 Roadmap

- [ ] Multi-turn conversational research sessions
- [ ] Cloud deployment (Render / Railway)

---

## 👨‍💻 Developed By

[Ebrahim Zaher](https://github.com/ebrahimzaher)
