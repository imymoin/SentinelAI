from ast import arguments
import json
import os

from dotenv import load_dotenv
from openai import OpenAI


from backend.guardrails.tool_guard import (
    validate_tool,
    validate_tool_arguments,
)

from backend.guardrails.output_guard import (
    validate_output,
)
from backend.observability import metrics
from backend.logging_config import get_logger

logger = get_logger(__name__)

load_dotenv()


# ============================================================
# LiteLLM Gateway Client
# ============================================================

client = OpenAI(
    api_key=os.getenv("LITELLM_MASTER_KEY"),
    base_url=os.getenv(
        "LITELLM_API_BASE",
        "http://localhost:4000/v1",
    ),
)


MODEL = "sentinel-primary"


# ============================================================
# 1. Decide route
# ============================================================

def decide_route(state, tools):

    user_query = state["user_query"]

    tool_descriptions = []
    

    for tool_name, info in tools.items():

        tool_descriptions.append(
            {
                "name": tool_name,
                "description": info["description"],
            }
        )

    prompt = f"""
You are the routing system for SentinelAI.

Your job is to decide how the user's request should be answered.

There are three possible routes:

1. "mcp"
Use MCP when the user needs information from an available
external tool such as an employee database or project information.

2. "rag"
Use RAG when the user is asking about information that may
exist inside uploaded or indexed documents.

3. "direct"
Use direct when the question can be answered using your
general knowledge and does not require MCP or document retrieval.

User request:
{user_query}

Available MCP tools:
{json.dumps(tool_descriptions, indent=2)}

Return ONLY valid JSON.

Example:

{{
    "route": "mcp"
}}

or

{{
    "route": "rag"
}}

or

{{
    "route": "direct"
}}

Rules:

- Employee/database/project lookup → mcp
- Information from uploaded documents → rag
- General knowledge → direct
- Do not include markdown.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_format={
            "type": "json_object",
        },
    )

    content = response.choices[0].message.content

    content = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    decision = json.loads(content)

    route = decision.get("route", "direct")

    logger.info(
    "Route selected | route=%s | query_length=%d",
    route,
    len(state["user_query"]),
    )

    metrics.record_route(route)

    if route not in {
        "direct",
        "rag",
        "mcp",
    }:
        route = "direct"

    return {
        "route": route,
        "needs_tool": route == "mcp",
    }


# ============================================================
# 2. Direct LLM response
# ============================================================

def generate_direct_response(state):

    user_query = state["user_query"]

    prompt = f"""
Answer the user's question clearly and concisely.

Do not use external tools.

User question:
{user_query}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        tool_choice="none",
    )

    final_response = response.choices[0].message.content

    approved, _ = validate_output(
        final_response
    )

    if not approved:
        final_response = (
            "🛡️ SentinelAI blocked the response "
            "due to a security policy."
        )

    return {
        "final_response": final_response
    }


# ============================================================
# 3. Choose MCP tool
# ============================================================

def choose_tool(state, tools):

    user_query = state["user_query"]

    tool_descriptions = []

    for tool_name, info in tools.items():

        tool_descriptions.append(
            {
                "name": tool_name,
                "description": info["description"],
            }
        )

    prompt = f"""
You are an AI agent working inside SentinelAI.

The user asked:

{user_query}

Available MCP tools:

{json.dumps(tool_descriptions, indent=2)}

Select the single best MCP tool.

Return ONLY valid JSON:

{{
    "tool_name": "tool name",
    "arguments": {{
        "parameter": "value"
    }}
}}

Do not include markdown.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_format={
            "type": "json_object",
        },
    )

    content = response.choices[0].message.content

    content = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    decision = json.loads(content)

    tool_name = decision["tool_name"]

    arguments = decision.get(
        "arguments",
        {},
    )

    logger.info(
        "Tool selected | tool=%s | arguments=%s",
        tool_name,
        arguments,
        )
    if tool_name == "db_get_employee":
        if "employee_id" in arguments:
            arguments["employee_id"] = str(
            arguments["employee_id"]
        )

    # --------------------------------------------------------
    # Tool authorization guardrail
    # --------------------------------------------------------

    approved, message = validate_tool(
        tool_name
    )

    if not approved:
        raise PermissionError(message)

    # --------------------------------------------------------
    # Tool argument guardrail
    # --------------------------------------------------------

    approved, message = validate_tool_arguments(
        tool_name,
        arguments,
    )

    if not approved:
        raise PermissionError(
            f"Tool argument blocked: {message}"
        )

    return {
        "selected_tool": tool_name,
        "tool_arguments": arguments,
    }


# ============================================================
# 4. Execute MCP tool
# ============================================================

async def execute_tool(state, manager):

    tool_name = state["selected_tool"]

    arguments = state["tool_arguments"]

    logger.info(
    "Executing tool | tool=%s",
    tool_name,
    )

    result = await manager.call_tool(
        tool_name,
        arguments,
    )
    metrics.record_tool(tool_name)

    tool_text = ""

    for content in result.content:

        if hasattr(content, "text"):
            tool_text += content.text

    return {
        "tool_result": tool_text
    }


# ============================================================
# 5. Generate MCP response
# ============================================================

def generate_response(state):

    user_query = state["user_query"]

    tool_result = state["tool_result"]

    prompt = f"""
Answer the user's question using the tool result below.

Do not call any external tools.

User question:
{user_query}

Tool result:
{tool_result}

Give a clear and concise answer.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        tool_choice="none",
    )

    final_response = response.choices[0].message.content

    approved, _ = validate_output(
        final_response
    )

    if not approved:
        final_response = (
            "🛡️ SentinelAI blocked the response "
            "due to a security policy."
        )

    return {
        "final_response": final_response
    }


# ============================================================
# 6. Retrieve RAG context
# ============================================================

def retrieve_rag_context(
    state,
    rag_pipeline,
):

    user_query = state["user_query"]

    context = rag_pipeline.get_context(
        user_query
    )
    logger.info(
    "RAG retrieval completed | context_length=%d",
    len(context),
    )

    return {
        "rag_context": context
    }


# ============================================================
# 7. Generate RAG response
# ============================================================

def generate_rag_response(state):

    user_query = state["user_query"]

    rag_context = state.get(
        "rag_context",
        "",
    )

    if not rag_context:

        return {
            "final_response": (
                "I couldn't find relevant information "
                "in the indexed documents."
            )
        }

    prompt = f"""
You are SentinelAI's document question-answering system.

Answer the user's question using ONLY the provided
document context.

If the answer cannot be found in the context,
say that the information was not found in the
available documents.

Do not use external tools.

User question:
{user_query}

Document context:
{rag_context}

Give a clear and concise answer.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        tool_choice="none",
    )

    final_response = response.choices[0].message.content

    approved, _ = validate_output(
        final_response
    )

    if not approved:
        final_response = (
            "🛡️ SentinelAI blocked the response "
            "due to a security policy."
        )

    return {
        "final_response": final_response
    }