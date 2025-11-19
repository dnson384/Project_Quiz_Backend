from fastapi import status, HTTPException

from app.domain.exceptions.course_exception import CoursesNotFoundError
from app.application.use_cases.course_service import CourseService


class CourseController:
    def __init__(self, service: CourseService):
        self.service = service

    def get_random_course(self):
        try:
            return self.service.get_random_course()
        except CoursesNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def get_course_detail_by_id(self, course_id: str):
        try:
            return self.service.get_course_detail_by_id(course_id=course_id)
        except CoursesNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
