from fastapi.testclient import TestClient

def test_signup(client: TestClient):
    response = client.post(
        "/api/v2/auth/signup",
        json={"email": "newuser@example.com", "password": "newpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data

def test_signup_duplicate_email(client: TestClient):
    # first signup
    client.post(
        "/api/v2/auth/signup",
        json={"email": "duplicate@example.com", "password": "password"},
    )
    # second signup (should fail)
    response = client.post(
        "/api/v2/auth/signup",
        json={"email": "duplicate@example.com", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "The user with this email already exists in the system"

def test_login(client: TestClient):
    # signup first
    email = "login_test@example.com"
    password = "login_password"
    client.post(
        "/api/v2/auth/signup",
        json={"email": email, "password": password},
    )
    
    # login
    response = client.post(
        "/api/v2/auth/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/api/v2/auth/login",
        data={"username": "wrong@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
