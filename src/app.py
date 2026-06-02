from src.graph import app
from src.services import load_memory

if __name__ == "__main__":
    query = input("Enter your research topic: ")
    memory = load_memory()
    chat_history = []

    for item in memory[-5:]:
        chat_history.append({
            "role": "user",
            "content": item["query"]
        })
        chat_history.append({
            "role": "assistant",
            "content": item["report"][:500]
        })

    result = app.invoke({
        "query": query,
        "chat_history": chat_history
    })

    # --- الجزء الجديد لطباعة الملخص ---
    print("\n--------------------------------------------")
    print("\nContext Summary (Sent to Planner):")
    # استخدمنا .get عشان لو مفيش summary ميرميش Error
    print(result.get("context_summary", "No summary generated.")) 

    print("\n--------------------------------------------")
    print("\nGenerated Report:")
    print(result["report"])

    print("\n--------------------------------------------")
    print("\nCritic Evaluation:")
    print(result["critique"])