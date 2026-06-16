from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.prompts import WRITER_PROMPT
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
model="openai/gpt-oss-120b",
temperature=0.3
)

prompt = ChatPromptTemplate.from_messages([
    ("system", WRITER_PROMPT),
    ("human",
"""
Research Topic:
{query}

Research Data:
{research_data}
"""
    )
])

writer_chain = prompt | llm

def writer_agent(query, research_data, source_index: dict = None):
    # Format source index for the prompt
    if source_index:
        formatted_index = "\n".join(
            [f"[{num}] {src['title']} — {src['url']}" for num, src in source_index.items()]
        )
    else:
        formatted_index = "No sources available."

    response = writer_chain.invoke({
        "query": query,
        "research_data": str(research_data),
        "source_index": formatted_index
    })
    
    return response.content