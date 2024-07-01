from fastapi.testclient import TestClient
from library.main import app

client = TestClient(app)

def test_create_book():
    response = client.post("/auth/register", params={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    book_data = {"title": "Test Book", "author": "Test Author", "description": "Test Description"}
    response = client.post("/books", json=book_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

def test_get_all_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_book():
    response = client.post("/auth/register", params={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    book_data = {"title": "Test Book", "author": "Test Author", "description": "Test Description"}
    create_response = client.post("/books", json=book_data, headers=headers)
    assert create_response.status_code == 200
    book_id = create_response.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

def test_update_book():
    response = client.post("/auth/register", params={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    book_data = {"title": "Test Book", "author": "Test Author", "description": "Test Description"}
    create_response = client.post("/books", json=book_data, headers=headers)
    assert create_response.status_code == 200
    book_id = create_response.json()["id"]

    updated_book_data = {"title": "Updated Book", "author": "Updated Author", "description": "Updated Description"}
    response = client.put(f"/books/{book_id}", json=updated_book_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Book"

def test_delete_book():
    response = client.post("/auth/register", params={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    book_data = {"title": "Test Book", "author": "Test Author", "description": "Test Description"}
    create_response = client.post("/books", json=book_data, headers=headers)
    assert create_response.status_code == 200
    book_id = create_response.json()["id"]

    response = client.delete(f"/books/{book_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"