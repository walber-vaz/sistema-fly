from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.user.model import User
from app.utils import RoleEnum


def seed_superuser(session: Session) -> None:
    user = session.execute(
        select(User).where(User.email == settings.ADMIN_USER['email'])
    ).first()

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
        session.commit()
