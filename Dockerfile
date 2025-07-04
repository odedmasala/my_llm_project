# File: Dockerfile
FROM python:3.11-slim

# Metadata
LABEL name="IntelliQuery"
LABEL description="AI-Powered Question Answering API with Context Understanding"
LABEL version="0.1.0"
LABEL maintainer="Oded Masala <odedmasala6@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.3

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
