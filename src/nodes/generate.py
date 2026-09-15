from langchain_openai import ChatOpenAI
from src.state import TicketState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

GENERATE_PROMPT = """You are a customer support agent replying to a ticket.

Ticket category: {category}
Priority: {priority}
Response deadline: {sla_hours} hours

Customer message:
{ticket_text}

Relevant product documentation:
{doc_context}

Similar past resolved tickets:
{ticket_context}

Write a clear, empathetic, concise reply to the customer. Use the
documentation and past ticket examples as grounding for accuracy, but do
not mention "documentation" or "past tickets" explicitly to the customer.
If the provided context does not contain enough information to answer
confidently, say so honestly instead of guessing.
"""

def generate_node(state: TicketState) -> dict:
    """Draft a grounded reply using retrieved context."""
    prompt = GENERATE_PROMPT.format(
        category=state["category"],
        priority=state["priority"],
        sla_hours=state["sla_hours"],
        ticket_text=state["clean_text"],
        doc_context="\n".join(state["doc_context"]),
        ticket_context="\n".join(state["ticket_context"]),
    )

    response = llm.invoke(prompt)

    return {"draft_reply": response.content}