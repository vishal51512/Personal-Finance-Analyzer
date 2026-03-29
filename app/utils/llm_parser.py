import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"


def extract_transactions_llm(text):
    prompt = f"""
Extract all transactions from this text.

Return ONLY JSON array:
[
  {{"date": "...", "description": "...", "amount": number}}
]

Text:
{text}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "kimi-k2.5:cloud",
            "prompt": prompt,
            "stream": False
        }
    )

    output = response.json()["response"]

    try:
        return json.loads(output)
    except:
        return []