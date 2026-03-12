from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timezone
import time

from app.core.logging import get_logger
from app.core.errors import (
    APIException,
    api_exception_handler,
    unhandled_exception_handler,
)
from app.schemas.base import SuccessResponse, success_response
from app.database import get_db
from app import models

from app.routers import auth, project, task, activity_log


# -----------------------------------------
# App Initialization
# -----------------------------------------

app = FastAPI(
    title="Midnight Personal OS API",
    version="1.0.0",
    docs_url="/docs",
)

logger = get_logger("request")


# -----------------------------------------
# Middleware
# -----------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = round((time.time() - start_time) * 1000, 2)

    logger.info(
        "%s %s | status=%s | duration=%sms",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response


# -----------------------------------------
# Exception Handlers
# -----------------------------------------

app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


# -----------------------------------------
# Routers
# -----------------------------------------

app.include_router(auth.router, prefix="/v1")
app.include_router(project.router, prefix="/v1")
app.include_router(task.router, prefix="/v1")
app.include_router(activity_log.router, prefix="/v1")


# -----------------------------------------
# Health Endpoint
# -----------------------------------------

@app.get("/v1/health", response_model=SuccessResponse[dict])
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return success_response({"status": "ok"})
    except Exception:
        logger.exception("Health check failed")
        raise APIException(
            code="INTERNAL_ERROR",
            message="Database connectivity failed",
            status_code=500,
        )


# -----------------------------------------
# Example: User Count
# -----------------------------------------

@app.get("/v1/users/count", response_model=SuccessResponse[dict])
def user_count(db: Session = Depends(get_db)):
    count = db.query(models.User).count()

    return success_response(
        {"count": count}
    )
