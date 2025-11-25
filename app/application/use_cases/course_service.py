import random
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

    def get_course_detail_by_id(self, course_id: str):
        try:
            course_detail_result = self.course_repo.get_course_detail_by_id(
                course_id=course_id
            )

            if not course_detail_result:
                raise CoursesNotFoundError("Không có học phần")

            return course_detail_result
        except Exception as e:
            raise Exception("Không thể thông tin học phần", e)

    def create_question(self, current_course, course_detail):
        pool = [item for item in course_detail if item != current_course]
        random_items = random.sample(pool, 3)

        return {"question": current_course, "options": random_items}

    def create_course_learn_by_id(self, course_id: str):
        try:
            response = self.get_course_detail_by_id(course_id)
            course = response.get("course")
            course_detail = response.get("course_detail")
            questions = list(
                map(
                    lambda current_course: self.create_question(
                        current_course, course_detail
                    ),
                    course_detail,
                )
            )

            return {"course": course, "questions": questions}
        except Exception as e:
            raise Exception("Không thể tạo tính năng học", e)
