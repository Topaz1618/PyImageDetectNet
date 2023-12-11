import logging
import threading
import multiprocessing
import subprocess
from time import sleep

from utils import redis_conn, get_running_tasks
from detect_demo import extract_table_data
from compression_utils import compress_to_zip, compress_to_tar, decompress_tar, decompress_zip
from enums import FileType
from config import DETECT_TASK_LIST_KEY, TRAINING_TASK_LIST_KEY, DETECT_DATA_PATH


class DetectPDF:
    @staticmethod
    def detector():
        # 测试用检测方法
        extract_table_data("pdf_path")


class TrainingTaskHandler:
    @staticmethod
    def executor():
        r = redis_conn()
        # 启动进程，训练数据
        # 更新任务信息逻辑


class ExtractFolder:
    def __init__(self, package_name):
        self.files = []
        self.package_name = package_name

    def _file_type_detector(self, file):
        res = FileTypeCode.PDF.value
        return res

    def extract_files(self):
        # 解压缩逻辑

        decompress_zip(self.package_name, DETECT_DATA_PATH)

    def loop_files(self):
        for file in self.files:
            file_type = self._file_type_detector(file)
            if file_type == FileTypeCode.PDF.value:
                # 调用检测方法
                t = threading.Thread(target=DetectPDF.detector)
                t.start()


class DetectTaskHandler:
    def __init__(self, application):
        # Initialize the task handler
        self.application = application
        self.worker()
        self.r = redis_conn()

    def get_workers_num(self):
        all_tasks = self.r.lrange(DETECT_TASK_LIST_KEY, 0, -1)
        running_tasks = get_running_tasks(all_tasks)
        workers_num = len(running_tasks)
        return workers_num

    def worker(self):
        try:
            while True:
                workers_num = self.get_workers_num()
                if workers_num < self.application.detect_total_workers_num:
                    pass
                    # 启动本地，远程进程，调用检测程序
                    # 本地启动进程
                    TrainingTaskHandler.executor()

                sleep(1)

        except Exception as e:
            logging.error(f"Monitor worker alive error: {e}")


class TrainingTaskHandler:
    def __init__(self, application):
        # Initialize the task handler
        self.application = application
        self.worker()
        self.r = redis_conn()

    def get_workers_num(self):
        all_tasks = self.r.lrange(TRAINING_TASK_LIST_KEY, 0, -1)
        running_tasks = get_running_tasks(all_tasks)
        workers_num = len(running_tasks)
        return workers_num

    def worker(self):
        try:
            while True:
                workers_num = self.get_workers_num()
                if workers_num < self.application.training_total_workers_num:
                    pass
                    # 启动本地，远程进程，调用检测程序
                    p = multiprocessing.Process()

                sleep(1)

        except Exception as e:
            logging.error(f"Monitor worker alive error: {e}")

