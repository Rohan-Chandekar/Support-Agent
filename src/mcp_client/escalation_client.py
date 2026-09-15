import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_SCRIPT = os.path.join(
    os.path.dirname(__file__), "..", "..", "mcp_server", "escalation_server.py"
)

async def call_create_escalation(
    customer_email: str,
    category: str,
    priority: str,
    reason: str,
    draft_reply: str,
) -> str:
    """Connects to the escalation MCP server, calls its tool, returns the result."""
    server_params = StdioServerParameters(
        command=sys.executable,   # use the same Python interpreter (venv-safe)
        args=[SERVER_SCRIPT],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "create_escalation_ticket",
                arguments={
                    "customer_email": customer_email,
                    "category": category,
                    "priority": priority,
                    "reason": reason,
                    "draft_reply": draft_reply,
                },
            )
            return result.content[0].text