from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        content={
            "code": exc.status_code,
            "message": "",
            "data": {"errors": [exc.detail]},
        },
        status_code=exc.status_code,
    )
