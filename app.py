from hybrid_agent import hybrid_agent

while True:
    query = input("\nAsk HR AI: ")
    result = hybrid_agent(query)

    print("\nTYPE:", result["type"])
    print("RESULT:", result)
    print("-" * 50)