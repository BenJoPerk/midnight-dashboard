from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class DateRangeFilter(BaseModel):
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
