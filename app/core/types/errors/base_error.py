from starlette.requests import Request
from starlette.responses import JSONResponse


async def base_error_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        content={
            "code": 500,
            "message": "",
            "data": {"errors": str(exc)},
        },
        status_code=500,
    )
