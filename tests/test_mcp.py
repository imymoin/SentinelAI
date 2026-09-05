import pytest

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.anyio
async def test_file_mcp_server():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_servers/file_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.list_tools()

            tool_names = [tool.name for tool in result.tools]

            assert "file_get_project_info" in tool_names
            assert "file_get_project_status" in tool_names


@pytest.mark.anyio
async def test_database_mcp_server():
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_servers/database_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.list_tools()

            tool_names = [tool.name for tool in result.tools]

            assert "db_get_employee" in tool_names
            assert "db_get_project_status" in tool_names
            assert "db_get_team_members" in tool_names