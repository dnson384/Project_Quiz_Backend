from sqlalchemy.orm import Session, joinedload
from typing import List

from app.models.course_model import CourseModel
from app.schemas.search_schema import SearchInput


class CoursesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_courses_by_keyword(self, keyword: str) -> List[CourseModel]:
        try:
            return (
                self.db.query(CourseModel)
                .options(joinedload(CourseModel.course_user))
                .filter(CourseModel.course_name.ilike(f"%{keyword}%"))
                .all()
            )

        except Exception as e:
            print("Error occused when query course", e)
            return []
