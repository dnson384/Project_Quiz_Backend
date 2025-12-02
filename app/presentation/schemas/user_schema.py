from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    ADMIN = "ADMIN"


class LoginMethod(str, Enum):
    EMAIL = "EMAIL"
    GOOGLE = "GOOGLE"


class UserOut(BaseModel):
    user_id: UUID
    username: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    role: UserRole
    avatar_url: str | None = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserOut
    access_token: str | None
    refresh_token: str | None
