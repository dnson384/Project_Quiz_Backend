from app.domain.entities.user.user_entity import User
from app.application.abstractions.user_abstraction import IUserRepository


class UserServices:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def get_me(self, access_token: str | None):
        return {"get_me": access_token}
