from uuid import UUID

from pydantic import BaseModel, Field


class BrandBase(BaseModel):
    name: str = Field(..., title='Brand name')


class BrandSchema(BrandBase):
    pass


class BrandListSchema(BaseModel):
    id: UUID = Field(..., title='Brand ID')
    name: str = Field(..., title='Brand name')
