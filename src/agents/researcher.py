from src.services import search_web

MAX_CONTENT_PER_SOURCE = 300  # chars — keeps total tokens within Groq free tier limits

def researcher_agent(plan: dict):

    topics = plan.get("topics", [])

    research_data = []
    source_index = {}
    source_counter = 1

    for topic in topics:

        print(f"\nResearching: {topic}")

        response = search_web(topic)

        formatted_results = []

        for item in response["results"]:
            # Assign a unique citation number to each source
            cite_num = source_counter
            source_index[str(cite_num)] = {
                "title": item["title"],
                "url": item["url"]
            }

            # Truncate content to stay within model token limits
            content = item["content"]
            if len(content) > MAX_CONTENT_PER_SOURCE:
                content = content[:MAX_CONTENT_PER_SOURCE] + "..."

            formatted_results.append({
                "cite_num": cite_num,
                "title": item["title"],
                "url": item["url"],
                "content": f"[{cite_num}] {content}"
            })

            source_counter += 1

        research_data.append({
            "topic": topic,
            "sources": formatted_results
        })

    return {
        "topics_data": research_data,
        "source_index": source_index
    }
