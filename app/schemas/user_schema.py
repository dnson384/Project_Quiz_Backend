from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID
from enum import Enum

from app.schemas.auth_schema import Token


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class LoginMethod(str, Enum):
    EMAIL = "EMAIL"
    GOOGLE = "GOOGLE"


class UserOut(BaseModel):
    user_id: UUID
    username: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    role: UserRole
    login_method: LoginMethod
    avatar_url: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    message: str
    user: UserOut
    token: Token | None = None
