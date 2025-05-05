from fastapi.testclient import TestClient
from app.main import app
from datetime import date, timedelta
from app.db import get_session
from app.models import User, Task
from sqlmodel import Session

client = TestClient(app)


def test_assign_task_success():
    # Добавляем пользователя с подходящим уровнем навыков
    with Session(get_session()) as session:
        user = User(name="Executor", email="exec@example.com",
                    password="hashedpass", skill_level=3, workload=0)
        session.add(user)
        session.commit()
        session.refresh(user)

        # Добавляем проект
        session.execute("INSERT INTO project (project_id, project_name) VALUES (1, 'Test Project')")
        session.commit()

    response = client.post("/auto/assign", json={
        "task_description": "Auto Assign Task",
        "difficulty": 2,
        "due_date": str(date.today() + timedelta(days=1)),
        "project": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["is_assigned"] is True
    assert data["assignee"] == user.user_id


def test_assign_task_no_candidates():
    # Удалим всех пользователей с нужным уровнем
    with Session(get_session()) as session:
        session.exec("DELETE FROM user")
        session.commit()

    response = client.post("/auto/assign", json={
        "task_description": "Impossible Task",
        "difficulty": 10,
        "due_date": str(date.today() + timedelta(days=1)),
        "project": 1
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Нет подходящих исполнителей"
