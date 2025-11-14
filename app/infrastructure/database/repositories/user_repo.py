from sqlalchemy.orm import Session
from typing import Optional
from app.infrastructure.database.models.user_model import UserModel, UserEmailModel
from app.application.abstractions.user_abstraction import IUserRepository
from app.domain.entities.user.user_entity import User
from app.domain.entities.user.user_email_entity import UserEmail


class UserRepository(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_new_user_email(self, user: User, user_email: UserEmail) -> User:
        new_user = UserModel(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            role=user.role,
            login_method=user.login_method,
            avatar_url=user.avatar_url,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        new_email_auth = UserEmailModel(
            user_id=user_email.user_id,
            hashed_password=user_email.hashed_password,
        )
        self.db.add(new_user)
        self.db.add(new_email_auth)

        self.db.commit()
        self.db.refresh(new_user)
        return user

    def get_user_email_auth(self, id: str) -> Optional[UserEmail]:
        email_auth = (
            self.db.query(UserEmailModel).filter(UserEmailModel.user_id == id).first()
        )
        return UserEmail(
            _user_id=email_auth.user_id, _hashed_password=email_auth.hashed_password
        )

    def get_user_by_email(self, email: str) -> Optional[User]:
        user = self.db.query(UserModel).filter(UserModel.email == email).first()
        return (
            User(
                _user_id=user.user_id,
                _username=user.username,
                _email=user.email,
                _role=user.role,
                _login_method=user.login_method,
                _avatar_url=user.avatar_url,
                _created_at=user.created_at,
                _updated_at=user.updated_at,
            )
            if user
            else None
        )

    def get_user_by_id(self, id: str) -> Optional[User]:
        user = self.db.query(UserModel).filter(UserModel.user_id == id).first()
        return User(
            _user_id=user.user_id,
            _username=user.username,
            _email=user.email,
            _role=user.role,
            _login_method=user.login_method,
            _avatar_url=user.avatar_url,
            _created_at=user.created_at,
            _updated_at=user.updated_at,
        )
