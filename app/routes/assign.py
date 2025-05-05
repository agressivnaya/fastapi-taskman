from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_async_session
from app.models import Task, User
from app.schemas.task import TaskAutoAssign, TaskRead

router = APIRouter(prefix="/auto", tags=["Управление задачами в БД"])

@router.post("/assign", response_model=TaskRead)
async def assign_task_auto(
    task_data: TaskAutoAssign,
    session: AsyncSession = Depends(get_async_session)
):
    # Найдём подходящих пользователей
    result = await session.execute(
        select(User).where(User.skill_level >= task_data.difficulty)
    )
    candidates = result.scalars().all()

    if not candidates:
        raise HTTPException(status_code=404, detail="Нет подходящих исполнителей")

    # Назначим того, у кого меньше workload
    assignee = min(candidates, key=lambda u: u.workload)

    # Создаём задачу
    task = Task(
        task_description=task_data.task_description,
        difficulty=task_data.difficulty,
        due_date=task_data.due_date,
        project=task_data.project,
        is_assigned=True,
        assignee=assignee.user_id
    )
    session.add(task)

    # Обновляем workload
    assignee.workload += task_data.difficulty
    session.add(assignee)
    await session.commit()
    await session.refresh(task)

    return task
