from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
from datetime import datetime, timezone

from app.database import get_db
from app.models.task import Task
from app.models.project import Project
from app.models.user import User

from app.schemas.task import TaskCreate, TaskOut
from app.schemas.base import SuccessResponse, success_response
from app.core.pagination import (
    paginate,
    PaginationParams,
    PaginatedResponse,
)
from app.core.errors import APIException
from app.core.security import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


# -----------------------------------------
# CREATE TASK
# -----------------------------------------

@router.post(
    "/",
    response_model=SuccessResponse[TaskOut],
)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Enforce timezone-aware due_date
    if data.due_date and data.due_date.tzinfo is None:
        raise APIException(
            code="VALIDATION_ERROR",
            message="due_date must include timezone (UTC).",
            status_code=400,
        )

    # Validate project ownership if provided
    if data.project_id is not None:
        project = (
            db.query(Project)
            .filter(
                Project.id == data.project_id,
                Project.user_id == current_user.id,
            )
            .first()
        )

        if not project:
            raise APIException(
                code="RESOURCE_NOT_FOUND",
                message="Project not found.",
                status_code=404,
            )

    task = Task(
        user_id=current_user.id,
        **data.model_dump(),
    )

    db.add(task)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise APIException(
            code="CONFLICT",
            message="Invalid task data.",
            status_code=400,
        )

    db.refresh(task)

    return success_response(task)


# -----------------------------------------
# LIST TASKS (Paginated + Filtered)
# -----------------------------------------

@router.get(
    "/",
    response_model=PaginatedResponse[TaskOut],
)
def list_tasks(
    pagination: PaginationParams = Depends(),
    completed: Optional[bool] = None,
    project_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Task).filter(
        Task.user_id == current_user.id
    )

    if completed is not None:
        query = query.filter(Task.completed == completed)

    if project_id is not None:
        query = query.filter(Task.project_id == project_id)

    query = query.order_by(Task.created_at.desc())

    return paginate(query, pagination)
