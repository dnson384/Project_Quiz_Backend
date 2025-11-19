from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, TypedDict

from app.domain.entities.course.course_entity import CourseOutput
from app.domain.entities.course.course_detail_entity import CourseDetailOutput

from app.application.abstractions.course_abstraction import ICourseRepository

from app.infrastructure.database.models.course_model import (
    CourseModel,
    CourseDetailModel,
)
from app.infrastructure.database.models.user_model import UserModel


class CourseWithDetails(TypedDict):
    course: CourseOutput
    course_detail: List[CourseDetailOutput]


class CoursesRepository(ICourseRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_courses_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[CourseOutput]:
        try:
            query = (
                self.db.query(
                    CourseModel.course_id,
                    CourseModel.course_name,
                    UserModel.username,
                    UserModel.role,
                    func.count(CourseDetailModel.course_detail_id).label(
                        "num_of_terms"
                    ),
                )
                .filter(CourseModel.course_name.ilike(f"%{keyword}%"))
                .join(UserModel, CourseModel.user_id == UserModel.user_id)
                .join(
                    CourseDetailModel,
                    CourseModel.course_id == CourseDetailModel.course_id,
                )
            )

            if cursor_id:
                query = query.filter(CourseModel.course_id < cursor_id)

            query = query.order_by(CourseModel.course_id.desc())

            db_results = (
                query.group_by(
                    CourseModel.course_id,
                    UserModel.username,
                    UserModel.role,
                    CourseModel.course_name,
                )
                .limit(12)
                .all()
            )

            domain_results: List[CourseOutput] = []
            for row in db_results:
                domain_results.append(
                    CourseOutput(
                        course_id=row.course_id,
                        course_name=row.course_name,
                        author_username=row.username,
                        author_role=row.role,
                        num_of_terms=row.num_of_terms,
                    )
                )

            return domain_results

        except Exception as e:
            print("Có lỗi xảy ra khi tìm kiếm học phần", e)
            return []

    def get_random_courses(self) -> List[CourseOutput]:
        try:
            query = (
                self.db.query(
                    CourseModel.course_id,
                    CourseModel.course_name,
                    UserModel.username,
                    UserModel.role,
                    func.count(CourseDetailModel.course_detail_id).label(
                        "num_of_terms"
                    ),
                )
                .join(UserModel, CourseModel.user_id == UserModel.user_id)
                .join(
                    CourseDetailModel,
                    CourseModel.course_id == CourseDetailModel.course_id,
                )
                .group_by(
                    CourseModel.course_id,
                    UserModel.username,
                    UserModel.role,
                    CourseModel.course_name,
                )
                .limit(3)
                .all()
            )

            domain_result: List[CourseOutput] = []
            for item in query:
                domain_result.append(
                    CourseOutput(
                        course_id=item.course_id,
                        course_name=item.course_name,
                        author_username=item.username,
                        author_role=item.role,
                        num_of_terms=item.num_of_terms,
                    )
                )

            return domain_result

        except Exception as e:
            print("Có lỗi xảy ra khi lấy học phần ngẫu nhiên", e)
            return []

    def get_course_detail_by_id(self, course_id: Optional[str]) -> CourseWithDetails:
        try:
            course_query = (
                self.db.query(
                    CourseModel.course_id,
                    CourseModel.course_name,
                    UserModel.username,
                    UserModel.role,
                )
                .filter(CourseModel.course_id == course_id)
                .join(UserModel, UserModel.user_id == CourseModel.user_id)
                .first()
            )

            detail_query = (
                self.db.query(
                    CourseDetailModel.course_detail_id,
                    CourseDetailModel.term,
                    CourseDetailModel.definition,
                )
                .filter(CourseDetailModel.course_id == course_id)
                .all()
            )

            course_domain_result = CourseOutput(
                course_id=course_query.course_id,
                course_name=course_query.course_name,
                author_username=course_query.username,
                author_role=course_query.role,
                num_of_terms=len(detail_query),
            )

            detail_domain_result: List[CourseDetailOutput] = []
            for item in detail_query:
                detail_domain_result.append(
                    CourseDetailOutput(
                        course_detail_id=item.course_detail_id,
                        term=item.term,
                        definition=item.definition,
                    )
                )

            return CourseWithDetails(
                course=course_domain_result, course_detail=detail_domain_result
            )
        except Exception as e:
            print("Có lỗi xảy ra khi lấy thông tin chi tiết học phần", e)
            return None
