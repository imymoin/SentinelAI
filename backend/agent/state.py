from typing import Literal, Optional, TypedDict


class AgentState(TypedDict):
    user_query: str

    # Routing
    route: Literal["direct", "rag", "mcp"]
    needs_tool: bool

    # MCP
    selected_tool: Optional[str]
    tool_arguments: dict
    tool_result: Optional[str]

    # RAG
    rag_context: Optional[str]

    # Final answer
    final_response: Optional[str]