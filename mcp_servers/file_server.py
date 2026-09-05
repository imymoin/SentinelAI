from mcp.server.fastmcp import FastMCP


mcp = FastMCP("SentinelAI File Server")


@mcp.tool()
def file_get_project_info() -> dict:
    """Get general information about the SentinelAI project."""
    return {
        "name": "SentinelAI",
        "description": "Secure AI gateway with LangGraph, LiteLLM, MCP and guardrails.",
        "status": "In development",
        "technology": [
            "Python",
            "FastAPI",
            "LangGraph",
            "LiteLLM",
            "Groq",
            "MCP",
        ],
    }


@mcp.tool()
def file_get_project_status() -> dict:
    """Get the current development status of SentinelAI."""
    return {
        "project": "SentinelAI",
        "status": "In development",
        "completed": [
            "FastAPI backend",
            "API key authentication",
            "Input guardrail",
            "Output guardrail",
            "Tool guardrail",
            "LangGraph agent",
            "LiteLLM gateway",
            "MCP integration",
        ],
        "next_steps": [
            "Testing",
            "Observability",
            "Production hardening",
        ],
    }


if __name__ == "__main__":
    mcp.run()