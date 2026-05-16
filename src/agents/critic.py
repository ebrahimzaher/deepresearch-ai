from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from prompts.critic_prompt import CRITIC_PROMPT
from dotenv import load_dotenv
import json

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", CRITIC_PROMPT),
    ("human", "{report}")
])

critic_chain = prompt | llm


def critic_agent(report: str):

    response = critic_chain.invoke({
        "report": report
    })

    content = response.content

    try:
        return json.loads(content)

    except Exception:

        return {
            "error": "Invalid JSON",
            "raw_output": content
        }