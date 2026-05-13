from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from prompts.planner_prompt import PLANNER_PROMPT
import json

load_dotenv()

llm = ChatGroq(
model="openai/gpt-oss-120b",
temperature=0
)

prompt = ChatPromptTemplate.from_messages([
("system", PLANNER_PROMPT),
("human", "{query}")
])

planner_chain = prompt | llm

def planner_agent(query: str):

    response = planner_chain.invoke({
        "query": query
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