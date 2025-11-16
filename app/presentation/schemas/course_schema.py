from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID


class CourseOutput(BaseModel):
    course_id: UUID
    course_name: str
    author_username: str
    author_role: str
    num_of_terms: int

    model_config = ConfigDict(from_attributes=True)
