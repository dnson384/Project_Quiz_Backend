from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import List, TypedDict, Literal


class DTOPracticeTestOutput(BaseModel):
    practice_test_id: UUID
    practice_test_name: str
    author_avatar_url: str
    author_username: str

    model_config = ConfigDict(from_attributes=True)


class DTOQuestion(BaseModel):
    question_id: UUID
    question_text: str
    question_type: str

    model_config = ConfigDict(from_attributes=True)


class DTOQuestionOptions(TypedDict):
    option_id: UUID
    option_text: str
    is_correct: bool

    model_config = ConfigDict(from_attributes=True)


class DTOPracticeTestQuestions(BaseModel):
    question: DTOQuestion
    options: List[DTOQuestionOptions]

    model_config = ConfigDict(from_attributes=True)


class DTOPracticeTestDetailOutput(BaseModel):
    practice_test: DTOPracticeTestOutput
    questions: List[DTOPracticeTestQuestions]

    model_config = ConfigDict(from_attributes=True)


# Thêm
class DTOBaseInfoInput(BaseModel):
    practice_test_name: str
    user_id: UUID


class DTOQuestionBaseInput(BaseModel):
    question_text: str
    question_type: str = Literal["MULTIPLE_CHOICE", "TRUE_FALSE"]


class DTOAnswerOptionsInput(BaseModel):
    option_text: str
    is_correct: bool


class DTOQuestionInput(BaseModel):
    question: DTOQuestionBaseInput
    options: List[DTOAnswerOptionsInput]


class DTONewPracticeTestInput(BaseModel):
    base_info: DTOBaseInfoInput
    questions: List[DTOQuestionInput]
