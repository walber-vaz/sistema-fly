import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.product.category.exceptions import (
    CategoryAlreadyExists,
    CategoryNotFound,
    CategoryNotOwner,
)
from app.product.category.model import Category
from app.product.category.schemas import CategoriesListSchema, CategorySchema

logger = logging.getLogger(__name__)


async def store_category(
    user_id: UUID, category: CategorySchema, session: AsyncSession
):
    try:
        stmt = select(Category).where(
            (Category.name == category.name) | (Category.user_id == user_id)
        )
        result = await session.scalar(stmt)

        if result:
            raise CategoryAlreadyExists

        new_category = Category(name=category.name, user_id=user_id)

        session.add(new_category)
        await session.commit()
        await session.refresh(new_category)

        logger.info(f'Categoria criada com sucesso: {new_category.id}')
        return CategorySchema(
            name=new_category.name,
        )
    except IntegrityError:
        logger.error(f'Error ao criar categoria: {category}')
        raise CategoryAlreadyExists


async def update_category(
    category_id: UUID, category: CategorySchema, user_id: UUID, session: AsyncSession
):
    stmt = select(Category).where(
        (Category.id == category_id) | (Category.user_id == user_id)
    )
    result = await session.scalar(stmt)

    if result:
        if result.user_id != user_id:
            logger.error(f'Usuário não autorizado: {user_id}')
            raise CategoryNotOwner
        if result.id != category_id:
            logger.error(f'Categoria não encontrada: {category_id}')
            raise CategoryNotFound

    result.name = category.name
    await session.commit()

    logger.info(f'Categoria atualizada com sucesso: {result.id}')
    return CategorySchema(
        name=result.name,
    )


async def get_category_by_id(category_id: UUID, user_id: UUID, session: AsyncSession):
    stmt = select(Category).where(
        (Category.id == category_id) | (Category.user_id == user_id)
    )
    result = await session.scalar(stmt)

    if result:
        if result.user_id != user_id:
            logger.error(f'Usuário não autorizado: {user_id}')
            raise CategoryNotOwner
        if result.id != category_id:
            logger.error(f'Categoria não encontrada: {category_id}')
            raise CategoryNotFound

    logger.info(f'Categoria encontrada: {result.id}')
    return CategorySchema(
        name=result.name,
    )


async def get_all_categories(user_id: UUID, session: AsyncSession):
    stmt = select(Category).where(Category.user_id == user_id)
    result = await session.execute(stmt)
    categories = result.scalars().all()

    return [
        CategoriesListSchema(
            id=category.id,
            name=category.name,
        )
        for category in categories
    ]
