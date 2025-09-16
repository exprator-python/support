from typing import Optional
from .classifier import TicketCategory
from .workflow import build_ticket_graph

_FAQ_DB: dict[TicketCategory, str] = {
    "Billing": "For billing issues, visit /billing or contact billing@company.com.",
    "Shipping": "Shipping delays may occur. Track your order at /shipping.",
    "Product": "Check product manuals at /products or contact support@company.com.",
    "Other": "Your query has been logged. A human agent will follow up."
}


class TicketResolver:
    """Resolves support tickets by classification + FAQ lookup."""

    def __init__(self) -> None:
        self.graph = build_ticket_graph()

    def resolve_graph(self, ticket: str) -> dict[str, str]:
        result = self.graph.invoke({"ticket": ticket})
        return {
            "ticket": result["ticket"],
            "category": result["category"],
            "answer": result["answer"],
        }
