from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import List, TypedDict, Optional


class DTOCourseOutput(BaseModel):
    course_id: UUID
    course_name: str
    author_avatar_url: str
    author_username: str
    author_role: str
    num_of_terms: int

    model_config = ConfigDict(from_attributes=True)


class DTOCourseDetailOutput(BaseModel):
    course_detail_id: UUID
    term: str
    definition: str

    model_config = ConfigDict(from_attributes=True)

class DTOCourseWithDetails(TypedDict):
    course: DTOCourseOutput
    course_detail: List[DTOCourseDetailOutput]


class DTONewCourseInput(BaseModel):
    course_name: str


class DTONewCourseDetailInput(BaseModel):
    term: str
    definition: str

# Sửa
class DTOUpdateCourseInput(BaseModel):
    course_name: str

class DTOUpdateCourseDetailInput(BaseModel):
    course_detail_id: UUID | None
    term: str
    definition: str

class DTOUpdateCourseRequest(BaseModel):
    course: Optional[DTOUpdateCourseInput] = None
    details: List[DTOUpdateCourseDetailInput]