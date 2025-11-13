from fastapi import APIRouter, Depends, status

from app.presentation.controllers.auth_controller import AuthController
from app.presentation.dependencies import get_auth_controller
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
    return UserResponse(message="Đăng ký thành công", user=new_user, token=None)


@router.post("/login", response_model=UserResponse, status_code=status.HTTP_200_OK)
def login_user_email_endpoint(
    user_in: UserLoginEmail, controller: AuthController = Depends(get_auth_controller)
):
    user_auth = controller.login_user_email(user_in=user_in)
    return UserResponse(message="Đăng nhập thành công", user=user_auth.get("user_data"), token=user_auth.get('access_token'))
