from agents import planner_agent

if __name__ == "__main__":
    query = input("Enter research topic: ")
    result = planner_agent(query)

print("\nResearch Plan:\n")
print(result)