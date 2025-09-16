from app.core.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class UserAdmin(Base):
    __tablename__ = "sys_admin_user"
    __table_args__ = {"schema": "store"}

    sys_user_id = Column(Integer,primary_key=True,nullable=False)
    sys_user_uuid = Column(String,nullable=False)
    sys_user_email_aes = Column(String,nullable=False)
    sys_user_email_sha = Column(String,nullable=False)
    sys_user_password = Column(String,nullable=False)
    sys_user_created_at = Column(TIMESTAMP(timezone=False),nullable=False, server_default=text('now()'))
    sys_user_updated_at = Column(TIMESTAMP(timezone=False),nullable=False, server_default=text('now()'))
    sys_user_attempts = Column(Integer,nullable=False, default=0)
    sys_user_last_attempt = Column(TIMESTAMP(timezone=False),nullable=False, server_default=text('now()'))
    sys_user_enabled = Column(Boolean, server_default='TRUE')