import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

pytestmark = pytest.mark.django_db

REGISTER_URL = "/api/v1/auth/register/"


def register(client, **payload):
    return client.post(
        REGISTER_URL,
        data=json.dumps(payload),
        content_type="application/json",
    )


def assert_field_error(response, field):
    assert response.status_code == 400
    data = response.json()
    assert field in data
    assert isinstance(data[field], list)
    assert data[field]
    assert all(isinstance(message, str) for message in data[field])


def test_register_returns_201_with_exact_response_shape(client):
    username = "response-shape-user"
    password = "fake-registration-password"

    response = register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    assert response.status_code == 201
    data = response.json()
    assert set(data) == {"token", "user"}
    assert set(data["user"]) == {"id", "username"}
    assert isinstance(data["token"], str)
    assert data["token"]
    assert isinstance(data["user"]["id"], int)
    assert data["user"]["username"] == username

    user = get_user_model().objects.get(username=username)
    assert data["user"]["id"] == user.pk


def test_register_persists_token_for_new_user(client):
    username = "persisted-token-user"
    password = "fake-token-password"

    response = register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    user = get_user_model().objects.get(username=username)
    token = Token.objects.get(key=response.json()["token"])
    assert token.user == user
    assert Token.objects.filter(user=user).count() == 1


def test_register_hashes_password_and_does_not_store_raw_values(client):
    username = "hashed-password-user"
    password = "fake-raw-password"
    password_confirm = password

    register(
        client,
        username=username,
        password=password,
        password_confirm=password_confirm,
    )

    user = get_user_model().objects.get(username=username)
    token = Token.objects.get(user=user)
    assert user.password != password
    assert user.check_password(password)
    assert "password_confirm" not in {field.name for field in user._meta.fields}
    for stored_value in (password, password_confirm):
        assert all(
            getattr(user, field.name) != stored_value
            for field in user._meta.fields
        )
        assert token.key != stored_value


def test_register_rejects_exact_duplicate_username(client):
    username = "duplicate-username-user"
    password = "fake-duplicate-password"
    get_user_model().objects.create_user(
        username=username,
        password="fake-existing-password",
    )

    response = register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    assert_field_error(response, "username")
    assert "token" not in response.json()
    assert get_user_model().objects.filter(username=username).count() == 1
    assert get_user_model().objects.count() == 1
    assert Token.objects.count() == 0


