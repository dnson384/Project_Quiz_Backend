from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"


class LoginMethod(str, Enum):
    EMAIL = "EMAIL"
    GOOGLE = "GOOGLE"


# Schema đăng ký
class UserCreateEmail(BaseModel):
    email: EmailStr = Field(max_length=255)
    username: str = Field(max_length=255)
    plain_password: str = Field(min_length=8, max_length=64)
    role: UserRole


# Schema đăng nhập
class UserLoginEmail(BaseModel):
    email: EmailStr = Field(max_length=255)
    plain_password: str = Field(min_length=8, max_length=64)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: str | None = None
    role: str | None = None
