from src.state import TicketState
from src.tools.sla_tool import calculate_sla

def sla_node(state: TicketState) -> dict:
    """Node wrapper: reads category/priority from state, calls the SLA tool,
    writes the result back into state."""
    result = calculate_sla(state["category"], state["priority"])
    return {
        "sla_hours": result["sla_hours"],
        "sla_deadline": result["sla_deadline"],
    }