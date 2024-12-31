import re

from pydantic import UUID4, BaseModel, EmailStr, field_validator

from app.user.exceptions import (
    LengthFirstNameException,
    LengthPhoneException,
    LengthSurnameException,
    PasswordRequirementsException,
)
from app.utils import RoleEnum


class ClientBase(BaseModel):
    user_id: UUID4
    company_name: str


class ClientCreate(ClientBase):
    @field_validator('company_name')
    @classmethod
    def validate_company_name(cls, v: str):
        if len(v) > 100 or len(v) < 2:
            raise LengthPhoneException(
                'Nome da empresa deve ter entre 2 e 100 caracteres'
            )
        return v.strip()


class ClientRead(BaseModel):
    id: UUID4
    company_name: str
    created_at: str
    updated_at: str


class ClientGetData(BaseModel):
    id: UUID4
    company_name: str
    first_name: str
    surname: str
    email: EmailStr
    phone_number: str
    created_at: str
    updated_at: str


class UserBase(BaseModel):
    first_name: str
    surname: str
    email: EmailStr
    password: str
    phone_number: str
    role: RoleEnum = RoleEnum.CUSTOMER
    is_active: bool = True


class UserRead(BaseModel):
    first_name: str
    surname: str
    email: EmailStr
    phone_number: str
    created_at: str
    updated_at: str


class UserReadMe(BaseModel):
    first_name: str
    surname: str
    email: EmailStr
    phone_number: str
    created_at: str
    updated_at: str


class ClientUpdate(BaseModel):
    first_name: str | None = None
    company_name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    password: str | None = None
    is_active: bool | None = None
    role: RoleEnum | None = None


class UserCreate(UserBase):
    @field_validator('first_name')
    @classmethod
    def validate_first_name(cls, v: str):
        if len(v) > 50 or len(v) < 2:
            raise LengthFirstNameException(
                'Primeiro nome deve ter entre 2 e 50 caracteres'
            )
        return v.capitalize().strip()

    @field_validator('surname')
    @classmethod
    def validate_surname(cls, v: str):
        if len(v) > 50 or len(v) < 2:
            raise LengthSurnameException('Sobrenome deve ter entre 2 e 50 caracteres')
        return v.capitalize().strip()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str):
        if not re.match(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9\s]).{8,32}$',
            v,
        ):
            raise PasswordRequirementsException(
                'Senha deve ter entre 8 e 32 caracteres, conter letras maiúsculas, minúsculas, números e caracteres especiais'  # noqa
            )
        return v.strip()

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v: str):
        if v.isdigit() and len(v) < 12:
            raise LengthPhoneException('Telefone deve ter 12 caracteres')

        return v.strip()


class UserResponse(BaseModel):
    message: str
