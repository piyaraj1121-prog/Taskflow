from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# =========================
# USER SCHEMAS
# =========================

class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


# =========================
# PROJECT SCHEMAS
# =========================

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# TASK SCHEMAS
# =========================

class TaskCreate(BaseModel):
    title: str
    priority: str = Field(
        default="medium",
        pattern="^(low|medium|high)$"
    )
    due_date: Optional[str] = None
    status: str = "todo"
    project_id: int

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")

        return value


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = Field(
        default=None,
        pattern="^(low|medium|high)$"
    )
    due_date: Optional[str] = None
    status: Optional[str] = None
    project_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def validate_title(
        cls,
        value: Optional[str]
    ) -> Optional[str]:
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")

        return value


class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    due_date: Optional[str] = None
    status: str
    project_id: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# STATISTICS SCHEMA
# =========================

class ProjectStatistics(BaseModel):
    project_id: int
    project_name: str
    task_count: int
    todo_count: int
    in_progress_count: int
    completed_count: int


# =========================
# QUICK ADD SCHEMA
# =========================

class QuickAddRequest(BaseModel):
    description: str
    project_id: int

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Description cannot be blank")

        return value