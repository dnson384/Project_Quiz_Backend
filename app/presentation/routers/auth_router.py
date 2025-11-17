from fastapi import APIRouter, Depends, status, Request

from app.presentation.controllers.auth_controller import AuthController
from app.presentation.dependencies.dependencies import get_auth_controller
from app.presentation.schemas.auth_schema import UserCreateEmail, UserLoginEmail
from app.presentation.schemas.user_schema import UserResponse


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register_user_email_endpoint(
    user_in: UserCreateEmail, controller: AuthController = Depends(get_auth_controller)
):
    new_user = controller.register_user_email(user_in=user_in)
    return UserResponse(
        message="Đăng ký thành công",
        user=new_user,
        access_token=None,
        refresh_token=None,
    )


@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login_user_email_endpoint(
    user_in: UserLoginEmail, controller: AuthController = Depends(get_auth_controller)
):
    user_auth = controller.login_user_email(user_in=user_in)
    return UserResponse(
        message="Đăng nhập thành công",
        user=user_auth.get("user_data"),
        access_token=user_auth.get("access_token"),
        refresh_token=user_auth.get("refresh_token"),
    )


@router.post("/refresh", status_code=status.HTTP_200_OK)
def refresh_access_token(
    req: Request, controller: AuthController = Depends(get_auth_controller)
):
    refresh_token = req.headers["Authorization"].split(" ")[-1]
    new_access_token = controller.re_generate_access_token(refresh_token)
    return {"access_token": new_access_token}
