from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_502_BAD_GATEWAY,
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_504_GATEWAY_TIMEOUT,
)

ERROR_MESSAGES = {
    HTTP_200_OK: "Success",
    HTTP_400_BAD_REQUEST: "Bad Request",
    HTTP_401_UNAUTHORIZED: "Unauthorized",
    HTTP_403_FORBIDDEN: "Forbidden",
    HTTP_404_NOT_FOUND: "Not Found",
    HTTP_422_UNPROCESSABLE_ENTITY: "Unprocessable Entity",
    HTTP_429_TOO_MANY_REQUESTS: "Request Limit Exceeded",
    HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
    HTTP_502_BAD_GATEWAY: "Bad Gateway",
    HTTP_503_SERVICE_UNAVAILABLE: "Service Unavailable",
    HTTP_504_GATEWAY_TIMEOUT: "Gateway Timeout",
}


def get_error_message(status_code: int) -> str:
    return ERROR_MESSAGES.get(status_code, "Unknown Error")
