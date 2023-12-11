import uuid
import json
import asyncio
import psutil
from time import time, sleep
from datetime import datetime

import tornado.websocket

from base import BaseHandler
from task_utils import (add_training_task_to_queue, generate_training_task_command, create_task, get_task_info, update_task_info,
                        remove_task_from_detect_queue, get_task_status_lists, get_available_nodes)
from enums import TaskType, TaskStatus, TaskInfoKey, UploadStatus, DatasetSource
from rpc_client import rpc_client_conn
from config import training_nodes, RPC_PORT
from extensions import DatasetsManager, ModelsManager, AsyncGridFSManager, TrainingTaskManager
from crypto_utils import decrypt_data
from file_utils import generate_model_gridfs_save_name, generate_dataset_gridfs_save_name
from account_utils import (get_token_user, get_account_info, admin_login_redirect, async_admin_login_redirect,
                           auth_login_redirect, async_auth_login_redirect)


class CreateTrainingTaskHandler(BaseHandler):
    # def get(self):
    #     self.render("create_training_task.html")

    @auth_login_redirect
    def get(self):
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        model_manager = ModelsManager()
        models_count = model_manager.get_models_count(username, is_admin=is_admin)
        model_list = model_manager.get_models(0, models_count, username, is_admin)

        dataset_manager = DatasetsManager()
        dataset_count = dataset_manager.get_datasets_count(username, is_admin=is_admin)
        dataset_list = dataset_manager.get_datasets(0, dataset_count, username, is_admin)
        # dataset_list = dataset_manager.get_datasets(0, dataset_count, username, is_admin)

        self.render("create_training_task.html", username=username, account_name=account_name, is_admin=is_admin, model_list=model_list, dataset_list=dataset_list)

    @auth_login_redirect
    def post(self):
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        model = self.get_argument('model')
        dataset = self.get_argument('dataset')
        epoch = int(self.get_argument('epoch'))
        batch_size = int(self.get_argument('batch_size'))
        learning_rate = float(self.get_argument('learning_rate'))

        task_id = str(uuid.uuid4())  # 生成唯一的任务ID
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        task_info = create_task(task_id, TaskType.TRAINING.value, create_time, model, dataset, epoch, batch_size, learning_rate)

        task_obj = TrainingTaskManager()

        task_obj.create_task(task_id, username, model, dataset, epoch, batch_size, learning_rate, create_time)
        task_obj.close()

        print("Task info", task_info)
        add_training_task_to_queue(task_id)

        self.set_status(200)
        self.write({'status': 'success', 'message': {"task_id": task_id}})
        # self.write({'status': 'success', 'message': '模型训练任务已创建。'})


class CancelTrainingTaskHandler(BaseHandler):
    async def post(self):
        """
        处理取消任务的逻辑

        :param task_id: Unique ID of task

        :return:
            Success:
                {"Task ID": "","error_code": "1000"}
            Failed:
                {"Task ID": "", "error_code": ""}
        """

        # 处理添加任务的逻辑
        task_id = self.get_argument('task_id')
        task_info = get_task_info(task_id)
        task_pid = task_info.get("task_pid")
        task_node = task_info.get("node")
        task_status = task_info.get("status")

        if task_status == TaskStatus.IN_PROGRESS.value:
            task_node_ip = training_nodes[task_node]["ip"]

            client = await rpc_client_conn(task_node_ip, RPC_PORT)
            res = await client.call("stop_worker", task_id, task_pid, task_node, TaskType.TRAINING.value)

        elif task_status == TaskStatus.PENDING.value:
            remove_task_from_detect_queue(task_id)
            update_task_info(task_id, TaskInfoKey.STATUS.value, TaskStatus.CANCELLED.value)
            update_task_info(task_id, TaskInfoKey.LOG.value, "Task has been canceled")

        else:
            raise ValueError("wrong TaskStatus type ")

        self.write({"error_msg": "success", "error_code": 1000})


