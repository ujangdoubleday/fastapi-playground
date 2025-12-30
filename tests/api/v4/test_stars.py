from fastapi.testclient import TestClient

def test_create_star(client: TestClient):
    data = {
        "name": "Sun",
        "description": "Our star",
        "galaxy": "Milky Way",
        "system": "Solar System",
    }
    response = client.post(
        "/api/v4/stars/", json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["galaxy"] == data["galaxy"]
    assert content["system"] == data["system"]
    assert "id" in content

def test_read_stars(client: TestClient):
    response = client.get("/api/v4/stars/")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)

def test_read_star(client: TestClient):
    # First create a star
    data = {
        "name": "Alpha Centauri",
        "description": "Nearest star system",
        "galaxy": "Milky Way",
        "system": "Alpha Centauri",
    }
    create_response = client.post(
        "/api/v4/stars/", json=data,
    )
    star_id = create_response.json()["id"]

    # Then read it
    response = client.get(f"/api/v4/stars/{star_id}")
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]

def test_update_star(client: TestClient):
    # First create a star
    data = {
        "name": "Betelgeuse",
        "description": "Red supergiant",
        "galaxy": "Milky Way",
        "system": "Orion",
    }
    create_response = client.post(
        "/api/v4/stars/", json=data,
    )
    star_id = create_response.json()["id"]

    # Then update it
    update_data = {"description": "Updated description"}
    response = client.put(
        f"/api/v4/stars/{star_id}", json=update_data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["description"] == update_data["description"]
    assert content["name"] == data["name"]

def test_delete_star(client: TestClient):
    # First create a star
    data = {
        "name": "Rigel",
        "description": "Blue supergiant",
        "galaxy": "Milky Way",
        "system": "Orion",
    }
    create_response = client.post(
        "/api/v4/stars/", json=data,
    )
    star_id = create_response.json()["id"]

    # Then delete it
    response = client.delete(f"/api/v4/stars/{star_id}")
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == star_id
    
    # Verify it's gone
    get_response = client.get(f"/api/v4/stars/{star_id}")
    assert get_response.status_code == 404
