from typing import Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from src.state import TicketState

class ClassificationResult(BaseModel):
    category: Literal["billing", "bug", "how_to", "other"] = Field(
        description="The best-fit category for this support ticket"
    )
    priority: Literal["low", "medium", "high"] = Field(
        description="Urgency of the ticket based on its content"
    )

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(ClassificationResult)

CLASSIFY_PROMPT = """You are a support ticket triage assistant.
Classify the following ticket into a category and priority.

Ticket: {ticket_text}
"""

def classify_node(state: TicketState) -> dict:
    """Classify the cleaned ticket text into category + priority."""
    prompt = CLASSIFY_PROMPT.format(ticket_text=state["clean_text"])
    result: ClassificationResult = structured_llm.invoke(prompt)

    return {
        "category": result.category,
        "priority": result.priority,
    }