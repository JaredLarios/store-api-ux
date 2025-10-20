import json
from typing import TypeVar, Optional, cast
from datetime import datetime
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.core.crypto import TextCrypto
from app.modules.admin.admin_model import AdminModel
from app.modules.admin.admin_schema import UserBase

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

T = TypeVar("T", bound=UserBase)


class AuthUtils:
    """
    Utils for verify identification
    """

    def verify_password(self, plain_password: str, hashed_password) -> bool:
        """
        Verify bcrypt password with hashed password
        args:
            plain_password: str -> plain text with password
            hashed_password: str -> hashed text with password
        return:
            A boolean result if the password hash matches or not
        """
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(
        self, username: str, password: str, auth_model: AdminModel
    ) -> Optional[T]:
        """
        Authenticate user using username and password
        args:
            username: str -> Username from the user (for now is not an email)
            password: str -> Plain password
        Return:
            A dictionary with the user information or a False state
            if is not
        """
        user = auth_model.get_user_by_username(username)
        if not user or not self.verify_password(password, user.sys_user_password):
            return None
        return cast(T, user)

    def verify_code(self, code: str):
        try:
            text_crypto = TextCrypto(encrypted_text=code)
            decrypt_data = text_crypto.decrypt_text()
            data = json.loads(decrypt_data)

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Code not valid."
            ) from exc

        exp = float(data.get("exp", 0))
        now_ts = datetime.now().timestamp()

        if exp < now_ts:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Code expired"
            )

        return data

    def get_password_hash(self, password: str) -> str:
        """
        Hashes a plain-text password using the configured password hashing context.

        Args:
            password (str): The plain-text password to hash.

        Returns:
            str: The hashed password.
        """
        return pwd_context.hash(password)
