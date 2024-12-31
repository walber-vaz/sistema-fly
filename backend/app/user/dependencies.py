from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.exceptions import (
    EmailAlreadyRegisteredException,
    PhoneNumberAlreadyRegisteredException,
    UserNotFoundException,
)
from app.user.model import Client, User
from app.user.schemas import ClientUpdate


async def validate_email_phone(client: ClientUpdate, session: AsyncSession):
    if client.email:
        stmt = select(User).where(User.email == client.email)
        existing_email_user = await session.scalar(stmt)
        if existing_email_user and existing_email_user.email == client.email:
            raise EmailAlreadyRegisteredException(
                'Email já cadastrado',
            )

    if client.phone_number:
        stmt = select(User).where(User.phone_number == client.phone_number)
        existing_phone_user = await session.scalar(stmt)
        if (
            existing_phone_user
            and existing_phone_user.phone_number == client.phone_number
        ):
            raise PhoneNumberAlreadyRegisteredException(
                'Telefone já cadastrado',
            )


async def return_data_client_user(id: UUID, session: AsyncSession):
    stmt_client = select(Client).where(Client.id == id)
    result_client = await session.scalar(stmt_client)

    if not result_client:
        raise UserNotFoundException('Cliente não encontrado')

    stmt = select(User).where(User.id == result_client.user_id)
    result = await session.scalar(stmt)

    if not result:
        raise UserNotFoundException('Cliente não encontrado')

    return result_client, result
