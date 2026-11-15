import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

pytestmark = pytest.mark.django_db

REGISTER_URL = "/api/v1/auth/register/"
LOGIN_URL = "/api/v1/auth/login/"
LOGOUT_URL = "/api/v1/auth/logout/"
ME_URL = "/api/v1/auth/me/"


def register(client, **payload):
    return client.post(
        REGISTER_URL,
        data=json.dumps(payload),
        content_type="application/json",
    )


def login(client, **payload):
    return client.post(
        LOGIN_URL,
        data=json.dumps(payload),
        content_type="application/json",
    )


def token_header(token):
    return f"Token {token}"


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


def test_login_returns_200_with_registration_response_shape(client):
    username = "login-shape-user"
    password = "fake-login-password"
    register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    response = login(client, username=username, password=password)

    assert response.status_code == 200
    data = response.json()
    assert set(data) == {"token", "user"}
    assert set(data["user"]) == {"id", "username"}
    assert isinstance(data["token"], str)
    assert data["token"]
    assert isinstance(data["user"]["id"], int)
    assert data["user"]["username"] == username
    user = get_user_model().objects.get(username=username)
    assert data["user"]["id"] == user.pk


def test_login_token_authenticates_me(client):
    username = "login-me-user"
    password = "fake-login-me-password"
    register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    response = login(client, username=username, password=password)
    token = response.json()["token"]

    me_response = client.get(ME_URL, HTTP_AUTHORIZATION=token_header(token))

    assert me_response.status_code == 200
    assert me_response.json() == {
        "id": get_user_model().objects.get(username=username).pk,
        "username": username,
    }


def test_login_is_public_without_authorization_header(client):
    username = "login-public-user"
    password = "fake-login-public-password"
    register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    response = client.post(
        LOGIN_URL,
        data=json.dumps({"username": username, "password": password}),
        content_type="application/json",
        HTTP_AUTHORIZATION="",
    )

    assert response.wsgi_request.META.get("HTTP_AUTHORIZATION") == ""
    assert response.status_code == 200
    assert response.json()["token"]


@pytest.mark.parametrize(
    "header",
    ["Token stale-token-value", "Bearer stale-token-value", "Token", "garbage"],
)
def test_login_ignores_invalid_or_stale_token_header(client, header):
    username = "login-stale-header-user"
    password = "fake-login-stale-password"
    register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    response = client.post(
        LOGIN_URL,
        data=json.dumps({"username": username, "password": password}),
        content_type="application/json",
        HTTP_AUTHORIZATION=header,
    )

    assert response.status_code == 200
    assert response.json()["token"]


def test_login_reuses_registration_token(client):
    username = "login-reuse-user"
    password = "fake-login-reuse-password"
    register_response = register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )
    registration_token = register_response.json()["token"]

    login_response = login(client, username=username, password=password)

    user = get_user_model().objects.get(username=username)
    assert login_response.status_code == 200
    assert login_response.json()["token"] == registration_token
    assert Token.objects.filter(user=user).count() == 1


def test_two_logins_return_same_token_and_leave_one_row(client):
    username = "login-twice-user"
    password = "fake-login-twice-password"
    register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    first_response = login(client, username=username, password=password)
    second_response = login(client, username=username, password=password)

    user = get_user_model().objects.get(username=username)
    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.json()["token"] == second_response.json()["token"]
    assert Token.objects.filter(user=user).count() == 1


def test_login_after_logout_returns_new_token(client):
    username = "login-after-logout-user"
    password = "fake-login-after-logout-password"
    register_response = register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )
    revoked_token = register_response.json()["token"]

    logout_response = client.post(
        LOGOUT_URL,
        HTTP_AUTHORIZATION=token_header(revoked_token),
    )
    assert logout_response.status_code == 204
    assert Token.objects.filter(user__username=username).count() == 0

    login_response = login(client, username=username, password=password)
    new_token = login_response.json()["token"]

    assert login_response.status_code == 200
    assert new_token
    assert new_token != revoked_token
    assert Token.objects.filter(user__username=username).count() == 1

    me_response = client.get(ME_URL, HTTP_AUTHORIZATION=token_header(new_token))
    assert me_response.status_code == 200


