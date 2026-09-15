from typing import Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from src.state import TicketState

class ConfidenceCheck(BaseModel):
    confidence: float = Field(
        description="Score from 0.0 to 1.0 on how safe/accurate this reply is to send as-is"
    )
    reason: str = Field(
        description="One short sentence explaining the score"
    )

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(ConfidenceCheck)

VALIDATE_PROMPT = """You are reviewing a draft customer support reply before it is sent.

Customer ticket:
{ticket_text}

Draft reply:
{draft_reply}

Rate confidence (0.0 to 1.0) that this reply is accurate, grounded in
real information, and safe to send to the customer without human review.
Lower the score if the reply guesses, hedges excessively, admits it
doesn't have enough information, or makes commitments it cannot verify.
"""

def validate_node(state: TicketState) -> dict:
    """Judge whether the draft reply is confident/safe enough to auto-send."""
    prompt = VALIDATE_PROMPT.format(
        ticket_text=state["clean_text"],
        draft_reply=state["draft_reply"],
    )
    result: ConfidenceCheck = structured_llm.invoke(prompt)

    return {"confidence": result.confidence}