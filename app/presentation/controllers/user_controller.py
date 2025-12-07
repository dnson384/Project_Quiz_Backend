from fastapi import status, HTTPException
from uuid import UUID

from app.domain.exceptions.auth_exceptions import AccountNotFoundError
from app.application.use_cases.user_service import UserServices
from app.application.dtos.user_dto import DTOUpdateUserInput
from app.presentation.schemas.user_schema import UpdateUserInput, UserOut


class UserController:
    def __init__(self, service: UserServices):
        self.service = service

    def get_access_user(self, access_token: str):
        try:
            user = self.service.get_me(access_token)
            return UserOut(
                user_id=user.user_id,
                email=user.email,
                username=user.username,
                role=user.role,
                avatar_url=user.avatar_url,
            )
        except AccountNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def update_me(self, user_id: UUID, payload: UpdateUserInput):
        updated_user = self.service.update_me(
            user_id,
            DTOUpdateUserInput(
                username=payload.username,
                email=payload.email,
                role=payload.role,
                avatar_url=payload.avatar_url,
            ),
        )
        return UserOut(
            user_id=updated_user.user_id,
            email=updated_user.email,
            username=updated_user.username,
            role=updated_user.role,
            avatar_url=updated_user.avatar_url,
        )
