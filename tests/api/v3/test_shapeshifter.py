from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings

def test_create_item_json(client: TestClient, db: Session) -> None:
    data = {"title": "Foo", "description": "Bar", "price": 10.5, "is_offer": True}
    response = client.post("/api/v3/shapeshifter/json/items/", json=data)
    assert response.status_code == 201
    content = response.json()
    assert content["title"] == data["title"]
    assert content["id"] is not None

def test_read_items_json(client: TestClient, db: Session) -> None:
    response = client.get("/api/v3/shapeshifter/json/items/")
    assert response.status_code == 200
    content = response.json()
    assert isinstance(content, list)

def test_read_item_json(client: TestClient, db: Session) -> None:
    # create item first
    data = {"title": "Foo", "description": "Bar", "price": 10.5, "is_offer": True}
    create_res = client.post("/api/v3/shapeshifter/json/items/", json=data)
    item_id = create_res.json()["id"]

    response = client.get(f"/api/v3/shapeshifter/json/items/{item_id}")
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == "Foo"
    assert content["id"] == item_id

def test_update_item_json(client: TestClient, db: Session) -> None:
    # create item first
    data = {"title": "Foo", "description": "Bar", "price": 10.5, "is_offer": True}
    create_res = client.post("/api/v3/shapeshifter/json/items/", json=data)
    item_id = create_res.json()["id"]

    update_data = {"title": "Updated Foo", "description": "Updated Bar", "price": 20.0, "is_offer": False}
    response = client.put(f"/api/v3/shapeshifter/json/items/{item_id}", json=update_data)
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == "Updated Foo"
    assert content["price"] == 20.0

def test_delete_item_json(client: TestClient, db: Session) -> None:
    # create item first
    data = {"title": "Foo", "description": "Bar", "price": 10.5, "is_offer": True}
    create_res = client.post("/api/v3/shapeshifter/json/items/", json=data)
    item_id = create_res.json()["id"]

    response = client.delete(f"/api/v3/shapeshifter/json/items/{item_id}")
    assert response.status_code == 200
    
    # verify deletion
    get_response = client.get(f"/api/v3/shapeshifter/json/items/{item_id}")
    assert get_response.status_code == 404

# --- XML Tests ---

def test_create_item_xml(client: TestClient, db: Session) -> None:
    data = {"title": "XML Item", "description": "XML Desc", "price": 100.0, "is_offer": False}
    response = client.post("/api/v3/shapeshifter/xml/items/", json=data)
    assert response.status_code == 201
    assert response.headers["content-type"] == "application/xml"
    assert "<Title>XML Item</Title>" in response.text
    assert "<Price>100.0</Price>" in response.text

def test_read_items_xml(client: TestClient, db: Session) -> None:
    response = client.get("/api/v3/shapeshifter/xml/items/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml"
    assert "<Items>" in response.text

def test_read_item_xml(client: TestClient, db: Session) -> None:
    # use JSON endpoint to create easily, then read with XML
    data = {"title": "XML Read", "description": "Desc", "price": 50.0}
    create_res = client.post("/api/v3/shapeshifter/json/items/", json=data)
    item_id = create_res.json()["id"]

    response = client.get(f"/api/v3/shapeshifter/xml/items/{item_id}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml"
    assert "<Title>XML Read</Title>" in response.text
    assert f"<ID>{item_id}</ID>" in response.text

def test_update_item_xml(client: TestClient, db: Session) -> None:
    # create
    data = {"title": "XML Update", "description": "Desc", "price": 50.0}
    create_res = client.post("/api/v3/shapeshifter/json/items/", json=data)
    item_id = create_res.json()["id"]

    # update
    update_data = {"title": "XML Updated", "description": "New Desc", "price": 60.0, "is_offer": True}
    response = client.put(f"/api/v3/shapeshifter/xml/items/{item_id}", json=update_data)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml"
    assert "<Title>XML Updated</Title>" in response.text

def test_delete_item_xml(client: TestClient, db: Session) -> None:
    # create
    data = {"title": "XML Delete", "description": "Desc", "price": 50.0}
    create_res = client.post("/api/v3/shapeshifter/json/items/", json=data)
    item_id = create_res.json()["id"]

    # delete
    response = client.delete(f"/api/v3/shapeshifter/xml/items/{item_id}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/xml"
    assert "<Message>Item deleted successfully</Message>" in response.text
    
    # verify
    get_response = client.get(f"/api/v3/shapeshifter/xml/items/{item_id}")
    assert get_response.status_code == 404
