from fastapi import status, HTTPException, UploadFile
import shutil
from uuid import UUID, uuid4
import os
from pathlib import Path


from app.domain.exceptions.auth_exceptions import AccountNotFoundError
from app.application.use_cases.user_service import UserServices
from app.application.dtos.user_dto import DTOUpdateUserInput
from app.presentation.schemas.user_schema import UpdateUserInput, UserOut

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
PUBLIC_DIR = BASE_DIR / "app" / "public"
TEMP_DIR = PUBLIC_DIR / "temp"
AVATAR_DIR = PUBLIC_DIR / "avatars"
TEMP_TTL_MINUTES = 15


os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(AVATAR_DIR, exist_ok=True)


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
                login_method=user.login_method,
            )
        except AccountNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    def update_me(self, user_id: UUID, payload: UpdateUserInput):
        if user_id != payload.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        new_avatar_url = payload.avatar_url
        if new_avatar_url and "/static/temp/" in new_avatar_url:
            # 1. Trích xuất tên file từ URL
            filename = os.path.basename(new_avatar_url)

            source_path = TEMP_DIR / filename
            dest_path = AVATAR_DIR / filename

            # 3. Kiểm tra file temp có tồn tại không
            if os.path.exists(source_path):
                # Di chuyển file từ Temp sang Avatars
                shutil.move(str(source_path), str(dest_path))

                # Cập nhật lại đường dẫn mới cho DB
                final_url = f"/static/avatars/{filename}"
                payload.avatar_url = final_url
            else:
                pass

        try:
            return self.service.update_me(
                user_id,
                DTOUpdateUserInput(
                    username=payload.username,
                    email=payload.email,
                    role=payload.role,
                    avatar_url=payload.avatar_url,
                ),
            )
        except Exception as e:
            print(e)
            return False

    def upload_temp_avatar(self, file: UploadFile):
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        print(file)
        filename = f"{uuid4()}{os.path.splitext(file.filename)[1]}"
        file_path = TEMP_DIR / filename
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            return f"/static/temp/{filename}"
        except Exception as e:
            print(f"Error: {e}")
            raise HTTPException(status_code=500, detail="Failed to upload temp file")
