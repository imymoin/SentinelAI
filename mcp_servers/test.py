import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    print("1. Starting MCP client...")

    # Get the directory where test.py exists
    current_dir = Path(__file__).parent

    # file_server.py is in the same directory
    server_path = current_dir / "file_server.py"

    print(f"2. Server path: {server_path}")
    print(f"3. Python executable: {sys.executable}")

    # Check whether the server file exists
    if not server_path.exists():
        print("ERROR: file_server.py not found!")
        return

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
    )

    print("4. Starting MCP server...")

    async with stdio_client(server_params) as (read, write):

        print("5. Server connected!")

        async with ClientSession(read, write) as session:

            print("6. Initializing session...")

            await session.initialize()

            print("7. Session initialized!")

            print("\n8. Getting available tools...")

            tools = await session.list_tools()

            print("\nAvailable Tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")

            print("\n9. Calling get_project_info...")

            result = await session.call_tool(
                "get_project_info",
                {}
            )

            print("\nProject Info:")

            for content in result.content:
                print(content.text)


if __name__ == "__main__":
    asyncio.run(main())