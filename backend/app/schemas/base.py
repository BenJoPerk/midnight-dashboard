from datetime import datetime, timezone
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class Meta(BaseModel):
    timestamp: datetime


class SuccessResponse(GenericModel, Generic[T]):
    data: T
    meta: Meta


class ErrorBody(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None


class ErrorResponse(BaseModel):
    error: ErrorBody
    meta: Meta


def success_response(data: T) -> SuccessResponse[T]:
    return SuccessResponse(
        data=data,
        meta=Meta(timestamp=datetime.now(timezone.utc)),
    )
