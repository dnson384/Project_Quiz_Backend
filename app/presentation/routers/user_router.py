from fastapi import Depends, APIRouter, status, Request

from app.presentation.controllers.user_controller import UserController
from app.presentation.schemas.user_schema import UserOut
from app.presentation.dependencies.dependencies import get_user_controller

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
def get_me(req: Request, controller: UserController = Depends(get_user_controller)):
    access_token = req.headers["Authorization"].split(" ")[-1]

    cur_user = controller.get_access_user(access_token=access_token)
    return UserOut(
        user_id=cur_user._user_id,
        username=cur_user._username,
        email=cur_user._email,
        role=cur_user._role,
        avatar_url=cur_user._avatar_url,
    )
