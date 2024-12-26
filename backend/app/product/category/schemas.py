from uuid import UUID

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(..., title='Category name')


class CategorySchema(CategoryBase):
    pass


class CategoriesListSchema(BaseModel):
    id: UUID = Field(..., title='Category id')
    name: str = Field(..., title='Category name')
