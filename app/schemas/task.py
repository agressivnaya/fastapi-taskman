"""
app/schemas/task.py: Схемы Pydantic для Task, User, Project.
"""

from datetime import date, timedelta
from typing import Annotated, Optional, TypeAlias

from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field
from pydantic_settings import SettingsConfigDict
from sqlalchemy import UniqueConstraint
from sqlmodel import Field as SQLField
from sqlmodel import SQLModel


def _empty_str_or_none(value: str | None) -> None:
    if value is None or value == "":
        return None
    raise ValueError("Expected empty value")


EmptyStrOrNone: TypeAlias = Annotated[None, BeforeValidator(_empty_str_or_none)]


class TaskCreate(BaseModel):
    """Schema to create a task."""
    task_description: str = Field(
        description="Описание задачи",
        max_length=300
    )
    assignee: int
    due_date: Optional[date] = Field(
        description="Крайний срок исполнения задачи. "
                    "Не допускаются даты, более ранние, "
                    "чем сегодняшняя.",
        gt=date.today() - timedelta(days=1),
        default_factory=lambda: date.today() + timedelta(days=1)
    )

class ProjectCreate(BaseModel):
    """Schema to create a project."""
    project_name: str
    project_description: str | None = None

class ProjectRead(ProjectCreate):
    """Schema to read project info."""
    project_id: int

    model_config = ConfigDict(from_attributes=True)


class TaskRead(BaseModel):
    """Schema to read task info."""
    task_id: int
    task_description: str
    due_date: date
    difficulty: int
    is_assigned: bool
    assignee: Optional[int] = None
    project: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)



class UserCreate(BaseModel):
    """Schema to register a user."""
    name: str
    email: EmailStr
    password: str
    skill_level: int = Field(ge=1, le=5, default=1)
    workload: int = 0

class UserRead(BaseModel):
    """Schema to read user info."""
    user_id: int
    name: str
    email: EmailStr
    skill_level: int
    workload: int

    model_config = ConfigDict(from_attributes=True)

class UserCrendentials(BaseModel):
    """Schema for login credentials."""
    email: EmailStr
    password: str

    model_config = SettingsConfigDict(
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "querty"
            }
        })

class TaskAutoAssign(BaseModel):
    """Schema for auto-assigning a task."""
    task_description: str
    difficulty: int
    due_date: date
    project: Optional[int] = None