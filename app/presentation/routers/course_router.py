from fastapi import APIRouter, Depends, status

from app.presentation.controllers.course_controller import CourseController
from app.presentation.schemas.course_schema import CourseOutput
from app.presentation.dependencies.dependencies import get_course_controller

router = APIRouter(prefix="/course", tags=["Course"])


@router.get(
    "/random-course", status_code=status.HTTP_200_OK
)
def get_random_courses(controller: CourseController = Depends(get_course_controller)):
    courses_sample = controller.get_random_course()
    return courses_sample
    # return CourseOutput(
    #     course_id=courses_sample.course_id,
    #     course_name=courses_sample.course_name,
    #     author_username=courses_sample.author_username,
    #     author_role=courses_sample.author_role,
    #     num_of_terms=courses_sample.num_of_terms,
    # )
