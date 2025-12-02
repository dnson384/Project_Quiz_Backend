from abc import ABC, abstractmethod
from typing import List, Optional, TypedDict

from app.domain.entities.practice_test.practice_test_entity import PracticeTestOutput
from app.domain.entities.practice_test.practice_test_question_entity import (
    QuestionOutput,
)
from app.domain.entities.practice_test.answer_option_entity import AnswerOptionOutput


class QuestionDetailOutput(TypedDict):
    question: QuestionOutput
    answer_option: List[AnswerOptionOutput]


class PraceticeTestWithDetailsResponse(TypedDict):
    practice_test: PracticeTestOutput
    questions: List[QuestionDetailOutput]


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
    def get_practice_test_detail_by_id(
        self, practice_test_id: str, count: int | None
    ) -> PraceticeTestWithDetailsResponse:
        pass
