import sys
from pathlib import Path
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPManager:
    def __init__(self):
        self.sessions = {}
        self.tools = {}

        self.project_root = Path(__file__).resolve().parents[2]

        self.servers = {
            "file": self.project_root / "mcp_servers" / "file_server.py",
            "database": self.project_root / "mcp_servers" / "database_server.py",
        }

        # Properly manages all async contexts
        self.exit_stack = AsyncExitStack()

    async def connect(self):
        """Connect to all MCP servers."""

        for server_name, server_path in self.servers.items():

            print(f"\nConnecting to {server_name} server...")

            server_params = StdioServerParameters(
                command=sys.executable,
                args=[str(server_path)],
            )

            # Enter STDIO connection safely
            read, write = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )

            # Enter MCP session safely
            session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )

            await session.initialize()

            self.sessions[server_name] = session

            # Discover tools
            result = await session.list_tools()

            for tool in result.tools:

                self.tools[tool.name] = {
                    "server": server_name,
                    "description": tool.description,
                }

                print(
                    f"  ✓ Registered tool: {tool.name} "
                    f"({server_name})"
                )

    async def call_tool(self, tool_name: str, arguments: dict):
        """Call a tool on the correct MCP server."""

        if tool_name not in self.tools:
            raise ValueError(
                f"Tool '{tool_name}' not found"
            )

        server_name = self.tools[tool_name]["server"]

        session = self.sessions[server_name]

        result = await session.call_tool(
            tool_name,
            arguments,
        )

        return result

    async def disconnect(self):
        """Close all MCP connections safely."""

        print("\nDisconnecting MCP servers...")

        try:
            await self.exit_stack.aclose()

            self.sessions.clear()
            self.tools.clear()

            print("✓ All MCP servers disconnected")

        except Exception as e:
            print(f"⚠ Error while disconnecting MCP servers: {e}")
