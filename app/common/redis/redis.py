import asyncio
import redis.asyncio as redis
from app.core.logger.logger import logger
from app.core import SingletonMeta


class RedisClient(metaclass=SingletonMeta):
    def __init__(self, url, port, db, passwd):
        self.redis = None
        self.redis_url = f"redis://{url}:{port}"
        self.db = db
        self.passwd = passwd

    @staticmethod
    def get_redis() -> "RedisClient":
        instance = SingletonMeta._instances.get(RedisClient, None)
        if instance is None:
            logger.error(f"redis not connected")
            raise Exception(f"redis not connected")
        return instance

    def is_connected(self):
        return self.redis is not None

    async def connect(self):
        try:
            if self.redis is None:
                self.redis = await  redis.Redis.from_url(
                    self.redis_url, db=self.db, password=self.passwd, encoding="utf-8"
                )
                logger.info(f"REDIS: connect {self.redis_url}")
        except Exception as e:
            logger.error(f"REDIS: connect {self.redis_url} error: {e}")
            raise e

    async def close(self):
        try:
            if self.redis is not None:
                await self.redis.close()
                self.redis = None
                logger.info(f"REDIS: close {self.redis_url}")
        except Exception as e:
            self.redis = None
            logger.error(f"REDIS: close {self.redis_url} error: {e}")
            raise e

    # 以下是对其他方法的更新，例如：
    async def set(self, key, value):
        try:
            res = await self.redis.set(key, value)
            logger.info(f"REDIS: set {key} {value}")
            return res
        except Exception as e:
            logger.error(f"REDIS: set {key} {value} error: {e}")
            raise e

    async def setex(self, name, time, value):
        try:
            await self.redis.setex(name, time, value)
            # logger.info(f"REDIS: setex {name} {time} {value}")
        except Exception as e:
            logger.error(f"REDIS: setex {name} {time} {value} error: {e}")
            raise e

    async def get(self, key):
        try:
            value = await self.redis.get(key)
            # logger.info(f"REDIS: get {key} {value}")
            return value
        except Exception as e:
            logger.error(f"REDIS: get {key} error: {e}")
            raise e

    async def delete(self, key):
        try:
            res = await self.redis.delete(key)  # 使用 delete 方法
            logger.info(f"REDIS: delete {key}")
            return res
        except Exception as e:
            logger.error(f"REDIS: delete {key} error: {e}")
            raise e  # 确保重新抛出异常

    async def exists(self, key):
        try:
            result = await self.redis.exists(key)
            logger.info(f"REDIS: exists {key}")
            return result
        except Exception as e:
            logger.error(f"REDIS: exists {key} error: {e}")
            raise e

    async def blpop(self, key):
        try:
            result = await self.redis.blpop(key, timeout=0)
            logger.info(f"REDIS: blpop {key}")
            return result
        except Exception as e:
            logger.error(f"REDIS: blpop {key} error: {e}")
            raise e

    async def rpush(self, key, value):
        try:
            result = await self.redis.rpush(key, value)
            logger.info(f"REDIS: rpush {key} {value}")
            return result
        except Exception as e:
            logger.error(f"REDIS: rpush {key} {value} error: {e}")
            raise e

    async def expire(self, key, expire):
        try:
            res = await self.redis.expire(key, expire)
            logger.info(f"REDIS: expire {key} {expire}")
            return res
        except Exception as e:
            logger.error(f"REDIS: expire {key} {expire} error: {e}")
            raise e

    async def hset(self, map_name, key, value):
        try:
            res = await self.redis.hset(map_name, key, value)
            logger.info(f"REDIS: hset {map_name} {key} {value}")
            return res
        except Exception as e:
            logger.error(f"REDIS: hset {map_name} {key} {value} error: {e}")
            raise e

    async def hget(self, map_name, key):
        try:
            value = await self.redis.hget(map_name, key)
            logger.info(f"REDIS: hget {map_name} {key}")
            return value
        except Exception as e:
            logger.error(f"REDIS: hget {map_name} {key} error: {e}")
            raise e

    async def hdel(self, map_name, key):
        try:
            res = await self.redis.hdel(map_name, key)
            logger.info(f"REDIS: hdel {map_name} {key}")
            return res
        except Exception as e:
            logger.error(f"REDIS: hdel {map_name} {key} error: {e}")
            raise e

    async def hgetall(self, map_name):
        try:
            value = await self.redis.hgetall(map_name)
            logger.info(f"REDIS: hgetall {map_name}")
            return value
        except Exception as e:
            logger.error(f"REDIS: hgetall {map_name} error: {e}")
            raise e

    async def hexists(self, map_name, key):
        try:
            result = await self.redis.hexists(map_name, key)
            logger.info(f"REDIS: hexists {map_name} {key}")
            return result
        except Exception as e:
            logger.error(f"REDIS: hexists {map_name} {key} error: {e}")
            raise e

    async def publish(self, channel, message):
        try:
            res = await self.redis.publish(channel, message)
            logger.info(f"REDIS: publish {channel} {message}")
            return res
        except Exception as e:
            logger.error(f"Publish error: {e}")

    async def subscribe(self, channel, callback):
        try:
            pubsub = self.redis.pubsub()
            await pubsub.subscribe(channel)
            logger.info(f"Subscribed to channel: {channel}")
            async for message in pubsub.listen():
                if message["type"] == "message":
                    logger.info(f"Redis received: {message['data']}")
                    stop_flag, res = await callback(message["data"])
                    if stop_flag:
                        await pubsub.unsubscribe(channel)
                        return res
        except Exception as e:
            logger.error(f"Subscribe error: {e}")

    async def unsubscribe(self, channel):
        try:
            pubsub = self.redis.pubsub()
            await pubsub.unsubscribe(channel)
            logger.info(f"Unsubscribed from channel: {channel}")
        except Exception as e:
            logger.error(f"Unsubscribe error: {e}")
            raise e

    async def llen(self, key):
        try:
            length = await self.redis.llen(key)
            logger.info(f"REDIS: llen {key}, result: {length}")
            return length
        except Exception as e:
            logger.error(f"llen error: {e}")
            raise e

    async def lrange(self, key, start, end):
        try:
            range_list = await self.redis.lrange(key, start, end)
            logger.info(f"REDIS: lrange {key} {start} {end}, result: {range_list}")
            return range_list
        except Exception as e:
            logger.error(f"lrange error: {e}")
            raise e


async def main():
    redis_client = RedisClient(
        url="sh-crs-rdx62u2r.sql.tencentcdb.com",
        port="27787",
        db="15",
        passwd="Baixing!2023",
    )
    await redis_client.connect()
    await redis_client.set("111111", "222222x")
    value = await redis_client.get("111111")
    logger.info(value)
    await redis_client.close()


if __name__ == "__main__":
    asyncio.run(main())
