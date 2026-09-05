import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    current_dir = Path(__file__).parent
    server_path = current_dir / "database_server.py"

    print("Starting Database MCP Server...")

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize MCP connection
            await session.initialize()

            print("\nConnected successfully!")

            # Get available tools
            tools = await session.list_tools()

            print("\nAvailable Tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")

            # Get project status
            result = await session.call_tool(
                "get_project_status",
                {
                    "project_name": "sentinel"
                }
            )

            print("\nProject Status:")

            for content in result.content:
                print(content.text)


if __name__ == "__main__":
    asyncio.run(main())