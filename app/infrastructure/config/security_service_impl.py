from typing import Dict, Any, Tuple
from app.application.abstractions.security_abstraction import ISecurityService

from app.infrastructure.config.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)


class SecurityServiceImpl(ISecurityService):
    def hash_password(self, password: str) -> str:
        return get_password_hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return verify_password(plain_password, hashed_password)

    def create_access_token(self, payload: Dict[str, Any]) -> str:
        return create_access_token(payload)
        
    def create_refresh_token(self, payload: Dict[str, Any]) -> str:
        return create_refresh_token(payload)

    def decode_refresh_token(self, token: str) -> Dict[str, Any]:
        return decode_refresh_token(token)