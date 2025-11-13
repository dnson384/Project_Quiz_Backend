from sqlalchemy import (
    Column,
    String,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

from app.infrastructure.database.connection import Base


class PracticeTestModel(Base):
    __tablename__ = "practice_tests"

    practice_test_id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    practice_test_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # practice_test_questions
    practice_test_question = relationship(
        "PracticeTestQuestionModel",
        back_populates="question_practice_test",
        cascade="all, delete-orphan",
    )
    # users
    practice_test_user = relationship("UserModel", back_populates="user_practice_test")


class PracticeTestQuestionModel(Base):
    __tablename__ = "practice_test_questions"

    question_id = Column(UUID(as_uuid=True), primary_key=True)
    practice_test_id = Column(
        UUID(as_uuid=True),
        ForeignKey("practice_tests.practice_test_id"),
        nullable=False,
    )
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)
    type_check = CheckConstraint(
        question_type.in_(["MULTIPLE_CHOICE", "TRUE_FALSE", "WRITTEN"])
    )

    __table_args__ = (type_check,)
    question_practice_test = relationship(
        "PracticeTestModel", back_populates="practice_test_question"
    )
    question_anwser_opt = relationship(
        "AnswerOptionModel", back_populates="answer_option_question"
    )


class AnswerOptionModel(Base):
    __tablename__ = "answer_options"

    option_id = Column(UUID(as_uuid=True), primary_key=True)
    question_id = Column(
        UUID(as_uuid=True),
        ForeignKey("practice_test_questions.question_id"),
        nullable=False,
    )
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    answer_option_question = relationship(
        "PracticeTestQuestionModel", back_populates="question_anwser_opt"
    )
