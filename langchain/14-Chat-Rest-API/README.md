# LangChain OpenAPI toolkit to chat with Swagger Rest API

## Create openapi agent

- [OpenAPI Toolkit Instructions](https://python.langchain.com/docs/integrations/tools/openapi/)
- [LangGraph Open API](https://python.langchain.com/api_reference/langchain/chains/langchain.chains.api.base.APIChain.html)

## Environments

```.env
OPENAI_API_KEY
SPOTIPY_CLIENT_ID="9f3849d85ade4561946275ca87e194a9"
SPOTIPY_CLIENT_SECRET="42fb5a45f54f4b88ba3dbdd6bb2c3231"
SPOTIPY_REDIRECT_URI="https://thangtrandev.net"
```

## Chat with Spotify API, through Bearer token

- Must register ClientId, Secret and a redirectURI with [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- See [Notebook](./openapi.ipynb)

## LangGraph chat with [Jsonplaceholder](https://jsonplaceholder.typicode.com/)

```bash
  python main.py
```
