from typing import TypedDict, Optional, List

class TicketState(TypedDict, total=False):
    # input
    raw_ticket: str

    # preprocess output
    clean_text: str
    customer_email: Optional[str]

    # classify output
    category: Optional[str]      # billing | bug | how_to | other
    priority: Optional[str]      # low | medium | high

    # RAG outputs (added Day 2)
    doc_context: Optional[List[str]]
    ticket_context: Optional[List[str]]

    # generation & validation (added Day 2)
    draft_reply: Optional[str]
    confidence: Optional[float]

    sla_hours: Optional[int]
    sla_deadline: Optional[str]

    # final (added Day 3)
    final_reply: Optional[str]
    escalated: Optional[bool]

