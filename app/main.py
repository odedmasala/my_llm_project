# File: app/main.py
import asyncio
import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from transformers.pipelines import pipeline

from app.db import AsyncSessionLocal, engine
from app.models import Base, QARecord

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="IntelliQuery",
    description="AI-Powered Question Answering API",
    version="0.1.0",
)

# Initialize the QA pipeline
logger.info("Loading AI model...")
qa = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
logger.info("AI model loaded successfully")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


async def init_database():
    """Initialize database with retry logic"""
    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            logger.info(
                f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})"
            )
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database initialized successfully")
            return
        except Exception as e:
            logger.warning(
                f"Database connection failed (attempt {attempt + 1}/{max_retries}): {e}"
            )
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error("Failed to connect to database after all retries")
                # Don't raise the exception - let the app start without database
                # Database operations will fail gracefully later


@app.on_event("startup")
async def startup_event():
    logger.info("Starting IntelliQuery application...")
    await init_database()
    logger.info("Application startup completed")


@app.get("/health")
async def health_check():
    """Health check endpoint for Kubernetes probes"""
    try:
        # Test database connection
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.warning(f"Database health check failed: {e}")
        db_status = "unhealthy"

    return {
        "status": "healthy",
        "service": "IntelliQuery",
        "database": db_status,
        "version": "0.1.0",
    }


@app.get("/")
def serve_home():
    """Serve the main web interface"""
    return FileResponse("app/static/index.html")


@app.get("/ask")
async def ask(question: str, context: str):
    """Ask a question with context and get an AI-powered answer"""
    if not question.strip() or not context.strip():
        raise HTTPException(status_code=400, detail="Question and context are required")

    try:
        logger.info(f"Processing question: {question[:50]}...")
        result = qa(question=question, context=context)  # type: ignore[call-arg]
        answer = result["answer"]

        # Try to save to database, but don't fail if database is unavailable
        try:
            async with AsyncSessionLocal() as session:
                qa_record = QARecord(question=question, context=context, answer=answer)
                session.add(qa_record)
                await session.commit()
            logger.info("Q&A record saved to database")
        except Exception as e:
            logger.warning(f"Failed to save to database: {e}")
            # Continue without failing - the answer is still valid

        return {"answer": answer}

    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail="Failed to process question")
