from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.db import engine
from app.main import app
from app.models import Base


@pytest.mark.asyncio
@patch("app.main.qa")  # Mock the HuggingFace pipeline
async def test_ask_endpoint(mock_qa):
    # Arrange: ensure tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Mock the model response
    mock_qa.return_value = {"answer": "Paris"}

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get(
            "/ask",
            params={
                "question": "What is the capital of France?",
                "context": "Paris is the capital of France.",
            },
        )

    assert response.status_code == 200
    assert response.json() == {"answer": "Paris"}
