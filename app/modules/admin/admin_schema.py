from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    sys_user_uuid: str
    sys_user_email_aes: str
    sys_user_email_sha: str
    sys_user_password: str
    sys_user_created_at: datetime | None = None
    sys_user_updated_at: datetime | None = None
    sys_user_attempts: int
    sys_user_last_attempt: datetime | None = None
    sys_user_enabled: bool

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    class Config:
        from_attributes = True