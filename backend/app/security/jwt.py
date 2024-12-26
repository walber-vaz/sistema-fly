from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import DecodeError, decode, encode

from app.config import settings


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        days=settings.JWT_ACCESS_TOKEN_EXPIRE_DAY
    )
    to_encode.update({
        'exp': expire,
        'iss': settings.JWT_ISSUER,
        'aud': settings.JWT_AUDIENCE,
    })
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
        )
        return payload
    except DecodeError:
        return None
