import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.auth.router import router as auth_router
from app.config import settings
from app.constants import Environment
from app.product.brand.router import router as brand_router
from app.product.category.router import router as category_router
from app.product.router import router as product_router
from app.user.router import router as user_router

if settings.SENTRY_DSN and settings.ENVIRONMENT == Environment.PRODUCTION:
    sentry_sdk.init(str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url=None if settings.ENVIRONMENT == Environment.PRODUCTION else '/docs',
    redoc_url=None if settings.ENVIRONMENT == Environment.PRODUCTION else '/redoc',
    openapi_url=(
        None
        if settings.ENVIRONMENT == Environment.PRODUCTION
        else f'{settings.API_PREFIX}/openapi.json'
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.mount(
    f'{settings.BASE_URL_API}/static', StaticFiles(directory='static'), name='static'
)
app.include_router(user_router, prefix=settings.API_PREFIX)
app.include_router(auth_router, prefix=settings.API_PREFIX)
app.include_router(product_router, prefix=settings.API_PREFIX)
app.include_router(category_router, prefix=settings.API_PREFIX)
app.include_router(brand_router, prefix=settings.API_PREFIX)
