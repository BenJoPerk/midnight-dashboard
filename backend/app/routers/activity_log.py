from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from app.models import Task
from app.database import get_db
from app.models.activity_log import ActivityLog
from app.models.user import User
from app.schemas.activity_log import ActivityLogCreate, ActivityLogOut
from app.core.security import get_current_user

router = APIRouter(prefix="/activity-logs", tags=["ActivityLogs"])


@router.post("/", response_model=ActivityLogOut)
def create_activity_log(
    data: ActivityLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Validate task ownership if task_id provided
    if data.task_id is not None:
        task = (
            db.query(Task)
            .filter(
                Task.id == data.task_id,
                Task.user_id == current_user.id,
            )
            .first()
        )

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

    log = ActivityLog(user_id=current_user.id, **data.model_dump())
    db.add(log)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid request")

    db.refresh(log)
    return log


@router.get("/today")
def total_today(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()

    total = (
        db.query(func.sum(ActivityLog.duration_minutes))
        .filter(ActivityLog.user_id == current_user.id)
        .filter(func.date(ActivityLog.logged_at) == today)
        .scalar()
    )

    return {"total_minutes_today": total or 0}


@router.get("/", response_model=list[ActivityLogOut])
def list_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logs = (
        db.query(ActivityLog)
        .filter(ActivityLog.user_id == current_user.id)
        .all()
    )
    return logs
