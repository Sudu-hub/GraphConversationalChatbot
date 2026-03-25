import requests
import os
import json
import re

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


def clean_json(text):
    """Remove markdown wrappers like ```json"""
    text = re.sub(r"```json|```", "", text).strip()
    return text


def parse_query(question):
    prompt = f"""
Convert this query into STRICT JSON only.

Query: "{question}"

Return ONLY JSON (no explanation):

{{
  "intent": "...",
  "entity": "...",
  "id": "..."
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
                "messages": [
                    {"role": "user", "content": prompt}
                ],
            },
            timeout=10
        )

        result = response.json()

        # 🔥 SAFE ACCESS
        if "choices" not in result:
            print("API ERROR:", result)
            return fallback_parser(question)

        content = result["choices"][0]["message"]["content"]

        # 🔥 CLEAN JSON
        content = clean_json(content)

        try:
            return json.loads(content)
        except:
            print("JSON PARSE FAILED:", content)
            return fallback_parser(question)

    except Exception as e:
        print("LLM ERROR:", str(e))
        return fallback_parser(question)


# 🔥 FALLBACK (VERY IMPORTANT)
def fallback_parser(question):
    import re

    ids = re.findall(r"\d+", question)

    return {
        "intent": "fallback",
        "entity": "unknown",
        "id": ids[0] if ids else ""
    }