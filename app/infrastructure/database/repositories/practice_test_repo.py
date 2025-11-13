from sqlalchemy.orm import Session
from typing import List, Optional

from app.infrastructure.database.models.practice_test_model import PracticeTestModel
from app.infrastructure.database.models.user_model import UserModel

from app.application.abstractions.practice_test_abstraction import (
    IPracticeTestRepository,
)
from app.domain.entities.practice_test.practice_test_entity import (
    PracticeTestSearchResult,
)


class PracticeTestRepository(IPracticeTestRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_practice_tests_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[PracticeTestSearchResult]:
        try:
            query = (
                self.db.query(
                    PracticeTestModel.practice_test_id,
                    PracticeTestModel.practice_test_name,
                    UserModel.username,
                )
                .filter(PracticeTestModel.practice_test_name.ilike(f"%{keyword}%"))
                .join(UserModel, PracticeTestModel.user_id == UserModel.user_id)
            )

            if cursor_id:
                query = query.filter(PracticeTestModel.practice_test_id < cursor_id)

            query = query.order_by(PracticeTestModel.practice_test_id)

            db_results = query.limit(12).all()

            domain_results: List[PracticeTestSearchResult] = []
            for row in db_results:
                domain_results.append(
                    PracticeTestSearchResult(
                        practice_test_id=row.practice_test_id,
                        practice_test_name=row.practice_test_name,
                        author_username=row.username,
                    )
                )
            return domain_results

        except Exception as e:
            print("Error occurred when query practice test", e)
            return []
