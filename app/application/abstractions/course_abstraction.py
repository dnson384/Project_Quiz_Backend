from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.course.course_entity import CourseSearchResult


class ICourseRepository(ABC):
    @abstractmethod
    def get_courses_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[CourseSearchResult]:
        pass
