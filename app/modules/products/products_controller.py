from typing import Annotated
from fastapi import APIRouter, Depends

from app.modules.products.products_schema import ProductDTO, UpdateProductDTO
from app.modules.admin.admin_schema import UserBase
from app.modules.admin.admin_model import AdminModel
from app.common.dependencies import get_current_admin_user
from app.core import config
from app.core.http_request import Client

router = APIRouter()
adminModel = AdminModel()

client: Client = Client(base_url=config.PRODUCT_API, timeout=50.0)


@router.get("/")
async def get_all_product(
    page: int = None, quantity: int = None, category_uuid: str = None
):
    return client.get(
        path="/product",
        params={"page": page, "quantity": quantity, "category_uuid": category_uuid},
    )


# Need to add Admin JWT Authentication
@router.post("/")
async def create_product(
    payload: ProductDTO,
    current_user: Annotated[UserBase, Depends(get_current_admin_user)],
):
    body = payload.model_dump(exclude_none=True)
    if payload.item_price_off_until_date:
        body["item_price_off_until_date"] = str(payload.item_price_off_until_date)

    return client.post(path="/product", json=body)


@router.patch("/")
async def update_product(
    payload: UpdateProductDTO,
    current_user: Annotated[UserBase, Depends(get_current_admin_user)],
):
    body = payload.model_dump(exclude_none=True)
    print(body)
    if payload.item_price_off_until_date:
        body["item_price_off_until_date"] = str(payload.item_price_off_until_date)
    return client.patch(path="/product", json=body)


@router.delete("/")
async def delete_product(
    item_uuid: str,
    current_user: Annotated[UserBase, Depends(get_current_admin_user)],
):
    return client.delete(path="/product", params={"item_uuid": item_uuid})
