from fastapi import APIRouter, Depends, status
from typing import List

from app.presentation.controllers.practice_test_controller import PracticeTestController
from app.presentation.schemas.practice_test_schema import (
    PracticeTestOutput,
    PracticeTestDetailOutput,
    NewPracticeTestInput
)
from app.presentation.dependencies.dependencies import get_practice_test_controller

router = APIRouter(prefix="/practice-test", tags=["PRACTICETEST"])


@router.get(
    "/random",
    response_model=List[PracticeTestOutput],
    status_code=status.HTTP_200_OK,
)
def get_random_courses(
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.get_random_practice_test()


@router.get(
    "/", response_model=PracticeTestDetailOutput, status_code=status.HTTP_200_OK
)
def get_random_courses(
    practice_test_id: str,
    count: int | None = None,
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.get_practice_test_detail_by_id(
        practice_test_id=practice_test_id, count=count
    )

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_practice_test(payload: NewPracticeTestInput, controller: PracticeTestController = Depends(get_practice_test_controller)):
    return controller.create_new_practice_test(payload)