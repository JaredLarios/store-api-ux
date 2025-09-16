from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.modules.admin import admin_schema
from app.modules.admin import admin_model
from app.core.database import get_db

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_new_admin_user(new_user:admin_schema.CreateUser, db:Session = Depends(get_db)):

    new_post_db = admin_model.UserAdmin(**new_user.dict())
    db.add(new_post_db)
    db.commit()
    db.refresh(new_post_db)

    return [new_post_db]

@router.get('/', status_code=status.HTTP_200_OK)
async def find_user_by_uuid(uuid: str, db:Session = Depends(get_db)):

    stmt = (
    select(
        admin_model.UserAdmin.sys_user_email_aes,
        admin_model.UserAdmin.sys_user_email_sha,
        admin_model.UserAdmin.sys_user_uuid,
        )
        .where(admin_model.UserAdmin.sys_user_uuid == uuid)
    )

    row = db.execute(stmt).first()

    if row:
        result = {
            "sys_user_email_aes": row[0],
            "sys_user_email_sha": row[1],
            "sys_user_uuid": row[2],
        }
    else:
        result = None

    return result
