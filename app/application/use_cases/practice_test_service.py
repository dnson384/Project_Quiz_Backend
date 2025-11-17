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
