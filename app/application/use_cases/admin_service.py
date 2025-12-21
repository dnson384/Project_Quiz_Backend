from uuid import UUID

from app.domain.exceptions.auth_exceptions import AccountNotFoundError

from app.application.abstractions.user_abstraction import IUserRepository
from app.application.dtos.user_dto import DTOUserOutput
from app.application.exceptions import UserNotAllowError


class AdminServices:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def get_all_users(self, user_id: UUID, role: str):
        if role != "ADMIN":
            raise UserNotAllowError

        cur_user = self.user_repo.get_user_by_id(user_id)
        if cur_user.role != "ADMIN":
            raise UserNotAllowError

        users_domain = self.user_repo.get_all_users()

        return [
            DTOUserOutput(
                user_id=user.user_id,
                email=user.email,
                username=user.username,
                role=user.role,
                avatar_url=user.avatar_url,
                login_method=user.login_method,
            )
            for user in users_domain
        ]
