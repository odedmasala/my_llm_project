# My LLM Project

This project is a FastAPI app using Huggingface Transformers, packaged with Poetry and developed with Tilt + Docker.

## Run locally

```bash
poetry install
poetry run uvicorn app.main:app --reload
```

## Dev via Tilt

```bash
tilt up
```
