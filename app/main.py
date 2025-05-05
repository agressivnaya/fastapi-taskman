from contextlib import \
    asynccontextmanager  # Uncomment if you need to create tables on app start >>>

from fastapi import FastAPI

from app.db import init_database
from app.routes import (assign, async_routes, auth, project, task, task_v2,
                        utils)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan context manager."""
    init_database()
    yield                                   # <<< Uncomment if you need to create tables on app start

"""
app/main.py: Точка входа FastAPI приложения.
"""
app = FastAPI(
    lifespan=lifespan,  # Uncomment if you need to create tables on app start
    title="Система управления задачами",
    description="Простейшая система управления задачами, основанная на "
                "фреймворке FastAPI.",
    version="0.0.1",
    contact={
        "name": "Цифровая кафедра МФТИ",
        "url": "https://mipt.ru",
        "email": "digitaldepartments@mipt.ru",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

app.include_router(task.router)
app.include_router(task_v2.router)
app.include_router(utils.router)
app.include_router(async_routes.router)
app.include_router(auth.router)
app.include_router(project.router)
app.include_router(assign.router)

