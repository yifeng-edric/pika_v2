import os
from typing import List

from loguru import logger
from pydantic import model_validator
from pydantic_settings import BaseSettings

from app.config.cors_config import CorsConf
from app.config.mysql_config import MySQLConf
from app.config.redis_config import RedisConf


class Config(BaseSettings):
    PROJECT_NAME: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SERVICE_HOST: str
    REDIS: RedisConf = RedisConf()
    MYSQL: MySQLConf = MySQLConf()
    WORK_PATH: str = ""
    CORS: CorsConf = CorsConf()
    API_PATH: str
    LOG_PATH: str = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        self.WORK_PATH = os.path.abspath(os.path.join(current_directory, '..', '..'))
        self.LOG_PATH: str = self.WORK_PATH + "/../logs/skeleton.logs"
        self.REDIS = RedisConf()
        self.MYSQL = MySQLConf()


# 通过环境变量或 .env 文件加载配置
config = Config()

if __name__ == "__main__":
    print(config)
