from app.application.abstractions.practice_test_abstraction import (
    IPracticeTestRepository,
)
from app.domain.exceptions.practice_test_exception import PracticeTestsNotFoundError


class PracticeTestService:
    def __init__(self, practice_test_repo: IPracticeTestRepository):
        self.practice_test_repo = practice_test_repo

    def get_random_practice_test(self):
        try:
            sample_practice_tests = self.practice_test_repo.get_random_practice_test()

            if not sample_practice_tests:
                raise PracticeTestsNotFoundError("Không có bài kiểm tra thử")

            return sample_practice_tests
        except Exception as e:
            raise Exception("Không thể lấy ngẫu nhiên bài kiểm tra thử", e)

    def get_practice_test_detail_by_id(self, practice_test_id: str):
        try:
            practice_test_detail_resutl = (
                self.practice_test_repo.get_practice_test_detail_by_id(
                    practice_test_id=practice_test_id
                )
            )

            if not practice_test_detail_resutl:
                raise PracticeTestsNotFoundError("Không có bài kiểm tra thử")

            return practice_test_detail_resutl
        except Exception as e:
            raise Exception("Không thể lấy thông tin chi tiết bài kiểm tra thử", e)
