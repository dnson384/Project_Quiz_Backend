from fastapi import status, HTTPException
from uuid import UUID
from typing import List


from app.application.use_cases.practice_test_service import PracticeTestService
from app.application.dtos.practice_test_dto import (
    # POST
    DTOBaseInfoInput,
    DTOQuestionBaseInput,
    DTOAnswerOptionsInput,
    DTOQuestionInput,
    DTONewPracticeTestInput,
    # PUT
    DTOUpdateBaseInfoInput,
    DTOUpdateQuestionBaseInput,
    DTOUpdateOptionInput,
    DTOUpdateQuestionInput,
    DTOUpdatePracticeTestInput,
)
from app.application.exceptions import (
    PracticeTestsNotFoundError,
    QuestionNotFoundError,
    OptionNotFoundError,
)

from app.presentation.schemas.practice_test_schema import (
    PracticeTestOutput,
    Question,
    QuestionOptions,
    PracticeTestQuestions,
    PracticeTestDetailOutput,
    NewPracticeTestInput,
    UpdatePracticeTestInput,
)


class PracticeTestController:
    def __init__(self, service: PracticeTestService):
        self.service = service

    def get_random_practice_test(self):
        try:
            return self.service.get_random_practice_test()
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def get_practice_test_detail_by_id(self, practice_test_id: str, count: int | None):
        try:
            response = self.service.get_practice_test_detail_by_id(
                practice_test_id=practice_test_id, count=count
            )
            practice_test = PracticeTestOutput(
                practice_test_id=response.base_info.practice_test_id,
                practice_test_name=response.base_info.practice_test_name,
                author_avatar_url=response.base_info.author_avatar_url,
                author_username=response.base_info.author_username,
            )

            questions: List[PracticeTestQuestions] = []
            for question in response.questions:
                question_data = Question(
                    question_id=question.question.question_id,
                    question_text=question.question.question_text,
                    question_type=question.question.question_type,
                )
                options_data: List[QuestionOptions] = []
                for option in question.options:
                    options_data.append(
                        QuestionOptions(
                            option_id=option.option_id,
                            option_text=option.option_text,
                            is_correct=option.is_correct,
                        )
                    )

                questions.append(
                    PracticeTestQuestions(question=question_data, options=options_data)
                )

            return PracticeTestDetailOutput(
                practice_test=practice_test, questions=questions
            )
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def create_new_practice_test(self, payload: NewPracticeTestInput):
        baseinfo_payload = payload.base_info

        base_info_dto = DTOBaseInfoInput(
            practice_test_name=baseinfo_payload.practice_test_name,
            user_id=baseinfo_payload.user_id,
        )

        questions_dto: List[DTOQuestionInput] = []
        for question_payload in payload.questions:
            question_base_dto = DTOQuestionBaseInput(
                question_text=question_payload.question.question_text,
                question_type=question_payload.question.question_type,
            )

            options_dto: List[DTOAnswerOptionsInput] = []
            for option_payload in question_payload.options:
                options_dto.append(
                    DTOAnswerOptionsInput(
                        option_text=option_payload.option_text,
                        is_correct=option_payload.is_correct,
                    )
                )

            questions_dto.append(
                DTOQuestionInput(question=question_base_dto, options=options_dto)
            )

        new_practice_test_dto = DTONewPracticeTestInput(
            base_info=base_info_dto, questions=questions_dto
        )

        try:
            practice_test_id = self.service.create_new_practice_test(
                payload=new_practice_test_dto
            )
            return self.get_practice_test_detail_by_id(
                practice_test_id=practice_test_id, count=None
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def update_practice_test(
        self, user_id: UUID, practice_test_id: UUID, payload: UpdatePracticeTestInput
    ):
        base_info_dto = (
            DTOUpdateBaseInfoInput(
                practice_test_name=payload.base_info.practice_test_name
            )
            if payload.base_info
            else None
        )

        questions_dto: List[DTOUpdateQuestionInput] = []
        for question_payload in payload.questions:
            question_id = question_payload.question_id
            question_base_dto = (
                DTOUpdateQuestionBaseInput(
                    question_text=question_payload.question.question_text,
                    question_type=question_payload.question.question_type,
                )
                if question_payload.question
                else None
            )
            options_dto: List[DTOUpdateOptionInput] = [
                DTOUpdateOptionInput(
                    option_id=option_payload.option_id,
                    option_text=option_payload.option_text,
                    is_correct=option_payload.is_correct,
                )
                for option_payload in question_payload.options
            ]
            questions_dto.append(
                DTOUpdateQuestionInput(
                    question_id=question_id,
                    question=question_base_dto,
                    options=options_dto,
                )
            )
        try:
            self.service.update_practice_test(
                user_id, 
                practice_test_id,
                DTOUpdatePracticeTestInput(
                    base_info=base_info_dto, questions=questions_dto
                ),
            )
            return self.get_practice_test_detail_by_id(
                practice_test_id=practice_test_id, count=None
            )
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def delete_option(
        self, user_id: UUID, practice_test_id: UUID, question_id: UUID, option_id: UUID
    ) -> bool:
        try:
            return self.service.delete_option(
                user_id, practice_test_id, question_id, option_id
            )
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except OptionNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def delete_question(
        self, user_id: UUID, practice_test_id: UUID, question_id: UUID
    ) -> bool:
        try:
            return self.service.delete_question(user_id, practice_test_id, question_id)
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except QuestionNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def delete_practice_test(self, user_id: UUID, practice_test_id: UUID) -> bool:
        try:
            return self.service.delete_practice_test(user_id, practice_test_id)
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
