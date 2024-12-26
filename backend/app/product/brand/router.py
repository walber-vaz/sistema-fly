from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import services as auth_services
from app.database import get_session
from app.product.brand import service as brand_service
from app.product.brand.schemas import BrandListSchema, BrandSchema
from app.user.model import User

router = APIRouter(tags=['Brand'], prefix='/products/brands')
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(auth_services.get_current_user)]


@router.post(
    '/create/',
    status_code=HTTPStatus.CREATED,
    response_model=BrandSchema,
)
async def create_brand(brand: BrandSchema, current_user: CurrentUser, session: Session):
    return await brand_service.store_brand(current_user.id, brand, session)


@router.patch(
    '/update/{brand_id}/',
    response_model=BrandSchema,
)
async def update_brand(
    brand_id: UUID,
    brand: BrandSchema,
    current_user: CurrentUser,
    session: Session,
):
    return await brand_service.update_brand(brand_id, current_user.id, brand, session)


@router.get(
    '/list/',
    response_model=list[BrandListSchema],
)
async def list_brands(
    current_user: CurrentUser,
    session: Session,
):
    return await brand_service.get_brands(current_user.id, session)


@router.get(
    '/{brand_id}/',
    response_model=BrandSchema,
)
async def get_brand(
    brand_id: UUID,
    current_user: CurrentUser,
    session: Session,
):
    return await brand_service.get_brand_by_id(brand_id, current_user.id, session)
