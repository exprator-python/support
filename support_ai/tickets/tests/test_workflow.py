import pytest


from support_ai.tickets.services import workflow
from support_ai.tickets.services.workflow import build_ticket_graph


@pytest.mark.parametrize("ticket,expected_category", [
    ("My payment was deducted twice", "Billing"),
    ("When will my package arrive?", "Shipping"),
    ("The laptop screen is broken", "Product"),
    ("I want to complain to your CEO", "Other"),
])
def test_ticket_graph(ticket: str, expected_category: str, monkeypatch):
    """GIVEN a ticket WHEN processed through LangGraph THEN correct category + answer returned."""

    # Patch classifier for deterministic test
    def mock_classify(state):
        text = state["ticket"].lower()
        if "payment" in text:
            return {**state, "category": "Billing"}
        if "package" in text:
            return {**state, "category": "Shipping"}
        if "laptop" in text:
            return {**state, "category": "Product"}
        return {**state, "category": "Other"}


    monkeypatch.setattr(workflow, "classify_node", mock_classify)

    graph = build_ticket_graph()
    result = graph.invoke({"ticket": ticket})

    assert result["category"] == expected_category
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0
