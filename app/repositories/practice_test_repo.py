from sqlalchemy.orm import Session, joinedload
from typing import List

from app.models.practice_test_model import PracticeTestModel
from app.schemas.search_schema import SearchInput


class PracticeTestRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_practice_tests_by_keyword(self, keyword: str) -> List[PracticeTestModel]:
        try:
            return (
                self.db.query(PracticeTestModel)
                .options(joinedload(PracticeTestModel.practice_test_user))
                .filter(PracticeTestModel.practice_test_name.ilike(f"%{keyword}%"))
                .all()
            )

        except Exception as e:
            print("Error occurred when query practice test", e)
            return []
