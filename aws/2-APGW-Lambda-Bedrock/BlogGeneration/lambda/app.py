import os
import boto3
import botocore.config
import json

from datetime import datetime

def blog_generate_using_bedrock(blogtopic:str)-> str:
    # Special tokens for Lllama model
    # <s>: Marks the start of the sequence
    # [INST]: Indicates the start of instruction/human input
    # [/INST]: Marks the end of instruction

    prompt=f"""<s>[INST]Human: Write a 200 words blog on the topic {blogtopic}
    Assistant:[/INST]
    """

    body={
        "prompt":prompt,
        "max_gen_len":512,
        "temperature":0.5,
        "top_p":0.9
    }


    # one of the on-demand models
    model_id="us.meta.llama3-2-11b-instruct-v1:0"

    try:
        boto_config=botocore.config.Config(read_timeout=300,retries={'max_attempts':3})
        bedrock_client=boto3.client(
            "bedrock-runtime",
            region_name="us-east-1",
            config=boto_config)
        
        response=bedrock_client.invoke_model(body=json.dumps(body),modelId=model_id)

        response_content=response.get('body').read()
        response_data=json.loads(response_content)
        print(response_data)
        blog_details=response_data['generation']
        return blog_details
    except Exception as e:
        print(f"Error generating the blog:{e}")
        return ""

def save_blog_details_s3(s3_key,s3_bucket,generate_blog):
    s3=boto3.client('s3')

    try:
        s3.put_object(Bucket = s3_bucket, Key = s3_key, Body =generate_blog )
        print("Code saved to s3")

    except Exception as e:
        print(f"Error when saving the code to s3. Exception:{e}")



def lambda_handler(event, context):
    # Get S3 bucket from environment variable
    s3_bucket = os.environ.get('S3_BUCKET')
    if not s3_bucket:
        return {
            'statusCode': 500,
            'body': json.dumps('S3_BUCKET environment variable not set')
        }
    
    try:
        event=json.loads(event['body'])
        blog_topic=event['blog_topic']

        generate_blog=blog_generate_using_bedrock(blogtopic=blog_topic)

        if generate_blog:
            current_time=datetime.now().strftime('%H%M%S')
            s3_key=f"blog-output/{current_time}.txt"
            s3_bucket=s3_bucket
            save_blog_details_s3(s3_key,s3_bucket,generate_blog)
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Blog Generation completed',
                    's3': f"{s3_bucket}/{s3_key}",       
                    'blog_content': generate_blog,
                    'topic': blog_topic
                })
            }
        else:
            print("No blog was generated")
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

    




