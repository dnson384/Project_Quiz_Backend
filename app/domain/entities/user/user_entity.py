import re
from uuid import UUID
from uuid6 import uuid7
from datetime import datetime

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


class User:
    def __init__(
        self,
        _user_id: UUID,
        _username: str,
        _email: str,
        _role: str,
        _login_method: str,
        _avatar_url: str | None,
        _created_at: datetime,
        _updated_at: datetime,
    ):
        User.validate_update_profile(_username, _email, _role)
        if not _login_method:
            raise ValueError("Phương thức đăng nhập không được bỏ trống")

        self._user_id = _user_id
        self._username = _username
        self._email = _email
        self._role = _role
        self._login_method = _login_method
        self._avatar_url = _avatar_url
        self._created_at = _created_at
        self._updated_at = _updated_at

    @classmethod
    def create_new_user(
        cls,
        username: str,
        email: str,
        role: str,
        login_method: str,
        avatar_url: str = None,
    ) -> "User":
        return cls(
            _user_id=uuid7(),
            _username=username,
            _email=email,
            _role=role,
            _login_method=login_method,
            _avatar_url=avatar_url,
            _created_at=datetime.utcnow(),
            _updated_at=datetime.utcnow(),
        )

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def role(self) -> str:
        return self._role

    @property
    def login_method(self) -> str:
        return self._login_method

    @property
    def avatar_url(self) -> str:
        return self._avatar_url

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def update_profile(
        self, new_username: str = None, new_email: str = None, new_role: str = None
    ):
        username_to_check = new_username if new_username is not None else self._username
        email_to_check = new_email if new_email is not None else self._email
        role_to_check = new_role if new_role is not None else self._role

        try:
            self.validate_update_profile(
                username_to_check, email_to_check, role_to_check
            )
        except ValueError as e:
            # Ném lại lỗi với ngữ cảnh rõ ràng hơn
            raise ValueError(f"Cập nhật không hợp lệ: {e}")

        is_updated = False
        if new_username is not None and new_username != self._username:
            self._username = new_username
            is_updated = True

        if new_email is not None and new_email != self._email:
            self._email = new_email
            is_updated = True

        if new_role is not None and new_role != self._role:
            self._role = new_role
            is_updated = True

        if is_updated:
            self._updated_at = datetime.utcnow()

    @staticmethod
    def validate_update_profile(username: str, email: str, role: str):
        VALID_ROLES = ["ADMIN", "STUDENT", "TEACHER"]
        if not username or len(username) < 3:
            raise ValueError("Tên người dùng phải có ít nhất 3 ký tự")

        if not email or not EMAIL_REGEX.match(email):
            raise ValueError("Email không đúng định dạng hoặc bị bỏ trống")

        if role not in VALID_ROLES:
            raise ValueError(f"Vai trò không hợp lệ. Phải là một trong: {VALID_ROLES}")
