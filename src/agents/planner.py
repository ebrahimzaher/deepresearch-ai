from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompts import PLANNER_PROMPT
import json

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([("system", PLANNER_PROMPT)])

planner_chain = prompt | llm

def planner_agent(query: str, context_summary: str = None):
    if not context_summary:
        context_summary = "No previous context."

    print("\n===== SUMMARY SENT TO PLANNER =====")
    print(context_summary)
    print("===================================\n")

    response = planner_chain.invoke({
        "query": query,
        "context_summary": context_summary
    })

    content = response.content

    try:
        parsed_response = json.loads(content)
        return parsed_response

    except Exception as e:      
        return {
            "error": "Invalid JSON response",
            "raw_output": content
        }