from typing import Annotated, Optional
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.modules.admin.admin_service import AdminService
from app.modules.admin.admin_schema import UserBase
from app.common.dependencies import get_refresh_token, get_current_admin_user
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

    user: Optional[UserBase] = admin_service.get_active_user_by_form(
        form_data=form_data
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token, refresh_token = admin_service.generate_tokens(user)

    response.set_cookie(
        "Authorization",
        access_token,
        httponly=True,
        secure=True,
        samesite="none",
        expires=config.REFRESH_TOKEN_EXPIRE_MINUTES * 100,
        max_age=config.ACCESS_TOKEN_EXPIRE_MINUTES * 100,
    )

    response.set_cookie(
        "Refresh",
        refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        expires=config.REFRESH_TOKEN_EXPIRE_MINUTES * 100,
        max_age=config.REFRESH_TOKEN_EXPIRE_MINUTES * 100,
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/auth/refresh", status_code=status.HTTP_200_OK)
async def refresh_session(
    admin_service: Annotated[AdminService, Depends(AdminService)],
    current_user: Annotated[UserBase, Depends(get_refresh_token)],
    response: Response,
):
    new_access_token = admin_service.generate_access_token_only(user=current_user)

    response.delete_cookie("Authorization", httponly=True)
    response.set_cookie(
        "Authorization",
        new_access_token,
        httponly=True,
        secure=True,
        samesite="none",
        expires=config.REFRESH_TOKEN_EXPIRE_MINUTES * 100,
        max_age=config.ACCESS_TOKEN_EXPIRE_MINUTES * 100,
    )

    return {"access_token": new_access_token}


@router.get("/logout")
async def remove_all_cookies(response: Response):
    """
    Delete all cookies to the client and log out the session
    """
    response.delete_cookie("Authorization", httponly=True)
    response.delete_cookie("Refresh", httponly=True)

    return {"message": "Logged out successfully"}


@router.get("/cryptography", status_code=status.HTTP_200_OK)
async def get_family_info(
    data: str,
    auth_utils: Annotated[AuthUtils, Depends(AuthUtils)],
    current_user: Annotated[UserBase, Depends(get_current_admin_user)],
):
    crypt_data = TextCrypto(plain_text=data)
    hashed = auth_utils.get_password_hash(data)
    return {
        "data_text": data,
        "data_aes": str(crypt_data.encrypt_text()),
        "data_sha": str(crypt_data.hash_text()),
        "data_hash": str(hashed),
    }
