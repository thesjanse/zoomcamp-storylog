"""Views for the StoryLog backend scaffold."""

from django.http import HttpResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer


def home(request):
    """Return placeholder content for the scaffold smoke test."""
    return HttpResponse("StoryLog backend scaffold")


class HealthView(APIView):
    """Report that the versioned API is reachable without authentication."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


class RegisterView(APIView):
    """Create a user account and return a DRF authentication token."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response(
            {
                "token": token.key,
                "user": {"id": user.pk, "username": user.username},
            },
            status=status.HTTP_201_CREATED,
        )
