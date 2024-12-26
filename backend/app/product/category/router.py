from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import services as auth_services
from app.database import get_session
from app.product.category import service as category_service
from app.product.category.schemas import CategoriesListSchema, CategorySchema
from app.user.model import User

router = APIRouter(tags=['Categories'], prefix='/products/categories')
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(auth_services.get_current_user)]


@router.post(
    '/create/',
    status_code=HTTPStatus.CREATED,
    response_model=CategorySchema,
)
async def create_category(
    category: CategorySchema, current_user: CurrentUser, session: Session
):
    return await category_service.store_category(current_user.id, category, session)


@router.patch(
    '/update/{category_id}/',
    response_model=CategorySchema,
)
async def update_category(
    category_id: UUID,
    category: CategorySchema,
    current_user: CurrentUser,
    session: Session,
):
    return await category_service.update_category(
        category_id, category, current_user.id, session
    )


@router.get(
    '/list/',
    response_model=list[CategoriesListSchema],
)
async def list_categories(current_user: CurrentUser, session: Session):
    return await category_service.get_all_categories(current_user.id, session)


@router.get(
    '/{category_id}/',
    response_model=CategorySchema,
)
async def get_category(category_id: UUID, current_user: CurrentUser, session: Session):
    return await category_service.get_category_by_id(
        category_id, current_user.id, session
    )
