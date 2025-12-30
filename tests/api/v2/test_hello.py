from fastapi.testclient import TestClient

def test_hello_no_auth(client: TestClient):
    response = client.get("/api/v2/hello/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_hello_success(client: TestClient, test_user_token: str):
    response = client.get(
        "/api/v2/hello/",
        headers={"Authorization": f"Bearer {test_user_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello World"
    assert data["user"] == "testuser@example.com"
