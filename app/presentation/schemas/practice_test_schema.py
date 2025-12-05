from pydantic import BaseModel, ConfigDict
from typing import List, Literal
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


class BaseInfoInput(BaseModel):
    practice_test_name: str
    user_id: UUID


class QuestionBaseInput(BaseModel):
    question_text: str
    question_type: str = Literal["MULTIPLE_CHOICE", "TRUE_FALSE"]


class AnswerOptionsInput(BaseModel):
    option_text: str
    is_correct: bool


class QuestionInput(BaseModel):
    question: QuestionBaseInput
    options: List[AnswerOptionsInput]


class NewPracticeTestInput(BaseModel):
    base_info: BaseInfoInput
    questions: List[QuestionInput]
