import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def connect_to_server(server_name: str, server_path: Path):

    print(f"\nConnecting to {server_name}...")
    print(f"Server path: {server_path}")

    # Check if file exists BEFORE starting
    if not server_path.exists():
        print(f"❌ ERROR: Server file not found!")
        return

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
    )

    try:
        async with stdio_client(server_params) as (read, write):

            print("STDIO connection created")

            async with ClientSession(read, write) as session:

                print("Initializing MCP session...")

                await session.initialize()

                print(f"✅ Connected to {server_name}!")

                tools = await session.list_tools()

                print(f"\nTools from {server_name}:")

                for tool in tools.tools:
                    print(f"  - {tool.name}")

    except Exception as e:
        print(f"\n❌ Error connecting to {server_name}")
        print(f"Error: {e}")


async def main():

    # client_manager.py is inside:
    # Sentinal AI/mcp/client_manager.py

    # Go one level up to project root
    project_root = Path(__file__).resolve().parents[2]

    print("🚀 Starting SentinelAI MCP Client Manager")
    print(f"Project root: {project_root}")

    file_server = (
        project_root
        / "mcp_servers"
        / "file_server.py"
    )

    database_server = (
        project_root
        / "mcp_servers"
        / "database_server.py"
    )

    # Connect to File Server
    await connect_to_server(
        "File MCP Server",
        file_server
    )

    # Connect to Database Server
    await connect_to_server(
        "Database MCP Server",
        database_server
    )

    print("\n🎉 MCP Client Manager finished!")


if __name__ == "__main__":
    asyncio.run(main())
