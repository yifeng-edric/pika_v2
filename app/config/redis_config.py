from pydantic_settings import BaseSettings


class RedisConf(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWD: str
    REDIS_MESSAGE_EXPIRE: int = 60 * 3
