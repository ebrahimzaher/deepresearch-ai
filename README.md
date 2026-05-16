# 🧠 DeepResearch AI

A stateful multi-agent AI research system designed to automate complex research workflows using LLM-powered planning, real-time web retrieval, and AI-generated report synthesis.

Built with Python, LangChain, LangGraph, Groq LLMs, and Tavily Search API.

---

# 🚀 Features

- Autonomous query decomposition using AI planning agents
- Real-time web retrieval with Tavily Search API
- AI-generated structured markdown research reports
- Stateful multi-agent orchestration with LangGraph
- Shared workflow state across agents
- Structured outputs using Pydantic
- Modular and scalable agent architecture
- Orchestration-ready pipeline for advanced agent workflows

---

# 🏗️ Current Architecture

The system operates using a LangGraph-powered state-based multi-agent workflow.

```text
                ┌─────────────────┐
                │   User Query    │
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
                │ Final AI Report │
                └─────────────────┘
```

---

# ⚡ LangGraph Workflow

The system uses LangGraph to orchestrate agent execution through a shared state-based workflow.

Each agent operates as an independent node:
- Planner Node
- Research Node
- Writer Node

The workflow maintains shared state across all agents, enabling scalable orchestration and future support for:
- Reflection loops
- Critic agents
- Agent memory
- Conditional routing
- Multi-turn research sessions

# 🤖 Agents

## 1. Planner Agent
- Uses `gpt-oss-120b` via Groq for intelligent task planning
- Breaks complex user queries into focused research topics
- Generates structured outputs for downstream agents using Pydantic schemas

## 2. Research Agent
- Performs real-time web retrieval using Tavily Search API
- Collects relevant articles, URLs, and research snippets
- Organizes retrieved information by topic for downstream synthesis

## 3. Writer Agent
- Synthesizes retrieved information into structured markdown reports
- Highlights emerging technologies, trends, and key insights
- Produces concise, readable, and professional AI-generated research summaries

---

# 🛠️ Tech Stack

## Core Frameworks
- Python
- LangChain
- LangGraph

## LLMs & AI
- Groq API
- `gpt-oss-120b`
- Pydantic

## Retrieval & Search
- Tavily Search API

## Planned Deployment
- FastAPI
- Streamlit

---

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

A fully structured AI-generated research report containing:
- Introduction
- Research sections
- Technology insights
- Key trends
- Conclusion

---

# 🔜 Roadmap

- Reflection / Critic Agent
- Citation-aware report generation
- Shared memory integration
- Conditional agent routing
- FastAPI backend deployment
- Streamlit interactive UI
- Multi-turn conversational research
- Persistent research sessions

---

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

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```bash
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Run the Application
```bash
python src/app.py
```

---

# 👨‍💻 Developed By

[Ebrahim Zaher](https://github.com/ebrahimzaher)