import os
from typing import List

from pydantic_settings import BaseSettings

from app.core.loader.yaml_loader import YAMLLoader


class CorsConf(BaseSettings):
    CORS_CONF_PATH: str
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    def __init__(self, path=os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "..")), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CORS_CONF_PATH = path + self.CORS_CONF_PATH
        yaml_loader = YAMLLoader(self.CORS_CONF_PATH)
        try:
            res = yaml_loader.load()['BACKEND_CORS_ORIGINS']
            self.BACKEND_CORS_ORIGINS = res if res else ["*"]
        except Exception:
            self.BACKEND_CORS_ORIGINS = ["*"]
