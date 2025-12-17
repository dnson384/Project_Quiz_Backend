from dataclasses import dataclass
from typing import List, TypedDict, Optional
from uuid import UUID

from app.domain.entities.practice_test.practice_test_entity import (
    NewBaseInfoInput,
    UpdateBaseInfoInput,
    PracticeTestOutput,
)
from app.domain.entities.practice_test.practice_test_question_entity import (
    NewQuestionBaseInput,
    UpdateQuestionBaseInput,
)
from app.domain.entities.practice_test.answer_option_entity import (
    NewAnswerOptionInput,
    UpdateAnswerOptionInput,
)
from app.domain.exceptions.practice_test_exception import (
    PracticeTestsNotFoundErrorDomain,
    QuestionNotFoundErrorDomain,
    OptionNotFoundErrorDomain,
)

from app.application.abstractions.practice_test_abstraction import (
    IPracticeTestRepository,
)
from app.application.dtos.practice_test_dto import (
    DTOPracticeTestOutput,
    DTONewPracticeTestInput,
    DTOUpdatePracticeTestInput,
)
from app.application.exceptions import (
    UserNotAllowError,
    PracticeTestsNotFoundError,
    QuestionNotFoundError,
    OptionNotFoundError,
)


@dataclass(frozen=True)
class NewQuestionInput:
    question: NewQuestionBaseInput
    options: List[NewAnswerOptionInput]


@dataclass(frozen=True)
class NewPracticeTestInput:
    base_info: NewBaseInfoInput
    questions: List[NewQuestionInput]


@dataclass(frozen=True)
class UpdateQuestionInput:
    question_id: Optional[UUID]
    question_base: UpdateQuestionBaseInput
    options: UpdateAnswerOptionInput


class PracticeTestService:
    def __init__(self, practice_test_repo: IPracticeTestRepository):
        self.practice_test_repo = practice_test_repo

    def get_user_practice_test(self, user_id: UUID):
        try:
            practice_tests: List[PracticeTestOutput] = (
                self.practice_test_repo.get_practice_tests_by_user_id(user_id)
            )
            return [
                DTOPracticeTestOutput(
                    practice_test_id=practice_test.practice_test_id,
                    practice_test_name=practice_test.practice_test_name,
                    author_avatar_url=practice_test.author_avatar_url,
                    author_username=practice_test.author_username,
                )
                for practice_test in practice_tests
            ]
        except PracticeTestsNotFoundErrorDomain as e:
            raise PracticeTestsNotFoundError(str(e))

    def get_random_practice_test(self):
        try:
            sample_practice_tests = self.practice_test_repo.get_random_practice_test()

            if not sample_practice_tests:
                raise PracticeTestsNotFoundError("Không có bài kiểm tra thử")

            return sample_practice_tests
        except Exception as e:
            raise Exception("Không thể lấy ngẫu nhiên bài kiểm tra thử", e)

    def get_practice_test_detail_by_id(self, practice_test_id: str):
        try:
            return self.practice_test_repo.get_practice_test_detail_by_id(
                practice_test_id=practice_test_id
            )
        except PracticeTestsNotFoundErrorDomain as e:
            raise PracticeTestsNotFoundError(str(e))
        except Exception as e:
            raise Exception("Không thể lấy thông tin chi tiết bài kiểm tra thử", e)
        
    def get_practice_test_random_detail_by_id(self, practice_test_id: str, count: int | None):
        try:
            return self.practice_test_repo.get_practice_test_random_detail_by_id(
                practice_test_id=practice_test_id, count=count
            )
        except PracticeTestsNotFoundErrorDomain as e:
            raise PracticeTestsNotFoundError(str(e))
        except Exception as e:
            raise Exception("Không thể lấy thông tin chi tiết bài kiểm tra thử", e)

    def create_new_practice_test(self, payload: DTONewPracticeTestInput):
        base_info_domain = NewBaseInfoInput(
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
        
        return self.practice_test_repo.create_new_practice_test(
            payload=NewPracticeTestInput(
                base_info=base_info_domain, questions=questions_domain
            )
        )

    def check_valid_practice_test(self, user_id: UUID, practice_test_id: UUID):
        try:
            if not self.practice_test_repo.check_user_practice_test(
                user_id, practice_test_id
            ):
                raise UserNotAllowError()
        except PracticeTestsNotFoundErrorDomain as e:
            raise PracticeTestsNotFoundError(str(e))

    def update_practice_test(
        self, user_id: UUID, practice_test_id: UUID, payload: DTOUpdatePracticeTestInput
    ):
        self.check_valid_practice_test(user_id, practice_test_id)

        base_info_domain = (
            UpdateBaseInfoInput(practice_test_name=payload.base_info.practice_test_name)
            if payload.base_info
            else None
        )

        questions_update_domain: List[UpdateQuestionInput] = []
        questions_create_domain: List[UpdateQuestionInput] = []
        for question_payload in payload.questions:
            question_id = question_payload.question_id
            question_base_domain = (
                UpdateQuestionBaseInput(
                    question_text=question_payload.question.question_text,
                    question_type=question_payload.question.question_type,
                )
                if question_payload.question
                else None
            )
            options_domain: List[UpdateAnswerOptionInput] = [
                UpdateAnswerOptionInput(
                    option_id=option_payload.option_id,
                    option_text=option_payload.option_text,
                    is_correct=option_payload.is_correct,
                )
                for option_payload in question_payload.options
            ]
            if question_id:
                questions_update_domain.append(
                    UpdateQuestionInput(
                        question_id=question_id,
                        question_base=question_base_domain,
                        options=options_domain,
                    )
                )
            else:
                questions_create_domain.append(
                    UpdateQuestionInput(
                        question_id=None,
                        question_base=question_base_domain,
                        options=options_domain,
                    )
                )

        self.practice_test_repo.update_practice_test(
            practice_test_id,
            base_info_domain,
            questions_create_domain,
            questions_update_domain,
        )

        return self.practice_test_repo.get_practice_test_detail_by_id(
            practice_test_id=practice_test_id, count=None
        )

    def delete_option(
        self, user_id: UUID, practice_test_id: UUID, question_id: UUID, option_id: UUID
    ):
        self.check_valid_practice_test(user_id, practice_test_id)
        return self.practice_test_repo.delete_answer_option(
            practice_test_id, question_id, option_id
        )

    def delete_question(self, user_id: UUID, practice_test_id: UUID, question_id: UUID):
        self.check_valid_practice_test(user_id, practice_test_id)
        return self.practice_test_repo.delete_question(practice_test_id, question_id)

    def delete_practice_test(self, user_id: UUID, practice_test_id: UUID):
        self.check_valid_practice_test(user_id, practice_test_id)

        return self.practice_test_repo.delete_practice_test(practice_test_id)
