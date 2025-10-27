from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hàm băm mật khẩu
def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


# Hàm xác thực mật khẩu
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
