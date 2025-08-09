from starlette.requests import Request
from starlette.responses import JSONResponse


class HostingException(Exception):
    def __init__(self, _id: str = "null", msg: str = "hosting error"):
        self._id = _id
        self.msg = msg

    def __str__(self) -> str:
        return "{}: {}".format(self._id, self.msg)

    __repr__ = __str__


async def hosting_exception_handler(_: Request, exc: HostingException) -> JSONResponse:
    return JSONResponse(
        content={
            "code": 0,
            "message": exc.__str__(),
        },
        status_code=200,
    )
