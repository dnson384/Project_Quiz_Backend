from pydantic import BaseModel
from typing import Optional
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
    username: str
    email: str
    role: UserRole
    avatar_url: str
    login_method: str


class UserResponse(BaseModel):
    user: UserOut
    access_token: str | None
    refresh_token: str | None


class UpdateUserInput(BaseModel):
    user_id: UUID
    username: Optional[str]
    email: Optional[str]
    role: Optional[UserRole]
    avatar_url: Optional[str]
