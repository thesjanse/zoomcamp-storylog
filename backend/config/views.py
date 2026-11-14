"""Views for the StoryLog backend scaffold."""

from django.http import HttpResponse


def home(request):
    """Return placeholder content for the scaffold smoke test."""
    return HttpResponse("StoryLog backend scaffold")
