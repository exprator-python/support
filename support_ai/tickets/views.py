from django.http import JsonResponse
from django.views import View
from .services.resolver import TicketResolver

class TicketView(View):
    """Django API endpoint for resolving support tickets."""

    def post(self, request):
        ticket: str = request.POST.get("ticket", "")
        resolver = TicketResolver()
        result = resolver.resolve_graph(ticket)
        return JsonResponse(result)
