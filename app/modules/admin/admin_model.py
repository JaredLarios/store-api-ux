from app.core.crypto import TextCrypto
from fastapi import HTTPException, status
from app.core.database import get_database
from app.modules.admin.admin_schema import UserBase


class AdminModel:
    def get_user_by_uuid(self, user_uuid: str):
        database = get_database()
        cursor = database.cursor()
        query = """
            SELECT  sys_user_id,
                    sys_user_uuid,
                    sys_user_email_aes,
                    sys_user_email_sha,
                    sys_user_password,
                    sys_user_created_at,
                    sys_user_updated_at,
                    sys_user_attempts,
                    sys_user_last_attempt,
                    sys_user_enabled
            FROM store.sys_admin_user
            WHERE sys_user_uuid = %s And sys_user_enabled = 'True'
        """

        params = (user_uuid,)

        try:
            cursor.execute(query, params)
            print("Executed Query: " + cursor.query.decode("utf-8"))
            user = cursor.fetchone()

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="DB is not responding",
            ) from exc

        if not user:
            return None

        return UserBase.model_validate(user)

    def get_user_by_username(self, username: str):
        username_sha = TextCrypto(plain_text=username).hash_text()

        database = get_database()
        cursor = database.cursor()
        query = """
            SELECT  sys_user_id,
                    sys_user_uuid,
                    sys_user_email_aes,
                    sys_user_email_sha,
                    sys_user_password,
                    sys_user_created_at,
                    sys_user_updated_at,
                    sys_user_attempts,
                    sys_user_last_attempt,
                    sys_user_enabled
            FROM store.sys_admin_user
            WHERE sys_user_email_sha = %s
        """

        params = (username_sha,)

        try:
            cursor.execute(query, params)
            print("Executed Query: " + cursor.query.decode("utf-8"))
            user = cursor.fetchone()

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="DB is not responding",
            ) from exc

        if not user:
            return None

        return UserBase.model_validate(user)
