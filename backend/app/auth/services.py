from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions import NotAuthenticatedException, PermissionDeniedException
from app.auth.schemas import Login, Token, TokenData
from app.config import settings
from app.database import get_session
from app.security.hash import verify_password
from app.security.jwt import create_access_token, decode_token
from app.user import service as user_services
from app.user.model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_PREFIX}/auth/login')


async def get_current_user(
    session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)
):
    try:
        payload = decode_token(token)

        if not payload:
            raise NotAuthenticatedException()

        user_id: UUID = payload.get('sub')
        if not user_id:
            raise NotAuthenticatedException()

        token_data = TokenData(id=user_id)
    except DecodeError:
        raise NotAuthenticatedException()

    result = await user_services.get_user_by_id(token_data.id, session)

    if not result:
        raise NotAuthenticatedException()

    return result


async def login(data: Login, session: AsyncSession) -> Token:
    try:
        stmt = select(User).where(User.email == data.username)
        result = await session.scalar(stmt)

        if not result:
            raise PermissionDeniedException('Email ou senha inválidos')

        if not verify_password(data.password, result.password):
            raise PermissionDeniedException('Email ou senha inválidos')

        token = create_access_token({'sub': str(result.id)})

        return Token(access_token=token, token_type='bearer')
    except Exception as e:
        raise PermissionDeniedException('Email ou senha inválidos') from e
