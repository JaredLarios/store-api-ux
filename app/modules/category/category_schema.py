from pydantic import BaseModel


class CategoryDTO(BaseModel):
    category_uuid: str
    category_name: str


class NewCategoryDTO(CategoryDTO):
    category_uuid: str | None = None
