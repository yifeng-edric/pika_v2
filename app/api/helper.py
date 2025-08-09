from typing import Any
from fastapi import APIRouter
from app.common.redis import RedisClient
from app.core.logger.logger import logger

router = APIRouter(tags=["helper"])


@router.get("/readiness")
async def test_hello_world() -> Any:
    return {"welcome"}

@router.get("/health")
async def test_health() -> Any:
    return {"welcome"}

@router.get("/redis-check")
async def test_redis():
    await RedisClient.get_redis().set("hello", "world")
    world = await RedisClient.get_redis().get("hello")
    logger.info(f"redis: {world}")
    return {"msg": f"redis: {world}"}
