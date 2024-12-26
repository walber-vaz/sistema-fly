import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.product.brand.exceptions import (
    BrandAlreadyExists,
    BrandNotFound,
    BrandNotOwner,
)
from app.product.brand.model import Brand
from app.product.brand.schemas import BrandListSchema, BrandSchema

logger = logging.getLogger(__name__)


async def store_brand(user_id: UUID, brand: BrandSchema, session: AsyncSession):
    try:
        stmt = select(Brand).where(
            (Brand.name == brand.name) | (Brand.user_id == user_id)
        )
        result = await session.scalar(stmt)

        if result:
            raise BrandAlreadyExists

        new_brand = Brand(name=brand.name, user_id=user_id)

        session.add(new_brand)
        await session.commit()
        await session.refresh(new_brand)

        logger.info(f'Marca criada com sucesso: {new_brand.id}')
        return BrandSchema(
            name=new_brand.name,
        )
    except HTTPException as e:
        logger.error(f'Erro ao criar marca: {brand}')
        raise e
    except IntegrityError:
        logger.error(f'Error ao criar marca: {brand}')
        raise BrandAlreadyExists


async def update_brand(
    brand_id: UUID, user_id: UUID, brand: BrandSchema, session: AsyncSession
):
    stmt = select(Brand).where((Brand.id == brand_id) | (Brand.user_id == user_id))
    result = await session.scalar(stmt)

    if result:
        if result.user_id != user_id:
            logger.error(f'Usuário não autorizado: {user_id}')
            raise BrandNotOwner
        if result.id != brand_id:
            logger.error(f'Marca não encontrada: {brand_id}')
            raise BrandNotFound

    result.name = brand.name
    await session.commit()

    logger.info(f'Marca atualizada com sucesso: {result.id}')
    return BrandSchema(
        name=result.name,
    )


async def get_brand_by_id(brand_id: UUID, user_id: UUID, session: AsyncSession):
    stmt = select(Brand).where((Brand.id == brand_id) | (Brand.user_id == user_id))
    result = await session.scalar(stmt)

    if result:
        if result.user_id != user_id:
            logger.error(f'Usuário não autorizado: {user_id}')
            raise BrandNotOwner
        if result.id != brand_id:
            logger.error(f'Marca não encontrada: {brand_id}')
            raise BrandNotFound

    logger.info(f'Marca encontrada: {result.id}')
    return BrandSchema(
        name=result.name,
    )


async def get_brands(user_id: UUID, session: AsyncSession):
    stmt = select(Brand).where(Brand.user_id == user_id)
    result = await session.execute(stmt)
    brands = result.scalars().all()

    logger.info(f'Marcas encontradas: {len(brands)}')
    return [
        BrandListSchema(
            id=brand.id,
            name=brand.name,
        )
        for brand in brands
    ]
