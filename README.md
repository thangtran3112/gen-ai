# Langchain Basis

## Installation

```bash
  conda create -p venv python==3.12
  conda activate venv/
  pip install -r requirements.txt
```

- Lock in dependencies in `requirements-lock.txt`:

```bash
  conda list --export > requirements-lock.txt
```

## Ollama open source models

- [Github Ollama models list](https://github.com/ollama/ollama?tab=readme-ov-file#model-library)
- [Download Ollama](https://ollama.com/download/linux)
- For example: Download `gemma2` 2 Billion parameters:

```bash
  ollama pull gemma2:2b
```

or running directly from remote source:

```bash
  ollama run gemma2:2b
```

- `ollama pull”` fetches a model or image from a remote source. “ollama run” executes that model locally once it has already been pulled.

## [Faiss installation](https://github.com/facebookresearch/faiss/blob/main/INSTALL.md)

```bash
# GPU(+CPU) version
$ conda install -c pytorch -c nvidia faiss-gpu=1.9.0
```

or

```bash
pip install faiss-gpu-cu12
```

## Setup Environment for LangChain

- [LangSmith Environment Setup](https://docs.smith.langchain.com/#3-set-up-your-environment)

```.env
  export LANGCHAIN_TRACING_V2=true
  export LANGCHAIN_API_KEY=<your-api-key>
```
