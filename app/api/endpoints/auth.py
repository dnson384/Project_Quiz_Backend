from fastapi import APIRouter, Depends, status

from app.services.auth_service import AuthService
from app.schemas.auth_schema import UserCreateEmail, UserLoginEmail
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user_email_endpoint(
    user_in: UserCreateEmail, service: AuthService = Depends()
):
    new_user = service.register_user_email(user_in=user_in)
    return UserResponse(message="Đăng ký thành công", data=new_user)


@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login_user_email_endpoint(
    user_in: UserLoginEmail, service: AuthService = Depends()
):
    current_user = service.login_user_email(user_in=user_in)
    return UserResponse(message="Đăng nhập thành công", data=current_user)
