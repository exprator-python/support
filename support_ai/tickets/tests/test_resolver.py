import pytest

from support_ai.tickets.services.resolver import TicketResolver


@pytest.mark.parametrize("ticket,expected_category", [
    ("Refund my payment", "Billing"),
    ("Track my package", "Shipping"),
    ("The phone is broken", "Product"),
    ("Random nonsense", "Other"),
])
def test_ticket_resolver(ticket: str, expected_category: str, monkeypatch):
    """GIVEN a ticket WHEN resolved THEN return category and answer."""

    def mock_classify(self, ticket: str) -> str:
        if "refund" in ticket.lower():
            return "Billing"
        if "package" in ticket.lower():
            return "Shipping"
        if "phone" in ticket.lower():
            return "Product"
        return "Other"

    monkeypatch.setattr("tickets.services.resolver.TicketClassifier.classify", mock_classify)

    resolver = TicketResolver()
    result = resolver.resolve(ticket)

    assert result["category"] == expected_category
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0
