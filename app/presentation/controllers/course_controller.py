from fastapi import status, HTTPException
from typing import List

from app.domain.exceptions.course_exception import CoursesNotFoundError
from app.application.use_cases.course_service import CourseService
from app.presentation.schemas.course_schema import (
    CourseQuestionOutput,
    CourseWithDetailsOutput,
    LearnQuestionOutput,
    CourseOutput,
)


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
            response = self.service.get_course_detail_by_id(course_id=course_id)
            return CourseWithDetailsOutput(
                course=response.get("course"),
                course_detail=response.get("course_detail"),
            )
        except CoursesNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def create_course_learn_by_id(self, course_id: str):
        try:
            response = self.service.create_course_learn_by_id(course_id)
            course = response.get("course")
            questions = response.get("questions")
            course_res = CourseOutput(
                course_id=course.course_id,
                course_name=course.course_name,
                author_avatar_url=course.author_avatar_url,
                author_username=course.author_username,
                author_role=course.author_role,
                num_of_terms=course.num_of_terms,
            )
            questions_res: List[LearnQuestionOutput] = []
            for question in questions:
                questions_res.append(
                    LearnQuestionOutput(
                        question=question.get("question"),
                        options=question.get("options"),
                    )
                )
            return CourseQuestionOutput(course=course_res, questions=questions_res)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    def create_course_test_by_id(self, course_id: str):
        try:
            response = self.service.create_course_test_by_id(course_id)
            course = response.get("course")
            questions = response.get("questions")
            course_res = CourseOutput(
                course_id=course.course_id,
                course_name=course.course_name,
                author_avatar_url=course.author_avatar_url,
                author_username=course.author_username,
                author_role=course.author_role,
                num_of_terms=course.num_of_terms,
            )
            questions_res: List[LearnQuestionOutput] = []
            for question in questions:
                questions_res.append(
                    LearnQuestionOutput(
                        question=question.get("question"),
                        options=question.get("options"),
                    )
                )
            return CourseQuestionOutput(course=course_res, questions=questions_res)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