class TrainingTaskProgressHandler(BaseHandler):
    def get(self, task_id):
        print(task_id)
        task_info = get_task_info(task_id)
        current_epoch = task_info.get("current_epoch", 0)
        total_epoch = task_info.get("epoch", 1)
        iterations = task_info.get("iterations", 1)
        current_iteration = task_info.get("current_iteration", 0)

        progress = round(int(current_epoch) / int(total_epoch) * 100, 2)


        self.render("training_progress.html", task_id=task_id, task_info=task_info, progress=progress)


class WsTrainingTaskProgressHandler(tornado.websocket.WebSocketHandler):
    def _send_progress(self, task_id, loop):
        asyncio.set_event_loop(loop)
        while True:
            task_info = get_task_info(task_id)
            if not task_info:
                continue

            current_epoch = task_info.get("current_epoch", 0)
            total_epoch = task_info.get("epoch", 1)


            if task_info.get("status") == TaskStatus.COMPLETED.value:
                data = {
                    "log": task_info.get("log", ["waiting..."])[-1],
                    "progress": 100,
                    "status": TaskStatus.COMPLETED.value,
                    "res": json.dumps(task_info.get("res", {})),
                }
                self.write_message(json.dumps(data))
                break

            progress = round(int(current_epoch) / int(total_epoch) * 100, 2)
            # progress = round(int(processed_file_count) / int(total_file_count) * 100, 2)
            data = {
                "log": task_info.get("log", ["waiting..."])[-1],
                "progress": progress,
                "status": task_info.get("status"),
            }
            self.write_message(json.dumps(data))

            sleep(1)

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        # Process the message (e.g., call OpenAI API) and send the response back
        message = json.loads(message)

        task_id = message["task_id"]
        loop = asyncio.get_event_loop()

        asyncio.gather(loop.run_in_executor(None, self._send_progress, task_id, loop), )

        print(f"Task ID: {task_id}")

    def on_close(self):
        print("WebSocket closed")


class WsTrainingStatusUpdateHandler(tornado.websocket.WebSocketHandler):
    def _send_progress(self, loop):
        asyncio.set_event_loop(loop)
        while True:
            nodes = get_available_nodes(TaskType.TRAINING.value)
            complete_task_list, pending_task_list, processing_task_list = get_task_status_lists(TaskType.TRAINING.value)

            data = {
                "nodes": nodes,
                # "complete_task_list": complete_task_list,
                "pending_task_list": pending_task_list,
                "processing_task_list": processing_task_list,
            }
            # print(data)

            self.write_message(json.dumps(data))

            sleep(5)

    async def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        # Process the message (e.g., call OpenAI API) and send the response back

        # task_id = message["task_id"]
        loop = asyncio.get_event_loop()
        asyncio.gather(loop.run_in_executor(None, self._send_progress, loop), )

    def on_close(self):
        print("WebSocket closed")


class UploadModelHandler(BaseHandler):
    @auth_login_redirect
    def get(self):
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        model_manager = ModelsManager()
        models_count = model_manager.get_models_count(username, is_admin=is_admin)
        model_list = model_manager.get_models(0, models_count, username, is_admin)

        self.render("upload_model.html", username=username, account_name=account_name, is_admin=is_admin, model_list=model_list)


    @async_auth_login_redirect
    async def post(self):

        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        chunk_number = int(self.request.headers.get('X-Chunk-Number'))
        model_name = self.get_argument("model_name", None)
        version = self.get_argument("version", None)
        model_desc = self.get_argument("model_desc", None)
        file_size = self.get_argument("file_size", None)
        total_chunks = self.get_argument("chunks", None)
        filename = self.get_argument("filename", None)
        content_type = self.get_argument("content_type", None)
        chunk_size = self.get_argument("chunk_size", None)

        print(f"Chunk Number: {chunk_number} Total chunks: {total_chunks}")

        print(f"[Upload API]: 内存占用率: {psutil.virtual_memory().percent} | CPU 使用率: {psutil.cpu_percent(0)}")

        # Retrieve the chunk data
        chunk_data = self.request.files["file"][0]["body"]

        if not isinstance(total_chunks, int):
            total_chunks = int(total_chunks)

        print("chunk data len:",  len(chunk_data), chunk_data)
        # encrypted_data = decrypt_data(chunk_data)
        async_gridfs_obj = AsyncGridFSManager()
        save_name = generate_model_gridfs_save_name(model_name, version, username)
        await async_gridfs_obj.upload_chunk(chunk_data, save_name)

        if chunk_number == 1:
            model_obj = ModelsManager()
            created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            model_obj.create_model(model_name, version, model_desc, created_time, username, filename, total_chunks)

        if chunk_number == total_chunks:
            model_obj = ModelsManager()
            model_obj.update_model(model_name, version, "upload_status", UploadStatus.COMPLETED.value)

        # 保存模型到数据库的逻辑

        self.set_status(200)
        self.write({'status': 'success', 'message': '模型上传成功。'})


