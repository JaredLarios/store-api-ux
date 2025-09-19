from typing import Union, Annotated
from datetime import datetime, timezone, timedelta
import jwt
from fastapi.security import APIKeyCookie
from fastapi import Depends

from app.core import config
from app.common import exceptions
from app.common.token_schema import AccessToken, Token
from app.modules.admin.admin_model import AdminModel
from app.core.crypto import TextCrypto


authentication_cookie_scheme = APIKeyCookie(name="Authorization")
refresh_cookie_scheme = APIKeyCookie(name="Refresh")


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


def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    issued_time = datetime.now(timezone.utc)
    if expires_delta:
        expire = issued_time + expires_delta
    else:
        expire = issued_time + timedelta(minutes=config.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"iss": config.ISSUER, "iat": issued_time, "exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.REFRESH_TOKEN_SECRET_KEY, algorithm=config.ALGORITHM
    )
    return encoded_jwt


async def validate_access_token(
    token: Annotated[str, Depends(authentication_cookie_scheme)],
) -> AccessToken:
    try:
        payload: dict = jwt.decode(
            token, config.ACCESS_TOKEN_SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        user_uuid = payload.get("sub")
        username = payload.get("name")

        if user_uuid is None or username is None:
            raise exceptions.credentials_exception

    except Exception as exc:
        raise exceptions.credentials_exception from exc

    return AccessToken.model_validate(payload)


async def validate_refresh_token(
    token: Annotated[str, Depends(refresh_cookie_scheme)],
) -> Token:
    try:
        payload: dict = jwt.decode(
            token, config.ACCESS_TOKEN_SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        user_uuid = payload.get("sub")

        if user_uuid is None:
            raise exceptions.credentials_exception

    except Exception as exc:
        raise exceptions.credentials_exception from exc

    return Token.model_validate(payload)


async def get_current_basic_user(
    token_data: Annotated[AccessToken, Depends(validate_access_token)],
):
    username = TextCrypto(encrypted_text=token_data.name).decrypt_text()
    role = TextCrypto(encrypted_text=token_data.role).decrypt_text()

    return {"user_uuid": token_data.sub, "username": username, "role": role}


async def get_refresh_token(
    token_data: Annotated[AccessToken, Depends(validate_access_token)],
    auth_model: Annotated[AdminModel, Depends(AdminModel)],
):
    user = auth_model.get_user_by_uuid(user_uuid=token_data.sub)

    if not user:
        raise exceptions.permission_exception

    return user


async def get_current_admin_user(
    current_user: Annotated[dict, Depends(get_current_basic_user)],
):
    print(current_user, config.ADMIN_ROLE)
    if current_user.get("role") != config.ADMIN_ROLE:
        raise exceptions.permission_exception

    return current_user
