from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from ..database import get_session_local
from ..models import ActivityLog
from ..schemas.activity_log import ActivityLogCreate, ActivityLogOut

router = APIRouter(prefix="/activity-logs", tags=["ActivityLogs"])


def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ActivityLogOut)
def create_log(data: ActivityLogCreate, db: Session = Depends(get_db)):
    log = ActivityLog(user_id=1, **data.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/today")
def total_today(db: Session = Depends(get_db)):
    today = date.today()
    total = db.query(func.sum(ActivityLog.duration_minutes))\
        .filter(func.date(ActivityLog.logged_at) == today)\
        .scalar()
    return {"total_minutes_today": total or 0}
