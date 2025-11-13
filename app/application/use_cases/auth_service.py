from uuid6 import uuid7
from datetime import datetime, timezone
from typing import Dict

from app.domain.exceptions.auth_exceptions import (
    EmailAlreadyExistsError,
    AccountNotFoundError,
    InvalidCredentialsError,
    WrongAuthMethodError,
)
from app.domain.entities.user.user_entity import (
    CreateNewUserEmailInput,
    LoginUserEmailInput,
    User,
)
from app.application.abstractions.security_abstraction import ISecurityService
from app.application.abstractions.user_abstraction import IUserRepository
from app.application.abstractions.refresh_token_abstraction import (
    IRefreshTokenRepository,
)


class AuthService:
    def __init__(
        self,
        user_repo: IUserRepository,
        token_repo: IRefreshTokenRepository,
        security_service: ISecurityService,
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.security_service = security_service

    def register_user_email(self, user_in: CreateNewUserEmailInput) -> User:
        # Kiểm tra email tồn tại
        if self.user_repo.get_user_by_email(user_in.email):
            raise EmailAlreadyExistsError("Email đã được đăng ký")

        hashed_password = self.security_service.hash_password(user_in.plain_password)

        user_id = uuid7()

        new_user = self.user_repo.create_new_user_email(
            user_id=user_id, user_in=user_in, hashed_password=hashed_password
        )
        return new_user

    def login_user_email(self, user_in: LoginUserEmailInput) -> Dict:
        # Kiểm tra tài khoản tồn tại
        user = self.user_repo.get_user_by_email(user_in.email)
        if not user:
            raise AccountNotFoundError("Tài khoản chưa tồn tại")

        # Kiểm tra tài khoản có phương thức là EMAIL
        if not user.email_auth:
            raise WrongAuthMethodError("Tài khoản được đăng nhập bằng phương thức khác")

        # Kiểm tra mật khẩu
        if not self.security_service.verify_password(
            user_in.plain_password, user.email_auth.hashed_password
        ):
            raise InvalidCredentialsError("Email hoặc mật khẩu không chính xác")

        token_payload = {"sub": str(user.user_id), "role": str(user.role)}

        # Tạo Access Token
        access_token = self.security_service.create_access_token(token_payload)

        # Tạo Refresh Token
        refresh_token = self.security_service.create_refresh_token(token_payload)

        # Lưu thông tin refresh token
        refresh_payload = self.security_service.decode_refresh_token(refresh_token)
        jti = refresh_payload.get("jti")
        expires_at = datetime.fromtimestamp(refresh_payload.get("exp"), tz=timezone.utc)
        issued_at = datetime.fromtimestamp(refresh_payload.get("iat"), tz=timezone.utc)

        self.token_repo.save_refresh_token_jti(
            user_id=user.user_id, jti=jti, expires_at=expires_at, issued_at=issued_at
        )

        return {
            "user_data": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
