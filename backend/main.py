from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.agent.graph import create_graph
from backend.mcp.client import MCPManager
from backend.api.routes import router
from backend.logging_config import setup_logging
from backend.middleware import request_logging_middleware


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting SentinelAI API...")

    manager = MCPManager()
    await manager.connect()

    app.state.manager = manager

    from backend.rag.pipeline import RAGPipeline

    rag_pipeline = RAGPipeline()

    graph = create_graph(
        manager,
        rag_pipeline,
    )

    app.state.graph = graph

    print("✅ SentinelAI agent ready")

    yield

    await app.state.manager.disconnect()

    print("🛑 SentinelAI API stopped")


app = FastAPI(
    title="SentinelAI",
    description="Secure AI Agent API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def request_logging(request, call_next):
    return await request_logging_middleware(
        request,
        call_next,
    )

@app.get("/")
async def root():
    return{
        "message": "SentinelAI API is running"
    }


app.include_router(router)