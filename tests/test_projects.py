from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Заглушка проекта
test_project_data = {
    "project_name": "Тестовый проект",
    "project_description": "Описание тестового проекта"
}

project_id = 0

def test_create_project():
    global project_id
    response = client.post("/projects/", json=test_project_data)
    assert response.status_code == 200
    result = response.json()
    assert result["project_name"] == test_project_data["project_name"]
    project_id = result["project_id"]

def test_read_projects():
    response = client.get("/projects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_project_by_id():
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["project_id"] == project_id

def test_get_project_not_found():
    response = client.get("/projects/99999")
    assert response.status_code == 404

def test_delete_project():
    response = client.delete(f"/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True

def test_delete_project_not_found():
    response = client.delete("/projects/99999")
    assert response.status_code == 404
