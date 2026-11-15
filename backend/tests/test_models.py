from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from journal.models import JournalItem, Note

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        username="test-user",
        password="fake-test-password",
    )


@pytest.fixture
def other_user():
    return get_user_model().objects.create_user(
        username="other-test-user",
        password="fake-other-password",
    )


def test_create_with_required_fields_applies_defaults(user):
    item = JournalItem.objects.create(
        owner=user,
        title="The Left Hand of Darkness",
        type=JournalItem.Type.BOOK,
    )

    assert item.owner == user
    assert item.title == "The Left Hand of Darkness"
    assert item.type == JournalItem.Type.BOOK
    assert item.status == JournalItem.Status.PLANNED
    assert item.creator == ""
    assert item.start_date is None
    assert item.finish_date is None
    assert item.created_at is not None
    assert item.updated_at is not None


def test_type_choices_use_stored_values_and_display_labels():
    assert list(JournalItem.Type.values) == ["book", "movie"]
    assert [label for _, label in JournalItem.Type.choices] == ["Book", "Movie"]


def test_status_choices_use_stored_values_and_display_labels():
    assert list(JournalItem.Status.values) == [
        "planned",
        "in_progress",
        "finished",
        "dropped",
    ]
    assert [label for _, label in JournalItem.Status.choices] == [
        "Planned",
        "In progress",
        "Finished",
        "Dropped",
    ]


def test_creator_is_optional_for_books_and_movies(user):
    book = JournalItem.objects.create(
        owner=user,
        title="A Wizard of Earthsea",
        type=JournalItem.Type.BOOK,
    )
    movie = JournalItem.objects.create(
        owner=user,
        title="Arrival",
        type=JournalItem.Type.MOVIE,
    )

    book.full_clean()
    movie.full_clean()
    assert book.creator == ""
    assert movie.creator == ""


def test_creator_and_dates_are_stored_unchanged(user):
    start_date = date(2024, 1, 2)
    finish_date = date(2024, 2, 3)

    item = JournalItem.objects.create(
        owner=user,
        title="Solaris",
        type=JournalItem.Type.MOVIE,
        creator="Andrei Tarkovsky",
        status=JournalItem.Status.FINISHED,
        start_date=start_date,
        finish_date=finish_date,
    )
    item.refresh_from_db()

    assert item.creator == "Andrei Tarkovsky"
    assert item.status == JournalItem.Status.FINISHED
    assert item.start_date == start_date
    assert item.finish_date == finish_date


def test_dates_default_to_null(user):
    item = JournalItem.objects.create(
        owner=user,
        title="Piranesi",
        type=JournalItem.Type.BOOK,
    )
    item.refresh_from_db()

    assert item.start_date is None
    assert item.finish_date is None


def test_for_owner_returns_only_that_users_items(user, other_user):
    own_item = JournalItem.objects.create(
        owner=user,
        title="Owned Item",
        type=JournalItem.Type.BOOK,
    )
    other_item = JournalItem.objects.create(
        owner=other_user,
        title="Other Item",
        type=JournalItem.Type.MOVIE,
    )

    items = JournalItem.objects.for_owner(user)

    assert list(items) == [own_item]
    assert other_item not in items


def test_for_owner_returns_empty_queryset_for_user_without_items(user):
    items = JournalItem.objects.for_owner(user)

    assert items.count() == 0
    assert list(items) == []


def test_for_owner_inherits_default_ordering(user):
    first = JournalItem.objects.create(
        owner=user,
        title="First",
        type=JournalItem.Type.BOOK,
    )
    second = JournalItem.objects.create(
        owner=user,
        title="Second",
        type=JournalItem.Type.BOOK,
    )
    now = timezone.now()
    JournalItem.objects.filter(pk=first.pk).update(
        updated_at=now - timedelta(days=1)
    )
    JournalItem.objects.filter(pk=second.pk).update(updated_at=now)

    assert list(JournalItem.objects.for_owner(user)) == [second, first]


