from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.core.security import (
    create_access_token,
    decode_access_token,
    decode_refresh_token,
)
from app.repositories.user_repo import UserRepository
from app.models.user_model import UserModel


def get_user_repo(db: Session = Depends(get_db)):
    return UserRepository(db)


class UserServices:
    def __init__(self, repo: UserRepository = Depends(get_user_repo)):
        self.repo = repo

    def get_all_users(self) -> List[UserModel]:
        users = self.repo.get_all_users()
        return users

    def get_me(self, access_token: str | None, refresh_token: str | None) -> UserModel:
        if not access_token:
            raise HTTPException(status_code=401, detail="Không tìm thấy access token")

        try:
            access_token_payload = decode_access_token(access_token)
            me = self.repo.get_user_by_id(access_token_payload.get("sub"))
            return {"current_user": me, "access_token": None}
        except HTTPException as http_err:
            if http_err.detail == "Token không hợp lệ hoặc đã hết hạn":
                if not refresh_token:
                    raise HTTPException(
                        status_code=401, detail="Không tìm thấy refresh token"
                    )

                try:
                    refresh_token_payload = decode_refresh_token(refresh_token)
                    new_access_token = create_access_token(
                        {
                            "sub": refresh_token_payload.get("sub"),
                            "role": refresh_token_payload.get("role"),
                        }
                    )
                    me = self.repo.get_user_by_id(refresh_token_payload.get("sub"))
                    return {"current_user": me, "access_token": new_access_token}
                except HTTPException as refresh_err:
                    raise HTTPException(
                        status_code=401,
                        detail=refresh_err.detail or "Phiên đăng nhập hết hạn",
                    )
            raise http_err
        except Exception as e:
            raise HTTPException(status_code=500, detail="Lỗi máy chủ nội bộ")
