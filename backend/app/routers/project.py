from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional

from app.database import get_db
from app.models.project import Project
from app.models.user import User

from app.schemas.project import ProjectCreate, ProjectOut
from app.schemas.base import SuccessResponse, success_response
from app.core.pagination import (
    paginate,
    PaginationParams,
    PaginatedResponse,
)
from app.core.errors import APIException
from app.core.security import get_current_user
from app.core.logging import get_logger


logger = get_logger(__name__)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


# -----------------------------------------
# CREATE PROJECT
# -----------------------------------------

@router.post(
    "/",
    response_model=SuccessResponse[ProjectOut],
)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger.info(
        "User %s attempting to create project '%s'",
        current_user.id,
        data.name,
    )

    project = Project(
        user_id=current_user.id,
        **data.model_dump(),
    )

    db.add(project)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()

        logger.warning(
            "Project creation conflict for user %s | name='%s'",
            current_user.id,
            data.name,
        )

        raise APIException(
            code="CONFLICT",
            message="Project with this name already exists.",
            status_code=400,
        )

    db.refresh(project)

    logger.info(
        "Project %s successfully created for user %s",
        project.id,
        current_user.id,
    )

    return success_response(project)


# -----------------------------------------
# GET SINGLE PROJECT
# -----------------------------------------

@router.get(
    "/{project_id}",
    response_model=SuccessResponse[ProjectOut],
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(Project)
        .filter(
            Project.id == project_id,
            Project.user_id == current_user.id,
        )
        .first()
    )

    if not project:
        logger.warning(
            "User %s attempted to access non-existent or unauthorized project_id=%s",
            current_user.id,
            project_id,
        )

        raise APIException(
            code="RESOURCE_NOT_FOUND",
            message="Project not found.",
            status_code=404,
        )

    return success_response(project)


# -----------------------------------------
# LIST PROJECTS (Paginated + Filtered)
# -----------------------------------------

@router.get(
    "/",
    response_model=PaginatedResponse[ProjectOut],
)
def list_projects(
    pagination: PaginationParams = Depends(),
    archived: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Project).filter(
        Project.user_id == current_user.id
    )

    if archived is not None:
        query = query.filter(Project.archived == archived)

    query = query.order_by(Project.created_at.desc())

    return paginate(query, pagination)
