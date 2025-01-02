# AWS-Bedrock

## Pre-requisites

- Enabled models inside `AWS Bedrock`. By default, Bedrock disables all models
- Checking for the list of supported on-demand inference models. [List of regional supported models](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
- Using `langchain-aws` libraries will provide type-safe chatting with AWS Bedrock
- Must `aws configure` the environment with IAM-authorized keys

## For Bedrock integration with AWS Cloud KnowledgeBase

- [Read this tutorial from AWS](https://aws.amazon.com/blogs/machine-learning/dive-deep-into-vector-data-stores-using-amazon-bedrock-knowledge-bases/)
- Execute [Bedrock_Knowledgebases_VectorDB](./Bedrock_Knowledgebases_VectorDB.ipynb)
