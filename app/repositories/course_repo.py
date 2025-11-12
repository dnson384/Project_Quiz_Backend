from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.models.course_model import CourseModel, CourseDetailModel
from app.models.user_model import UserModel


class CoursesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_courses_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[CourseModel]:
        try:
            query = (
                self.db.query(
                    CourseModel.course_id,
                    UserModel.username,
                    UserModel.role,
                    CourseModel.course_name,
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

            return (
                query.group_by(
                    CourseModel.course_id,
                    UserModel.username,
                    UserModel.role,
                    CourseModel.course_name,
                )
                .limit(12)
                .all()
            )

        except Exception as e:
            print("Error occused when query course", e)
            return []
