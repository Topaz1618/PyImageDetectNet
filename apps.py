import os.path
import asyncio
import multiprocessing

import tornado.httpserver
import tornado.web
import tornado.options
from tornado.options import define, options

from base import UploadHandler, IndexHandler
from account import RegisterHandler, LoginHandler, LogoutHandler, RestPasswordView
from file_management import UploadPackageHandler, DownloadFileHandler


from detect_management import (CreateDetectTaskHandler, CancelDetectTaskHandler, GetDetectResultHandler,
                               DetectTaskProgressHandler, WsDetectTaskProgressHandler, WsDetectStatusUpdateHandler, UploadDetectFileHandler)

from training_management import (CreateTrainingTaskHandler, CancelTrainingTaskHandler, UploadModelHandler,
                                 UploadDatasetHandler, WsTrainingTaskProgressHandler, TrainingTaskProgressHandler, WsTrainingStatusUpdateHandler,
                                 CheckIsModelExistsHandler, CheckIsDatasetExistsHandler)

from task_monitor import CheckDetectWorkerStatusHandler, CheckTrainingWorkerStatusHandler

from backend import (GetDatasetsHandler, GetModelsHandler, DeleteDatasetManagerHandler, DeleteModelManagerHandler,
                     GetDetectionTaskListHandler, GetTrainingTaskListHandler, DeleteDetectionTaskHandler, DeleteTrainingTaskHandler,
                     GetSingleDetectionTaskHandler, GetSingleTrainingTaskHandler)

from user import (UserDatasetListHandler, UserModelListHandler, DeleteUserDatasetHandler, DeleteUserModelHandler,
                  SingleDetectionTaskHandler, SingleTrainingTaskHandler,  UserDetectionTaskListHandler, UserTrainingTaskListHandler,
                  DeleteUserDetectionTaskHandler, DeleteUserTrainingTaskHandler)

from task_queue_listener import listen_idle_detect_task_workers
# from task_handler import DetectTaskHandler, TrainingTaskHandler


define("port", default=8011, help="run on the given port", type=int)


def process_function():

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
    # print(settings["static_path"])

    application = tornado.web.Application([
        (r"/static/", tornado.web.StaticFileHandler, {"path": settings["static_path"]}),
        (r"/detect/static/(.*)", tornado.web.StaticFileHandler, {"path": settings["static_path"]}),
        (r"/training_model/static/(.*)", tornado.web.StaticFileHandler, {"path": settings["static_path"]}),
        (r"/user/static/(.*)", tornado.web.StaticFileHandler, {"path": settings["static_path"]}),
        (r"/managers/static/(.*)", tornado.web.StaticFileHandler, {"path": settings["static_path"]}),
        (r'/', IndexHandler),

        # 用户系统
        (r'/register', RegisterHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/reset_password', RestPasswordView),

        # 文件识别接口
        (r'/upload', UploadHandler),
        # (r'/download_file', DownloadFileHandler),

        ## 后台管理

        (r'/managers/get_datasets', GetDatasetsHandler),
        (r'/managers/get_models', GetModelsHandler),
        (r'/managers/delete_dataset', DeleteDatasetManagerHandler),
        (r'/managers/delete_model', DeleteModelManagerHandler),

        (r'/managers/get_detection_tasks', GetDetectionTaskListHandler),  # 我的任务
        (r'/managers/get_training_tasks', GetTrainingTaskListHandler),  # 我的任务
        (r'/managers/delete_training_task', DeleteDetectionTaskHandler),  # 删除任务
        (r'/managers/delete_detection_task', DeleteTrainingTaskHandler),  # 删除任务
        (r'/managers/single_detection_task', GetSingleDetectionTaskHandler),  # 单独任务
        (r'/managers/single_training_task', GetSingleTrainingTaskHandler),

        # (r'/managers/single_task', SingleTaskHandler),


        # 用户
        # (r'/user/download_detection_file', DownloadDetectionFileHandler),

        (r'/user/get_datasets', UserDatasetListHandler),  # 我的数据集
        (r'/user/get_models', UserModelListHandler),  # 我的模型
        (r'/user/delete_dataset', DeleteUserDatasetHandler),     # 删除数据集
        (r'/user/delete_model', DeleteUserModelHandler),         # 删除模型
        (r'/user/get_detection_tasks', UserDetectionTaskListHandler),                  # 我的任务
        (r'/user/get_training_tasks', UserTrainingTaskListHandler),  # 我的任务
        (r'/user/delete_training_task', DeleteUserTrainingTaskHandler),  # 删除任务
        (r'/user/delete_detection_task', DeleteUserDetectionTaskHandler),            # 删除任务
        (r'/user/single_detection_task', SingleDetectionTaskHandler),             # 单独任务
        (r'/user/single_training_task', SingleTrainingTaskHandler),

        #
        # 识别检测
        (r'/detect/create_task', CreateDetectTaskHandler),
        (r'/detect/cancel_task', CancelDetectTaskHandler),
        (r'/detect/upload', UploadDetectFileHandler),
        (r'/detect/progress/([^/]+)', DetectTaskProgressHandler),
        (r'/detect/wsprogress', WsDetectTaskProgressHandler),
        (r'/detect/ws_status_update', WsDetectStatusUpdateHandler),
        (r'/detect/result/([^/]+)', GetDetectResultHandler),

        #  模型训练
        (r'/training_model/create_task', CreateTrainingTaskHandler),
        (r'/training_model/cancel_task', CancelTrainingTaskHandler),
        (r'/training_model/progress/([^/]+)', TrainingTaskProgressHandler),
        (r'/training_model/result/([^/]+)', GetDetectResultHandler),
        (r'/training_model/wsprogress', WsTrainingTaskProgressHandler),
        (r'/training_model/ws_status_update', WsTrainingStatusUpdateHandler),

        (r'/training_model/check_is_model_exists', CheckIsModelExistsHandler),
        (r'/training_model/check_is_dataset_exists', CheckIsDatasetExistsHandler),

        (r'/training_model/upload_model', UploadModelHandler),
        (r'/training_model/upload_dataset', UploadDatasetHandler),

        # 任务监听
        (r'/monitor/is_detect_worker_alive', CheckDetectWorkerStatusHandler),
        (r'/monitor/is_training_model_alive', CheckTrainingWorkerStatusHandler),
    ], debug=True, **settings)

    # application.detect_worker_list = DETECT_WORKER_LIST
    # application.training_worker_list = TRAINING_WORKER_LIST

    # application.detect_total_workers_num = len(DETECT_WORKER_LIST)
    # application.training_total_workers_num = len(TRAINING_WORKER_LIST)

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

        # Listen on the specified port
        http_server.listen(options.port)
        print("server start")

        # Start the event loop
        asyncio.get_event_loop().run_forever()

    except KeyboardInterrupt as e:
        print("Quit")