def test_default_ordering_is_updated_at_descending_then_id_descending(user):
    first = JournalItem.objects.create(
        owner=user,
        title="First",
        type=JournalItem.Type.BOOK,
    )
    second = JournalItem.objects.create(
        owner=user,
        title="Second",
        type=JournalItem.Type.BOOK,
    )
    third = JournalItem.objects.create(
        owner=user,
        title="Third",
        type=JournalItem.Type.BOOK,
    )
    now = timezone.now()
    JournalItem.objects.filter(pk=first.pk).update(
        updated_at=now - timedelta(days=1)
    )
    JournalItem.objects.filter(pk=second.pk).update(updated_at=now)
    JournalItem.objects.filter(pk=third.pk).update(updated_at=now)

    assert list(JournalItem.objects.all()) == [third, second, first]


def test_timestamps_are_set_on_creation_and_updated_on_save(user):
    item = JournalItem.objects.create(
        owner=user,
        title="Original Title",
        type=JournalItem.Type.BOOK,
    )
    created_at = item.created_at
    updated_at = item.updated_at
    assert JournalItem._meta.get_field("created_at").editable is False
    assert JournalItem._meta.get_field("updated_at").editable is False

    item.title = "Changed Title"
    item.save()
    item.refresh_from_db()

    assert item.created_at == created_at
    assert item.updated_at > updated_at


def test_str_returns_title(user):
    item = JournalItem.objects.create(
        owner=user,
        title="Kindred",
        type=JournalItem.Type.BOOK,
    )

    assert str(item) == "Kindred"


def test_deleting_owner_cascades_to_items(user):
    item = JournalItem.objects.create(
        owner=user,
        title="Cascade Me",
        type=JournalItem.Type.BOOK,
    )
    item_id = item.pk
    assert user.journal_items.count() == 1

    user.delete()

    assert not JournalItem.objects.filter(pk=item_id).exists()


def test_validation_rejects_missing_title(user):
    item = JournalItem(owner=user, type=JournalItem.Type.BOOK)

    with pytest.raises(ValidationError) as exc_info:
        item.full_clean()

    assert "title" in exc_info.value.message_dict


def test_validation_rejects_blank_title(user):
    item = JournalItem(owner=user, title="", type=JournalItem.Type.BOOK)

    with pytest.raises(ValidationError) as exc_info:
        item.full_clean()

    assert "title" in exc_info.value.message_dict


def test_validation_rejects_missing_type(user):
    item = JournalItem(owner=user, title="Missing Type")

    with pytest.raises(ValidationError) as exc_info:
        item.full_clean()

    assert "type" in exc_info.value.message_dict


def test_validation_rejects_missing_owner():
    item = JournalItem(title="Missing Owner", type=JournalItem.Type.BOOK)

    with pytest.raises(ValidationError) as exc_info:
        item.full_clean()

    assert "owner" in exc_info.value.message_dict


def test_validation_rejects_invalid_type_and_status(user):
    item = JournalItem(
        owner=user,
        title="Invalid Choices",
        type="podcast",
        status="paused",
    )

    with pytest.raises(ValidationError) as exc_info:
        item.full_clean()

    assert "type" in exc_info.value.message_dict
    assert "status" in exc_info.value.message_dict


def test_note_creation_with_required_fields(user):
    item = JournalItem.objects.create(
        owner=user,
        title="The Dispossessed",
        type=JournalItem.Type.BOOK,
    )
    body = "First line\nSecond line"

    note = Note.objects.create(item=item, body=body)
    note.refresh_from_db()

    assert note.item == item
    assert note.body == body
    assert note.created_at is not None
    assert list(item.notes.all()) == [note]


def test_note_requires_item(user):
    with pytest.raises(IntegrityError):
        Note.objects.create(body="Orphan note")


def test_note_created_at_is_automatic_and_preserved_on_edit(user):
    item = JournalItem.objects.create(
        owner=user,
        title="The Lathe of Heaven",
        type=JournalItem.Type.BOOK,
    )
    note = Note.objects.create(item=item, body="Original body")
    created_at = note.created_at
    assert Note._meta.get_field("created_at").editable is False

    note.body = "Edited body"
    note.save()
    note.refresh_from_db()

    assert note.body == "Edited body"
    assert note.created_at == created_at


