from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.schemas.base import ErrorResponse, ErrorBody, Meta
from app.core.logging import get_logger


class APIException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, details=None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


async def api_exception_handler(request: Request, exc: APIException):
    error_response = ErrorResponse(
        error=ErrorBody(
            code=exc.code,
            message=exc.message,
            details=exc.details,
        ),
        meta=Meta(timestamp=datetime.now(timezone.utc)),
    )

    logger = get_logger("errors")

    logger.warning(
        "APIException | code=%s | message=%s | path=%s",
        exc.code,
        exc.message,
        request.url.path,
    )


    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(mode="json"),
    )





async def unhandled_exception_handler(request: Request, exc: Exception):
    error_response = ErrorResponse(
        error=ErrorBody(
            code="INTERNAL_ERROR",
            message="An unexpected error occurred.",
            details=None,
        ),
        meta=Meta(timestamp=datetime.now(timezone.utc)),
    )

    logger.exception("Unhandled exception at %s", request.url.path)

    return JSONResponse(
        status_code=500,
        content=error_response.model_dump(mode="json"),
    )



