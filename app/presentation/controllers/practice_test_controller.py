from fastapi import status, HTTPException
from typing import List

from app.domain.exceptions.practice_test_exception import PracticeTestsNotFoundError

from app.application.use_cases.practice_test_service import PracticeTestService
from app.application.dtos.practice_test_dto import (
    DTOBaseInfoInput,
    DTOQuestionBaseInput,
    DTOAnswerOptionsInput,
    DTOQuestionInput,
    DTONewPracticeTestInput,
)

from app.presentation.schemas.practice_test_schema import (
    PracticeTestOutput,
    Question,
    QuestionOptions,
    PracticeTestQuestions,
    PracticeTestDetailOutput,
    NewPracticeTestInput,
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
                practice_test_id=response.get("practice_test").practice_test_id,
                practice_test_name=response.get("practice_test").practice_test_name,
                author_avatar_url=response.get("practice_test").author_avatar_url,
                author_username=response.get("practice_test").author_username,
            )

            questions: List[PracticeTestQuestions] = []
            for question in response.get("questions"):
                question_data = Question(
                    question_id=question.get("question").question_id,
                    question_text=question.get("question").question_text,
                    question_type=question.get("question").question_type,
                )
                options_data: List[QuestionOptions] = []
                for option in question.get("options"):
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
            return self.service.create_new_practice_test(payload=new_practice_test_dto)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
