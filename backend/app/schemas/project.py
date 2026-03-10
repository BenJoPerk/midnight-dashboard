from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class ProjectOut(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    archived: bool
    created_at: datetime

    class Config:
        from_attributes = True
