from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_password_hash, verify_password
from app.repositories.user_repo import UserRepository
from app.models.user_model import User as UserModel
from app.schemas.auth_schema import UserCreateEmail, UserLoginEmail


def get_user_repo(db: Session = Depends(get_db)):
    return UserRepository(db)


class AuthService:
    def __init__(self, repo: UserRepository = Depends(get_user_repo)):
        self.repo = repo

    def register_user_email(self, user_in: UserCreateEmail) -> UserModel:
        # Kiểm tra mật khẩu & xác nhận mật khẩu
        if user_in.plain_password != user_in.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mật khẩu xác nhận không chính xác",
            )

        # Kiểm tra email tồn tại
        if self.repo.get_user_by_email(user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email đã được đăng ký"
            )

        # Kiểm tra và thay thế username
        if not user_in.username:
            user_in.username = user_in.email.split("@")[0]

        hashed_password = get_password_hash(user_in.plain_password)

        new_user = self.repo.create_user_email(
            user_in=user_in, hashed_password=hashed_password
        )
        return new_user

    def login_user_email(self, user_in: UserLoginEmail) -> UserModel:
        # Kiểm tra tài khoản tồn tại
        user = self.repo.get_user_by_email(user_in.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email hoặc mật khẩu không chính xác",
            )

        # Kiểm tra tài khoản có phương thức là EMAIL
        if not user.email_auth:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tài khoản được đăng nhập bằng phương thức khác",
            )

        # Kiểm tra mật khẩu
        if not verify_password(user_in.plain_password, user.email_auth.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email hoặc mật khẩu không chính xác",
            )

        return user
