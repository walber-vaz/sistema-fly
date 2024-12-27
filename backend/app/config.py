from pathlib import Path

import tomllib
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import Environment

PROJECT_DIR = Path(__file__).parent.parent
with open(f'{PROJECT_DIR}/pyproject.toml', 'rb') as f:
    PYPROJECT_CONTENT = tomllib.load(f)['tool']['poetry']


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', extra='allow', case_sensitive=True
    )

    BASE_URL_API: HttpUrl = 'http://localhost:8000'
    SENTRY_DSN: HttpUrl | None = None
    ENVIRONMENT: Environment = Environment.LOCAL
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_DAY: int
    JWT_ISSUER: str
    JWT_AUDIENCE: str

    PROJECT_NAME: str = PYPROJECT_CONTENT['name']
    VERSION: str = PYPROJECT_CONTENT['version']
    DESCRIPTION: str = PYPROJECT_CONTENT['description']

    API_PREFIX: str = '/v1'


settings: Settings = Settings()  # type: ignore
