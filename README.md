# FastAPI Task Manager

## 📌 Описание

Система управления задачами (Task Manager) с авторизацией, REST API и возможностью хранения задач в БД и CSV-файле. Реализована на FastAPI с использованием SQLModel и JWT-аутентификации. Поддерживается автоматическое назначение задач пользователям на основе их загруженности и уровня навыков.

---

## ⚙️ Стек технологий

- Python 3.11
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- SQLite
- Pydantic v2
- Uvicorn
- Pytest + Coverage
- Faker
- Pylint + Pydocstyle

---

## 🚀 Запуск проекта

1. **Клонировать репозиторий**
   ```bash
   git clone <your-repo-url>
   cd fastapi-taskman

2. **Создать виртуальное окружение и активировать его**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # или .venv\Scripts\activate в Windows
   
3. **Установить зависимости**
    ```bash
    pip install -r requirements.txt

4. **Запустить сервер**
    ```bash
    uvicorn app.main:app --reload

5. **Открыть документацию**
http://127.0.0.1:8000/docs

🔐 Аутентификация
JWT-авторизация:

Регистрация: POST /auth/signup

Вход: POST /auth/login

Текущий пользователь: GET /auth/me

📦 REST API
Задачи (из базы данных) /v2/tasks
GET /v2/tasks/

POST /v2/tasks/

PATCH /v2/tasks/{task_id}

DELETE /v2/tasks/{task_id}

Задачи (из CSV-файла) /v1/tasks
GET /v1/tasks/

POST /v1/tasks/

PATCH /v1/tasks/{task_id}

GET /v1/tasks/{task_id}

Проекты /projects
GET /projects/

POST /projects/

GET /projects/{project_id}

DELETE /projects/{project_id}

Пользователи /utils/me
GET /utils/me — получить текущего пользователя

⚙️ Автоматическое распределение задач
POST /auto/assign
Создает задачу и назначает её подходящему пользователю (по уровню навыков и загрузке).

🧪 Тестирование
Запуск тестов:
    ```bash
    pytest

Покрытие кода:
    ```bash
    pytest --cov=app > coverage.txt

Проверка качества кода:
    ```bash
    pylint app > pylint.txt
    pydocstyle app > pydocstyle.txt

👩‍💻 Автор
Irina Shiferson, 2025