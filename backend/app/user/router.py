from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import services as auth_services
from app.database import get_session
from app.user import service as user_service
from app.user.model import User
from app.user.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(tags=['User'], prefix='/users')
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(auth_services.get_current_user)]


@router.post('/create/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
async def create_user(user: UserCreate, session: Session):
    return await user_service.store(user, session)


@router.patch('/update/', status_code=HTTPStatus.OK, response_model=UserResponse)
async def update_user(user: UserUpdate, current_user: CurrentUser, session: Session):
    return await user_service.update(current_user.id, user, session)
