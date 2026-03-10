from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ActivityLogCreate(BaseModel):
    category: str
    duration_minutes: Optional[int] = None
    quantity: Optional[int] = None
    notes: Optional[str] = None
    task_id: Optional[int] = None
    logged_at: datetime


class ActivityLogOut(BaseModel):
    id: int
    category: str
    duration_minutes: Optional[int]
    quantity: Optional[int]
    notes: Optional[str]
    logged_at: datetime

    class Config:
        from_attributes = True
