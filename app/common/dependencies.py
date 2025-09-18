from typing import Union
from datetime import datetime, timezone, timedelta
import jwt
from app.core import config


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    issued_time = datetime.now(timezone.utc)
    if expires_delta:
        expire = issued_time + expires_delta
    else:
        expire = issued_time + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"iss": config.ISSUER, "iat": issued_time, "exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.ACCESS_TOKEN_SECRET_KEY, algorithm=config.ALGORITHM
    )
    return encoded_jwt
