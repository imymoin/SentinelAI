import pytest

from backend.mcp.client import MCPManager
from backend.agent.graph import create_graph


@pytest.mark.anyio
async def test_employee_query_end_to_end():
    manager = MCPManager()

    try:
        await manager.connect()

        graph = create_graph(manager)

        result = await graph.ainvoke({
            "user_query": "Who is employee 101?",
            "selected_tool": None,
            "tool_arguments": {},
            "tool_result": None,
            "final_response": None,
            "needs_tool": False,
        })

        response = result["final_response"]

        normalized_response = response.replace("\u202f", " ")
        assert "John Smith" in normalized_response

    finally:
        await manager.disconnect()