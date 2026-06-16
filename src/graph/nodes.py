from src.agents import planner_agent, researcher_agent, writer_agent, revision_agent, critic_agent, summarizer_agent
from src.services import load_memory, save_memory
import json

MAX_REVISIONS = 2
SCORE_THRESHOLD = 7

def planner_node(state):
    print("\nRunning Planner Node...")
    
    summary = state.get("context_summary", "No previous context.")
    plan = planner_agent(state["query"], summary)
    
    return {"plan": plan}

def researcher_node(state):
    print("\nRunning Researcher Node...")

    result = researcher_agent(state["plan"])

    return {
        "research": result["topics_data"],
        "source_index": result["source_index"]
    }

def writer_node(state):
    print("\nRunning Writer Node...")
    
    source_index = state.get("source_index", {})
    report = writer_agent(state["query"], state["research"], source_index)

    memory = load_memory()
    memory.append({"query": state["query"], "report": report})
    save_memory(memory)

    return {"report": report, "revision_count": 0}

def critic_node(state):
    print("\nRunning Critic Node...")

    critique = critic_agent(state["report"])

    # Build critique feedback string for potential revision
    feedback_parts = []
    if isinstance(critique, dict) and "error" not in critique:
        if critique.get("weaknesses"):
            feedback_parts.append("Weaknesses: " + "; ".join(critique["weaknesses"]))
        if critique.get("missing_topics"):
            feedback_parts.append("Missing topics: " + "; ".join(critique["missing_topics"]))
        if critique.get("revision_suggestions"):
            feedback_parts.append("Suggestions: " + "; ".join(critique["revision_suggestions"]))
    
    critique_feedback = "\n".join(feedback_parts) if feedback_parts else "No specific feedback."

    return {"critique": critique, "critique_feedback": critique_feedback}

def revision_node(state):
    revision_count = state.get("revision_count", 0) + 1
    print(f"\n Running Revision Node (Revision #{revision_count})...")

    source_index = state.get("source_index", {})
    critique_feedback = state.get("critique_feedback", "")

    revised_report = revision_agent(
        query=state["query"],
        original_report=state["report"],
        critique_feedback=critique_feedback,
        research_data=state["research"],
        source_index=source_index
    )

    return {"report": revised_report, "revision_count": revision_count}

def should_revise(state):
    """Conditional routing: revise if score < 7 and under max revisions."""
    critique = state.get("critique", {})
    revision_count = state.get("revision_count", 0)
    
    score = critique.get("score", 10)
    # Handle score as string
    if isinstance(score, str):
        try:
            score = int(score)
        except ValueError:
            score = 10

    if score < SCORE_THRESHOLD and revision_count < MAX_REVISIONS:
        print(f"\n⚠️ Score {score}/10 < {SCORE_THRESHOLD} — Sending for revision (attempt {revision_count + 1}/{MAX_REVISIONS})")
        return "revision"
    else:
        if score >= SCORE_THRESHOLD:
            print(f"\n✅ Score {score}/10 >= {SCORE_THRESHOLD} — Report accepted!")
        else:
            print(f"\n⚠️ Score {score}/10 — Max revisions ({MAX_REVISIONS}) reached. Accepting report.")
        return "end"

def summarizer_node(state):
    print("\nRunning Summarizer Node...")
    
    history = state.get("chat_history", [])
    
    summary = summarizer_agent(state["query"], history)
    print(f"Context Summary:\n{summary}\n")
    
    return {"context_summary": summary}