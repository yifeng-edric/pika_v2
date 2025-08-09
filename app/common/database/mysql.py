from app.core import SingletonMeta
from app.common.database import DatabaseClient


class MySQL(DatabaseClient, metaclass=SingletonMeta):
    def __init__(self, db_url: str, modules: dict, generate_schemas: bool = False):
        super().__init__(db_url, modules, generate_schemas)