from RAG import get_policy_answer
from main import apply_leave  # MCP tool

def hybrid_agent(query: str):

    q = query.lower()

    # -------------------------
    # 1. PURE RAG (knowledge)
    # -------------------------
    rag_keywords = ["policy", "leave rules", "holiday", "rules", "how many"]

    # -------------------------
    # 2. MCP ACTION
    # -------------------------
    action_keywords = ["apply leave", "take leave", "book leave"]

    # -------------------------
    # 3. HYBRID CASE
    # -------------------------
    hybrid_keywords = ["can i", "what if", "should i"]

    # ---- HYBRID FIRST (IMPORTANT) ----
    if any(word in q for word in hybrid_keywords):
        rag_response = get_policy_answer(query)
        return {
            "type": "HYBRID",
            "rag": rag_response,
            "action_suggestion": "You can apply leave if eligible using MCP tool"
        }

    # ---- RAG ONLY ----
    if any(word in q for word in rag_keywords):
        return {
            "type": "RAG",
            "response": get_policy_answer(query)
        }

    # ---- MCP ONLY ----
    if any(word in q for word in action_keywords):
        return {
            "type": "MCP",
            "response": apply_leave("Aman", 2, "Auto request from AI")
        }

    # ---- DEFAULT ----
    return {
        "type": "UNKNOWN",
        "response": "I can help with HR policy or leave management."
    }

if __name__ == "__main__":
    print(hybrid_agent("What is leave policy?"))