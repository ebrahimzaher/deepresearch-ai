from src.agents import planner_agent, researcher_agent, writer_agent, critic_agent

def planner_node(state):
    print("\nRunning Planner Node...")

    plan = planner_agent(state["query"])

    return {"plan": plan}

def researcher_node(state):
    print("\nRunning Researcher Node...")

    research = researcher_agent(state["plan"])

    return {"research": research}

def writer_node(state):
    print("\nRunning Writer Node...")
    
    report = writer_agent(state["research"])

    return {"report": report}

def critic_node(state):
    print("\nRunning Critic Node...")

    critique = critic_agent(state["report"])

    return {"critique": critique}