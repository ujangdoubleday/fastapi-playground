from fastapi.testclient import TestClient

def test_create_planet(client: TestClient):
    response = client.post(
        "/api/v4/milky-way/solar-system/mars",
        json={"name": "Mars", "description": "The Red Planet"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mars"
    assert data["galaxy"] == "milky-way"
    assert data["system"] == "solar-system"
    assert data["planet"] == "mars"
    assert "id" in data

def test_read_planet(client: TestClient):
    # create first
    client.post(
        "/api/v4/milky-way/solar-system/earth",
        json={"name": "Earth", "description": "Blue Marble"},
    )
    
    response = client.get("/api/v4/milky-way/solar-system/earth")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Earth"
    assert data["galaxy"] == "milky-way"

def test_update_planet(client: TestClient):
    # create first
    client.post(
        "/api/v4/milky-way/solar-system/jupiter",
        json={"name": "Jupiter", "description": "Gas Giant"},
    )
    
    response = client.put(
        "/api/v4/milky-way/solar-system/jupiter",
        json={"description": "Largest Planet"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Largest Planet"

def test_delete_planet(client: TestClient):
    # create first
    client.post(
        "/api/v4/milky-way/solar-system/pluto",
        json={"name": "Pluto", "description": "Dwarf Planet"},
    )
    
    response = client.delete("/api/v4/milky-way/solar-system/pluto")
    assert response.status_code == 200
    
    # verify deletion
    response = client.get("/api/v4/milky-way/solar-system/pluto")
    assert response.status_code == 404
