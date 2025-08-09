from pydantic import BaseModel


class ErrorResponse(BaseModel):
    code: int
    message: str
    data: dict


class CustomAPIException(Exception):
    def __init__(self, code: int, message: str, data: dict = None):
        self.code = code
        self.message = message
        self.data = data or {}

    def __str__(self):
        return f"CustomAPIException: {self.code} - {self.message}"
