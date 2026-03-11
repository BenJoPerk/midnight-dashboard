from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    project_id: Optional[int] = Field(None, ge=1)
    due_date: Optional[datetime] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    project_id: Optional[int]
    due_date: Optional[datetime]
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
