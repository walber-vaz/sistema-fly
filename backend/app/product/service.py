import logging
import os
import tempfile
from http import HTTPStatus
from io import BytesIO
from uuid import UUID

import humanize as h
from barcode import EAN13
from barcode.writer import SVGWriter
from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.product.brand import service as brand_service
from app.product.category import service as category_service
from app.product.dependencies import save_image
from app.product.exceptions import (
    ProductAlreadyExists,
    ProductNotFound,
    ProductNotOwner,
)
from app.product.model import Product
from app.product.schemas import (
    ProductCreate,
    ProductGet,
    ProductListAll,
    ProductUpdate,
    ResponseCreateProduct,
    ResponseProduct,
)
from app.utils import generate_barcode, generate_code_product, pagination

logger = logging.getLogger(__name__)
h.activate('pt_BR')


async def store_product(
    user_id: UUID,
    product: ProductCreate,
    session: AsyncSession,
) -> ResponseCreateProduct:
    try:
        stmt = select(Product).where(Product.name == product.name)
        result = await session.scalar(stmt)

        if result:
            logging.exception(f'Ops! O produto já existe: {product.name}')
            raise ProductAlreadyExists

        get_category = None
        get_brand = None

        if product.category_id:
            get_category = await category_service.get_category_by_id(
                product.category_id,
                user_id,
                session,
            )

        if product.brand_id:
            get_brand = await brand_service.get_brand_by_id(
                product.brand_id,
                user_id,
                session,
            )

        product_code = generate_code_product()
        product_barcode = generate_barcode()

        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            price_sale=product.price_sale,
            stock=product.stock,
            brand_id=product.brand_id,
            category_id=product.category_id,
            user_id=user_id,
            code_product=product_code,
            barcode=product_barcode,
        )

        session.add(new_product)

        await session.commit()
        await session.refresh(new_product)

        price_sale = h.intcomma(new_product.price_sale)

        logger.info(f'Produto cadastrado com sucesso: {new_product.name}')
        return ResponseCreateProduct(
            brand=get_brand.name if get_brand else None,
            category=get_category.name if get_category else None,
            name=new_product.name,
            price_sale=f'R$ {price_sale}',
            code_product=new_product.code_product,
            barcode=int(new_product.barcode),
            image_url=new_product.image_url if new_product.image_url else None,
            created_at=h.naturaltime(new_product.created_at),
        )
    except HTTPException:
        logging.exception(f'Ops! O produto já existe: {product.name}')
        await session.rollback()
        raise ProductAlreadyExists
    except Exception as e:
        logging.exception(f'Ops! Ocorreu um erro inesperado. {str(e)}')
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Ops! Ocorreu um erro inesperado.',
        )


async def update_product(
    user_id: UUID, product_id: UUID, product: ProductUpdate, session: AsyncSession
):
    try:
        product_db_is_owner = select(Product).where(
            (Product.id == product_id) | (Product.user_id == user_id)
        )
        result = await session.scalar(product_db_is_owner)

        if result:
            if result.user_id != user_id:
                logging.exception(
                    f'Ops! Esse produto não está associado ao seu usuário. {user_id}'  # noqa
                )
                raise ProductNotOwner
            elif result.id != product_id:
                logging.exception(f'Ops! Produto não encontrado. {product_id}')
                raise ProductNotFound

        if product.category_id:
            await category_service.get_category_by_id(
                product.category_id,
                user_id,
                session,
            )

        if product.brand_id:
            await brand_service.get_brand_by_id(
                product.brand_id,
                user_id,
                session,
            )

        for key, value in product.model_dump(exclude_none=True).items():
            setattr(result, key, value)

        await session.commit()

        logger.info(f'Produto atualizado com sucesso: {result.name}')
        return ResponseProduct(
            message='Produto atualizado com sucesso.',
        )

    except HTTPException as e:
        logging.exception(f'Ops! O produto não foi encontrado. {product_id}')
        await session.rollback()
        raise e
    except Exception:
        logging.exception('Ops! Ocorreu um erro inesperado.')
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Ops! Ocorreu um erro inesperado.',
        )


