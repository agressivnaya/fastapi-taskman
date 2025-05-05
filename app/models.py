
"""
app/models.py: Модели базы данных (User, Project, Task).
"""

from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User model."""
    user_id: int = Field(default=None, primary_key=True)
    email: str
    password: str
    name: str
    skill_level: int = Field(default=1)
    workload: int = Field(default=0)

class Project(SQLModel, table=True):
    """Project model."""
    project_id: int = Field(default=None, primary_key=True)
    project_name: str
    project_description: str | None = None

class Task(SQLModel, table=True):
    """Task model."""
    task_id: int = Field(default=None, primary_key=True)
    task_description: str
    difficulty: int = Field(default=1)
    due_date: date
    is_assigned: bool = Field(default=False)
    assignee: Optional[int] = Field(default=None, foreign_key="user.user_id")
    project: Optional[int] = Field(default=None, foreign_key="project.project_id")
