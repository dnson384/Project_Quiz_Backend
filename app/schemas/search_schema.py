from pydantic import BaseModel, Field, ConfigDict, computed_field
from datetime import datetime
from uuid import UUID
from typing import List, Optional

from app.schemas.user_schema import UserOut


class SearchInput(BaseModel):
    keyword: str = Field()
    type: str = Field(default="all")
    cursor_id: str | None = Field(default=None)


class CourseOutput(BaseModel):
    course_id: UUID
    username: str
    role: str
    course_name: str
    num_of_terms: int

    model_config = ConfigDict(from_attributes=True)


class PracticeTestOutput(BaseModel):
    practice_test_id: UUID
    username: str
    practice_test_name: str
    
    model_config = ConfigDict(from_attributes=True)


class SearchOutput(BaseModel):
    courses: List[CourseOutput]
    practice_tests: List[PracticeTestOutput]
