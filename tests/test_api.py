import os

import pytest
from httpx import ASGITransport, AsyncClient
from dotenv import load_dotenv

from backend.main import app

load_dotenv()

API_KEY = os.getenv(
    "SENTINEL_API_KEY",
    "sentinel-dev-key-123"
)


@pytest.mark.anyio
async def test_root():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "SentinelAI API is running"


@pytest.mark.anyio
async def test_health():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.anyio
async def test_chat_requires_authentication():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/chat",
            json={
                "message": "Explain Python"
            },
        )

    assert response.status_code in [401, 403]


@pytest.mark.anyio
async def test_chat_with_invalid_api_key():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/chat",
            json={
                "message": "Explain Python"
            },
            headers={
                "Authorization": "Bearer wrong-key"
            },
        )

    assert response.status_code == 401


@pytest.mark.anyio
async def test_chat_with_valid_api_key():
    # Import using the actual project structure:
    # backend/agents/
    from backend.mcp.client import MCPManager
    from backend.agent.graph import create_graph

    manager = MCPManager()

    try:
        # Connect to MCP servers
        await manager.connect()

        from backend.rag.pipeline import RAGPipeline

        rag_pipeline = RAGPipeline()


        # Create the LangGraph agent
        graph = create_graph(manager, rag_pipeline)

        # Store graph in FastAPI application state
        app.state.graph = graph

        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:

            response = await client.post(
                "/chat",
                json={
                    "query": "Who is employee 101?"
                },
                headers={
                    "Authorization": f"Bearer {API_KEY}"
                },
            )

        # API should return successfully
        assert response.status_code == 200

        # Response should contain "response"
        data = response.json()

        assert "response" in data
        assert data["response"]

        # Normalize Unicode narrow no-break spaces
        normalized_response = data["response"].replace(
            "\u202f",
            " "
        )

        # MCP database should return employee 101
        assert "John Smith" in normalized_response

    finally:
        # Always clean up MCP connections
        await manager.disconnect()

        # Remove graph from application state
        app.state.graph = None