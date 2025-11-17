from fastapi import APIRouter, Depends, status

from app.presentation.controllers.practice_test_controller import PracticeTestController
from app.presentation.schemas.practice_test_schema import PracticeTestOutput
from app.presentation.dependencies.dependencies import get_practice_test_controller

router = APIRouter(prefix="/practice-test", tags=["PracticeTest"])


@router.get("/random-practice-test", status_code=status.HTTP_200_OK)
def get_random_courses(
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    practice_test_sample = controller.get_random_practice_test()
    return practice_test_sample
    # return CourseOutput(
    #     course_id=courses_sample.course_id,
    #     course_name=courses_sample.course_name,
    #     author_username=courses_sample.author_username,
    #     author_role=courses_sample.author_role,
    #     num_of_terms=courses_sample.num_of_terms,
    # )
