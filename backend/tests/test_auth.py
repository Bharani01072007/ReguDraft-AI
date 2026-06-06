import pytest
from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    payload = {
        "email": "testwriter@regudraft.com",
        "password": "securepassword123",
        "role": "WRITER"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testwriter@regudraft.com"
    assert data["role"] == "WRITER"
    assert "id" in data

def test_register_duplicate_email(client: TestClient):
    payload = {
        "email": "testwriter@regudraft.com",
        "password": "securepassword123",
        "role": "WRITER"
    }
    # Register first time (201)
    response_first = client.post("/api/v1/auth/register", json=payload)
    assert response_first.status_code == 201
    
    # Second register should fail (400)
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_login_user(client: TestClient):
    # Register the user first
    payload = {
        "email": "testwriter@regudraft.com",
        "password": "securepassword123",
        "role": "WRITER"
    }
    client.post("/api/v1/auth/register", json=payload)

    # Form data format for OAuth2 Password Form flow
    login_data = {
        "username": "testwriter@regudraft.com",
        "password": "securepassword123"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "testwriter@regudraft.com"

def test_login_invalid_credentials(client: TestClient):
    # Register user first
    payload = {
        "email": "testwriter@regudraft.com",
        "password": "securepassword123",
        "role": "WRITER"
    }
    client.post("/api/v1/auth/register", json=payload)

    login_data = {
        "username": "testwriter@regudraft.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 400
    assert "Incorrect email or password" in response.json()["detail"]
