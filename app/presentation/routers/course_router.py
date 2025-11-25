from fastapi import APIRouter, Depends, status
from typing import List

from app.presentation.controllers.course_controller import CourseController
from app.presentation.schemas.course_schema import (
    CourseOutput,
    CourseWithDetailsOutput,
    CourseLearnQuestionOutput,
)
from app.presentation.dependencies.dependencies import get_course_controller

router = APIRouter(prefix="/course", tags=["Course"])


@router.get(
    "/random-course", response_model=List[CourseOutput], status_code=status.HTTP_200_OK
)
def get_random_courses(controller: CourseController = Depends(get_course_controller)):
    return controller.get_random_course()


@router.get("/", response_model=CourseWithDetailsOutput, status_code=status.HTTP_200_OK)
def get_coures_detail_by_id(
    course_id: str, controller: CourseController = Depends(get_course_controller)
):
    result = controller.get_course_detail_by_id(course_id=course_id)
    return CourseWithDetailsOutput(
        course=result.get("course"), course_detail=result.get("course_detail")
    )


@router.get(
    "/learn", response_model=CourseLearnQuestionOutput, status_code=status.HTTP_200_OK
)
def create_course_learn_by_id(
    course_id: str, controller: CourseController = Depends(get_course_controller)
):
    return controller.create_course_learn_by_id(course_id)
    
