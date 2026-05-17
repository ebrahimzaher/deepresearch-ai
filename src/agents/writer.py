from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.prompts.writer_prompt import WRITER_PROMPT
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
model="openai/gpt-oss-120b",
temperature=0.3
)

prompt = ChatPromptTemplate.from_messages([
("system", WRITER_PROMPT),
("human", "{research_data}")
])

writer_chain = prompt | llm

def writer_agent(research_data):

    response = writer_chain.invoke({
        "research_data": str(research_data)
    })

    return response.content