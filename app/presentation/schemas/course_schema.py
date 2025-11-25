from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List, TypedDict


class CourseOutput(BaseModel):
    course_id: UUID
    course_name: str
    author_avatar_url: str
    author_username: str
    author_role: str
    num_of_terms: int

    model_config = ConfigDict(from_attributes=True)


class CourseDetailOutput(BaseModel):
    course_detail_id: UUID
    term: str
    definition: str

    model_config = ConfigDict(from_attributes=True)


class CourseWithDetailsOutput(TypedDict):
    course: CourseOutput
    course_detail: List[CourseDetailOutput]


class LearnQuestionOutput(TypedDict):
    question: CourseDetailOutput
    options: List[CourseDetailOutput]


class CourseLearnQuestionOutput(TypedDict):
    course: CourseOutput
    questions: List[LearnQuestionOutput]
