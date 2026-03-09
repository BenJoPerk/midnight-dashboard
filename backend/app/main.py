from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import psycopg2
import os

from .database import get_session_local
from . import models

app = FastAPI()


# Dependency
def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT"),
        )
        conn.close()
        return JSONResponse(status_code=200, content={"status": "healthy"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/users/count")
def user_count(db: Session = Depends(get_db)):
    return {"count": db.query(models.User).count()}
