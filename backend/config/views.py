"""Views for the StoryLog backend scaffold."""

from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer


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


class LoginView(APIView):
    """Exchange valid credentials for the user's existing DRF token."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": {"id": user.pk, "username": user.username},
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """Revoke exactly the token presented with the request."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    """Return the authenticated user's minimal public record."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"id": request.user.pk, "username": request.user.username}
        )
