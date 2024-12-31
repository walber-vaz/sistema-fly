import logging
from http import HTTPStatus
from uuid import UUID

import humanize as h
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.security.hash import get_password_hash
from app.user.dependencies import return_data_client_user, validate_email_phone
from app.user.exceptions import (
    EmailAlreadyRegisteredException,
    ErrorCreateUserException,
    PhoneNumberAlreadyRegisteredException,
)
from app.user.model import Client, User
from app.user.schemas import (
    ClientGetData,
    ClientRead,
    ClientUpdate,
    UserCreate,
    UserRead,
    UserResponse,
)
from app.utils import RoleEnum

logger = logging.getLogger(__name__)
h.activate('pt_BR')


async def store(user: UserCreate, session: AsyncSession):
    try:
        stmt = select(User).where(
            (User.email == user.email) | (User.phone_number == user.phone_number)
        )
        result = await session.scalar(stmt)

        if result:
            if result.email == user.email:
                raise EmailAlreadyRegisteredException(
                    'Email já cadastrado',
                )
            elif result.phone_number == user.phone_number:
                raise PhoneNumberAlreadyRegisteredException(
                    'Telefone já cadastrado',
                )

        pwd_hash = get_password_hash(user.password)
        result = User(
            email=user.email,
            first_name=user.first_name,
            surname=user.surname,
            phone_number=user.phone_number,
            password=pwd_hash,
            role=user.role,
            is_active=user.is_active,
        )

        session.add(result)
        session.flush()

        client = Client(
            user_id=result.id,
            company_name=user.company_name,
        )

        session.add(client)
        await session.commit()

        return UserResponse(
            message='Usuário criado com sucesso',
        )
    except IntegrityError:
        await session.rollback()
        raise ErrorCreateUserException(
            'Erro ao salvar usuário',
        )
    except HTTPException as e:
        logger.error(e)
        raise e
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Erro interno',
        )


async def get_user_by_id(id: UUID | None, session: AsyncSession):
    _, result = await return_data_client_user(id, session)

    humanize_created_at = h.naturaltime(result.created_at)
    humanize_updated_at = h.naturaltime(result.updated_at)
    user = UserRead(
        email=result.email,
        first_name=result.first_name,
        surname=result.surname,
        phone_number=result.phone_number,
        created_at=humanize_created_at,
        updated_at=humanize_updated_at,
    )

    client = ClientRead(
        id=result.client.id,
        company_name=result.client.company_name,
        created_at=humanize_created_at,
        updated_at=humanize_updated_at,
    )

    response = ClientGetData(
        id=client.id,
        company_name=client.company_name,
        email=user.email,
        first_name=user.first_name,
        surname=user.surname,
        phone_number=user.phone_number,
        created_at=client.created_at,
        updated_at=client.updated_at,
    )

    return response


async def update(id: UUID, client: ClientUpdate, session: AsyncSession):
    try:
        result_client, result = await return_data_client_user(id, session)

        await validate_email_phone(client, session)

        for key, value in client.model_dump(exclude_none=True).items():
            if key == 'password':
                value = get_password_hash(value)
            if key == 'company_name':
                setattr(result_client, key, value)
            if key == 'role':
                if value not in RoleEnum:
                    raise ValueError('Role não existe')
            setattr(result, key, value)

        await session.commit()

        return UserResponse(
            message='Usuário atualizado com sucesso',
        )
    except IntegrityError:
        await session.rollback()
        raise ErrorCreateUserException(
            'Erro ao atualizar usuário',
        )
