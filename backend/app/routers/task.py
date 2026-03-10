from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_session_local
from ..models import Task
from ..schemas.task import TaskCreate, TaskOut

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TaskOut)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(user_id=1, **data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
