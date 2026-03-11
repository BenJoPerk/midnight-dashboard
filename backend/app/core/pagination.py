from typing import TypeVar, Generic, Sequence
from math import ceil
from fastapi import Query
from pydantic.generics import GenericModel
from pydantic import BaseModel
from sqlalchemy.orm import Query as SAQuery
from datetime import datetime, timezone

T = TypeVar("T")


class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
    ):
        self.page = page
        self.page_size = page_size


class PaginationMeta(BaseModel):
    timestamp: datetime
    page: int
    page_size: int
    total_items: int
    total_pages: int


class PaginatedResponse(GenericModel, Generic[T]):
    data: Sequence[T]
    meta: PaginationMeta


def paginate(query: SAQuery, params: PaginationParams) -> PaginatedResponse[T]:
    total_items = query.count()

    offset = (params.page - 1) * params.page_size

    items = (
        query
        .offset(offset)
        .limit(params.page_size)
        .all()
    )

    total_pages = ceil(total_items / params.page_size) if total_items else 1

    return PaginatedResponse(
        data=items,
        meta=PaginationMeta(
            timestamp=datetime.now(timezone.utc),
            page=params.page,
            page_size=params.page_size,
            total_items=total_items,
            total_pages=total_pages,
        ),
    )

