"""URL configuration for the StoryLog backend scaffold."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/v1/health/", views.HealthView.as_view(), name="health"),
]
