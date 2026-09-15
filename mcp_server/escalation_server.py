import json
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("escalation-server")

ESCALATIONS_FILE = os.path.join(os.path.dirname(__file__), "escalations.json")

@mcp.tool()
def create_escalation_ticket(
    customer_email: str,
    category: str,
    priority: str,
    reason: str,
    draft_reply: str,
) -> str:
    """Create an escalation ticket for human review when the agent is not
    confident enough to auto-resolve a support ticket.

    Args:
        customer_email: the customer's email address
        category: ticket category (billing, bug, how_to, other)
        priority: ticket priority (low, medium, high)
        reason: why this was escalated (low confidence, etc.)
        draft_reply: the AI-drafted reply, for the human agent to review/edit
    """
    escalation = {
        "escalation_id": f"ESC-{int(datetime.utcnow().timestamp())}",
        "customer_email": customer_email,
        "category": category,
        "priority": priority,
        "reason": reason,
        "draft_reply": draft_reply,
        "created_at": datetime.utcnow().isoformat(),
        "status": "pending_human_review",
    }

    existing = []
    if os.path.exists(ESCALATIONS_FILE):
        with open(ESCALATIONS_FILE, "r") as f:
            content = f.read().strip()
        if content:
            try:
                existing = json.loads(content)
            except json.JSONDecodeError:
                existing = []

    existing.append(escalation)
    with open(ESCALATIONS_FILE, "w") as f:
        json.dump(existing, f, indent=2)

    return f"Escalation created: {escalation['escalation_id']}"

if __name__ == "__main__":
    mcp.run(transport="stdio")