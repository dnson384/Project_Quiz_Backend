import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status
from passlib.context import CryptContext
from uuid import uuid4

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hàm băm mật khẩu
def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


# Hàm xác thực mật khẩu
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Hàm tạo jwt_access
def create_access_token(payload: dict, expires_delta: timedelta | None = None):
    encoded_payload = payload.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=5))
    issued_at = datetime.now(timezone.utc)

    encoded_payload.update(
        {"exp": int(expire.timestamp()), "iat": int(issued_at.timestamp())}
    )
    encoded_jwt = jwt.encode(encoded_payload, settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt


def create_refresh_token(payload: dict, expires_delta: timedelta | None = None):
    # JWT Id
    jti = str(uuid4())
    refresh_payload = {
        "jti": jti,
        "sub": payload.get("sub"),
        "role": payload.get("role"),
    }
    # Thời hạn của token
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=30))
    # Thời điểm tạo token
    issued_at = datetime.now(timezone.utc)

    refresh_payload.update(
        {"exp": int(expire.timestamp()), "iat": int(issued_at.timestamp())}
    )
    encoded_jwt = jwt.encode(refresh_payload, settings.JWT_REFRESH, algorithm="HS256")
    return encoded_jwt


def decode_refresh_token(refresh_token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token không hợp lệ hoặc đã hết hạn",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(refresh_token, settings.JWT_REFRESH, algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ (Chữ ký sai)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise credentials_exception
