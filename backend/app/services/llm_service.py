import requests
import os
import json
import re

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def clean_json(text):
    """Remove markdown wrappers like ```json"""
    text = re.sub(r"```json|```", "", text).strip()
    return text


# 🔥 MAIN FUNCTION
def parse_query(question):
    prompt = f"""
You are an intelligent system that converts business questions into structured graph queries.

Available entities:
- order
- invoice
- delivery
- payment
- customer
- product

Available intents:
- TRACE_FLOW            (trace lifecycle of an entity)
- FIND_TOP_PRODUCTS     (most billed products)
- FIND_BROKEN_FLOW      (missing steps)
- FIND_RELATION         (connections between entities)
- LOOKUP                (basic lookup)

Extract:
- intent
- entity
- id (if present)
- filters (optional)

Query: "{question}"

Return STRICT JSON ONLY:

{{
  "intent": "...",
  "entity": "...",
  "id": "...",
  "filters": {{}}
}}
"""

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct",
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=10
        )

        result = response.json()

        # 🔥 Handle API failure
        if "choices" not in result:
            print("API ERROR:", result)
            return fallback_parser(question)

        content = result["choices"][0]["message"]["content"]
        content = clean_json(content)

        try:
            parsed = json.loads(content)

            # 🔥 safety normalization
            return {
                "intent": parsed.get("intent", "LOOKUP"),
                "entity": parsed.get("entity", "unknown"),
                "id": str(parsed.get("id", "")),
                "filters": parsed.get("filters", {})
            }

        except Exception:
            print("JSON PARSE FAILED:", content)
            return fallback_parser(question)

    except Exception as e:
        print("LLM ERROR:", str(e))
        return fallback_parser(question)


# 🔥 FALLBACK (VERY IMPORTANT)
def fallback_parser(question):
    ids = re.findall(r"\d+", question)

    # simple heuristic intent detection
    q = question.lower()

    if "trace" in q or "flow" in q:
        intent = "TRACE_FLOW"
    elif "top" in q or "highest" in q:
        intent = "FIND_TOP_PRODUCTS"
    elif "broken" in q or "missing" in q:
        intent = "FIND_BROKEN_FLOW"
    else:
        intent = "LOOKUP"

    return {
        "intent": intent,
        "entity": "unknown",
        "id": ids[0] if ids else "",
        "filters": {}
    }