import logging

from fastapi import APIRouter, Depends, HTTPException, Request

from backend.auth import verify_api_key
from backend.agent.graph import create_graph
from backend.agent.state import AgentState
from backend.guardrails.input_guard import validate_input
from backend.rag.pipeline import RAGPipeline
from backend.observability import metrics


logger = logging.getLogger(__name__)

router = APIRouter()


# ---------------------------------------------------------
# Shared application components
# ---------------------------------------------------------

rag_pipeline = RAGPipeline()

mcp_manager = None
agent_graph = None


def set_dependencies(manager):
    """
    Initialize shared MCP manager and LangGraph agent.
    """

    global mcp_manager
    global agent_graph

    mcp_manager = manager

    agent_graph = create_graph(
        manager=mcp_manager,
        rag_pipeline=rag_pipeline,
    )


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@router.get("/health")
async def health_check(
    request: Request,
):
    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    logger.info(
        "Health check | request_id=%s",
        request_id,
    )

    return {
        "status": "healthy",
        "service": "SentinelAI",
        "request_id": request_id,
    }


# ---------------------------------------------------------
# Main AI endpoint
# ---------------------------------------------------------

@router.post("/chat")
async def chat(
    request: Request,
    payload: dict,
    _: bool = Depends(verify_api_key),
):
    request_id = getattr(
        request.state,
        "request_id",
        "unknown",
    )

    logger.info(
        "Chat request received | request_id=%s",
        request_id,
    )

    # -----------------------------------------------------
    # Validate request body
    # -----------------------------------------------------

    if "query" not in payload:
        logger.warning(
            "Missing query | request_id=%s",
            request_id,
        )

        raise HTTPException(
            status_code=400,
            detail="Query is required.",
        )

    query = payload["query"]

    if not isinstance(query, str):
        logger.warning(
            "Invalid query type | request_id=%s",
            request_id,
        )

        raise HTTPException(
            status_code=400,
            detail="Query must be a string.",
        )

    # -----------------------------------------------------
    # Input guardrail
    # -----------------------------------------------------

    approved, message = validate_input(query)

    if not approved:
        logger.warning(
            "Input blocked | request_id=%s | reason=%s",
            request_id,
            message,
        )

        raise HTTPException(
            status_code=400,
            detail=message,
        )

    # -----------------------------------------------------
    # Check agent
    # -----------------------------------------------------

    agent_graph = getattr(request.app.state, "graph", None)
    if agent_graph is None:
        logger.error(
            "Agent not initialized | request_id=%s",
            request_id,
        )

        raise HTTPException(
            status_code=503,
            detail="AI agent is not initialized.",
        )

    # -----------------------------------------------------
    # Create initial agent state
    # -----------------------------------------------------

    initial_state: AgentState = {
        "user_query": query,
        "route": "direct",
        "needs_tool": False,
        "selected_tool": None,
        "tool_arguments": {},
        "tool_result": None,
        "rag_context": None,
        "final_response": None,
    }

    logger.info(
        "Agent execution started | request_id=%s",
        request_id,
    )

    # -----------------------------------------------------
    # Execute LangGraph
    # -----------------------------------------------------

    try:
        result = await agent_graph.ainvoke(
            initial_state
        )

    except Exception:
        logger.exception(
            "Agent execution failed | request_id=%s",
            request_id,
        )

        raise HTTPException(
            status_code=500,
            detail="AI agent execution failed.",
        )

    # -----------------------------------------------------
    # Get final response
    # -----------------------------------------------------

    response_text = result.get(
        "final_response"
    )

    if not response_text:
        logger.error(
            "Empty agent response | request_id=%s",
            request_id,
        )

        raise HTTPException(
            status_code=500,
            detail="Agent returned an empty response.",
        )

    logger.info(
        "Chat request completed | "
        "request_id=%s | "
        "response_length=%d",
        request_id,
        len(response_text),
    )

    return {
        "request_id": request_id,
        "response": response_text,
    }

@router.get("/metrics")
async def get_metrics():
    return metrics.snapshot()