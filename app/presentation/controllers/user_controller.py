from fastapi import status, HTTPException

from app.application.use_cases.user_service import UserServices
from app.domain.exceptions.auth_exceptions import AccountNotFoundError


class UserController:
    def __init__(self, service: UserServices):
        self.service = service

    def get_access_user(self, access_token: str):
        try:
            cur_user = self.service.get_me(access_token)
            return cur_user
        except AccountNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Đã xảy ra lỗi không mong muốn.",
            )
