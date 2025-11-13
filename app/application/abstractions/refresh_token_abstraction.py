from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime

from app.domain.entities.token.refresh_token_entity import RefreshToken


class IRefreshTokenRepository(ABC):
    @abstractmethod
    def save_refresh_token_jti(
        self, user_id: UUID, expires_at: datetime, issued_at: datetime
    ) -> RefreshToken:
        pass
