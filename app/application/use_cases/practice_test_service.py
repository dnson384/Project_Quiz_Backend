from typing import List, TypedDict

from app.domain.entities.practice_test.practice_test_entity import (
    NewPracticeTestBaseInfoInput,
)
from app.domain.entities.practice_test.practice_test_question_entity import (
    NewQuestionBaseInput,
)
from app.domain.entities.practice_test.answer_option_entity import NewAnswerOptionInput
from app.domain.exceptions.practice_test_exception import PracticeTestsNotFoundError

from app.application.abstractions.practice_test_abstraction import (
    IPracticeTestRepository,
)
from app.application.dtos.practice_test_dto import DTONewPracticeTestInput


class NewQuestionInput(TypedDict):
    question: NewQuestionBaseInput
    options: List[NewAnswerOptionInput]


class NewPracticeTestInput(TypedDict):
    base_info: NewPracticeTestBaseInfoInput
    questions: List[NewQuestionInput]


class PracticeTestService:
    def __init__(self, practice_test_repo: IPracticeTestRepository):
        self.practice_test_repo = practice_test_repo

    def get_random_practice_test(self):
        try:
            sample_practice_tests = self.practice_test_repo.get_random_practice_test()

            if not sample_practice_tests:
                raise PracticeTestsNotFoundError("Không có bài kiểm tra thử")

            return sample_practice_tests
        except Exception as e:
            raise Exception("Không thể lấy ngẫu nhiên bài kiểm tra thử", e)

    def get_practice_test_detail_by_id(self, practice_test_id: str, count: int | None):
        try:
            practice_test_detail_resutl = (
                self.practice_test_repo.get_practice_test_detail_by_id(
                    practice_test_id=practice_test_id, count=count
                )
            )

            if not practice_test_detail_resutl:
                raise PracticeTestsNotFoundError("Không có bài kiểm tra thử")

            return practice_test_detail_resutl
        except Exception as e:
            raise Exception("Không thể lấy thông tin chi tiết bài kiểm tra thử", e)

    def create_new_practice_test(self, payload: DTONewPracticeTestInput):
        base_info_domain = NewPracticeTestBaseInfoInput(
            practice_test_name=payload.base_info.practice_test_name,
            user_id=payload.base_info.user_id,
        )

        questions_domain: List[NewQuestionInput] = []
        for question_payload in payload.questions:
            question_domain = NewQuestionBaseInput(
                question_text=question_payload.question.question_text,
                question_type=question_payload.question.question_type,
            )

            options_domain: List[NewAnswerOptionInput] = [
                NewAnswerOptionInput(
                    option_text=option_payload.option_text,
                    is_correct=option_payload.is_correct,
                )
                for option_payload in question_payload.options
            ]

            questions_domain.append(
                NewQuestionInput(question=question_domain, options=options_domain)
            )
        try:
            response = self.practice_test_repo.create_new_practice_test(
                payload=NewPracticeTestInput(
                    base_info=base_info_domain, questions=questions_domain
                )
            )
            return self.practice_test_repo.get_practice_test_detail_by_id(response, None)
        except Exception as e:
            raise e
