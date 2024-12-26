from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import services as auth_services
from app.database import get_session
from app.product import service as product_service
from app.product.exceptions import ProductImageNotSupported
from app.product.schemas import (
    ProductCreate,
    ProductGet,
    ProductListAll,
    ProductUpdate,
    ResponseCreateProduct,
    ResponseProduct,
)
from app.user.model import User

router = APIRouter(tags=['Product'], prefix='/products')

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(auth_services.get_current_user)]


@router.patch(
    '/update/image/{product_id}/',
    response_model=ResponseProduct,
    status_code=HTTPStatus.OK,
)
async def update_image_product(
    product_id: UUID,
    current_user: CurrentUser,
    session: Session,
    image_product: UploadFile = File(...),
):
    if image_product:
        if image_product.content_type not in {'image/jpeg', 'image/png', 'image/jpg'}:
            raise ProductImageNotSupported

    return await product_service.update_image_product(
        product_id=product_id,
        user_id=current_user.id,
        session=session,
        image_product=image_product,
    )


@router.post(
    '/create/',
    response_model=ResponseCreateProduct,
    status_code=HTTPStatus.CREATED,
)
async def create_product(
    current_user: CurrentUser,
    session: Session,
    product: ProductCreate,
):
    return await product_service.store_product(
        product=product,
        user_id=current_user.id,
        session=session,
    )


@router.patch(
    '/update/{product_id}/',
    response_model=ResponseProduct,
    status_code=HTTPStatus.OK,
)
async def update_product(
    product_id: UUID,
    product: ProductUpdate,
    current_user: CurrentUser,
    session: Session,
):
    return await product_service.update_product(
        current_user.id, product_id, product, session
    )


@router.delete(
    '/delete/{product_id}/',
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_product(product_id: UUID, current_user: CurrentUser, session: Session):
    return await product_service.delete_product(current_user.id, product_id, session)


@router.get(
    '/list/',
    response_model=ProductListAll,
    status_code=HTTPStatus.OK,
)
async def list_all_products(
    current_user: CurrentUser,
    session: Session,
    page: int = Query(1, ge=1, description='Número da página'),
    limit: int = Query(10, ge=10, le=100, description='Itens por página'),
):
    return await product_service.find_all_products(
        current_user.id, session, limit, page
    )


@router.get(
    '/barcode/{code_product}/',
    status_code=HTTPStatus.OK,
)
async def get_barcode(
    current_user: CurrentUser,
    code_product: str,
):
    return await product_service.generate_and_serve_barcode(code_product)


@router.get(
    '/{product_id}/',
    status_code=HTTPStatus.OK,
    response_model=ProductGet,
)
async def get_product(
    product_id: UUID,
    current_user: CurrentUser,
    session: Session,
):
    return await product_service.get_product_by_id(
        product_id=product_id, user_id=current_user.id, session=session
    )
