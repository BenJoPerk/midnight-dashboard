from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone
from typing import Optional

from app.database import get_db
from app.models.activity_log import ActivityLog
from app.models.task import Task
from app.models.user import User

from app.schemas.activity_log import ActivityLogCreate, ActivityLogOut
from app.schemas.base import SuccessResponse, success_response
from app.core.pagination import (
    paginate,
    PaginationParams,
    PaginatedResponse,
)
from app.core.errors import APIException
from app.core.security import get_current_user


router = APIRouter(
    prefix="/activity-logs",
    tags=["ActivityLogs"],
)


# -----------------------------------------
# CREATE ACTIVITY LOG
# -----------------------------------------

@router.post(
    "/",
    response_model=SuccessResponse[ActivityLogOut],
)
def create_activity_log(
    data: ActivityLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Enforce UTC awareness
    if data.logged_at.tzinfo is None:
        raise APIException(
            code="VALIDATION_ERROR",
            message="logged_at must include timezone (UTC).",
            status_code=400,
        )

    # Validate task ownership
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
            raise APIException(
                code="RESOURCE_NOT_FOUND",
                message="Task not found",
                status_code=404,
            )

    log = ActivityLog(
        user_id=current_user.id,
        **data.model_dump(),
    )

    db.add(log)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise APIException(
            code="CONFLICT",
            message="Invalid activity log data.",
            status_code=400,
        )

    db.refresh(log)

    return success_response(log)


# -----------------------------------------
# LIST ACTIVITY LOGS (Paginated + Filtered)
# -----------------------------------------

@router.get(
    "/",
    response_model=PaginatedResponse[ActivityLogOut],
)
def list_logs(
    pagination: PaginationParams = Depends(),
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(ActivityLog).filter(
        ActivityLog.user_id == current_user.id
    )

    if from_date:
        if from_date.tzinfo is None:
            raise APIException(
                code="VALIDATION_ERROR",
                message="from_date must include timezone.",
                status_code=400,
            )
        query = query.filter(ActivityLog.logged_at >= from_date)

    if to_date:
        if to_date.tzinfo is None:
            raise APIException(
                code="VALIDATION_ERROR",
                message="to_date must include timezone.",
                status_code=400,
            )
        query = query.filter(ActivityLog.logged_at <= to_date)

    query = query.order_by(ActivityLog.logged_at.desc())

    return paginate(query, pagination)


# -----------------------------------------
# TODAY TOTAL (UTC SAFE)
# -----------------------------------------

@router.get(
    "/today",
    response_model=SuccessResponse[dict],
)
def total_today(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now_utc = datetime.now(timezone.utc)

    start_of_day = now_utc.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    total = (
        db.query(func.sum(ActivityLog.duration_minutes))
        .filter(ActivityLog.user_id == current_user.id)
        .filter(ActivityLog.logged_at >= start_of_day)
        .scalar()
    )

    return success_response(
        {"total_minutes_today": total or 0}
    )
