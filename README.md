# 🧠 DeepResearch AI

A stateful multi-agent AI research system that automates complex research workflows using LLM-powered planning, real-time web retrieval, AI-generated report synthesis, reflection-based evaluation, and API-based orchestration.

Built with Python, LangChain, LangGraph, Groq LLMs, FastAPI, Streamlit, and Tavily Search API.

---

## 🚀 Features

- Autonomous query decomposition using AI planning agents
- Real-time web retrieval with Tavily Search API
- AI-generated structured markdown research reports
- PDF export with Unicode-safe rendering
- Reflection / Critic agent for structured report evaluation
- Stateful multi-agent orchestration with LangGraph
- Shared workflow state across all agents
- Structured outputs using Pydantic
- FastAPI backend with production-style REST API
- Interactive API documentation via Swagger UI
- Streamlit frontend with critic score dashboard
- Modular and scalable agent architecture

---

## 🏗️ Architecture

The system operates as a LangGraph-powered state-based multi-agent workflow exposed through a FastAPI backend and a Streamlit frontend.

```text
                ┌─────────────────┐
                │   User Query    │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Streamlit Front │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │  FastAPI Layer  │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Planner Agent   │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Research Agent  │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │  Writer Agent   │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │  Critic Agent   │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Final AI Report │
                └─────────────────┘
```

---

## ⚡ LangGraph Workflow

The system uses LangGraph to orchestrate agent execution through a shared state-based workflow.

Each agent operates as an independent node:

- **Planner Node** — decomposes the query into focused research subtopics
- **Research Node** — retrieves real-time web content per subtopic
- **Writer Node** — synthesizes findings into a structured markdown report
- **Critic Node** — evaluates the report and returns structured JSON feedback

The workflow maintains shared state across all agents, enabling scalable orchestration and future support for reflection loops, agent memory, conditional routing, and human-in-the-loop workflows.

---

## 🤖 Agents

### 1. Planner Agent
- Uses `gpt-oss-120b` via Groq for intelligent task planning
- Breaks complex user queries into focused research topics
- Generates structured outputs for downstream agents using Pydantic schemas

### 2. Research Agent
- Performs real-time web retrieval using Tavily Search API
- Collects relevant articles, URLs, and research snippets
- Organizes retrieved information by topic for downstream synthesis

### 3. Writer Agent
- Synthesizes retrieved information into structured markdown reports
- Highlights emerging technologies, trends, and key insights
- Produces concise, readable, and professional AI-generated research summaries

### 4. Critic Agent
- Evaluates generated reports for clarity, completeness, and technical depth
- Returns a numeric score, strengths, weaknesses, missing topics, and a final verdict
- Outputs structured JSON using Pydantic schemas

---

## 🖥️ Streamlit Frontend

The interactive frontend (`frontend/app.py`) connects to the FastAPI backend and provides:

- Research topic input area
- Live report rendering in markdown
- **PDF export** — downloadable, Unicode-safe report via ReportLab
- Critic score metric display
- Strengths / Weaknesses side-by-side columns
- Missing topics and final verdict sections

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

#### Example Request

```json
{
  "query": "Future of AI agents in software engineering"
}
```

#### Example Response

```json
{
  "query": "Future of AI agents in software engineering",
  "report": "# AI Enhanced Software Development...",
  "critique": {
    "score": 8,
    "strengths": ["Comprehensive coverage", "Well structured"],
    "weaknesses": ["Lacks case studies"],
    "missing_topics": ["Cost analysis", "Vendor lock-in risks"],
    "final_verdict": "Strong report with minor gaps."
  }
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

A fully structured markdown research report containing an introduction, per-topic research sections, key technology insights, a conclusion — plus a structured critic evaluation with score, strengths, weaknesses, and verdict. Exportable as a PDF.

---

## 🔜 Roadmap

- [ ] Citation-aware report generation
- [ ] Shared agent memory integration
- [ ] Conditional agent routing & reflection loops
- [ ] Multi-turn conversational research sessions
- [ ] Persistent research session storage
- [ ] Cloud deployment (Render / Railway)

---

## 👨‍💻 Developed By

[Ebrahim Zaher](https://github.com/ebrahimzaher)