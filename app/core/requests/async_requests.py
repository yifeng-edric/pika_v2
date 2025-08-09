import httpx
from typing import Dict
from httpx import HTTPError
from tenacity import wait_random_exponential, stop_after_attempt, retry
from app.core.logger.logger import log_call


class AsyncRequests(object):

    @staticmethod
    @log_call
    @retry(wait=wait_random_exponential(min=1, max=3), stop=stop_after_attempt(3))
    async def request(method, url, timeout=30, *args, **kwargs) -> Dict:
        async with httpx.AsyncClient() as client:
            rsp = await client.request(method, url, timeout=httpx.Timeout(timeout), *args, **kwargs)
            if rsp.status_code != 200:
                raise HTTPError
            data = rsp.json()
            return data

    @staticmethod
    @log_call
    @retry(wait=wait_random_exponential(min=1, max=3), stop=stop_after_attempt(3))
    async def raw_request(method, url, timeout=30, *args, **kwargs):
        # 封装原始 async request
        async with httpx.AsyncClient() as client:
            rsp = await client.request(method, url, timeout=httpx.Timeout(timeout), *args, **kwargs)
            if rsp.status_code != 200:
                raise HTTPError
            return rsp
