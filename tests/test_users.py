from fastapi.testclient import TestClient
from app.main import app
from app.models import User
from sqlmodel import Session
from app.db import get_session

client = TestClient(app)

def test_create_user():
    data = {
        "email": "testuser@example.com",
        "password": "securepassword",
        "name": "Test",
        "skill_level": 3,
        "workload": 0
    }
    response = client.post("/auth/signup", json=data)
    assert response.status_code == 201
    assert isinstance(response.json(), int)

def test_login_user():
    data = {
        "username": "testuser@example.com",
        "password": "securepassword"
    }
    response = client.post("/auth/login", data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_me_user():
    login_data = {
        "username": "testuser@example.com",
        "password": "securepassword"
    }
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"
