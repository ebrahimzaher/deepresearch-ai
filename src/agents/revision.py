from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.prompts import REVISION_PROMPT
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3
)

revision_prompt = ChatPromptTemplate.from_messages([
    ("system", REVISION_PROMPT),
    ("human",
"""
Research Topic:
{query}

Original Report:
{original_report}

Research Data:
{research_data}
"""
    )
])

revision_chain = revision_prompt | llm


def _format_source_index(source_index: dict) -> str:
    if source_index:
        return "\n".join(
            [f"[{num}] {src['title']} — {src['url']}" for num, src in source_index.items()]
        )
    return "No sources available."


def revision_agent(query: str, original_report: str, critique_feedback: str, research_data, source_index: dict = None):
    response = revision_chain.invoke({
        "query": query,
        "original_report": original_report,
        "research_data": str(research_data),
        "source_index": _format_source_index(source_index),
        "critique_feedback": critique_feedback
    })
    
    return response.content
