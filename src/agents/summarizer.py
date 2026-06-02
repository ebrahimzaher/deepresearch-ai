from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompts.summarizer_prompt import SUMMARIZER_PROMPT

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SUMMARIZER_PROMPT)
])

summarizer_chain = prompt | llm

def summarizer_agent(query: str, history: list):
    if not history:
        return "No previous context."
        
    formatted_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    
    response = summarizer_chain.invoke({
        "query": query,
        "history": formatted_history
    })
    
    return response.content