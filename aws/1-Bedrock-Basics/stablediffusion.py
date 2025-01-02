import boto3
import json
import base64
import os

prompt_data = """
provide me an 4k hd image of a beach, also use a blue sky rainy season and
cinematic display
"""


"""
request_body = {
    "modelId": "stability.stable-diffusion-xl-v1",
    "contentType": "application/json",
    "accept": "application/json",
    "body": {
        "text_prompts": [
            {
                "text": "this is where you place your input text",
                "weight": 1
            }
        ],
        "cfg_scale": 10,  # Controls how closely the image follows the prompt
        "seed": 0,        # Random seed for reproducibility
        "steps": 50,      # Number of diffusion steps
        "width": 512,     # Output image width
        "height": 512     # Output image height
    }
}
"""

prompt_template=[{"text":prompt_data,"weight":1}]
bedrock = boto3.client(service_name="bedrock-runtime")
payload = {
    "text_prompts": prompt_template,
    "cfg_scale": 10,  # Controls how closely the image follows the prompt
    "seed": 0,        # Random seed for reproducibility
    "steps": 50,      # Number of diffusion steps
    "width": 512,     # Output image width
    "height": 512     # Output image height
}

body = json.dumps(payload)
model_id = "stability.stable-diffusion-xl-v1"
response = bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json",
)

response_body = json.loads(response.get("body").read())
print(response_body)
artifact = response_body.get("artifacts")[0]
image_encoded = artifact.get("base64").encode("utf-8")
image_bytes = base64.b64decode(image_encoded)

# Save image to a file in the output directory.
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
file_name = f"{output_dir}/generated-img.png"
with open(file_name, "wb") as f:
    f.write(image_bytes)
