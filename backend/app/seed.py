from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.user.model import User
from app.utils import RoleEnum


async def seed_superuser(session: AsyncSession) -> None:
    stmt = select(User).where(User.email == settings.ADMIN_USER['email'])
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            first_name=settings.ADMIN_USER['first_name'],
            surname=settings.ADMIN_USER['surname'],
            email=settings.ADMIN_USER['email'],
            is_active=True,
            password=settings.ADMIN_USER['password'],
            role=RoleEnum.ADMIN,
            phone_number=settings.ADMIN_USER['phone_number'],
        )

        session.add(user)
        await session.commit()
