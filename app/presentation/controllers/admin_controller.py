from fastapi import status, HTTPException, UploadFile
from uuid import UUID

from app.application.use_cases.admin_service import AdminServices
from app.application.dtos.user_dto import DTOUpdateUserInput
from app.application.exceptions import UserNotAllowError
from app.presentation.schemas.user_schema import UpdateUserInput, UserOut


class AdminController:
    def __init__(self, service: AdminServices):
        self.service = service

    def get_all_users(self, user_id: UUID, role: str):
        try:
            response = self.service.get_all_users(user_id, role)
            return [
                UserOut(
                    user_id=raw.user_id,
                    email=raw.email,
                    username=raw.username,
                    role=raw.role,
                    avatar_url=raw.avatar_url,
                )
                for raw in response
            ]
        except UserNotAllowError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
