from fastapi import APIRouter, status, Depends, HTTPException

from app.modules.admin import admin_schema
from app.modules.admin import admin_model
from app.modules.admin.admin_model import AdminModel

router = APIRouter()
adminModel = AdminModel()


@router.get('/', status_code=status.HTTP_200_OK)
async def find_user_by_uuid(uuid: str):

    result = adminModel.get_user_by_uuid(user_uuid=uuid)
    return result