from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import timedelta

from app.database import get_db
from app.models.user import User

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

from app.schemas.base import SuccessResponse, success_response
from app.core.errors import APIException


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


# -----------------------------------------
# REQUEST SCHEMA (REGISTER ONLY)
# -----------------------------------------

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# -----------------------------------------
# REGISTER (JSON BODY)
# -----------------------------------------

@router.post(
    "/register",
    response_model=SuccessResponse[dict],
)
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.email == payload.email).first()

    if existing:
        raise APIException(
            code="CONFLICT",
            message="Email already registered.",
            status_code=400,
        )

    hashed_password = get_password_hash(payload.password)

    user = User(
        email=payload.email,
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return success_response(
        {
            "id": user.id,
            "email": user.email,
        }
    )


# -----------------------------------------
# LOGIN (OAUTH2 FORM — REQUIRED FOR SWAGGER)
# -----------------------------------------

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise APIException(
            code="UNAUTHORIZED",
            message="Incorrect email or password.",
            status_code=401,
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
