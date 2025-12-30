from fastapi.testclient import TestClient

def test_create_todo(client: TestClient):
    response = client.post(
        "/api/v1/todos/",
        json={"title": "Test Todo", "description": "Do testing"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["completed"] is False
    assert "id" in data

def test_read_todos(client: TestClient):
    response = client.get("/api/v1/todos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_todo(client: TestClient):
    create_response = client.post(
        "/api/v1/todos/",
        json={"title": "Read Me", "completed": False},
    )
    todo_id = create_response.json()["id"]

    response = client.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Read Me"

def test_update_todo(client: TestClient):
    create_response = client.post(
        "/api/v1/todos/",
        json={"title": "Update Me", "completed": False},
    )
    todo_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/todos/{todo_id}",
        json={"title": "Updated", "completed": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["completed"] is True

def test_delete_todo(client: TestClient):
    create_response = client.post(
        "/api/v1/todos/",
        json={"title": "Delete Me", "completed": False},
    )
    todo_id = create_response.json()["id"]

    # delete
    response = client.delete(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    
    # verify deletion
    get_response = client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 404
