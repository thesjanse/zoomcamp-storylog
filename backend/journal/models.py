from django.conf import settings
from django.db import models


class JournalItemQuerySet(models.QuerySet):
    def for_owner(self, user):
        return self.filter(owner=user)


class NoteQuerySet(models.QuerySet):
    def for_owner(self, user):
        return self.filter(item__owner=user)


class JournalItem(models.Model):
    class Type(models.TextChoices):
        BOOK = "book", "Book"
        MOVIE = "movie", "Movie"

    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        IN_PROGRESS = "in_progress", "In progress"
        FINISHED = "finished", "Finished"
        DROPPED = "dropped", "Dropped"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="journal_items",
    )
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=Type.choices)
    creator = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED,
    )
    start_date = models.DateField(null=True, blank=True, default=None)
    finish_date = models.DateField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = JournalItemQuerySet.as_manager()

    class Meta:
        ordering = ["-updated_at", "-id"]

    def __str__(self):
        return self.title


class Note(models.Model):
    item = models.ForeignKey(
        JournalItem,
        on_delete=models.CASCADE,
        related_name="notes",
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    objects = NoteQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return self.body
