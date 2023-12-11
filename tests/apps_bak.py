import os.path
import asyncio
import multiprocessing

import tornado.httpserver
import tornado.web
import tornado.options
from tornado.options import define, options

from file_management import UploadPackageHandler

from task_management import (AddTaskHandler, CancelTaskHandler, GetTaskHandler, GetCompletedTasksHandler,
                             DeleteTaskHandler, SingleTaskHandler)

from detect_management import CreateDetectTaskHandler, GetModelsHandler, GetDetectResultHandler

from training_management import (CreateTrainingTaskHandler, UploadModelHandler, GetDatasetsHandler,
                                 UploadDatasetHandler)

from task_monitor import CheckDetectWorkerStatusHandler, CheckTrainingWorkerStatusHandler

from backend import (DatasetManagerHandler, ModelManagerHandler, DeleteDatasetManagerHandler,
                     DeleteModelManagerHandler)

from task_queue_listener import listen_idle_detect_task_workers
from task_handler import DetectTaskHandler, TrainingTaskHandler

from config import DETECT_WORKER_LIST, TRAINING_WORKER_LIST


define("port", default=8011, help="run on the given port", type=int)



def process_function():
    print("!!!")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(listen_idle_detect_task_workers())



if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "default_locale": "en_US.UTF-8",
        "default_encoding": "utf-8",
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "login_url": "/login",
    }

    application = tornado.web.Application([
        # 文件识别接口

        ## 识别目录压缩包上传
        (r'/upload_package', UploadPackageHandler),

        ## 文件识别队列管理(并行, 分布式支持)
        (r'/detect/result', GetDetectResultHandler),

        ## 训练 & 识别任务管理
        (r'/task/add_task', AddTaskHandler),
        (r'/task/cancel_task', CancelTaskHandler),
        (r'/task/get_tasks', GetTaskHandler),
        (r'/task/completed', GetCompletedTasksHandler),
        (r'/task/delete_task', DeleteTaskHandler),
        (r'/task/single_task', SingleTaskHandler),

        # 识别检测
        (r'/detect/create_task', CreateDetectTaskHandler),


        #  模型训练
        (r'/training_model/create_task', CreateTrainingTaskHandler),
        (r'/training_model/upload_model', UploadModelHandler),
        (r'/training_model/upload_dataset', UploadDatasetHandler),
        (r'/training_model/get_datasets', GetDatasetsHandler),

        # 模型
        (r'/model/get_models', GetModelsHandler),

        # 任务监听
        (r'/monitor/is_detect_worker_alive', CheckDetectWorkerStatusHandler),
        (r'/monitor/is_training_model_alive', CheckTrainingWorkerStatusHandler),

        # 后台管理
        (r'/managers/get_datasets', DatasetManagerHandler),
        (r'/managers/get_models',  ModelManagerHandler),
        (r'/managers/delete_dataset', DeleteDatasetManagerHandler),
        (r'/managers/delete_model', DeleteModelManagerHandler),


    ], debug=True, **settings)

    application.detect_worker_list = DETECT_WORKER_LIST
    application.training_worker_list = TRAINING_WORKER_LIST

    application.detect_total_workers_num = len(DETECT_WORKER_LIST)
    application.training_total_workers_num = len(TRAINING_WORKER_LIST)

    try:

        loop = asyncio.get_event_loop()
        # asyncio.gather(listen_idle_detect_task_workers(application))
        # task = asyncio.create_task(listen_idle_detect_task_workers(application))
        process = multiprocessing.Process(target=process_function)
        process.start()
        print("Async task process started")
        # Create an HTTP server instance
        http_server = tornado.httpserver.HTTPServer(
            application,
            # ssl_options=context,
            max_buffer_size=10485760000)

        # Listen on thespecified port
        http_server.listen(options.port)
        print("server start")
        # Start the event loop
        asyncio.get_event_loop().run_forever()

    except KeyboardInterrupt as e:
        print("Quit")
