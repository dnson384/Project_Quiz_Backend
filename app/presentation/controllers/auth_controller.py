from fastapi import status, HTTPException

from app.application.use_cases.auth_service import AuthService
from app.presentation.schemas.auth_schema import UserCreateEmail, UserLoginEmail
from app.domain.exceptions.auth_exceptions import (
    EmailAlreadyExistsError,
    AccountNotFoundError,
    InvalidCredentialsError,
    WrongAuthMethodError,
)


class AuthController:
    def __init__(self, service: AuthService):
        self.service = service

    def register_user_email(self, user_in: UserCreateEmail):
        try:
            new_user = self.service.register_user_email(user_in=user_in)
            return new_user
        except EmailAlreadyExistsError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Đã xảy ra lỗi không mong muốn.",
            )

    def login_user_email(self, user_in: UserLoginEmail):
        try:
            user_auth = self.service.login_user_email(user_in=user_in)
            return user_auth

        except AccountNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        except WrongAuthMethodError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

        except InvalidCredentialsError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Đã xảy ra lỗi không mong muốn.",
            )
