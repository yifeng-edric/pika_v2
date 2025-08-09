from typing import Union

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .codes import get_error_message
from .exceptions import ErrorResponse, CustomAPIException


async def custom_error_handler(_: Request, exc: Union[
    CustomAPIException, HTTPException, RequestValidationError, ValidationError]) -> JSONResponse:
    if isinstance(exc, (RequestValidationError, ValidationError)):
        code = HTTP_422_UNPROCESSABLE_ENTITY
        message = get_error_message(HTTP_422_UNPROCESSABLE_ENTITY)
        errors = exc.errors()
    elif isinstance(exc, HTTPException):
        code = exc.status_code
        message = exc.detail
        errors = [exc.detail]
    else:
        code = exc.code
        message = exc.message
        errors = exc.data.get("errors", [])

    return JSONResponse(
        content=ErrorResponse(
            code=code,
            message=message,
            data={"errors": errors}
        ).model_dump(),
        status_code=code,
    )
