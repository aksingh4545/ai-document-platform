import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_answer(context, question):
    prompt = f"""
You are an intelligent assistant.

Use ONLY the context below to answer the question.
If the answer is not in the context, say "Not found in document".

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(OLLAMA_URL, json={
        "model": "phi3",
        "prompt": prompt,
        "stream": False
    })

    return response.json()["response"]
