import os
import google.generativeai as genai
from query_engine import execute_query

# API Configuration
# Note: Ensure GOOGLE_API_KEY is set in your environment
API_KEY = os.environ.get("GOOGLE_API_KEY", "")
if not API_KEY:
    print("Warning: GOOGLE_API_KEY not found in environment.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')

def route_query(user_query: str):
    """
    Routes user query using LLM → maps to supported intent → executes query
    """
    user_query_lower = user_query.lower().strip()
    
    # STEP 0: DETERMINISTIC SEMANTIC MAPPING (OVERRIDES)
    # This ensures extremely common terms map instantly without LLM
    if any(word in user_query_lower for word in ["unpaid", "not paid", "pending payments"]):
        return {
            "input_query": user_query,
            "mapped_query": "invoices without payment",
            "status": "success",
            "data": execute_query("invoices without payment")
        }
    if any(word in user_query_lower for word in ["undelivered", "not delivered", "pending deliveries"]):
        return {
            "input_query": user_query,
            "mapped_query": "orders without delivery",
            "status": "success",
            "data": execute_query("orders without delivery")
        }

    # STEP 1: HARD GUARDRAIL
    keywords = ["order", "invoice", "customer", "product", "delivery", "payment", "item", "what", "show"]
    if not any(kw in user_query_lower for kw in keywords):
        return {
            "status": "rejected",
            "reason": "Query outside supported dataset domain"
        }

    # STEP 2: LLM CLASSIFICATION (NORMALIZATION)
    prompt = f"""You are a strict query classifier for an SAP O2C Graph.
Normalize flexible natural language into EXACTLY one of these formats:
1. orders by customer <ID>
2. products in order <ID>
3. orders without delivery
4. invoices without payment

Mapping Examples:
- "what did customer X order" -> orders by customer X
- "items in order Y" -> products in order Y
- "undelivered orders" -> orders without delivery
- "pending payments" -> invoices without payment

Rules:
- Return ONLY the normalized string.
- No explanation. No extra text.
- If the query is unrelated or you are UNCERTAIN -> return: REJECT

User Query: {user_query}"""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.0,
            )
        )
        mapped_query = response.text.strip()
    except Exception as e:
        return {
            "status": "error",
            "reason": f"LLM mapping failed: {str(e)}"
        }

    # STEP 3: VALIDATION (STRICT PATTERN MATCH)
    valid_patterns = [
        r"orders by customer \w+",
        r"products in order \w+",
        r"orders without delivery",
        r"invoices without payment"
    ]
    
    import re
    is_valid = any(re.match(p, mapped_query) for p in valid_patterns)
    
    if mapped_query == "REJECT" or not is_valid:
        return {
            "input_query": user_query,
            "mapped_query": mapped_query,
            "status": "rejected",
            "reason": "LLM mapping returned an invalid or rejected intent. Try phrasing differently."
        }

    # STEP 4: EXECUTION
    result = execute_query(mapped_query)


    # STEP 5: FINAL RESPONSE
    return {
        "input_query": user_query,
        "mapped_query": mapped_query,
        "status": "success",
        "data": result
    }

if __name__ == "__main__":
    # Test queries
    test_queries = [
        "give me orders for customer 310000108",
        "what are the products in order 740506",
        "show me orders that haven't been delivered yet",
        "find all unpaid invoices",
        "what is the weather in Mumbai?" # Should be rejected by guardrail
    ]
    
    for q in test_queries:
        print(f"\nUser Query: {q}")
        print(route_query(q))
