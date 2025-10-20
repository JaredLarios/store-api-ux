from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductBase(BaseModel):
    item_image_url: Optional[str] = None
    item_price_off: Optional[float | int] = None
    item_price_off_until_date: Optional[datetime] = None


class ProductDTO(ProductBase):
    item_name: str
    item_price: float
    item_quantity: int


class UpdateProductDTO(ProductBase):
    item_uuid: str
    item_name: Optional[str] = None
    item_price: Optional[float] = None
    item_quantity: Optional[int] = None
