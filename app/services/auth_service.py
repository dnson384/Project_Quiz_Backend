from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid6 import uuid7
from datetime import timedelta, datetime, timezone

from app.db.database import get_db
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.repositories.user_repo import UserRepository
from app.repositories.refresh_token_repo import RefreshTokenRepository
from app.models.user_model import UserModel
from app.schemas.auth_schema import UserCreateEmail, UserLoginEmail


def get_user_repo(db: Session = Depends(get_db)):
    return UserRepository(db)


def get_token_repo(db: Session = Depends(get_db)):
    return RefreshTokenRepository(db)


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository = Depends(get_user_repo),
        token_repo: RefreshTokenRepository = Depends(get_token_repo),
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo

    def register_user_email(self, user_in: UserCreateEmail) -> UserModel:
        # Kiểm tra email tồn tại
        if self.user_repo.get_user_by_email(user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email đã được đăng ký"
            )

        hashed_password = get_password_hash(user_in.plain_password)

        user_id = uuid7()

        new_user = self.user_repo.create_user_email(
            user_id=user_id,
            user_in=user_in, hashed_password=hashed_password
        )
        return new_user

    def login_user_email(self, user_in: UserLoginEmail) -> UserModel:
        # Kiểm tra tài khoản tồn tại
        user = self.user_repo.get_user_by_email(user_in.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tài khoản chưa tồn tại",
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

        token_payload = {"sub": str(user.user_id), "role": str(user.role)}

        # Tạo Access Token
        access_token_expires = timedelta(minutes=5)
        access_token = create_access_token(token_payload, access_token_expires)

        # Tạo Refresh Token
        refresh_token_expires = timedelta(days=30)
        refresh_token = create_refresh_token(token_payload, refresh_token_expires)

        # Lưu thông tin refresh token
        refresh_payload = decode_refresh_token(refresh_token)
        jti = refresh_payload.get("jti")
        expires_at = datetime.fromtimestamp(refresh_payload.get("exp"), tz=timezone.utc)
        issued_at = datetime.fromtimestamp(refresh_payload.get("iat"), tz=timezone.utc)
        
        self.token_repo.save_refresh_token_jti(
            user_id=user.user_id,
            jti=jti,
            expires_at=expires_at,
            issued_at=issued_at
        )

        return {
            "user_data": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
