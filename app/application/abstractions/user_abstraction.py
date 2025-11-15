from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.user.user_entity import User
from app.domain.entities.user.user_email_entity import UserEmail


class IUserRepository(ABC):
    @abstractmethod
    def create_new_user_email(
        self, user: User, user_email: UserEmail
    ) -> User:
        pass

    @abstractmethod
    def get_user_email_auth(self, id: str) -> Optional[UserEmail]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, id: str) -> Optional[User]:
        pass
