import json


def test_health_returns_ok_json(client):
    response = client.get("/api/v1/health/")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("application/json")
    assert json.loads(response.content) == {"status": "ok"}


def test_health_does_not_require_authentication(client):
    response = client.get("/api/v1/health/")

    assert response.status_code == 200
