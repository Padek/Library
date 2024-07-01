from fastapi.testclient import TestClient
from library.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", params={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"

def test_register_existing_user():
    client.post("/auth/register", params={"username": "testuser", "password": "testpassword"})
    response = client.post("/auth/register", params={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_login_user():
    client.post("/auth/register", params={"username": "testuser", "password": "testpassword"})
    response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_user():
    response = client.post("/auth/token", data={"username": "invaliduser", "password": "invalidpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"