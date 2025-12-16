from fastapi import APIRouter, Depends, status
from uuid import UUID
from typing import List

from app.presentation.controllers.practice_test_controller import PracticeTestController
from app.presentation.schemas.practice_test_schema import (
    PracticeTestOutput,
    PracticeTestDetailOutput,
    NewPracticeTestInput,
    UpdatePracticeTestInput,
)
from app.presentation.dependencies.dependencies import (
    get_practice_test_controller,
    get_current_user,
)

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
def get_detail(
    practice_test_id: str,
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.get_practice_test_detail_by_id(
        practice_test_id=practice_test_id
    )

@router.get(
    "/random-question", response_model=PracticeTestDetailOutput, status_code=status.HTTP_200_OK
)
def get_detail(
    practice_test_id: str,
    count: int | None = None,
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.get_practice_test_random_detail_by_id(
        practice_test_id=practice_test_id, count=count
    )


@router.post(
    "/", response_model=PracticeTestDetailOutput, status_code=status.HTTP_201_CREATED
)
def create_new_practice_test(
    payload: NewPracticeTestInput,
    user_id: UUID = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.create_new_practice_test(user_id, payload)


@router.put("/{practice_test_id}", status_code=status.HTTP_200_OK)
def update_practice_test(
    practice_test_id: UUID,
    payload: UpdatePracticeTestInput,
    user_id: UUID = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.update_practice_test(user_id, practice_test_id, payload)


@router.delete(
    "/{practice_test_id}/question/{question_id}/option/{option_id}",
    response_model=bool,
    status_code=status.HTTP_200_OK,
)
def delete_option(
    practice_test_id: UUID,
    question_id: UUID,
    option_id: UUID,
    user_id: UUID = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.delete_option(user_id, practice_test_id, question_id, option_id)


@router.delete(
    "/{practice_test_id}/question/{question_id}",
    response_model=bool,
    status_code=status.HTTP_200_OK,
)
def delete_question(
    practice_test_id: UUID,
    question_id: UUID,
    user_id: UUID = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.delete_question(user_id, practice_test_id, question_id)


@router.delete(
    "/{practice_test_id}", response_model=bool, status_code=status.HTTP_200_OK
)
def delete_practice_test(
    practice_test_id: UUID,
    user_id: UUID = Depends(get_current_user),
    controller: PracticeTestController = Depends(get_practice_test_controller),
):
    return controller.delete_practice_test(user_id, practice_test_id)
