"""URL configuration for the StoryLog backend scaffold."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/v1/health/", views.HealthView.as_view(), name="health"),
    path(
        "api/v1/auth/register/",
        views.RegisterView.as_view(),
        name="register",
    ),
    path("api/v1/auth/login/", views.LoginView.as_view(), name="login"),
    path("api/v1/auth/logout/", views.LogoutView.as_view(), name="logout"),
    path("api/v1/auth/me/", views.MeView.as_view(), name="me"),
]
