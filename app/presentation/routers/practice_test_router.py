from fastapi import APIRouter, Depends, status
from typing import List

from app.presentation.controllers.practice_test_controller import PracticeTestController
from app.presentation.schemas.practice_test_schema import PracticeTestOutput
from app.presentation.dependencies.dependencies import get_practice_test_controller

router = APIRouter(prefix="/practice-test", tags=["PracticeTest"])


@router.get(
    "/random-practice-test",
    response_model=List[PracticeTestOutput],
    status_code=status.HTTP_200_OK,
)
def get_random_courses(
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.get_random_practice_test()


@router.get("/", status_code=status.HTTP_200_OK)
def get_random_courses(
    practice_test_id: str,
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.get_practice_test_detail_by_id(practice_test_id=practice_test_id)
