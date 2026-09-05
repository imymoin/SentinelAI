import asyncio

from backend.mcp.client import MCPManager


async def main():

    manager = MCPManager()

    try:
        # Connect to all servers
        await manager.connect()

        print("\n" + "=" * 50)
        print("ALL REGISTERED TOOLS")
        print("=" * 50)

        for tool_name, info in manager.tools.items():

            print(
                f"\nTool: {tool_name}"
                f"\nServer: {info['server']}"
            )

        # Call Database Tool
        print("\n" + "=" * 50)
        print("CALLING DATABASE TOOL")
        print("=" * 50)

        result = await manager.call_tool(
            "db_get_employee",
            {
                "employee_id": "101"
            },
        )

        for content in result.content:
            print(content.text)

        # Call File Tool
        print("\n" + "=" * 50)
        print("CALLING FILE TOOL")
        print("=" * 50)

        result = await manager.call_tool(
            "file_get_project_info",
            {},
        )

        for content in result.content:
            print(content.text)

    finally:

        await manager.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
