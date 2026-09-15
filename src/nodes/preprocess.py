import re
from src.state import TicketState

def preprocess_node(state: TicketState) -> dict:
    """Clean raw ticket text and pull out an email if present."""
    raw = state["raw_ticket"]

    # basic cleanup: collapse whitespace
    clean = re.sub(r"\s+", " ", raw).strip()

    # naive email extraction (good enough for demo data)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", raw)
    email = email_match.group(0) if email_match else None

    return {
        "clean_text": clean,
        "customer_email": email,
    }