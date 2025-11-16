from app.application.abstractions.course_abstraction import ICourseRepository
from app.domain.exceptions.course_exception import CoursesNotFoundError


class CourseService:
    def __init__(self, course_repo: ICourseRepository):
        self.course_repo = course_repo

    def get_random_course(self):
        try:
            sample_courses = self.course_repo.get_random_courses()

            if not sample_courses:
                raise CoursesNotFoundError("Không có học phần")
            
            return sample_courses
        except Exception as e:
            raise Exception("Không thể lấy ngẫu nhiên học phần", e)