def test_note_default_ordering_is_created_at_descending_then_id_descending(user):
    item = JournalItem.objects.create(
        owner=user,
        title="Ordered Notes",
        type=JournalItem.Type.BOOK,
    )
    first = Note.objects.create(item=item, body="First")
    second = Note.objects.create(item=item, body="Second")
    third = Note.objects.create(item=item, body="Third")
    now = timezone.now()
    Note.objects.filter(pk=first.pk).update(created_at=now - timedelta(days=1))
    Note.objects.filter(pk=second.pk).update(created_at=now)
    Note.objects.filter(pk=third.pk).update(created_at=now)

    assert Note._meta.ordering == ["-created_at", "-id"]
    assert list(Note.objects.all()) == [third, second, first]
    assert list(Note.objects.for_owner(user)) == [third, second, first]


def test_note_for_owner_returns_only_notes_through_parent_item(user, other_user):
    own_item = JournalItem.objects.create(
        owner=user,
        title="Owned Note Item",
        type=JournalItem.Type.BOOK,
    )
    other_item = JournalItem.objects.create(
        owner=other_user,
        title="Other Note Item",
        type=JournalItem.Type.MOVIE,
    )
    own_note = Note.objects.create(item=own_item, body="Own note")
    other_note = Note.objects.create(item=other_item, body="Other note")

    notes = Note.objects.for_owner(user)

    assert list(notes) == [own_note]
    assert other_note not in notes


def test_note_for_owner_returns_empty_queryset_for_user_without_notes(user):
    notes = Note.objects.for_owner(user)

    assert notes.count() == 0
    assert list(notes) == []


def test_note_str_returns_body(user):
    item = JournalItem.objects.create(
        owner=user,
        title="String Note",
        type=JournalItem.Type.BOOK,
    )
    note = Note.objects.create(item=item, body="A plain-text note")

    assert str(note) == "A plain-text note"


def test_note_validation_rejects_missing_body(user):
    item = JournalItem.objects.create(
        owner=user,
        title="Missing Body",
        type=JournalItem.Type.BOOK,
    )
    note = Note(item=item)

    with pytest.raises(ValidationError) as exc_info:
        note.full_clean()

    assert "body" in exc_info.value.message_dict


def test_note_validation_rejects_blank_body(user):
    item = JournalItem.objects.create(
        owner=user,
        title="Blank Body",
        type=JournalItem.Type.BOOK,
    )
    note = Note(item=item, body="")

    with pytest.raises(ValidationError) as exc_info:
        note.full_clean()

    assert "body" in exc_info.value.message_dict


def test_note_validation_rejects_missing_item(user):
    note = Note(body="No parent")

    with pytest.raises(ValidationError) as exc_info:
        note.full_clean()

    assert "item" in exc_info.value.message_dict


def test_note_validation_accepts_valid_note(user):
    item = JournalItem.objects.create(
        owner=user,
        title="Valid Note",
        type=JournalItem.Type.BOOK,
    )
    note = Note(item=item, body="Valid body")

    note.full_clean()


def test_deleting_item_cascades_to_its_notes_only(user):
    item = JournalItem.objects.create(
        owner=user,
        title="Deleted Item",
        type=JournalItem.Type.BOOK,
    )
    other_item = JournalItem.objects.create(
        owner=user,
        title="Preserved Item",
        type=JournalItem.Type.BOOK,
    )
    note = Note.objects.create(item=item, body="Deleted note")
    other_note = Note.objects.create(item=other_item, body="Preserved note")
    note_id = note.pk
    item_id = item.pk

    JournalItem.objects.filter(pk=item_id).delete()

    assert not Note.objects.filter(pk=note_id).exists()
    assert Note.objects.filter(pk=other_note.pk).exists()


def test_deleting_owner_cascades_to_items_and_notes(user, other_user):
    item = JournalItem.objects.create(
        owner=user,
        title="Owner Item",
        type=JournalItem.Type.BOOK,
    )
    other_item = JournalItem.objects.create(
        owner=other_user,
        title="Other Owner Item",
        type=JournalItem.Type.BOOK,
    )
    note = Note.objects.create(item=item, body="Owner note")
    other_note = Note.objects.create(item=other_item, body="Other owner note")
    note_id = note.pk
    item_id = item.pk

    user.delete()

    assert not JournalItem.objects.filter(pk=item_id).exists()
    assert not Note.objects.filter(pk=note_id).exists()
    assert Note.objects.filter(pk=other_note.pk).exists()
