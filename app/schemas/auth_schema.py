from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
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
    username: str | None = Field(default=None, max_length=255)
    plain_password: str = Field(min_length=8, max_length=64)
    confirm_password: str = Field(min_length=8, max_length=64)
    role: UserRole

    # mode='before': chạy trước khi các biến được gán vào UserCreateEmail
    @field_validator("username", mode="before")
    @classmethod
    # v: giá trị raw của trường trong field_validator
    def set_username_from_email(cls, v: str | None, info):
        if v is not None:
            return v
        email_value = info.data.get("email")
        if email_value:
            return email_value.split("@")[0]

        raise ValueError("Email cần phải được cung cấp")

    @model_validator(mode="after")
    def passwords_match(self) -> "UserCreateEmail":
        if self.plain_password != self.confirm_password:
            raise ValueError("Mật khẩu xác nhận không trùng khớp")
        return self


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
