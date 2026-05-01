import os
import requests

def generate_answer(context, query):
    prompt = f"""
    Answer the question based on context.

    Context:
    {context}

    Question:
    {query}
    """

    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "llama3")

    response = requests.post(
        f"{base_url}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=180
    )

    response.raise_for_status()
    result = response.json()

    return result.get("response", "")
