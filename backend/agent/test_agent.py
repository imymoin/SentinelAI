import asyncio
from backend.agent.graph import create_graph
from backend.guardrails.input_guard import validate_input
from backend.mcp.client import MCPManager


async def main():

    print("🚀 Starting SentinelAI Agent")

    manager = MCPManager()

    try:
        # Connect to MCP servers
        await manager.connect()

        # Create LangGraph workflow
        graph = create_graph(manager)

        print("\n🤖 Ask SentinelAI a question!")
        print("Type 'exit' or 'quit' to stop.\n")

        while True:

            question = input("You: ").strip()

            # Exit condition
            if question.lower() in ["exit", "quit"]:
                break

            # Ignore empty input
            if not question:
                continue

            # =========================
            # INPUT GUARDRAIL
            # =========================

            approved, message = validate_input(question)

            if not approved:
                print(f"\n🛡️ {message}")
                continue

            # =========================
            # RUN AGENT
            # =========================

            try:

                result = await graph.ainvoke(
                    {
                        "user_query": question,
                        "selected_tool": None,
                        "tool_arguments": {},
                        "tool_result": None,
                        "final_response": None,
                        "need_tool": None
                    }
                )

                print("\n🤖 SentinelAI:")
                print(result.get("final_response"))

                # =========================
                # DEBUG INFORMATION
                # =========================

                print("\n========== DEBUG ==========")

                print("\nSelected Tool:")
                print(result.get("selected_tool"))

                print("\nTool Arguments:")
                print(result.get("tool_arguments"))

                print("\nTool Result:")
                print(result.get("tool_result"))

                print("===========================\n")

            except PermissionError as e:
                print(f"\n🛡️ Request blocked: {e}")


            except Exception as e:

                print("\n❌ AGENT ERROR:")
                print(f"{type(e).__name__}: {e}")
                
                import traceback
                traceback.print_exc()

    finally:
        # Disconnect ONLY when loop exits
        await manager.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
