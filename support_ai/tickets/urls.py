from django.urls import path
from .views import TicketView

urlpatterns = [
    path("resolve/", TicketView.as_view(), name="resolve_ticket"),
]
