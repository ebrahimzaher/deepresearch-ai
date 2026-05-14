from agents import planner_agent, researcher_agent

if __name__ == "__main__":

    query = input("Enter research topic: ")

    plan = planner_agent(query)

    print("\nResearch Plan:") 
    print(plan)

    research_results = researcher_agent(plan)

    print("\nResearch Results:")
    
    for topic_data in research_results:
        print(f"\nTopic: {topic_data['topic']}")

        for source in topic_data["sources"]:
            print(f"Title: {source['title']}")
            print(f"URL: {source['url']}")
            print(f"Content: {source['content'][:200]}...")
