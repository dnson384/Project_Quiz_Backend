from sqlalchemy.orm import Session, joinedload
from typing import List

from app.models.user_model import UserModel
from app.models.user_model import UserEmailModel
from app.schemas.auth_schema import UserCreateEmail


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self) -> List[UserModel]:
        return self.db.query(UserModel).all()

    def create_user_email(
        self, user_in: UserCreateEmail, hashed_password: str
    ) -> UserModel:
        db_user = UserModel(
            email=user_in.email,
            username=user_in.username,
            role=user_in.role,
            login_method="EMAIL",
        )
        self.db.add(db_user)
        # Lấy user_id trước khi commit
        self.db.flush()

        db_email_auth = UserEmailModel(
            user_id=db_user.user_id, hashed_password=hashed_password
        )
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
