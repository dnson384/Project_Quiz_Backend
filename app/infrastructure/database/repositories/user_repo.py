from sqlalchemy.orm import Session, joinedload
from typing import List
from uuid import UUID

from app.infrastructure.database.models.user_model import UserModel, UserEmailModel
from app.presentation.schemas.auth_schema import UserCreateEmail


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_new_user_email(
        self, user_id: UUID, user_in: UserCreateEmail, hashed_password: str
    ) -> UserModel:
        db_user = UserModel(
            user_id=user_id,
            email=user_in.email,
            username=user_in.username,
            role=user_in.role,
            login_method="EMAIL",
        )
        self.db.add(db_user)

        db_email_auth = UserEmailModel(user_id=user_id, hashed_password=hashed_password)
        self.db.add(db_email_auth)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str) -> UserModel | None:
        return (
            self.db.query(UserModel)
            .options(joinedload(UserModel.email_auth))
            .filter(UserModel.email == email)
            .first()
        )

    def get_user_by_id(self, user_id: str) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.user_id == user_id).first()
