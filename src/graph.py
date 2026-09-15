from typing import Literal
from langgraph.graph import StateGraph, END
from src.state import TicketState
from src.nodes.preprocess import preprocess_node
from src.nodes.classify import classify_node
from src.nodes.rag_docs import rag_docs_node
from src.nodes.rag_tickets import rag_tickets_node
from src.nodes.sla import sla_node
from src.nodes.generate import generate_node
from src.nodes.validate import validate_node
from src.nodes.format_reply import format_reply_node
from src.nodes.escalate import escalate_node

# CONFIDENCE_THRESHOLD = 0.99
CONFIDENCE_THRESHOLD = 0.7

def route_after_validation(state: TicketState) -> Literal["confident", "not_confident"]:
    """Conditional edge routing function: decide success vs fallback path."""
    if state["confidence"] >= CONFIDENCE_THRESHOLD:
        return "confident"
    return "not_confident"

def build_graph():
    graph = StateGraph(TicketState)
    graph.add_node("preprocess", preprocess_node)
    graph.add_node("classify", classify_node)
    graph.add_node("rag_docs", rag_docs_node)
    graph.add_node("rag_tickets", rag_tickets_node)
    graph.add_node("sla", sla_node)
    graph.add_node("generate", generate_node)
    graph.add_node("validate", validate_node)
    graph.add_node("format_reply", format_reply_node)
    graph.add_node("escalate", escalate_node)

    graph.set_entry_point("preprocess")
    graph.add_edge("preprocess", "classify")
    graph.add_edge("classify", "rag_docs")
    graph.add_edge("rag_docs", "rag_tickets")
    graph.add_edge("rag_tickets", "sla")
    graph.add_edge("sla", "generate")
    graph.add_edge("generate", "validate")

    graph.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "confident": "format_reply",
            "not_confident": "escalate",
        }
    )

    graph.add_edge("format_reply", END)
    graph.add_edge("escalate", END)

    return graph.compile()