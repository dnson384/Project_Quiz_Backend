from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.practice_test.practice_test_entity import PracticeTestOutput


class IPracticeTestRepository(ABC):
    @abstractmethod
    def get_practice_tests_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[PracticeTestOutput]:
        pass

    def get_random_practice_test(self) -> List[PracticeTestOutput]:
        pass
