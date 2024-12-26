from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import services as auth_services
from app.auth.schemas import Token
from app.database import get_session
from app.security.jwt import create_access_token
from app.user.model import User
from app.user.schemas import UserReadMe

router = APIRouter(tags=['Auth'], prefix='/auth')
Session = Annotated[AsyncSession, Depends(get_session)]


@router.post('/login/', response_model=Token, status_code=HTTPStatus.OK)
async def login(session: Session, data: OAuth2PasswordRequestForm = Depends()) -> Token:
    return await auth_services.login(data, session)


@router.post('/refresh/', response_model=Token, status_code=HTTPStatus.OK)
async def refresh_token(user: User = Depends(auth_services.get_current_user)):
    token = create_access_token({'sub': str(user.id)})

    return Token(access_token=token, token_type='bearer')


@router.get('/me/', response_model=UserReadMe, status_code=HTTPStatus.OK)
async def me(
    session: Session, user: User = Depends(auth_services.get_current_user)
) -> UserReadMe:
    return UserReadMe(
        first_name=user.first_name,
        surname=user.surname,
        email=user.email,
        phone_number=user.phone_number,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
