# File: app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from transformers import pipeline

from app.models import Base, QARecord
from app.db import engine, AsyncSessionLocal

app = FastAPI()
qa = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def serve_home():
    return FileResponse("app/static/index.html")

@app.get("/ask")
async def ask(question: str, context: str):
    result = qa(question=question, context=context)

    async with AsyncSessionLocal() as session:
        qa_record = QARecord(
            question=question,
            context=context,
            answer=result["answer"]
        )
        session.add(qa_record)
        await session.commit()

    return {"answer": result["answer"]}