from typing import Literal
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

TicketCategory = Literal["Billing", "Shipping", "Product", "Other"]

class TicketClassifier:
    """Classifies support tickets into predefined categories using LLM."""

    def __init__(self, model_name: str = "gpt-4o-mini") -> None:
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Classify the support ticket into: Billing, Shipping, Product, or Other."),
            ("user", "{ticket}")
        ])

    def classify(self, ticket: str) -> TicketCategory:
        chain = self.prompt | self.llm
        result = chain.invoke({"ticket": ticket})
        category = result.content.strip()
        valid_categories: set[str] = {"Billing", "Shipping", "Product", "Other"}
        return category if category in valid_categories else "Other"
