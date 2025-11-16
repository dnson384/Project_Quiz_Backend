from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.infrastructure.database.models.course_model import (
    CourseModel,
    CourseDetailModel,
)
from app.infrastructure.database.models.user_model import UserModel

from app.application.abstractions.course_abstraction import ICourseRepository
from app.domain.entities.course.course_entity import CourseOutput


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
            return self.db.query(CourseModel).order_by(func.random()).limit(3).all()
        except Exception as e:
            print("Có lỗi xảy ra khi lấy học phần ngẫu nhiêneen", e)
            return []
