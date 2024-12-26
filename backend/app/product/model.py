from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import DECIMAL, ForeignKey, String, func, sql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import table_registry


@table_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'tb_products'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        index=True,
        init=False,
        default_factory=uuid4,
        nullable=False,
        server_default=func.gen_random_uuid(),
        unique=True,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    price_sale: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False)
    code_product: Mapped[str] = mapped_column(String(8), nullable=False, unique=True)
    barcode: Mapped[str] = mapped_column(String(13), nullable=False, unique=True)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('tb_users.id'), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        nullable=False,
        init=False,
        index=True,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        nullable=False,
        init=False,
        onupdate=func.now(),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
    brand: Mapped['Brand'] = relationship(  # noqa: F821 # type: ignore
        'Brand', back_populates='products', init=False, lazy='selectin'
    )
    user: Mapped['User'] = relationship(  # noqa: F821 # type: ignore
        'User', back_populates='products', init=False, lazy='selectin'
    )
    category: Mapped['Category'] = relationship(  # noqa: F821 # type: ignore
        'Category', back_populates='products', init=False, lazy='selectin'
    )
    image_url: Mapped[str | None] = mapped_column(
        nullable=True,
        default=None,
        server_default=sql.expression.null(),
    )
    brand_id: Mapped[UUID | None] = mapped_column(
        ForeignKey('tb_brands.id'),
        nullable=True,
        index=True,
        default=None,
        server_default=sql.expression.null(),
    )
    category_id: Mapped[UUID | None] = mapped_column(
        ForeignKey('tb_categories.id'),
        nullable=True,
        index=True,
        default=None,
        server_default=sql.expression.null(),
    )
