import asyncio
import time
from functools import wraps
from loguru import logger
from httpx import RequestError

from app.config.config import config

# 设置日志输出到文件，每天轮换，并且压缩
logger.add(config.LOG_PATH,
           # 设置日志输出到文件，每天轮换，并且压缩
           rotation="00:00",  # 每天凌晨轮换日志
           retention="7 days",  # 保留7天的日志文件
           compression="zip",  # 压缩日志文件为zip格式
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
           level="DEBUG",  # 默认记录DEBUG及以上级别的日志
           enqueue=True)  # 支持多线程/多进程环境中的日志输出


def log_call(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            logger.info(f"Calling async '{func.__name__}' with args: {args[1:]}, kwargs: {kwargs}")
            result = await func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f"Async '{func.__name__}' after {elapsed_time:.2f} seconds")
            return result

        except RequestError as e:
            error_message = f"Network error in async '{func.__name__}'"
            logger.exception(error_message)
            raise RuntimeError(f"{error_message}: {e}") from e
        except Exception as e:
            error_message = f"Error in async '{func.__name__}'"
            logger.exception(error_message)
            raise RuntimeError(f"{error_message}: {e}") from e

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            logger.info(f"Calling '{func.__name__}' with args: {args[1:]}, kwargs: {kwargs}")
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f"'{func.__name__}' after {elapsed_time:.2f} seconds")
            return result
        except RequestError as e:
            error_message = f"Network error in '{func.__name__}'"
            logger.exception(error_message)
            raise RuntimeError(f"{error_message}: {e}") from e
        except Exception as e:
            error_message = f"Error in '{func.__name__}'"
            logger.exception(error_message)
            raise RuntimeError(f"{error_message}: {e}") from e

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
