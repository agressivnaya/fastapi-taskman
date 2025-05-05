from fastapi.testclient import TestClient
from datetime import date, timedelta
from app.main import app

client = TestClient(app)

def test_create_task():
    # Создание проекта для задачи
    project_resp = client.post("/projects/", json={
        "project_name": "Учебный проект",
        "project_description": "Описание проекта"
    })
    assert project_resp.status_code == 200
    project_id = project_resp.json()["project_id"]

    # Добавление задачи
    response = client.post("/v2/tasks/", json={
        "task_description": "Тестовая задача",
        "assignee": 1,
        "due_date": str(date.today() + timedelta(days=2)),
        "project": project_id
    })

    assert response.status_code == 201
    assert "task_id" in response.json()
    assert response.json()["task_description"] == "Тестовая задача"

    assert response.status_code == 200
    data = response.json()
    assert data["task_description"] == "Автоназначенная задача"
    assert data["is_assigned"] is True
    assert data["assignee"] is not None

def test_read_all_tasks():
    response = client.get("/v2/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert any(task["task_description"] == "Автоназначенная задача" for task in tasks)

def test_read_task_by_id():
    response = client.get(f"/v2/tasks/{client.task_id}")
    assert response.status_code == 200
    task = response.json()
    assert task["task_id"] == client.task_id
    assert task["task_description"] == "Автоназначенная задача"

def test_update_task():
    update_data = {"task_description": "Обновлённая задача"}
    response = client.patch(f"/v2/tasks/{client.task_id}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["task_description"] == "Обновлённая задача"

def test_delete_task():
    response = client.delete(f"/v2/tasks/{client.task_id}")
    assert response.status_code == 204 or response.status_code == 200
