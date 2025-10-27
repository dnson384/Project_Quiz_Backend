from fastapi import APIRouter, Depends
from typing import List

from app.services.user_service import UserServices
from app.schemas.user_schema import UserOut

router = APIRouter(prefix="", tags=["Users"])


@router.get("/", response_model=List[UserOut])
def read_all_users(service: UserServices = Depends()):
    users_db = service.get_all_users()
    return users_db
