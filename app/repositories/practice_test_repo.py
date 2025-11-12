from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.practice_test_model import PracticeTestModel
from app.models.user_model import UserModel


class PracticeTestRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_practice_tests_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[PracticeTestModel]:
        try:
            query = (
                self.db.query(
                    PracticeTestModel.practice_test_id,
                    UserModel.username,
                    PracticeTestModel.practice_test_name,
                )
                .filter(PracticeTestModel.practice_test_name.ilike(f"%{keyword}%"))
                .join(UserModel, PracticeTestModel.user_id == UserModel.user_id)
            )

            if cursor_id:
                query = query.filter(PracticeTestModel.practice_test_id < cursor_id)

            query = query.order_by(PracticeTestModel.practice_test_id)

            return query.limit(12).all()

        except Exception as e:
            print("Error occurred when query practice test", e)
            return []
