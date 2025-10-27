from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.repositories.user_repo import UserRepository
from app.models.user_model import User as UserModel


def get_user_repo(db: Session = Depends(get_db)):
    """
    Dependency này yêu cầu hàm get_db cung cấp Session
    và sau đó dùng Session đó để khởi tạo UserRepository.
    """
    return UserRepository(db)


class UserServices:
    def __init__(self, repo: UserRepository = Depends(get_user_repo)):
        self.repo = repo

    def get_all_users(self) -> List[UserModel]:
        users = self.repo.get_all_users()
        return users
