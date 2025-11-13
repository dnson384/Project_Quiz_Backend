from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional

from app.domain.entities.user.user_entity import User, CreateNewUserEmailInput


class IUserRepository(ABC):
    @abstractmethod
    def create_new_user_email(
        self, user_id: UUID, user_in: CreateNewUserEmailInput, hashed_password: str
    ) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        pass
