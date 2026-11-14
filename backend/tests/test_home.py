def test_home_returns_http_200(client):
    response = client.get("/")

    assert response.status_code == 200
