from src.state import TicketState
from src.rag.product_docs_store import retrieve_product_docs

def rag_docs_node(state: TicketState) -> dict:
    """Retrieve relevant product documentation chunks for this ticket."""
    query = state["clean_text"]
    chunks = retrieve_product_docs(query, k=2)
    return {"doc_context": chunks}