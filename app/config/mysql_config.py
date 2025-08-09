from pydantic_settings import BaseSettings


class MySQLConf(BaseSettings):

    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int

    @property
    def db_url(self) -> str:
        return f"mysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    @property
    def tortoise_modules(self) -> dict:
        # 这里可以基于某些条件动态定义模型
        return {
            "models": [
                "app.models.pilot_basic_token_info",
                "app.models.pilot_expand_token_info",
                "app.models.memebox_token",
                "app.models.pilot_chain_info",
            ]
        }

    # 其他配置和方法