"""URL configuration for the StoryLog backend scaffold."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
]
