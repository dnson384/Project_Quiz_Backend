from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, TypedDict, Dict
from uuid import UUID

from app.domain.entities.practice_test.practice_test_entity import (
    PracticeTest,
    PracticeTestOutput,
    NewPracticeTestBaseInfoInput,
)
from app.domain.entities.practice_test.practice_test_question_entity import (
    PracticeTestQuestion,
    QuestionOutput,
    NewQuestionBaseInput,
)
from app.domain.entities.practice_test.answer_option_entity import (
    AnswerOption,
    AnswerOptionOutput,
    NewAnswerOptionInput,
)

from app.infrastructure.database.models.practice_test_model import (
    PracticeTestModel,
    PracticeTestQuestionModel,
    AnswerOptionModel,
)
from app.infrastructure.database.models.user_model import UserModel

from app.application.abstractions.practice_test_abstraction import (
    IPracticeTestRepository,
)


class QuestionDetailOutput(TypedDict):
    question: QuestionOutput


class CourseWithDetails(TypedDict):
    practice_test: PracticeTestOutput
    question: QuestionDetailOutput


class NewQuestionInput(TypedDict):
    question: NewQuestionBaseInput
    options: List[NewAnswerOptionInput]


class NewPracticeTestInput(TypedDict):
    base_info: NewPracticeTestBaseInfoInput
    questions: List[NewQuestionInput]


