from app.common import dependencies
from app.core.crypto import TextCrypto
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm

from app.modules.admin.admin_model import AdminModel
from app.modules.admin.admin_schema import UserBase
from app.core.security import AuthUtils
from app.core import config


class AdminService:
    def get_active_user_by_form(
        self,
        form_data: OAuth2PasswordRequestForm,
        auth_utils: AuthUtils = AuthUtils(),
        admin_model: AdminModel = AdminModel(),
    ) -> Optional[UserBase]:
        user: Optional[UserBase] = auth_utils.authenticate_user(
            username=form_data.username,
            password=form_data.password,
            auth_model=admin_model,
        )
        if not user:
            return None

        return user

    def get_active_user_by_uuid(
        self,
        user_uuid: str,
        admin_model: AdminModel = AdminModel(),
    ) -> Optional[UserBase]:
        user = admin_model.get_user_by_uuid(user_uuid=user_uuid)

        if not user:
            return None

        return user

    def generate_tokens(self, user: UserBase, dependencies=dependencies):
        payload = {
            "sub": user.sys_user_uuid,
            "name": user.sys_user_email_aes,
            "role": TextCrypto(plain_text=config.ADMIN_ROLE).encrypt_text(),
        }
        access_token = dependencies.create_access_token(data=payload)
        refresh_token = dependencies.create_refresh_token(
            data={"sub": user.sys_user_uuid}
        )

        return access_token, refresh_token

    def generate_access_token_only(
        self, user: UserBase, dependencies=dependencies
    ) -> str:
        payload = {
            "sub": user.sys_user_uuid,
            "name": user.sys_user_email_aes,
            "role": TextCrypto(plain_text=config.ADMIN_ROLE).encrypt_text(),
        }
        access_token = dependencies.create_access_token(data=payload)

        return access_token
