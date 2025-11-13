from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.practice_test.practice_test_entity import PracticeTestSearchResult


class IPracticeTestRepository(ABC):
    @abstractmethod
    def get_practice_tests_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[PracticeTestSearchResult]:
        pass
