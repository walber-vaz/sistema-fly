from decimal import Decimal

from pydantic import UUID4, BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., description='Product name')
    description: str | None = Field(None, description='Product description')
    price: Decimal = Field(..., gt=0.0, description='Product price')
    price_sale: Decimal = Field(..., gt=0.0, description='Product price sale')
    stock: int = Field(..., ge=1, description='Product stock')
    image_url: str | None = Field(None, description='Product image URL')
    brand_id: str | None = Field(None, description='Brand ID')
    category_id: str | None = Field(None, description='Category ID')
    code_product: str = Field(description='Product code')
    barcode: int = Field(description='Product barcode')


class ProductCreate(BaseModel):
    name: str = Field(..., description='Product name')
    description: str | None = Field(None, description='Product description')
    price: Decimal = Field(..., gt=0.0, description='Product price')
    price_sale: Decimal = Field(..., gt=0.0, description='Product price sale')
    stock: int = Field(..., ge=1, description='Product stock')
    brand_id: str | None = Field(None, description='Brand ID')
    category_id: str | None = Field(None, description='Category ID')


class ProductUpdate(BaseModel):
    name: str | None = Field(None, description='Product name')
    description: str | None = Field(None, description='Product description')
    price: Decimal | None = Field(None, gt=0.0, description='Product price')
    price_sale: Decimal | None = Field(None, gt=0.0, description='Product price sale')
    stock: int | None = Field(None, ge=1, description='Product stock')
    image_url: str | None = Field(None, description='Product image URL')
    brand_id: str | None = Field(None, description='Brand ID')
    category_id: str | None = Field(None, description='Category ID')


class ResponseCreateProduct(BaseModel):
    name: str = Field(..., description='Product name')
    category: str | None = Field(None, description='Product category')
    brand: str | None = Field(None, description='Product brand')
    price_sale: str = Field(..., description='Product price sale')
    code_product: str = Field(..., description='Product code')
    barcode: int = Field(..., description='Product barcode')
    image_url: str | None = Field(None, description='Product image URL')
    created_at: str = Field(..., description='Product created at')


class ResponseProduct(BaseModel):
    message: str = Field(..., description='Product updated message')


class ProductGet(BaseModel):
    id: UUID4
    name: str
    description: str | None
    price: str
    price_sale: str
    stock: int
    image_url: str | None
    brand_name: str | None
    category_name: str | None
    code_product: str
    barcode: int
    created_at: str
    updated_at: str


class ProductListAll(BaseModel):
    data: list[ProductGet]
    total: int
    page: int
    per_page: int
    total_pages: int
    has_next: bool
    has_previous: bool
    next_page: int | None = None
    previous_page: int | None = None
