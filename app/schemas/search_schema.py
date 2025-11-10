from pydantic import BaseModel, Field, ConfigDict, computed_field
from datetime import datetime
from uuid import UUID
from typing import List, Optional

from app.schemas.user_schema import UserOut


class SearchInput(BaseModel):
    keyword: str = Field()
    type: str = Field()


class CourseOutput(BaseModel):
    course_id: UUID

    course_user: Optional[UserOut] = Field(None, exclude=True)

    @computed_field
    @property
    def username(self) -> str:
        return self.course_user.username

    course_name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PracticeTestOutput(BaseModel):
    practice_test_id: UUID

    practice_test_user: Optional[UserOut] = Field(None, exclude=True)

    @computed_field
    @property
    def username(self) -> str:
        return self.practice_test_user.username

    practice_test_name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SearchOutput(BaseModel):
    courses: List[CourseOutput]
    practice_tests: List[PracticeTestOutput]

