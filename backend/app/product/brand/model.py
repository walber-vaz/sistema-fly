from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import table_registry


@table_registry.mapped_as_dataclass
class Brand:
    __tablename__ = 'tb_brands'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        index=True,
        init=False,
        default_factory=uuid4,
        nullable=False,
        server_default=func.gen_random_uuid(),
        unique=True,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    client_id: Mapped[UUID] = mapped_column(
        ForeignKey('tb_clients.id'), nullable=False, index=True
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
    client: Mapped['Client'] = relationship(  # noqa: F821 # type: ignore
        'Client', back_populates='brands', init=False, lazy='selectin'
    )
    products: Mapped[list['Product']] = relationship(  # noqa: F821 # type: ignore
        'Product',
        back_populates='brand',
        init=False,
        cascade='all, delete-orphan',
    )
