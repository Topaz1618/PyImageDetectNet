"""
    在 multiprocessing 启动的进程中使用 subprocess 启动子进程，并捕获子进程报错
    Start the process using multiprocessing while started started sub process using subprocess within process,
    and  capture the standard output and standard error output.
"""
import os
import sys
import threading
import multiprocessing as mp
import subprocess as sp
from enum import Enum
from time import sleep


class ErrorKeyword(Enum):
    ERROR = "Error"
    ERR = "Err"
    RAISE = "raise"
    ERROR_CASE_INSENSITIVE = "error"
    # TRACEBACK = "Traceback"


class DetectionAlgorithm(Enum):
    YOLO = "YOLO"
    MaskRCNN = "Mask R-CNN"
    Tesseract = "Tesseract"


def monitor_sub_process(pipe, task_id):
    try:
        while True:
            data = pipe.stdout.readline().strip()
            if data:
                # print(data)
                if any(keyword.value in data for keyword in ErrorKeyword):
                    print("Error: ", data)
                    raise Exception(data)

                else:
                    print(f"[output]:", data)

    except Exception as e:
        print("Error occurred in subprocess:", e)
        # Todo: 子进程状态修改为 3 Failed, 更新报错信息到子进程日志， 释放节点
        # 在这里处理其他类型的异


def worker_task():
    # Start the subprocess
    try:
        task_id = 123
        subprocess_command = f"python detect_demo.py --task_id {task_id} --model {DetectionAlgorithm.TESSERACT.value}"
        command = subprocess_command.split()
        pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT,
                        universal_newlines=True)

        print("Sub process", pipe.pid)
        monitor_thread = threading.Thread(target=monitor_sub_process, args=(pipe, task_id))
        monitor_thread.start()

    except Exception as e:
        # 按需加异常处理
        print("catch", e)


def main():
    # Start the worker task in a separate process
    p = mp.Process(target=worker_task)
    p.start()

    print("Main process", p.pid)


if __name__ == "__main__":
    main()

