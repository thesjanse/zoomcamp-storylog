"""Views for the StoryLog backend scaffold."""

from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


def home(request):
    """Return placeholder content for the scaffold smoke test."""
    return HttpResponse("StoryLog backend scaffold")


class HealthView(APIView):
    """Report that the versioned API is reachable without authentication."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})
