from app.core.logger.logger import logger
from app.core.types.errors.hosting_error import HostingException


class ReflectUtils:
    @staticmethod
    def call_by_name(obj, method_name, *args, **kwargs):
        try:
            method = getattr(obj, method_name)
            if callable(method):
                return method(*args, **kwargs)
            else:
                raise AttributeError(f"{method_name} is not callable")
        except HostingException:
            raise  # 不处理 hosting 业务的异常
        except AttributeError as e:
            logger.error(f"AttributeError: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

    @staticmethod
    async def acall_by_name(obj, method_name, *args, **kwargs):
        try:
            method = getattr(obj, method_name)
            if callable(method):
                return await method(*args, **kwargs)
            else:
                raise AttributeError(f"{method_name} is not callable")
        except HostingException:
            raise  # 不处理 hosting 业务的异常
        except AttributeError as e:
            logger.error(f"AttributeError: {e}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
