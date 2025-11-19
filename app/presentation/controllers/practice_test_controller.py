from fastapi import status, HTTPException

from app.domain.exceptions.practice_test_exception import PracticeTestsNotFoundError
from app.application.use_cases.practice_test_service import PracticeTestService


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

    def get_practice_test_detail_by_id(self, practice_test_id: str):
        try:
            return self.service.get_practice_test_detail_by_id(
                practice_test_id=practice_test_id
            )
        except PracticeTestsNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
