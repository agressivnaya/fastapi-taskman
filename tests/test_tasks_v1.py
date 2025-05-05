import os
from fastapi.testclient import TestClient
from app.main import app
from datetime import date, timedelta

client = TestClient(app)
test_task_id = None

def test_create_task_csv():
    global test_task_id
    response = client.post("/v1/tasks/", json={
        "task_description": "Тестовая задача",
        "assignee": 1,
        "due_date": (date.today() + timedelta(days=1)).isoformat()
    })
    assert response.status_code == 201
    data = response.json()
    assert data["task_description"] == "Тестовая задача"
    test_task_id = data["task_id"]

def test_read_tasks_csv():
    response = client.get("/v1/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_task_by_id_csv():
    response = client.get(f"/v1/tasks/{test_task_id}")
    assert response.status_code == 200
    assert response.json()["task_id"] == test_task_id

def test_update_task_by_id_csv():
    response = client.patch(f"/v1/tasks/{test_task_id}", json={
        "task_description": "Обновленная задача"
    })
    assert response.status_code == 200
    assert response.json()["task_description"] == "Обновленная задача"

def test_update_task_invalid_field():
    response = client.patch(f"/v1/tasks/{test_task_id}", json={
        "invalid_field": "value"
    })
    assert response.status_code == 400
