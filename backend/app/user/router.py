from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import services as auth_services
from app.database import get_session
from app.user import service as user_service
from app.user.model import User
from app.user.schemas import ClientResponse, ClientUpdate, UserCreate

router = APIRouter(tags=['User'], prefix='/users')
Session = Annotated[AsyncSession, Depends(get_session)]
CurrentClient = Annotated[User, Depends(auth_services.check_user_access)]
AdminUser = Annotated[User, Depends(auth_services.check_admin_role)]


@router.post('/create/', status_code=HTTPStatus.CREATED, response_model=ClientResponse)
async def create_user(user: UserCreate, current_user: AdminUser, session: Session):
    return await user_service.store(user, session)


@router.patch('/update/', status_code=HTTPStatus.OK, response_model=ClientResponse)
async def update_user(
    client: ClientUpdate, current_user: CurrentClient, session: Session
):
    return await user_service.update(current_user.id, client, session)
