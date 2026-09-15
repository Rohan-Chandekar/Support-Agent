import asyncio
from src.state import TicketState
from src.mcp_client.escalation_client import call_create_escalation

def escalate_node(state: TicketState) -> dict:
    """Fallback path: escalate low-confidence tickets to a human via MCP."""
    result_message = asyncio.run(
        call_create_escalation(
            customer_email=state.get("customer_email") or "unknown",
            category=state["category"],
            priority=state["priority"],
            reason=f"Low confidence score: {state['confidence']}",
            draft_reply=state["draft_reply"],
        )
    )

    return {
        "final_reply": None,
        "escalated": True,
    }