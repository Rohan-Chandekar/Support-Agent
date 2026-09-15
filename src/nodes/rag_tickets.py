from src.state import TicketState
from src.rag.past_tickets_store import retrieve_past_tickets

def rag_tickets_node(state: TicketState) -> dict:
    """Retrieve similar past resolved tickets for this ticket."""
    query = state["clean_text"]
    chunks = retrieve_past_tickets(query, k=2)
    return {"ticket_context": chunks}