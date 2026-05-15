from agents import planner_agent, researcher_agent, writer_agent

if __name__ == "__main__":

    query = input("Enter research topic: ")

    print("\nRunning Planner Agent...")
    plan = planner_agent(query)

    print("\nRunning Research Agent...")
    research = researcher_agent(plan)

    print("\nRunning Writer Agent...")
    report = writer_agent(research)

    print("\n========================")
    print(report)