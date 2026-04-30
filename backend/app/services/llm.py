import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def generate_answer(context, query):
    prompt = f"""
    Answer the question based on context.

    Context:
    {context}

    Question:
    {query}
    """

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=json.dumps({
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 300
        }),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())

    return result["content"][0]["text"]
