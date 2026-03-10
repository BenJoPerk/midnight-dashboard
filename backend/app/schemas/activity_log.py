from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ActivityLogCreate(BaseModel):
    category: str = Field(..., min_length=1, max_length=50)

    duration_minutes: Optional[int] = Field(None, ge=0)
    quantity: Optional[int] = Field(None, ge=0)

    notes: Optional[str] = Field(None, max_length=1000)

    task_id: Optional[int] = Field(None, ge=1)

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
