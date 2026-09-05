from langgraph.graph import StateGraph, START, END

from backend.agent.state import AgentState
from backend.agent.nodes import (
    decide_route,
    choose_tool,
    execute_tool,
    generate_response,
    generate_direct_response,
    retrieve_rag_context,
    generate_rag_response,
)


def create_graph(manager, rag_pipeline=None):

    workflow = StateGraph(AgentState)

    # ========================================================
    # 1. Decide route
    # ========================================================

    def route_request(state):
        return decide_route(
            state,
            manager.tools,
        )

    # ========================================================
    # 2. MCP tool selection
    # ========================================================

    def select_tool(state):
        return choose_tool(
            state,
            manager.tools,
        )

    # ========================================================
    # 3. MCP tool execution
    # ========================================================

    async def run_tool(state):
        return await execute_tool(
            state,
            manager,
        )

    # ========================================================
    # 4. MCP final response
    # ========================================================

    def create_response(state):
        return generate_response(state)

    # ========================================================
    # 5. Direct LLM response
    # ========================================================

    def direct_response(state):
        return generate_direct_response(state)

    # ========================================================
    # 6. RAG retrieval
    # ========================================================

    def retrieve_context(state):

        if rag_pipeline is None:
            return {
                "rag_context": ""
            }

        return retrieve_rag_context(
            state,
            rag_pipeline,
        )

    # ========================================================
    # 7. RAG final response
    # ========================================================

    def rag_response(state):
        return generate_rag_response(state)

    # ========================================================
    # Nodes
    # ========================================================

    workflow.add_node(
        "route_request",
        route_request,
    )

    workflow.add_node(
        "select_tool",
        select_tool,
    )

    workflow.add_node(
        "execute_tool",
        run_tool,
    )

    workflow.add_node(
        "generate_response",
        create_response,
    )

    workflow.add_node(
        "direct_response",
        direct_response,
    )

    workflow.add_node(
        "retrieve_rag",
        retrieve_context,
    )

    workflow.add_node(
        "rag_response",
        rag_response,
    )

    # ========================================================
    # Start
    # ========================================================

    workflow.add_edge(
        START,
        "route_request",
    )

    # ========================================================
    # Route
    # ========================================================

    workflow.add_conditional_edges(
        "route_request",
        lambda state: state["route"],
        {
            "direct": "direct_response",
            "rag": "retrieve_rag",
            "mcp": "select_tool",
        },
    )

    # ========================================================
    # MCP path
    # ========================================================

    workflow.add_edge(
        "select_tool",
        "execute_tool",
    )

    workflow.add_edge(
        "execute_tool",
        "generate_response",
    )

    workflow.add_edge(
        "generate_response",
        END,
    )

    # ========================================================
    # Direct path
    # ========================================================

    workflow.add_edge(
        "direct_response",
        END,
    )

    # ========================================================
    # RAG path
    # ========================================================

    workflow.add_edge(
        "retrieve_rag",
        "rag_response",
    )

    workflow.add_edge(
        "rag_response",
        END,
    )

    return workflow.compile()