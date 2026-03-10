from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_session_local
from ..models import Project
from ..schemas.project import ProjectCreate, ProjectOut

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProjectOut)
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(user_id=1, **data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
