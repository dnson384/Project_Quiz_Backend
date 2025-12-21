from fastapi import Depends, APIRouter, status, Request, File, UploadFile
from uuid import UUID
from typing import List

from app.presentation.controllers.admin_controller import AdminController
from app.presentation.schemas.user_schema import UserOut, CurrentUser
from app.presentation.dependencies.dependencies import (
    get_admin_controller,
    get_current_user,
)

router = APIRouter(prefix="/admin", tags=["ADMIN"])


@router.get(
    "/all-users", response_model=List[UserOut], status_code=status.HTTP_200_OK
)
def get_all_users(
    current_user: CurrentUser = Depends(get_current_user),
    controller: AdminController = Depends(get_admin_controller),
):
    user_id = current_user.user_id
    role = current_user.role.value
    return controller.get_all_users(user_id, role)


# @router.put("/update-me", status_code=status.HTTP_200_OK)
# def update_me(
#     payload: UpdateUserInput,
#     user_id: UUID = Depends(get_current_user),
#     controller: UserController = Depends(get_user_controller),
# ):
#     return controller.update_me(user_id, payload)
