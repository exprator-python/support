from typing import TypedDict
from langgraph.graph import StateGraph, END
from .classifier import TicketClassifier, TicketCategory

_FAQ_DB: dict[TicketCategory, str] = {
    "Billing": "For billing issues, visit /billing or contact billing@company.com.",
    "Shipping": "Track your package at /shipping. Delays may occur.",
    "Product": "Find product manuals at /products or email support@company.com.",
    "Other": "We could not auto-resolve your issue. A human agent will follow up."
}


class TicketState(TypedDict):
    """State passed between workflow nodes."""
    ticket: str
    category: TicketCategory
    answer: str


def classify_node(state: TicketState) -> TicketState:
    classifier = TicketClassifier()
    category = classifier.classify(state["ticket"])
    return {**state, "category": category}


def faq_lookup_node(state: TicketState) -> TicketState:
    answer = _FAQ_DB.get(state["category"], _FAQ_DB["Other"])
    return {**state, "answer": answer}


def escalate_node(state: TicketState) -> TicketState:
    # This node simulates escalation to a human support queue
    return {**state, "answer": "Escalated to human support team."}


def build_ticket_graph() -> StateGraph:
    graph = StateGraph(TicketState)

    # Register nodes
    graph.add_node("classify", classify_node)
    graph.add_node("faq_lookup", faq_lookup_node)
    graph.add_node("escalate", escalate_node)

    # Define flow
    graph.set_entry_point("classify")
    graph.add_edge("classify", "faq_lookup")

    # Conditional edge for escalation
    graph.add_conditional_edges(
        "faq_lookup",
        lambda state: "escalate" if state["category"] == "Other" else END,
        {"escalate": "escalate", END: END}
    )
    graph.add_edge("escalate", END)

    return graph.compile()