class UploadDatasetHandler(BaseHandler):
    @auth_login_redirect
    def get(self):
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)


        model_manager = ModelsManager()
        models_count = model_manager.get_models_count(username, is_admin=is_admin)
        model_list = model_manager.get_models(0, models_count, username, is_admin)

        self.render("upload_dataset.html", username=username, account_name=account_name, is_admin=is_admin, model_list=model_list)

    @async_auth_login_redirect
    async def post(self):

        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        chunk_number = int(self.request.headers.get('X-Chunk-Number'))
        dataset_name = self.get_argument("dataset_name", None)
        dataset_desc = self.get_argument("dataset_desc", None)
        file_size = self.get_argument("file_size", None)
        total_chunks = self.get_argument("chunks", None)
        model_name = self.get_argument("model_name", None)
        filename = self.get_argument("filename", None)

        content_type = self.get_argument("content_type", None)
        chunk_size = self.get_argument("chunk_size", None)


        print(f"Chunk Number: {chunk_number} Total chunks: {total_chunks}")

        print(f"[Upload API]: 内存占用率: {psutil.virtual_memory().percent} | CPU 使用率: {psutil.cpu_percent(0)}")

        # Retrieve the chunk data
        chunk_data = self.request.files["file"][0]["body"]

        if not isinstance(total_chunks, int):
            total_chunks = int(total_chunks)

        print("chunk data len:",  len(chunk_data), type(total_chunks))
        # encrypted_data = decrypt_data(chunk_data)
        async_gridfs_obj = AsyncGridFSManager()
        save_name = generate_dataset_gridfs_save_name(dataset_name, username)
        await async_gridfs_obj.upload_chunk(chunk_data, save_name)

        if chunk_number == 1:
            dataset_obj = DatasetsManager()
            created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            dataset_obj.create_dataset(dataset_name, model_name, DatasetSource.CUSTOM.value, username, created_time, filename, total_chunks, dataset_desc)

        print(chunk_number, total_chunks, type(total_chunks))
        if chunk_number == total_chunks:
            dataset_obj = DatasetsManager()
            dataset_obj.update_dataset(dataset_name, "upload_status", UploadStatus.COMPLETED.value)

        # 保存模型到数据库的逻辑

        self.set_status(200)
        self.write({'status': 'success', 'message': '模型上传成功。'})


class GetDatasetsHandler(BaseHandler):
    def post(self):
        """
        获取所有数据集
        Get the current status of the processing task.


        :return:
            Success:
                {"data": ["dataset1", "dataset2", ... ], "error_code": "1000"}
            Failed:
                {"error_message": "", "error_code": ""}
        """

        pass


class CheckIsModelExistsHandler(BaseHandler):
    @auth_login_redirect
    def get(self):
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        model_name = self.get_argument("model_name", None)
        filename = self.get_argument("filename", None)
        version = self.get_argument("version", None)
        model_obj = ModelsManager()
        is_exists = model_obj.is_exists(model_name, version, filename)
        if is_exists:
            data = {"error_msg": "Already exist", "error_code": -1}
        else:
            data = {"error_msg": "not exists", "error_code": 1000}

        self.write(data)


class CheckIsDatasetExistsHandler(BaseHandler):
    @auth_login_redirect
    def get(self):
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        dataset_name = self.get_argument("dataset_name", None)
        dataset_obj = DatasetsManager()
        is_exists = dataset_obj.is_exists(dataset_name, username)
        if is_exists:
            data = {"error_msg": "Already exist", "error_code": -1}
        else:
            data = {"error_msg": "not exists", "error_code": 1000}

        self.write(data)
