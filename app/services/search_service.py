from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.repositories.course_repo import CoursesRepository
from app.repositories.practice_test_repo import PracticeTestRepository
from app.schemas.search_schema import SearchInput


def get_course_repo(db: Session = Depends(get_db)):
    return CoursesRepository(db)


def get_practice_test_repo(db: Session = Depends(get_db)):
    return PracticeTestRepository(db)


class SearchServices:
    def __init__(
        self,
        course_repo: CoursesRepository = Depends(get_course_repo),
        practice_test_repo: PracticeTestRepository = Depends(get_practice_test_repo),
    ):
        self.course_repo = course_repo
        self.practice_test_repo = practice_test_repo

    def search_by_keyword(self, query_input: SearchInput) -> dict:
        try:
            keyword = query_input.keyword
            courses_result = self.course_repo.get_courses_by_keyword(keyword)
            practice_tests_result = (
                self.practice_test_repo.get_practice_tests_by_keyword(keyword)
            )
            return {"courses": courses_result, "practice_tests": practice_tests_result}
        except Exception as e:
            print(e)
