from http import HTTPStatus
from uuid import UUID

import humanize as h
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.security.hash import get_password_hash
from app.user.exceptions import (
    EmailAlreadyRegisteredException,
    ErrorCreateUserException,
    PhoneNumberAlreadyRegisteredException,
    UserNotFoundException,
)
from app.user.model import User
from app.user.schemas import UserCreate, UserRead, UserResponse, UserUpdate

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
        )

        session.add(result)
        await session.commit()

        return UserResponse(
            message='Usuário criado com sucesso',
        )
    except IntegrityError:
        await session.rollback()
        raise ErrorCreateUserException(
            'Erro ao salvar usuário',
        )
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Erro interno',
        )


async def get_user_by_id(id: UUID | None, session: AsyncSession):
    stmt = select(User).where(User.id == id)
    result = await session.scalar(stmt)

    if not result:
        raise UserNotFoundException('Usuário não encontrado')

    humanize_created_at = h.naturaltime(result.created_at)
    humanize_updated_at = h.naturaltime(result.updated_at)
    response = UserRead(
        id=result.id,
        email=result.email,
        first_name=result.first_name,
        surname=result.surname,
        phone_number=result.phone_number,
        created_at=humanize_created_at,
        updated_at=humanize_updated_at,
    )

    return response


async def update(id: UUID, user: UserUpdate, session: AsyncSession):
    try:
        stmt = select(User).where(User.id == id)
        user_to_update = await session.scalar(stmt)

        if not user_to_update:
            raise UserNotFoundException('Usuário não encontrado')

        if user.email:
            stmt = select(User).where(User.email == user.email)
            existing_email_user = await session.scalar(stmt)

            if existing_email_user:
                if existing_email_user.email == user.email:
                    raise EmailAlreadyRegisteredException(
                        'Email já cadastrado',
                    )

        if user.phone_number:
            stmt = select(User).where(User.phone_number == user.phone_number)
            existing_phone_user = await session.scalar(stmt)

            if existing_phone_user:
                if existing_phone_user.phone_number == user.phone_number:
                    raise PhoneNumberAlreadyRegisteredException(
                        'Telefone já cadastrado',
                    )

        for key, value in user.model_dump(exclude_none=True).items():
            if key == 'password':
                value = get_password_hash(value)
            setattr(user_to_update, key, value)

        await session.commit()

        return UserResponse(
            message='Usuário atualizado com sucesso',
        )
    except IntegrityError:
        await session.rollback()
        raise ErrorCreateUserException(
            'Erro ao atualizar usuário',
        )
