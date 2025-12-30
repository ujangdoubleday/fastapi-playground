from fastapi.testclient import TestClient

def test_create_item(client: TestClient):
    response = client.post(
        "/api/v1/items/",
        json={"title": "Test Item", "description": "This is a test item", "price": 10.5},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item"
    assert data["price"] == 10.5
    assert "id" in data

def test_read_items(client: TestClient):
    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_item(client: TestClient):
    # create item first
    create_response = client.post(
        "/api/v1/items/",
        json={"title": "Specific Item", "price": 5.0},
    )
    item_id = create_response.json()["id"]

    # Read item
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Specific Item"
    assert response.json()["id"] == item_id
