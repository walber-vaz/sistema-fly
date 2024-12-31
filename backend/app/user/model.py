from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import table_registry
from app.utils import RoleEnum


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'tb_users'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        index=True,
        init=False,
        default_factory=uuid4,
        nullable=False,
        server_default=func.gen_random_uuid(),
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(200), index=True, nullable=False, unique=True
    )
    phone_number: Mapped[str] = mapped_column(String(12), nullable=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum),
        nullable=False,
        default=RoleEnum.CUSTOMER.value,
        server_default=RoleEnum.CUSTOMER.name,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True, nullable=False, index=True, server_default='true'
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
    client: Mapped['Client'] = relationship(
        'Client', back_populates='user', init=False, uselist=False
    )


@table_registry.mapped_as_dataclass
class Client:
    __tablename__ = 'tb_clients'

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        index=True,
        init=False,
        default_factory=uuid4,
        nullable=False,
        server_default=func.gen_random_uuid(),
        unique=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('tb_users.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
        unique=True,
    )
    company_name: Mapped[str] = mapped_column(String(100), nullable=False)
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
    user: Mapped['User'] = relationship('User', back_populates='client', init=False)
    brands: Mapped[list['Brand']] = relationship(  # noqa: F821 # type: ignore
        'Brand', back_populates='client', init=False, lazy='selectin'
    )
    categories: Mapped[list['Category']] = relationship(  # noqa: F821 # type: ignore
        'Category', back_populates='client', init=False, lazy='selectin'
    )
    products: Mapped[list['Product']] = relationship(  # noqa: F821 # type: ignore
        'Product', back_populates='client', init=False, lazy='selectin'
    )
