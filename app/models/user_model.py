from sqlalchemy import (
    Column,
    String,
    DateTime,
    Text,
    CheckConstraint,
    ForeignKey,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True), primary_key=True, default=text("gen_random_uuid()")
    )
    username = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(20), nullable=False)
    role_check = CheckConstraint(
        role.in_(["ADMIN", "STUDENT", "TEACHER"]), name="role_check"
    )

    login_method = Column(String(20), nullable=False)
    login_method_check = CheckConstraint(
        login_method.in_(["EMAIL", "GOOGLE"]), name="login_method_check"
    )

    avatar_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (role_check, login_method_check)
    email_auth = relationship("UserEmail", back_populates="user", uselist=False)


class UserEmail(Base):
    __tablename__ = "users_email"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    hashed_password = Column(Text, nullable=False)

    user = relationship("User", back_populates="email_auth")
