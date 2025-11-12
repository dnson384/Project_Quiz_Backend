from fastapi import APIRouter, Depends, Request, Response
from typing import List

from app.services.user_service import UserServices
from app.schemas.user_schema import UserOut

router = APIRouter(prefix="", tags=["Users"])


@router.get("/", response_model=List[UserOut])
def read_all_users(service: UserServices = Depends()):
    users_db = service.get_all_users()
    return users_db


@router.get("/me", response_model=UserOut)
def read_me(request: Request, response: Response, service: UserServices = Depends()):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    me = service.get_me(access_token, refresh_token)
    return UserOut(me.get("current_user"))
