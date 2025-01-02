import boto3
import json

prompt_data="""
Act as a Shakespeare and write a poem on Genertaive AI
"""

bedrock=boto3.client(service_name="bedrock-runtime")


"""
https://us-west-2.console.aws.amazon.com/bedrock/home?region=us-west-2#/model-catalog/serverless/meta.llama3-3-70b-instruct-v1:0
{
 "modelId": "meta.llama3-3-70b-instruct-v1:0",
 "contentType": "application/json",
 "accept": "application/json",
 "body": "{\"prompt\":\"this is where you place your input text\",\"max_gen_len\":512,\"temperature\":0.5,\"top_p\":0.9}"
}
"""

payload={
    "prompt":prompt_data,
    "max_gen_len":512,
    "temperature":0.5,
    "top_p":0.9
}

body=json.dumps(payload)

# Notes: not all models will support on-demand invocation
# See: https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html

model_id="us.meta.llama3-2-11b-instruct-v1:0"
response=bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json"
)

response_body=json.loads(response.get("body").read())
repsonse_text=response_body['generation']
print(repsonse_text)