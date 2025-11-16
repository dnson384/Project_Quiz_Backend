from abc import ABC, abstractmethod
from typing import List, Optional, TypedDict

from app.domain.entities.course.course_entity import CourseOutput
from app.domain.entities.course.course_detail_entity import CourseDetailOutput


class CourseWithDetailsResponse(TypedDict):
    course: CourseOutput
    course_detail: List[CourseDetailOutput]


class ICourseRepository(ABC):
    @abstractmethod
    def get_courses_by_keyword(
        self, keyword: str, cursor_id: Optional[str] = None
    ) -> List[CourseOutput]:
        pass

    @abstractmethod
    def get_random_courses(self) -> List[CourseOutput]:
        pass

    # @abstractmethod
    # def get_course_detail_by_id(self, id: str) -> CourseWithDetailsResponse:
    #     pass
