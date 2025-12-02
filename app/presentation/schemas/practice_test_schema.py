from pydantic import BaseModel, ConfigDict
from typing import List
from uuid import UUID


class PracticeTestOutput(BaseModel):
    practice_test_id: UUID
    practice_test_name: str
    author_avatar_url: str
    author_username: str

    model_config = ConfigDict(from_attributes=True)


class Question(BaseModel):
    question_id: UUID
    question_text: str
    question_type: str

    model_config = ConfigDict(from_attributes=True)


class QuestionOptions(BaseModel):
    option_id: UUID
    option_text: str
    is_correct: bool

    model_config = ConfigDict(from_attributes=True)


class PracticeTestQuestions(BaseModel):
    question: Question
    options: List[QuestionOptions]
    
    model_config = ConfigDict(from_attributes=True)


class PracticeTestDetailOutput(BaseModel):
    practice_test: PracticeTestOutput
    questions: List[PracticeTestQuestions]

    model_config = ConfigDict(from_attributes=True)
