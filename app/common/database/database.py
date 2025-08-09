from fastapi import FastAPI

from app.core import SingletonMeta
from app.core.logger.logger import logger
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
import asyncio


class DatabaseClient(metaclass=SingletonMeta):
    def __init__(self, db_url: str, modules: dict, generate_schemas: bool = False):
        self.db_url = db_url
        self.modules = modules
        self.generate_schemas = generate_schemas
        self.initialized = False

    async def connect(self):
        """
        初始化数据库连接（适用于脚本和非FastAPI启动场景）
        """
        if not self.initialized:
            await Tortoise.init(
                db_url=self.db_url,
                modules=self.modules
            )
            if self.generate_schemas:
                await Tortoise.generate_schemas()
            self.initialized = True
            logger.info("Database connected and initialized.")

    async def register_to_app(self, app: FastAPI):
        """
        将 Tortoise ORM 注册到 FastAPI 应用（仅适用于FastAPI启动场景）
        """
        if app is not None and not self.initialized:
            register_tortoise(
                app,
                db_url=self.db_url,
                modules=self.modules,
                generate_schemas=self.generate_schemas,
                add_exception_handlers=True,
            )
            self.initialized = True
            logger.info("Tortoise ORM registered to FastAPI app.")

    @staticmethod
    def get_db() -> "DatabaseClient":
        instance = SingletonMeta._instances.get(DatabaseClient, None)
        if instance is None:
            logger.error("Database not connected")
            raise Exception("Database not connected")
        return instance

    def is_connected(self):
        return self.initialized

    async def close(self):
        """
        关闭数据库连接
        """
        await Tortoise.close_connections()
        self.initialized = False
        logger.info("Database connections closed.")


# 使用示例
async def main():
    db_url = "database://user:password@localhost:3306/dbname"
    modules = {"models": ["your_app.models"]}
    tortoise_client = DatabaseClient(db_url, modules, generate_schemas=True)
    await tortoise_client.connect()
    # 进行数据库操作
    await tortoise_client.close()


if __name__ == "__main__":
    asyncio.run(main())
