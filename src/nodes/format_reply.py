from datetime import datetime
from src.state import TicketState

def format_reply_node(state: TicketState) -> dict:
    """Finalize the validated draft reply for sending (success path)."""
    footer = f"\n\n---\nTicket priority: {state['priority'].upper()} | SLA: {state['sla_hours']}h"
    final = state["draft_reply"].strip() + footer

    return {
        "final_reply": final,
        "escalated": False,
    }