def test_login_wrong_password_returns_generic_400(client):
    username = "login-wrong-password-user"
    password = "fake-login-correct-password"
    register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )
    user = get_user_model().objects.get(username=username)
    existing_token = Token.objects.get(user=user)

    response = login(
        client,
        username=username,
        password="fake-login-wrong-password",
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password."}
    assert Token.objects.filter(user=user).count() == 1
    assert Token.objects.get(user=user).key == existing_token.key


def test_login_unknown_username_returns_generic_400(client):
    existing_user = get_user_model().objects.create_user(
        username="login-existing-other-user",
        password="fake-login-existing-password",
    )
    existing_token = Token.objects.create(user=existing_user)

    response = login(
        client,
        username="login-unknown-user",
        password="fake-login-unknown-password",
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password."}
    assert get_user_model().objects.filter(username="login-unknown-user").count() == 0
    assert Token.objects.count() == 1
    assert Token.objects.get().key == existing_token.key


def test_login_failures_share_generic_body_without_leaking(client):
    username = "login-generic-existing-user"
    password = "fake-login-generic-password"
    wrong_password = "fake-login-generic-wrong"
    unknown_username = "login-generic-missing-user"
    register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    wrong_password_response = login(
        client,
        username=username,
        password=wrong_password,
    )
    unknown_username_response = login(
        client,
        username=unknown_username,
        password=password,
    )

    assert wrong_password_response.status_code == 400
    assert unknown_username_response.status_code == 400
    assert wrong_password_response.json() == unknown_username_response.json()
    assert wrong_password_response.json() == {
        "detail": "Invalid username or password."
    }
    body = wrong_password_response.content.decode()
    assert username not in body
    assert unknown_username not in body
    assert password not in body
    assert wrong_password not in body


@pytest.mark.parametrize("username", [None, "", "   "])
def test_login_rejects_missing_or_blank_username(client, username):
    payload = {"password": "fake-login-blank-username-password"}
    if username is not None:
        payload["username"] = username

    response = login(client, **payload)

    assert_field_error(response, "username")
    assert "token" not in response.json()
    assert get_user_model().objects.count() == 0
    assert Token.objects.count() == 0


@pytest.mark.parametrize("password", [None, ""])
def test_login_rejects_missing_or_empty_password(client, password):
    payload = {"username": "login-missing-password-user"}
    if password is not None:
        payload["password"] = password

    response = login(client, **payload)

    assert_field_error(response, "password")
    assert "token" not in response.json()
    assert get_user_model().objects.count() == 0
    assert Token.objects.count() == 0


def test_login_trims_username_but_not_password(client):
    username = "trimmed-login-user"
    password = "  fake-spaced-login-password  "
    register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    spaced_username_response = login(
        client,
        username=f"  {username}  ",
        password=password,
    )
    trimmed_password_response = login(
        client,
        username=username,
        password=password.strip(),
    )

    assert spaced_username_response.status_code == 200
    assert spaced_username_response.json()["user"]["username"] == username
    assert trimmed_password_response.status_code == 400
    assert trimmed_password_response.json() == {
        "detail": "Invalid username or password."
    }


def test_login_is_case_sensitive(client):
    username = "CaseSensitiveLoginUser"
    password = "fake-case-login-password"
    register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )
    user = get_user_model().objects.get(username=username)
    token = Token.objects.get(user=user)

    lowercase_response = login(
        client,
        username=username.lower(),
        password=password,
    )
    uppercase_response = login(
        client,
        username=username.upper(),
        password=password,
    )
    correct_response = login(client, username=username, password=password)

    assert lowercase_response.status_code == 400
    assert lowercase_response.json() == {
        "detail": "Invalid username or password."
    }
    assert uppercase_response.status_code == 400
    assert correct_response.status_code == 200
    assert Token.objects.filter(user=user).count() == 1
    assert Token.objects.get(user=user).key == token.key


def test_login_rejects_malformed_json(client):
    response = client.post(
        LOGIN_URL,
        data='{"username": ',
        content_type="application/json",
    )

    assert response.status_code == 400
    assert Token.objects.count() == 0


def test_logout_requires_authentication(client):
    response = client.post(LOGOUT_URL)

    assert response.status_code == 401
    assert response.status_code != 403


@pytest.mark.parametrize(
    "header",
    [
        "",
        "Token",
        "Token ",
        "Token too many parts",
        "Bearer valid-looking-token",
        "Token unknown-token-value",
    ],
)
def test_logout_rejects_missing_malformed_or_unknown_tokens(client, header):
    user = get_user_model().objects.create_user(
        username="logout-reject-user",
        password="fake-logout-reject-password",
    )
    token = Token.objects.create(user=user)

    response = client.post(LOGOUT_URL, HTTP_AUTHORIZATION=header)

    assert response.status_code == 401
    assert response.status_code != 403
    assert Token.objects.filter(user=user).count() == 1
    assert Token.objects.get(user=user).key == token.key


def test_logout_deletes_only_presented_token_and_returns_204(client):
    first_user = get_user_model().objects.create_user(
        username="logout-first-user",
        password="fake-logout-first-password",
    )
    second_user = get_user_model().objects.create_user(
        username="logout-second-user",
        password="fake-logout-second-password",
    )
    first_token = Token.objects.create(user=first_user)
    second_token = Token.objects.create(user=second_user)

    response = client.post(
        LOGOUT_URL,
        HTTP_AUTHORIZATION=token_header(first_token.key),
    )

    assert response.status_code == 204
    assert response.content == b""
    assert not Token.objects.filter(pk=first_token.pk).exists()
    assert Token.objects.filter(pk=second_token.pk).exists()
    assert get_user_model().objects.filter(pk=first_user.pk).exists()
    assert get_user_model().objects.filter(pk=second_user.pk).exists()


def test_second_logout_with_revoked_token_returns_401(client):
    user = get_user_model().objects.create_user(
        username="logout-revoked-user",
        password="fake-logout-revoked-password",
    )
    token = Token.objects.create(user=user)

    first_response = client.post(
        LOGOUT_URL,
        HTTP_AUTHORIZATION=token_header(token.key),
    )
    second_response = client.post(
        LOGOUT_URL,
        HTTP_AUTHORIZATION=token_header(token.key),
    )

    assert first_response.status_code == 204
    assert second_response.status_code == 401
    assert second_response.status_code != 403
    assert not Token.objects.filter(pk=token.pk).exists()


def test_revoked_token_is_rejected_by_me(client):
    user = get_user_model().objects.create_user(
        username="logout-me-revoked-user",
        password="fake-logout-me-revoked-password",
    )
    token = Token.objects.create(user=user)

    logout_response = client.post(
        LOGOUT_URL,
        HTTP_AUTHORIZATION=token_header(token.key),
    )
    me_response = client.get(
        ME_URL,
        HTTP_AUTHORIZATION=token_header(token.key),
    )

    assert logout_response.status_code == 204
    assert me_response.status_code == 401
    assert me_response.status_code != 403


def test_me_returns_exact_user_shape(client):
    user = get_user_model().objects.create_user(
        username="me-shape-user",
        password="fake-me-shape-password",
    )
    token = Token.objects.create(user=user)

    response = client.get(ME_URL, HTTP_AUTHORIZATION=token_header(token.key))

    assert response.status_code == 200
    assert response.json() == {"id": user.pk, "username": user.username}
    assert set(response.json()) == {"id", "username"}


def test_me_requires_authentication(client):
    response = client.get(ME_URL)

    assert response.status_code == 401
    assert response.status_code != 403


@pytest.mark.parametrize(
    "header",
    [
        "",
        "Token",
        "Token ",
        "Token too many parts",
        "Bearer valid-looking-token",
        "Token unknown-token-value",
    ],
)
def test_me_rejects_missing_malformed_or_unknown_tokens(client, header):
    user = get_user_model().objects.create_user(
        username="me-reject-user",
        password="fake-me-reject-password",
    )
    token = Token.objects.create(user=user)

    response = client.get(ME_URL, HTTP_AUTHORIZATION=header)

    assert response.status_code == 401
    assert response.status_code != 403
    body = response.content.decode()
    assert token.key not in body
    assert user.password not in body
    assert user.username not in body


def test_protected_auth_endpoints_return_401_not_403(client):
    for header in ("", "Bearer abc", "Token", "Token unknown-token-value"):
        logout_response = client.post(LOGOUT_URL, HTTP_AUTHORIZATION=header)
        me_response = client.get(ME_URL, HTTP_AUTHORIZATION=header)

        assert logout_response.status_code == 401
        assert logout_response.status_code != 403
        assert me_response.status_code == 401
        assert me_response.status_code != 403


@pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
def test_login_unsupported_methods_return_405(client, method):
    user = get_user_model().objects.create_user(
        username="login-methods-user",
        password="fake-login-methods-password",
    )
    token = Token.objects.create(user=user)

    response = getattr(client, method)(
        LOGIN_URL,
        HTTP_AUTHORIZATION=token_header(token.key),
    )

    assert response.status_code == 405


@pytest.mark.parametrize("method", ["get", "put", "patch", "delete"])
def test_logout_unsupported_methods_return_405_with_valid_auth(client, method):
    user = get_user_model().objects.create_user(
        username="logout-methods-user",
        password="fake-logout-methods-password",
    )
    token = Token.objects.create(user=user)

    response = getattr(client, method)(
        LOGOUT_URL,
        HTTP_AUTHORIZATION=token_header(token.key),
    )

    assert response.status_code == 405
    assert Token.objects.filter(pk=token.pk).exists()


@pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
def test_me_unsupported_methods_return_405_with_valid_auth(client, method):
    user = get_user_model().objects.create_user(
        username="me-methods-user",
        password="fake-me-methods-password",
    )
    token = Token.objects.create(user=user)

    response = getattr(client, method)(
        ME_URL,
        HTTP_AUTHORIZATION=token_header(token.key),
    )

    assert response.status_code == 405


def test_login_success_response_does_not_include_sensitive_data(client):
    other_user = get_user_model().objects.create_user(
        username="login-other-token-owner",
        password="fake-login-other-password",
    )
    other_token = Token.objects.create(user=other_user)
    username = "login-safe-success-user"
    password = "fake-login-safe-success-password"
    register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    response = login(client, username=username, password=password)

    body = response.content.decode()
    user = get_user_model().objects.get(username=username)
    assert response.status_code == 200
    assert password not in body
    assert user.password not in body
    assert other_token.key not in body
    assert set(response.json()) == {"token", "user"}
    assert set(response.json()["user"]) == {"id", "username"}


def test_login_error_response_does_not_include_sensitive_data(client):
    other_user = get_user_model().objects.create_user(
        username="login-error-other-token-owner",
        password="fake-login-error-other-password",
    )
    other_token = Token.objects.create(user=other_user)
    username = "login-error-safe-user"
    password = "fake-login-error-safe-password"
    wrong_password = "fake-login-error-wrong-password"
    register(
        client,
        username=username,
        password=password,
        password_confirm=password,
    )

    response = login(client, username=username, password=wrong_password)

    body = response.content.decode()
    data = response.json()
    assert response.status_code == 400
    assert set(data) == {"detail"}
    assert "token" not in data
    assert username not in body
    assert password not in body
    assert wrong_password not in body
    assert other_token.key not in body


def test_me_response_does_not_include_sensitive_data(client):
    other_user = get_user_model().objects.create_user(
        username="me-other-token-owner",
        password="fake-me-other-password",
    )
    other_token = Token.objects.create(user=other_user)
    user = get_user_model().objects.create_user(
        username="me-safe-user",
        password="fake-me-safe-password",
    )
    token = Token.objects.create(user=user)

    response = client.get(ME_URL, HTTP_AUTHORIZATION=token_header(token.key))

    body = response.content.decode()
    assert response.status_code == 200
    assert token.key not in body
    assert user.password not in body
    assert other_token.key not in body
    assert set(response.json()) == {"id", "username"}
