import traceback
from pydantic import BaseModel
from typing import Union, Optional
from fastapi import HTTPException
from fastapi.responses import JSONResponse



# 响应模型
class ResponseModel(BaseModel):
    code: int
    message: str
    data: Optional[Union[dict, list, str, None]] = None

    class Config:
        # Pydantic的配置，确保在数据转换为JSON时，使用的是蛇形命名
        alias_generator = lambda s: s.lower()

    @classmethod
    def create_response(
            cls,
            code: int,
            message: str,
            data: Optional[Union[dict, list, str, None]] = None,
    ) -> "ResponseModel":
        """
        创建统一响应格式
        """
        return cls(code=code, message=message, data=data)

    @classmethod
    def success(cls, data: Optional[Union[dict, list, str, None]] = None) -> "ResponseModel":
        """
        生成成功响应
        """
        return cls.create_response(
            code=ErrorCodes.SUCCESS.value,
            message=ErrorMessages.SUCCESS,
            data=data,
        )

    @classmethod
    def error(
            cls,
            code: int,
            message: str,
            data: Optional[Union[dict, list, str, None]] = None
    ) -> "ResponseModel":
        """
        生成错误响应
        """
        return cls.create_response(
            code=code,
            message=message,
            data=data
        )

    @classmethod
    def handle_http_exception(cls, exc: HTTPException) -> JSONResponse:
        """
        处理HTTPException并返回JSONResponse，统一格式
        """
        # 捕获详细的错误堆栈信息
        error_message = f"{str(exc.detail)}\n{traceback.format_exc()}" if isinstance(exc.detail, Exception) else str(exc.detail)

        # 统一格式的错误信息
        return JSONResponse(
            status_code=exc.status_code,
            content=cls.create_response(
                code=exc.status_code,
                message=error_message,  # 错误信息与堆栈信息放入message中
                data=None,  # data 字段可以是其他上下文或为空
            ).dict(),
        )

# 在应用中添加异常处理器，用来处理HTTPException
from fastapi import FastAPI

app = FastAPI()

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc: HTTPException):
    return ResponseModel.handle_http_exception(exc)
