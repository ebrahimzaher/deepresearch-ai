from src.agents import planner_agent, researcher_agent, writer_agent, critic_agent, summarizer_agent
from src.services import load_memory, save_memory

def planner_node(state):
    print("\nRunning Planner Node...")
    
    summary = state.get("context_summary", "No previous context.")
    plan = planner_agent(state["query"], summary)
    
    return {"plan": plan}

def researcher_node(state):
    print("\nRunning Researcher Node...")

    research = researcher_agent(state["plan"])

    return {"research": research}

def writer_node(state):
    print("\nRunning Writer Node...")
    
    report = writer_agent(state["query"], state["research"])

    memory = load_memory()
    memory.append({"query": state["query"], "report": report})
    save_memory(memory)

    return {"report": report}

def critic_node(state):
    print("\nRunning Critic Node...")

    critique = critic_agent(state["report"])

    return {"critique": critique}

def summarizer_node(state):
    print("\nRunning Summarizer Node...")
    history = state.get("chat_history", [])
    
    summary = summarizer_agent(state["query"], history)
    print(f"Context Summary: {summary}")
    
    return {"context_summary": summary}

def summarizer_node(state):
    print("\nRunning Summarizer Node...")
    
    history = state.get("chat_history", [])
    
    summary = summarizer_agent(state["query"], history)
    print(f"Context Summary:\n{summary}\n")
    
    return {"context_summary": summary}