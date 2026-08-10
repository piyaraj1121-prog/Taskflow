from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import case, func

from .database import get_db
from .models import User, Project, Task

from .schemas import (
    UserCreate,
    UserResponse,
    ProjectCreate,
    ProjectResponse,
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    ProjectStatistics,
    QuickAddRequest,
)
router = APIRouter()
from .algorithms.search_sort import (
    insertion_sort,
    binary_search,
    linear_search,
)

from .ai.parser import build_prompt, mock_parse_task


# =========================
# USER ENDPOINTS
# =========================

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):

    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=422,
            detail="Email already exists"
        )

    user = User(
        name=user_data.name,
        email=user_data.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user



    # Convert SQLAlchemy objects into dictionaries
    records = [
        {
            "id": task.id,
            "title": task.title,
            "priority": task.priority,
            "priority_rank": {
                "low": 1,
                "medium": 2,
                "high": 3,
            }.get(task.priority, 2),
            "due_date": task.due_date,
            "status": task.status,
            "project_id": task.project_id,
        }
        for task in tasks
    ]

    if sort == "priority":
        insertion_sort(records, "priority_rank")

        return [
            {
                "id": record["id"],
                "title": record["title"],
                "priority": record["priority"],
                "due_date": record["due_date"],
                "status": record["status"],
                "project_id": record["project_id"],
            }
            for record in records
        ]

    raise HTTPException(
        status_code=400,
        detail="Supported sort option: priority"
    )
@router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db)
):

    owner = (
        db.query(User)
        .filter(User.id == project_data.owner_id)
        .first()
    )

    if not owner:
        raise HTTPException(
            status_code=422,
            detail="Owner user does not exist"
        )

    project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=project_data.owner_id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


@router.get(
    "/projects",
    response_model=list[ProjectResponse]
)
def list_projects(db: Session = Depends(get_db)):

    return db.query(Project).all()


# =========================
# TASK CREATE
# =========================

@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):

    project = (
        db.query(Project)
        .filter(Project.id == task_data.project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=422,
            detail="Project does not exist"
        )

    task = Task(
        title=task_data.title,
        priority=task_data.priority,
        due_date=task_data.due_date,
        status=task_data.status,
        project_id=task_data.project_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


# =========================
# TASK LIST
# =========================

@router.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def list_tasks(db: Session = Depends(get_db)):

    return db.query(Task).all()


# =========================
# TASK GET BY ID
# =========================

@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# =========================
# TASK UPDATE
# =========================

@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    update_data = task_data.model_dump(
        exclude_unset=True
    )

    if "project_id" in update_data:

        project = (
            db.query(Project)
            .filter(
                Project.id == update_data["project_id"]
            )
            .first()
        )

        if not project:
            raise HTTPException(
                status_code=422,
                detail="Project does not exist"
            )

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# =========================
# TASK DELETE
# =========================

@router.delete(
    "/tasks/{task_id}"
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }
    # =========================
# PROJECT TASK STATISTICS
# =========================

@router.get(
    "/projects/statistics",
    response_model=list[ProjectStatistics]
)
def project_statistics(
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Project.id.label("project_id"),
            Project.name.label("project_name"),
            func.count(Task.id).label("task_count"),

            func.sum(
                case(
                    (Task.status == "todo", 1),
                    else_=0
                )
            ).label("todo_count"),

            func.sum(
                case(
                    (Task.status == "in_progress", 1),
                    else_=0
                )
            ).label("in_progress_count"),

            func.sum(
                case(
                    (Task.status == "completed", 1),
                    else_=0
                )
            ).label("completed_count"),
        )
        .outerjoin(
            Task,
            Project.id == Task.project_id
        )
        .group_by(
            Project.id,
            Project.name
        )
        .all()
    )

    return [
        {
            "project_id": row.project_id,
            "project_name": row.project_name,
            "task_count": row.task_count,
            "todo_count": row.todo_count or 0,
            "in_progress_count": row.in_progress_count or 0,
            "completed_count": row.completed_count or 0,
        }
        for row in results
    ]
    # =========================
# TASK SEARCH
# =========================

@router.get(
    "/tasks/search",
    response_model=TaskResponse
)
def search_tasks(
    title: str,
    algo: str = "binary",
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    # Build an in-memory search index
    index = [
        {
            "id": task.id,
            "title": task.title,
        }
        for task in tasks
    ]

    if algo == "binary":
        # Binary search requires sorted data.
        insertion_sort(index, "title")

        position = binary_search(
            index,
            title,
            "title"
        )

    elif algo == "linear":
        # Linear search works on unsorted data.
        position = linear_search(
            index,
            title,
            "title"
        )

    else:
        raise HTTPException(
            status_code=400,
            detail="algo must be binary or linear"
        )

    if position == -1:
        raise HTTPException(
            status_code=404,
            detail="Task with exact title not found"
        )

    task_id = index[position]["id"]

    task = (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task
