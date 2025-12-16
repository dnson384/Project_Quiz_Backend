from fastapi import (
    Depends,
    APIRouter,
    status,
    Request,
    UploadFile,
    File,
)
from uuid import UUID

from app.presentation.controllers.user_controller import UserController
from app.presentation.schemas.user_schema import UserOut, UpdateUserInput
from app.presentation.dependencies.dependencies import (
    get_user_controller,
    get_current_user,
)

router = APIRouter(prefix="/user", tags=["USER"])


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
def get_me(req: Request, controller: UserController = Depends(get_user_controller)):
    access_token = req.headers["Authorization"].split(" ")[-1]

    return controller.get_access_user(access_token=access_token)


@router.post("/upload-avatar", status_code=status.HTTP_201_CREATED)
def upload_image(
    file: UploadFile = File(...),
    controller: UserController = Depends(get_user_controller),
):
    return controller.upload_temp_avatar(file)


@router.put("/update-me", response_model=bool, status_code=status.HTTP_200_OK)
def update_me(
    payload: UpdateUserInput,
    user_id: UUID = Depends(get_current_user),
    controller: UserController = Depends(get_user_controller),
):
    return controller.update_me(user_id, payload)
