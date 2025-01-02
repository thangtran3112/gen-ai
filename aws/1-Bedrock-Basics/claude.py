import boto3
import json

prompt_data="""
Act as a Shakespeare and write a poem on Genertaive AI
"""

bedrock=boto3.client(service_name="bedrock-runtime")

"""
{
  "modelId": "anthropic.claude-3-5-sonnet-20241022-v2:0",
  "contentType": "application/json",
  "accept": "application/json",
  "body": {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 200,
    "top_k": 250,
    "stop_sequences": [],
    "temperature": 1,
    "top_p": 0.999,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "hello world"
          }
        ]
      }
    ]
  }
}
"""

def getClaudePayload(data):
  return {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens":512,
    "temperature":0.8,
    "stop_sequences": [],
    "top_k":300, # Only consider 300 most likely tokens for next word prediction
    "top_p":0.8,
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": data
          }
        ]
      }
    ]
}

payload = getClaudePayload(prompt_data)
body = json.dumps(payload)
model_id = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
response = bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json",
)

response_body = json.loads(response.get("body").read())
poem_content = response_body.get("content")[0].get("text")

print(poem_content)