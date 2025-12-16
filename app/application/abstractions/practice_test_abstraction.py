from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List, Optional, TypedDict
from uuid import UUID

from app.domain.entities.practice_test.practice_test_entity import (
    PracticeTestOutput,
    NewBaseInfoInput,
    UpdateBaseInfoInput,
)
from app.domain.entities.practice_test.practice_test_question_entity import (
    QuestionOutput,
    NewQuestionBaseInput,
    UpdateQuestionBaseInput,
)
from app.domain.entities.practice_test.answer_option_entity import (
    AnswerOptionOutput,
    NewAnswerOptionInput,
    UpdateAnswerOptionInput,
)


@dataclass(frozen=True)
class QuestionDetailOutput:
    question: QuestionOutput
    options: List[AnswerOptionOutput]


@dataclass(frozen=True)
class PraceticeTestWithDetailsResponse:
    base_info: PracticeTestOutput
    questions: List[QuestionDetailOutput]


class NewQuestionInput(TypedDict):
    question: NewQuestionBaseInput
    options: List[NewAnswerOptionInput]


class NewPracticeTestInput(TypedDict):
    base_info: NewBaseInfoInput
    questions: List[NewQuestionInput]


@dataclass(frozen=True)
class UpdateQuestionInput:
    question: UpdateQuestionBaseInput
    options: List[UpdateAnswerOptionInput]


class IPracticeTestRepository(ABC):
    @abstractmethod
    def get_practice_tests_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[PracticeTestOutput]:
        pass

    @abstractmethod
    def get_random_practice_test(self) -> List[PracticeTestOutput]:
        pass

    @abstractmethod
    def check_user_practice_test(self, user_id: UUID, practice_test_id: UUID) -> bool:
        pass

    @abstractmethod
    def get_practice_test_detail_by_id(
        self, practice_test_id: str
    ) -> PraceticeTestWithDetailsResponse:
        pass

    @abstractmethod
    def get_practice_test_random_detail_by_id(
        self, practice_test_id: str, count: int | None
    ) -> PraceticeTestWithDetailsResponse:
        pass


    @abstractmethod
    def create_new_practice_test(self, payload: NewPracticeTestInput) -> UUID:
        pass

    @abstractmethod
    def update_practice_test(
        self,
        practice_test_id: UUID,
        base_info: Optional[UpdateBaseInfoInput],
        question_create: List[UpdateQuestionInput],
        question_update: List[UpdateQuestionInput],
    ):
        pass

    @abstractmethod
    def delete_answer_option(
        self, practice_test_id: UUID, question_id: UUID, option_id: UUID
    ) -> bool:
        pass

    @abstractmethod
    def delete_question(self, practice_test_id: UUID, question_id: UUID) -> bool:
        pass

    @abstractmethod
    def delete_practice_test(self, practice_test_id: UUID) -> bool:
        pass
