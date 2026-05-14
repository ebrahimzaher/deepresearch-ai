# 🧠 Multi-Agent Research System (DeepResearch AI)

A robust, multi-agent AI system designed to automate complex research workflows. Built with Python, this project leverages LangChain, Groq (gpt-oss-120b), and the Tavily Search API to autonomously break down high-level user queries, execute targeted web searches, and compile comprehensive, up-to-date insights.

---

## 🏗️ Project Architecture (Current State - Phase 1)

The system currently operates using a sequential multi-agent pipeline:

1.  **User Input:** The system accepts a broad or complex research query from the user.
2.  **Planner Agent (gpt-oss-120b via Groq):** 
    *   Acts as the strategic brain.
    *   Decomposes the high-level query into 3-4 highly specific, actionable sub-topics.
    *   Outputs a structured JSON format (`pydantic` integratiovn).
3.  **Research Agent (Tavily Search):**
    *   Takes the output from the Planner.
    *   Executes real-time, targeted web searches for each sub-topic.
    *   Retrieves raw, relevant content, URLs, and titles directly from the web.

*Note: The pipeline is currently processing raw search results, laying the groundwork for the upcoming Writer and Critic agents.*

---

## 🛠️ Technology Stack

*   **Core Languages:** Python
*   **LLM Orchestration:** LangChain
*   **Models:** gpt-oss-120b (via Groq API)
*   **Web Retrieval:** Tavily Search API
*   **Data Validation:** Pydantic

---

## 🚀 Current Output Example

**User Query:** `Future of AI agents in software engineering`

**1. Planner Agent Output (Decomposed Topics):**
*   *AI-driven code generation and synthesis*
*   *Automated debugging, testing, and quality assurance*
*   *AI-assisted software architecture and design*
*   *Human-AI collaborative workflows in development teams*

**2. Research Agent Output (Live Retrieval):**
*   *(Fetches relevant live articles, PDFs, and LinkedIn discussions for each topic, returning titles, URLs, and content snippets).*

---

## 🔜 Next Steps (Roadmap)

- [ ] **Writer Agent:** Implement an LLM-driven agent to synthesize raw search results into a clean, structured Markdown report.
- [ ] **LangGraph Orchestration:** Transition from sequential Python functions to a state-based graph structure for dynamic agent routing.
- [ ] **Shared State & Memory:** Integrate FAISS vector store to maintain context across multi-turn research tasks.
- [ ] **Backend Integration:** Wrap the system in a scalable FastAPI RESTful backend.

## 💻 How to Run (Local Development)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ebrahimzaher/deepresearch-ai.git
2. **Set up the environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
3. **Environment Variables:**
    Create a .env file in the root directory and add your API keys:
    ```bash
    GROQ_API_KEY=your_groq_key
    TAVILY_API_KEY=your_tavily_key
4. **Execute the Pipeline:**
    ```bash
    python src/app.py
Developed by [Ebrahim Zaher](https://github.com/ebrahimzaher)