async def delete_product(user_id: UUID, product_id: UUID, session: AsyncSession):
    try:
        product_db_is_owner = select(Product).where(
            (Product.id == product_id) | (Product.user_id == user_id)
        )
        result = await session.scalar(product_db_is_owner)

        if result:
            if result.user_id != user_id:
                logging.exception(
                    f'Ops! Esse produto não está associado ao seu usuário. {user_id}'  # noqa
                )
                raise ProductNotOwner
            elif result.id != product_id:
                logging.exception(f'Ops! Produto não encontrado. {product_id}')
                raise ProductNotFound

        session.delete(result)

        await session.commit()

        logger.info(f'Produto deletado com sucesso: {result.name}')
    except HTTPException as e:
        logging.exception('Ops! Ocorreu um erro inesperado.')
        await session.rollback()
        raise e
    except Exception:
        logging.exception('Ops! Ocorreu um erro inesperado.')
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Ops! Ocorreu um erro inesperado.',
        )


async def get_product_count(user_id: UUID, session: AsyncSession) -> int:
    stmt = select(func.count(Product.id)).where(Product.user_id == user_id)
    result = await session.scalar(stmt)

    if not result:
        return 0

    return result


async def find_all_products(
    user_id: UUID, session: AsyncSession, limit: int = 10, page: int = 0
):
    stmt = (
        select(Product)
        .where(Product.user_id == user_id)
        .limit(limit)
        .offset((page - 1) * limit)
        .order_by(Product.name)
    )
    result = await session.execute(stmt)
    products = result.scalars().all()

    data = [
        ProductGet(
            id=product.id,
            name=product.name,
            description=product.description,
            price=f'R$ {h.intcomma(product.price)}',
            price_sale=f'R$ {h.intcomma(product.price_sale)}',
            stock=product.stock,
            image_url=product.image_url,
            brand_name=product.brand.name if product.brand else None,
            category_name=product.category.name if product.category else None,
            barcode=int(product.barcode),
            code_product=product.code_product,
            created_at=h.naturaltime(product.created_at),
            updated_at=h.naturaltime(product.updated_at),
        )
        for product in products
    ]

    total = await get_product_count(user_id, session)

    return ProductListAll(data=data, **pagination(total, page, limit))


async def generate_and_serve_barcode(code: str):
    try:
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, f'{code}.svg')

        rv = BytesIO()
        code = EAN13(code, writer=SVGWriter())

        code.write(rv)

        with open(temp_file, 'wb') as f:
            f.write(rv.getvalue())

        return FileResponse(
            temp_file, media_type='image/svg+xml', filename=f'{code}.svg'
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Erro ao gerar código de barras: {str(e)}',
        )


async def get_product_by_id(product_id: UUID, user_id: UUID, session: AsyncSession):
    stmt = select(Product).where(
        (Product.id == product_id) | (Product.user_id == user_id)
    )
    result = await session.scalar(stmt)

    if not result:
        raise ProductNotFound

    category = await category_service.get_category_by_id(
        result.category_id, user_id, session
    )
    brand = await brand_service.get_brand_by_id(result.brand_id, user_id, session)

    return ProductGet(
        id=result.id,
        name=result.name,
        description=result.description,
        price=f'R$ {h.intcomma(result.price)}',
        price_sale=f'R$ {h.intcomma(result.price_sale)}',
        stock=result.stock,
        image_url=result.image_url,
        brand_name=brand.name,
        category_name=category.name,
        barcode=int(result.barcode),
        code_product=result.code_product,
        created_at=h.naturaltime(result.created_at),
        updated_at=h.naturaltime(result.updated_at),
    )


async def update_image_product(
    product_id: UUID, user_id: UUID, image_product: UploadFile, session: AsyncSession
):
    try:
        stmt = select(Product).where(
            (Product.id == product_id) | (Product.user_id == user_id)
        )
        result = await session.scalar(stmt)

        if not result:
            raise ProductNotFound

        url_image = await save_image(
            image_product, user_id, product_id, update_image=True
        )

        result.image_url = url_image

        await session.commit()

        return ResponseProduct(
            message='Imagem atualizada com sucesso.',
        )
    except HTTPException as e:
        await session.rollback()
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=f'Ops! Ocorreu um erro inesperado. {str(e)}',
        )
