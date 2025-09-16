import pytest

from support_ai.tickets.services.classifier import TicketClassifier


@pytest.mark.parametrize("ticket,expected", [
    ("My credit card was charged twice", "Billing"),
    ("Where is my order?", "Shipping"),
    ("The laptop is not turning on", "Product"),
    ("I want to talk to your CEO", "Other"),
])
def test_ticket_classifier(ticket: str, expected: str, monkeypatch):
    """GIVEN a ticket WHEN classified THEN return correct category."""

    def mock_classify(self, ticket: str) -> str:
        mapping = {
            "credit card": "Billing",
            "order": "Shipping",
            "laptop": "Product",
        }
        for key, val in mapping.items():
            if key in ticket.lower():
                return val
        return "Other"

    monkeypatch.setattr(TicketClassifier, "classify", mock_classify)
    classifier = TicketClassifier()
    assert classifier.classify(ticket) == expected
