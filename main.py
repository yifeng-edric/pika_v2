import asyncio
import multiprocessing
import platform

import uvicorn
from app.core.logger.logger import logger
from app.factory import (create_app)

# 创建 FastAPI 应用
app = create_app()


# FastAPI 运行函数
def run_fastapi():
    logger.info("Starting uvicorn in main process with 4 workers")
    # 只在非Windows系统上使用uvloop
    loop_type = "uvloop" if platform.system() != "Windows" else "asyncio"
    uvicorn.run("main:app", host="0.0.0.0", port=9580, workers=1, loop=loop_type)


if __name__ == "__main__":
    run_fastapi()
