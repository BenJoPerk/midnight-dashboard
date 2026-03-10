from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectOut
from app.core.security import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectOut)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = Project(user_id=current_user.id, **data.model_dump())
    db.add(project)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Project with this name already exists",
        )

    db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectOut)
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
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.get("/", response_model=list[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Project)
        .filter(Project.user_id == current_user.id)
        .all()
    )
