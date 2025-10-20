from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    category_name: str

class CategoryDTO(CategoryBase):
    category_uuid: str


class NewCategoryDTO(CategoryBase):
    category_uuid: Optional[str] = None
