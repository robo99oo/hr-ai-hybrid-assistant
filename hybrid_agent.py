from RAG import get_policy_answer
from main import apply_leave


def hybrid_agent(query: str):

    q = query.lower()

    rag_keywords = ["policy", "leave rules", "holiday", "rules", "how many"]
    action_keywords = ["apply leave", "take leave", "book leave"]
    hybrid_keywords = ["can i", "what if", "should i"]

    onboarding_keywords = [
        "joining",
        "onboarding",
        "new joiner",
        "documents required",
        "document",
        "first week",
        "orientation",
        "checklist"
    ]

    # ONBOARDING AGENT
    if any(word in q for word in onboarding_keywords):
        rag_response = get_policy_answer(query)
        return {
            "type": "ONBOARDING",
            "response": f"{rag_response}\n\n✅ Recommended Next Step: Complete HR documentation, laptop request, system access setup, email activation, and orientation training."        }

    # HYBRID AGENT
    if any(word in q for word in hybrid_keywords):
        rag_response = get_policy_answer(query)
        return {
            "type": "HYBRID",
            "rag": rag_response,
            "action_suggestion": "Based on policy eligibility, the Compliance Decision Agent recommends the next HR action."
        }

    # POLICY RETRIEVAL AGENT
    if any(word in q for word in rag_keywords):
        return {
            "type": "RAG",
            "response": get_policy_answer(query)        }

    # LEAVE ACTION AGENT
    if any(word in q for word in action_keywords):
        return {
            "type": "MCP",
            "response": apply_leave("Employee", 2, "Auto request from Agentic HR OS")        }

    # DEFAULT
    return {
        "type": "UNKNOWN",
        "response": "I can help with HR policy, onboarding, compliance decisions, and leave management."
    }


if __name__ == "__main__":
    print(hybrid_agent("What is leave policy?"))