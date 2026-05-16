from graph import app

if __name__ == "__main__":
    query = input("Enter your research topic: ")
    result = app.invoke({"query": query})

    print("\n--------------------------------------------")
    print("\nGenerated Report:")
    print(result["report"])