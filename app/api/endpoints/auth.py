from fastapi import APIRouter, Depends, status, Response

from app.services.auth_service import AuthService
from app.schemas.auth_schema import UserCreateEmail, UserLoginEmail
from app.schemas.user_schema import UserResponse


router = APIRouter(prefix="", tags=["Auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user_email_endpoint(
    user_in: UserCreateEmail, service: AuthService = Depends()
):
    new_user = service.register_user_email(user_in=user_in)
    return UserResponse(message="Đăng ký thành công", user=new_user, token=None)


@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login_user_email_endpoint(
    user_in: UserLoginEmail, response: Response, service: AuthService = Depends()
):
    user_auth = service.login_user_email(user_in=user_in)
    response.set_cookie(
        key="access_token",
        value=user_auth.get("access_token"),
        max_age=5 * 60,
        httponly=True,
        samesite="Lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=user_auth.get("refresh_token"),
        max_age=30 * 24 * 60 * 60,
        httponly=True,
        samesite="Lax",
    )
    return UserResponse(
        message="Đăng nhập thành công",
        user=user_auth.get("user_data")
    )
