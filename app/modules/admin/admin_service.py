from app.common.dependencies import create_access_token
from app.core.crypto import TextCrypto
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm

from app.modules.admin.admin_model import AdminModel
from app.modules.admin.admin_schema import UserBase
from app.core.security import AuthUtils
from app.core import config


class AdminService:
    def get_active_user(
        self,
        form_data: OAuth2PasswordRequestForm,
        auth_utils: AuthUtils = AuthUtils(),
        admin_model: AdminModel = AdminModel(),
    ) -> Optional[UserBase]:
        user: UserBase = auth_utils.authenticate_user(
            username=form_data.username,
            password=form_data.password,
            auth_model=admin_model,
        )
        if not user:
            return None

        return user

    def generate_access_token(
        self, user: UserBase, create_access_token=create_access_token
    ) -> str:
        payload = {
            "sub": user.sys_user_uuid,
            "name": user.sys_user_email_aes,
            "role": TextCrypto(plain_text=config.ADMIN_ROLE).hash_text(),
        }
        access_token = create_access_token(data=payload)

        return access_token
