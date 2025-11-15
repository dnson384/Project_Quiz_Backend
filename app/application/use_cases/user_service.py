from app.domain.entities.user.user_entity import User
from app.application.abstractions.user_abstraction import IUserRepository
from app.application.abstractions.auth_abstraction import IAuthService

from app.domain.exceptions.auth_exceptions import AccountNotFoundError


class UserServices:
    def __init__(self, user_repo: IUserRepository, auth_service: IAuthService):
        self.user_repo = user_repo
        self.auth_service = auth_service

    def get_me(self, access_token: str | None):
        payload = self.auth_service.validate_access_token(access_token)

        user_id = payload.get("sub")
        cur_user = self.user_repo.get_user_by_id(id=user_id)
        if not cur_user:
            raise AccountNotFoundError("Không tìm được tài khoản người dùng")
        return cur_user