class PracticeTestRepository(IPracticeTestRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_practice_tests_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[PracticeTestOutput]:
        try:
            query = (
                self.db.query(
                    PracticeTestModel.practice_test_id,
                    PracticeTestModel.practice_test_name,
                    UserModel.avatar_url,
                    UserModel.username,
                )
                .filter(PracticeTestModel.practice_test_name.ilike(f"%{keyword}%"))
                .join(UserModel, PracticeTestModel.user_id == UserModel.user_id)
            )

            if cursor_id:
                query = query.filter(PracticeTestModel.practice_test_id < cursor_id)

            query = query.order_by(PracticeTestModel.practice_test_id)

            db_results = query.limit(12).all()

            domain_results: List[PracticeTestOutput] = []
            for row in db_results:
                domain_results.append(
                    PracticeTestOutput(
                        practice_test_id=row.practice_test_id,
                        practice_test_name=row.practice_test_name,
                        author_avatar_url=row.avatar_url,
                        author_username=row.username,
                    )
                )
            return domain_results

        except Exception as e:
            print("Error occurred when query practice test", e)
            return []

    def get_random_practice_test(self) -> List[PracticeTestOutput]:
        try:
            query = (
                self.db.query(
                    PracticeTestModel.practice_test_id,
                    PracticeTestModel.practice_test_name,
                    UserModel.username.label("author_username"),
                    UserModel.avatar_url.label("author_avatar_url"),
                )
                .join(UserModel, UserModel.user_id == PracticeTestModel.user_id)
                .order_by(func.random())
                .limit(3)
                .all()
            )

            domain_result: List[PracticeTestOutput] = []
            for item in query:
                domain_result.append(
                    PracticeTestOutput(
                        practice_test_id=item.practice_test_id,
                        practice_test_name=item.practice_test_name,
                        author_avatar_url=item.author_avatar_url,
                        author_username=item.author_username,
                    )
                )

            return domain_result

        except Exception as e:
            print("Có lỗi xảy ra khi lấy bài kiểm tra thử ngẫu nhiên", e)
            return []

    def get_practice_test_detail_by_id(self, practice_test_id: str, count: int):
        test_query = (
            self.db.query(
                PracticeTestModel.practice_test_id,
                PracticeTestModel.practice_test_name,
                UserModel.username.label("author_username"),
                UserModel.avatar_url.label("author_avatar_url"),
            )
            .filter(PracticeTestModel.practice_test_id == practice_test_id)
            .join(UserModel, UserModel.user_id == PracticeTestModel.user_id)
        ).first()

        questions_id_query = (
            self.db.query(PracticeTestQuestionModel.question_id)
            .filter(PracticeTestQuestionModel.practice_test_id == practice_test_id)
            .order_by(func.random())
            .limit(count)
            .all()
        )

        questions_id_list = [qid[0] for qid in questions_id_query]

        question_query = (
            self.db.query(
                PracticeTestQuestionModel.question_id,
                PracticeTestQuestionModel.question_text,
                PracticeTestQuestionModel.question_type,
                AnswerOptionModel.option_id,
                AnswerOptionModel.option_text,
                AnswerOptionModel.is_correct,
            )
            .join(
                PracticeTestModel,
                PracticeTestModel.practice_test_id
                == PracticeTestQuestionModel.practice_test_id,
            )
            .join(
                AnswerOptionModel,
                AnswerOptionModel.question_id == PracticeTestQuestionModel.question_id,
            )
            .filter(PracticeTestQuestionModel.question_id.in_(questions_id_list))
            .all()
        )

        grouped_questions: Dict[UUID, QuestionDetailOutput] = {}

        for item in question_query:
            if item.question_id not in grouped_questions:
                grouped_questions[item.question_id] = {
                    "question": QuestionOutput(
                        question_id=item.question_id,
                        question_text=item.question_text,
                        question_type=item.question_type,
                    ),
                    "options": [],
                }

            grouped_questions[item.question_id]["options"].append(
                AnswerOptionOutput(
                    option_id=item.option_id,
                    option_text=item.option_text,
                    is_correct=item.is_correct,
                )
            )

        test_domain_result = PracticeTestOutput(
            practice_test_id=test_query.practice_test_id,
            practice_test_name=test_query.practice_test_name,
            author_avatar_url=test_query.author_avatar_url,
            author_username=test_query.author_username,
        )

        question_anwser_domain_result: List[QuestionDetailOutput] = list(
            grouped_questions.values()
        )

        return CourseWithDetails(
            practice_test=test_domain_result, questions=question_anwser_domain_result
        )

    def create_new_practice_test(self, payload: NewPracticeTestInput):
        new_practice_test_domain = PracticeTest.create_new_practice_test(
            user_id=payload.get("base_info").user_id,
            practice_test_name=payload.get("base_info").practice_test_name,
        )

        new_questions_domain: List[PracticeTestQuestion] = []
        new_options_domain: List[AnswerOption] = []
        for question_payload in payload.get("questions"):
            new_question_domain = PracticeTestQuestion.create_new_question(
                practice_test_id=new_practice_test_domain.practice_test_id,
                question_text=question_payload.get("question").question_text,
                question_type=question_payload.get("question").question_type,
            )

            new_questions_domain.append(new_question_domain)

            for option_payload in question_payload.get("options"):
                new_options_domain.append(
                    AnswerOption.create_new_answer_option(
                        question_id=new_question_domain.question_id,
                        option_text=option_payload.option_text,
                        is_correct=option_payload.is_correct,
                    )
                )

        try:
            # Thêm base info
            new_practice_test_model = PracticeTestModel(
                practice_test_id=new_practice_test_domain.practice_test_id,
                user_id=new_practice_test_domain.user_id,
                practice_test_name=new_practice_test_domain.practice_test_name,
                created_at=new_practice_test_domain.created_at,
                updated_at=new_practice_test_domain.updated_at,
            )

            self.db.add(new_practice_test_model)

            # Thêm câu hỏi
            new_questions_model = [
                PracticeTestQuestionModel(
                    question_id=question_domain.question_id,
                    practice_test_id=question_domain.practice_test_id,
                    question_text=question_domain.question_text,
                    question_type=question_domain.question_type,
                )
                for question_domain in new_questions_domain
            ]
            self.db.add_all(new_questions_model)

            # Thêm options
            new_options_model = [
                AnswerOptionModel(
                    option_id=option_domain.option_id,
                    question_id=option_domain.question_id,
                    option_text=option_domain.option_text,
                    is_correct=option_domain.is_correct,
                )
                for option_domain in new_options_domain
            ]
            self.db.add_all(new_options_model)
            self.db.commit()
            return new_practice_test_model.practice_test_id
        except Exception as e:
            print("Lỗi khi thêm bài kiểm tra thử mới", e)
            self.db.rollback()
            raise e
