from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import Session, select

from app.db import get_async_session, get_session
from app.models import Task

from ..api_docs import request_examples
from ..schemas import task as schema_task

router = APIRouter(prefix="/v2/tasks", tags=["Управление задачами в БД"])

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schema_task.TaskRead,
             summary = 'Добавить задачу')
def create_task(task: Annotated[
                        schema_task.TaskCreate,
                        request_examples.example_create_task
                ],
                session: Session = Depends(get_session)):
    """
    Добавить задачу.
    """
    new_task = Task(
        task_description=task.task_description,
        assignee=task.assignee,
        due_date=task.due_date
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@router.get("/", status_code=status.HTTP_200_OK,
            response_model=List[schema_task.TaskRead])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    if tasks is None or len(tasks) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The task list is empty."
        )
    return tasks


@router.get("/{task_id}", response_model=schema_task.TaskRead)
def read_task_by_id(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Task).where(Task.task_id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    await session.delete(task)
    await session.commit()


@router.patch("/{task_id}", response_model=schema_task.TaskRead, summary="Обновить задачу")
async def update_task_by_id(
    task_id: int,
    data_for_update: dict,
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Task).where(Task.task_id == task_id))
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    # Обновляем только существующие поля
    allowed_fields = {"task_description", "due_date", "assignee", "difficulty", "project"}
    for field, value in data_for_update.items():
        if field in allowed_fields:
            setattr(task, field, value)

    await session.commit()
    await session.refresh(task)
    return task


