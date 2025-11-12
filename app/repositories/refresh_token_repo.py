from sqlalchemy.orm import Session
from datetime import datetime, timezone
from uuid import UUID

from app.models.token_model import RefreshTokenModel


class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_refresh_token_jti(
        self, user_id: UUID, jti: UUID, expires_at: datetime, issued_at: datetime
    ) -> RefreshTokenModel:
        db_token = RefreshTokenModel(
            jti=jti,
            user_id=user_id,
            expires_at=expires_at,
            issued_at=issued_at,
        )

        self.db.add(db_token)
        self.db.commit()
        self.db.refresh(db_token)

        return db_token
