import pytest

from backend.agent.graph import create_graph
from backend.agent.state import AgentState


class MockManager:
    def __init__(self):
        self.tools = {
            "file_get_project_info": {
                "server": "file",
                "description": "Get SentinelAI project information",
            },
            "db_get_employee": {
                "server": "database",
                "description": "Get employee information",
            },
        }


@pytest.mark.anyio
async def test_agent_direct_response():
    manager = MockManager()
    graph = create_graph(manager)

    result = await graph.ainvoke({
        "user_query": "Explain Python in simple words.",
        "selected_tool": None,
        "tool_arguments": {},
        "tool_result": None,
        "final_response": None,
        "needs_tool": False,
    })

    assert result["final_response"]
    assert isinstance(result["final_response"], str)


def test_agent_state_structure():
    state: AgentState = {
        "user_query": "test",
        "selected_tool": None,
        "tool_arguments": {},
        "tool_result": None,
        "final_response": None,
        "needs_tool": False,
    }

    assert state["user_query"] == "test"
    assert state["needs_tool"] is False