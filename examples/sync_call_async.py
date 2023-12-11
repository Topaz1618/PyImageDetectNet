"""
非阻塞启动进程调用同步函数，并在这个同步函数中调用 async 异步函数

Launching a process that invokes a synchronous function, which calls an asynchronous function.

"""

import asyncio
import multiprocessing
from time import sleep


# 异步方法
async def async_task():
    print("Async task running")
    while True:
        print("Aaaa")
        sleep(1)
    await asyncio.sleep(1)
    print("Async task completed")


# 进程函数，用于启动异步方法
def process_function():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_task())


if __name__ == "__main__":
    # 创建一个新的进程，传入进程函数作为目标函数
    process = multiprocessing.Process(target=process_function)

    # 启动进程
    process.start()
    print("Main process start")
    # 等待进程执行完成
    process.join()

    print("Main process completed")