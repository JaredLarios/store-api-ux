from pydantic import BaseModel
from datetime import datetime

class ProductDTO(BaseModel):
    item_name: str
    item_price: float
    item_quantity: int
    item_image_url: str | None = None
    item_price_off: float | int | None = None
    item_price_off_until_date: datetime | None = None

class UpdateProductDTO(ProductDTO):
    item_uuid: str
    item_name: str | None = None
    item_price: float | None = None
    item_quantity: int | None = None
