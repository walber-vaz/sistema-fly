from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class Login(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    id: UUID | None = None
