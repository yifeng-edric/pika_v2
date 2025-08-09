import asyncio
import importlib
import inspect
import pkgutil

from aiohttp import web
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from app.api.api_load import api_router
from app.config.config import config
from app.core.logger.logger import logger
from app.core.types.errors.base_error import base_error_handler
from app.core.types.errors.hosting_error import HostingException, hosting_exception_handler
from app.common.database import DatabaseClient
from app.common.redis import RedisClient
from app.core.types.errors.http_error import http_error_handler
from app.core.types.errors.validation_error import http422_error_handler


async def start_redis():
    redis_client = RedisClient(
        config.REDIS.REDIS_HOST,
        config.REDIS.REDIS_PORT,
        config.REDIS.REDIS_DB,
        config.REDIS.REDIS_PASSWD,
    )
    await redis_client.connect()


async def start_app(app: FastAPI) -> None:
    await start_redis()
    db_client = DatabaseClient(
        config.MYSQL.db_url,
        config.MYSQL.tortoise_modules,
    )
    await db_client.register_to_app(app)


def create_app():
    description = f"{config.PROJECT_NAME} API"
    app = FastAPI(
        title=config.PROJECT_NAME,
        openapi_url=f"{config.API_PATH}/openapi.json",
        docs_url="/docs/",
        description=description,
        redoc_url=None,
    )

    # 使用装饰器注册启动事件处理器
    @app.on_event("startup")
    async def on_startup():
        await start_app(app)

    setup_routers(app)
    setup_cors_middleware(app)
    setup_exception_handler(app)
    return app


def setup_routers(app: FastAPI):
    app.include_router(api_router, prefix=config.API_PATH)


def setup_cors_middleware(app):
    if config.CORS.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in config.CORS.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            expose_headers=["Content-Range", "Range"],
            allow_headers=["Authorization", "Range", "Content-Range"],
        )


def setup_exception_handler(app):
    app.add_exception_handler(HostingException, hosting_exception_handler)
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.add_exception_handler(Exception, base_error_handler)
