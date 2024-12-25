# Chatbot answering based on customed pdf dataset

- The Chat bot will only based on custom dataset to answer questions

## Dataset

- Dataset includes 3 PDF papers about Dog breeds, Cat breeds and Cat behaviors

## Streamlit UI Execution

```zsh
  streamlit run app_llama3.py
```

or

```zsh
  streamlit run app_openai.py
```

## Exposing RestAPI with FastAPI

- Note: The rest api exposing requires a server, it may incur a lot of cold-start if running in serverless mode
- Example of calling API:

```zsh
  curl -X 'POST' \
    'http://127.0.0.1:8000/chat' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "question": "When were dogs domesticated?"
  }'
```
