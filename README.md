# 🧠 DeepResearch AI

A multi-agent AI research system designed to automate complex research workflows using LLM-powered planning, real-time web retrieval, and AI-driven report generation.

Built with Python, LangChain, LangGraph (upcoming), Groq LLMs, and Tavily Search API.

---

# 🚀 Features

- Autonomous query decomposition using LLM agents
- Real-time web research with Tavily Search
- AI-generated structured research reports
- Modular multi-agent architecture
- Structured outputs with Pydantic
- Scalable orchestration-ready pipeline

---

# 🏗️ Current Architecture

The system currently operates as a sequential multi-agent workflow:

```text
User Query
    ↓
Planner Agent
    ↓
Research Agent
    ↓
Writer Agent
    ↓
Structured Markdown Report
```

# 🤖 Agents

## 1. Planner Agent
- Uses `gpt-oss-120b` via Groq
- Breaks complex user queries into focused research topics
- Generates structured outputs for downstream agents

## 2. Research Agent
- Performs real-time web retrieval using Tavily Search API
- Collects relevant articles, URLs, and research snippets
- Organizes retrieved information by topic

## 3. Writer Agent
- Synthesizes retrieved information into structured markdown reports
- Highlights trends, technologies, and key insights
- Produces concise, readable research summaries

# 🛠️ Tech Stack

## Core
- Python
- LangChain
- LangGraph (In Progress)

## LLMs & AI
- Groq API
- gpt-oss-120b
- Pydantic

## Retrieval
- Tavily Search API

## Deployment (Planned)
- FastAPI
- Streamlit

# 📌 Example Workflow

## User Query
```bash
Future of AI agents in software engineering
```

## Planner Output
- AI-driven code generation
- Automated debugging and testing
- AI-assisted software architecture
- Human-AI collaboration models

## Final Output
### A fully structured AI-generated research report containing:

- Introduction
- Research sections
- Technology insights
- Key trends
- Conclusion

# 🔜 Roadmap
- LangGraph state-based orchestration
- Shared memory and reflection agents
- Citation-aware report generation
- FastAPI backend deployment
- Streamlit interactive UI
- Multi-turn conversational research

# ⚙️ Local Setup

## Clone Repository
```bash
git clone https://github.com/ebrahimzaher/deepresearch-ai.git
```
## Create Virtual Environment

### Linux / macOS
```bash
python -m venv venv
source venv/bin/activate
```
### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Variables

Create a .env file:

``` bash
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Run the Application
```bash
python src/app.py
```
# 👨‍💻 Developed By [Ebrahim Zaher](https://github.com/ebrahimzaher)