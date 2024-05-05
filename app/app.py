import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import redis.asyncio as aioredis
import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.services import redis
from app.settings import app_settings, redis_settings
from app.tasks.router import router as notes_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    logger.info(f"lifespan: starting redis_client at {redis_settings.REDIS_URL}")
    pool = aioredis.ConnectionPool.from_url(
        str(redis_settings.REDIS_URL), max_connections=10, decode_responses=True
    )

    redis.redis_client = aioredis.Redis(connection_pool=pool)

    yield

    if app_settings.ENVIRONMENT.is_testing:
        return

    logger.info("lifespan: clossing redis_client")

    await pool.disconnect()


app = FastAPI(
    **app_settings.model_dump(),
    lifespan=lifespan,
    debug=app_settings.ENVIRONMENT.is_debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.CORS_ORIGINS,
    allow_origin_regex=app_settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=app_settings.CORS_HEADERS,
)

if app_settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=app_settings.SENTRY_DSN,
        environment=app_settings.ENVIRONMENT,
    )


@app.get("/status")
async def status():
    logger.info("status")
    return {"status": "ok"}


app.include_router(notes_router, prefix="/tasks", tags=["tasks"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
