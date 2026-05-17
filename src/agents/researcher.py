from src.services import search_web

def researcher_agent(plan: dict):

    topics = plan.get("topics", [])

    research_data = []

    for topic in topics:

        print(f"\nResearching: {topic}")

        response = search_web(topic)

        formatted_results = []

        for item in response["results"]:

            formatted_results.append({
                "title": item["title"],
                "url": item["url"],
                "content": item["content"]
            })

        research_data.append({
            "topic": topic,
            "sources": formatted_results
        })

    return research_data
