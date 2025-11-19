from pydantic import BaseModel, ConfigDict
from uuid import UUID


class PracticeTestOutput(BaseModel):
    practice_test_id: UUID
    practice_test_name: str
    author_username: str

    model_config = ConfigDict(from_attributes=True)
