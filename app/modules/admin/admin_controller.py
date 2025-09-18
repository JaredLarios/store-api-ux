from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.modules.admin.admin_service import AdminService
from app.core.security import AuthUtils
from app.core.crypto import TextCrypto
from app.core import config


router = APIRouter()


@router.post("/auth/login", status_code=status.HTTP_200_OK)
async def login_access(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    admin_service: Annotated[AdminService, Depends(AdminService)],
    response: Response,
):

    user = admin_service.get_active_user(form_data=form_data)

    if not user:
        raise HTTPException(
            detail="Not found user", status_code=status.HTTP_404_NOT_FOUND
        )

    access_token = admin_service.generate_access_token(user)

    response.set_cookie(
        "Authorization", access_token, httponly=True, secure=True, samesite="none",
        expires=config.REFRESH_TOKEN_EXPIRE_MINUTES*100,
        max_age=config.ACCESS_TOKEN_EXPIRE_MINUTES*100
    )

    return { "access_token": access_token }


@router.get("/crytography", status_code=status.HTTP_200_OK)
async def get_family_info(
    data: str, auth_utils: Annotated[AuthUtils, Depends(AuthUtils)]
):
    crypt_data = TextCrypto(plain_text=data)
    hashed = auth_utils.get_password_hash(data)
    return {
        "data_text": data,
        "data_aes": str(crypt_data.encrypt_text()),
        "data_sha": str(crypt_data.hash_text()),
        "data_hash": str(hashed),
    }
