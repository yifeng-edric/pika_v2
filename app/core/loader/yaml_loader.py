import yaml
from typing import Any, Dict


class YAMLLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> Dict[str, Any]:
        """
        加载并解析 YAML 配置文件。

        返回:
        Dict[str, Any] - 解析后的配置字典。
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            raise RuntimeError(f"无法解析 YAML 文件: {self.file_path}") from e
        except FileNotFoundError:
            raise RuntimeError(f"找不到文件: {self.file_path}")