def test_register_treats_username_uniqueness_as_case_sensitive(client):
    uppercase_username = "CaseSensitiveUser"
    lowercase_username = "casesensitiveuser"
    password = "fake-case-password"

    first_response = register(
        client,
        username=uppercase_username,
        password=password,
        password_confirm=password,
    )
    second_response = register(
        client,
        username=lowercase_username,
        password=password,
        password_confirm=password,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert get_user_model().objects.count() == 2
    assert set(
        get_user_model().objects.values_list("username", flat=True)
    ) == {uppercase_username, lowercase_username}


def test_register_trims_username_before_validation_and_storage(client):
    password = "fake-trim-password"

    response = register(
        client,
        username="  trimmed-username-user  ",
        password=password,
        password_confirm=password,
    )

    assert response.status_code == 201
    assert response.json()["user"]["username"] == "trimmed-username-user"
    user = get_user_model().objects.get()
    assert user.username == "trimmed-username-user"
    assert not get_user_model().objects.filter(
        username="  trimmed-username-user  "
    ).exists()


@pytest.mark.parametrize("username", [None, "", "   "])
def test_register_rejects_missing_or_blank_username(client, username):
    password = "fake-blank-username-password"
    payload = {"password": password, "password_confirm": password}
    if username is not None:
        payload["username"] = username

    response = register(client, **payload)

    assert_field_error(response, "username")
    assert get_user_model().objects.count() == 0
    assert Token.objects.count() == 0


@pytest.mark.parametrize("password", [None, ""])
def test_register_rejects_missing_or_empty_password(client, password):
    username = "missing-password-user"
    payload = {"username": username, "password_confirm": "fake-confirmation"}
    if password is not None:
        payload["password"] = password

    response = register(client, **payload)

    assert_field_error(response, "password")
    assert get_user_model().objects.count() == 0
    assert Token.objects.count() == 0


@pytest.mark.parametrize("password_confirm", [None, ""])
def test_register_rejects_missing_or_empty_password_confirm(
    client,
    password_confirm,
):
    username = "missing-confirmation-user"
    payload = {"username": username, "password": "fake-password"}
    if password_confirm is not None:
        payload["password_confirm"] = password_confirm

    response = register(client, **payload)

    assert_field_error(response, "password_confirm")
    assert get_user_model().objects.count() == 0
    assert Token.objects.count() == 0


def test_register_rejects_mismatched_password_confirmation(client):
    username = "mismatched-confirmation-user"

    response = register(
        client,
        username=username,
        password="fake-password-one",
        password_confirm="fake-password-two",
    )

    assert_field_error(response, "password_confirm")
    assert get_user_model().objects.count() == 0
    assert Token.objects.count() == 0


def test_register_validation_errors_use_field_error_shape(client):
    response = register(client)

    assert response.status_code == 400
    data = response.json()
    assert set(data) == {"username", "password", "password_confirm"}
    for field in ("username", "password", "password_confirm"):
        assert isinstance(data[field], list)
        assert data[field]
        assert all(isinstance(message, str) for message in data[field])
    assert get_user_model().objects.count() == 0
    assert Token.objects.count() == 0


def test_register_rejects_malformed_json(client):
    response = client.post(
        REGISTER_URL,
        data='{"username": ',
        content_type="application/json",
    )

    assert response.status_code == 400
    assert get_user_model().objects.count() == 0
    assert Token.objects.count() == 0


def test_register_is_public_without_authentication(client):
    username = "public-registration-user"
    password = "fake-public-password"

    response = client.post(
        REGISTER_URL,
        data=json.dumps(
            {
                "username": username,
                "password": password,
                "password_confirm": password,
            }
        ),
        content_type="application/json",
        HTTP_AUTHORIZATION="",
    )

    assert response.wsgi_request.META.get("HTTP_AUTHORIZATION") == ""
    assert response.status_code == 201
    assert get_user_model().objects.filter(username=username).exists()


def test_register_get_returns_405(client):
    response = client.get(REGISTER_URL)

    assert response.status_code == 405


def test_register_success_response_does_not_include_sensitive_data(client):
    other_user = get_user_model().objects.create_user(
        username="other-token-owner",
        password="fake-other-token-owner-password",
    )
    other_token = Token.objects.create(user=other_user)
    username = "safe-success-user"
    password = "fake-safe-success-password"

    response = register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    body = response.content.decode()
    user = get_user_model().objects.get(username=username)
    assert response.status_code == 201
    assert password not in body
    assert user.password not in body
    assert other_token.key not in body
    assert set(response.json()["user"]) == {"id", "username"}


def test_register_error_response_does_not_include_sensitive_data(client):
    other_user = get_user_model().objects.create_user(
        username="error-other-token-owner",
        password="fake-error-other-password",
    )
    other_token = Token.objects.create(user=other_user)
    username = "safe-error-user"
    password = "fake-safe-error-password"
    password_confirm = "fake-safe-error-confirmation"

    response = register(
        client,
        username=username,
        password=password,
        password_confirm=password_confirm,
    )

    body = response.content.decode()
    data = response.json()
    assert response.status_code == 400
    assert "password_confirm" in data
    assert "token" not in data
    assert password not in body
    assert password_confirm not in body
    assert other_user.password not in body
    assert other_token.key not in body
    assert get_user_model().objects.filter(username=username).count() == 0
    assert Token.objects.filter(user=other_user).count() == 1
