from app.modules.category.category_schema import NewCategoryDTO
from fastapi import APIRouter
from app.modules.category.category_schema import CategoryDTO

from app.modules.admin.admin_model import AdminModel
from app.core import config
from app.core.http_request import Client

router = APIRouter()
adminModel = AdminModel()

client: Client = Client(base_url=config.PRODUCT_API, timeout=50.0)

@router.get('/')
async def get_all_category():
    return client.get(path='/category')

# Need to add JWT Authentication
@router.post('/')
async def create_category(payload: NewCategoryDTO):
    body = payload.model_dump(exclude_none=True)
    return client.post(path='/category', json=body)

@router.patch('/')
async def update_category(payload: CategoryDTO):
    body = payload.model_dump(exclude_none=True)
    return client.patch(path='/category', json=body)

@router.delete('/')
async def delete_category(category_uuid: str):
    return client.delete(path='/category', params={'category_uuid': category_uuid})
