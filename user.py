from base import BaseHandler

from extensions import (DatasetsManager, ModelsManager, TrainingTaskManager, DetectionTaskManager,
                        AsyncGridFSManager)

from file_utils import generate_dataset_gridfs_save_name, generate_model_gridfs_save_name
from account_utils import (get_token_user, get_account_info, admin_login_redirect, async_admin_login_redirect,
                           auth_login_redirect, async_auth_login_redirect)


class UserDatasetListHandler(BaseHandler):
    @async_auth_login_redirect
    async def get(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        dataset_obj = DatasetsManager()
        datasets_count = dataset_obj.get_datasets_count(username, is_admin)
        dataset_list = dataset_obj.get_datasets(0, datasets_count, username, is_admin)
        print(dataset_list)
        # self.write({"msg":data_list })
        self.render("user_datasets.html", username=username, account_name=account_name, is_admin=is_admin, dataset_list=dataset_list)


class UserModelListHandler(BaseHandler):
    @async_auth_login_redirect
    async def get(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        model_obj = ModelsManager()
        models_count = model_obj.get_models_count(username, is_admin)
        model_list = model_obj.get_models(0, models_count, username, is_admin)
        print(model_list)
        # self.render("user_models.html", data=data_list)
        self.render("user_models.html", username=username, account_name=account_name, is_admin=is_admin, model_list=model_list)



class DeleteUserDatasetHandler(BaseHandler):
    @async_auth_login_redirect
    async def post(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)
        dataset_name = self.get_argument('dataset_name')
        filename = self.get_argument('filename')
        dataset_obj = DatasetsManager()
        dataset_obj.delete_dataset(dataset_name, filename)

        self.set_status(200)
        self.write({'status': 'success'})


class DeleteUserModelHandler(BaseHandler):
    @async_auth_login_redirect
    async def post(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)
        model_name = self.get_argument('model_name')
        version = self.get_argument('version')
        filename = self.get_argument('filename')
        model_obj = ModelsManager()
        model_obj.delete_model(model_name, version, filename)
        self.set_status(200)
        self.write({'status': 'success'})


class UserDetectionTaskListHandler(BaseHandler):
    @async_auth_login_redirect
    async def get(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        task_obj = DetectionTaskManager()
        task_count = task_obj.get_tasks_count(username, is_admin)
        task_list = task_obj.get_tasks(0, task_count, username, is_admin, is_personal=True)

        # self.render("user_models.html", data=data_list)
        self.render("user_detection_tasks.html", username=username, account_name=account_name, is_admin=is_admin, task_list=task_list)


class UserTrainingTaskListHandler(BaseHandler):
    @async_auth_login_redirect
    async def get(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        task_obj = TrainingTaskManager()
        task_count = task_obj.get_tasks_count(username, is_admin)
        task_list = task_obj.get_tasks(0, task_count, username, is_admin, is_personal=True)

        # self.render("user_models.html", data=data_list)
        self.render("user_training_tasks.html", username=username, account_name=account_name, is_admin=is_admin, task_list=task_list)


class SingleDetectionTaskHandler(BaseHandler):
    @async_auth_login_redirect
    async def get(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)
        task_id = self.get_argument("task_id", None)

        task_obj = DetectionTaskManager()

        task_info = task_obj.get_task(task_id)
        result = task_info["res"]
        # self.render("user_models.html", data=data_list)
        self.render("single_detection_task.html", username=username, account_name=account_name, is_admin=is_admin, task_id=task_id, task_result=result)


class SingleTrainingTaskHandler(BaseHandler):
    @async_auth_login_redirect
    async def get(self):
        # 处理获取数据集管理的逻辑
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)
        task_id = self.get_argument("task_id", None)

        task_obj = TrainingTaskManager()

        task_info = task_obj.get_task(task_id)
        # result = task_info.get("res")
        # self.render("user_models.html", data=data_list)
        self.render("single_training_task.html", username=username, account_name=account_name, is_admin=is_admin, task_id=task_id, task_result=task_info)


class DeleteUserDetectionTaskHandler(BaseHandler):
    @async_auth_login_redirect
    async def post(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)
        task_id = self.get_argument('task_id')
        print("task_id", task_id)

        task_obj = DetectionTaskManager()
        task_obj.delete_task(task_id)
        self.set_status(200)
        self.write({'status': 'success'})


class DeleteUserTrainingTaskHandler(BaseHandler):
    @async_auth_login_redirect
    async def post(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)
        task_id = self.get_argument('task_id')

        task_obj = TrainingTaskManager()
        task_obj.delete_task(task_id)
        self.set_status(200)
        self.write({'status': 'success'})


class DownloadDatasetHandler(BaseHandler):
    async def get(self):
        # 处理获取数据集管理的逻辑
        gridfs_manager = AsyncGridFSManager()

        chunk_number = int(self.request.headers.get('X-Chunk-Number', default='0'))
        dataset_name = self.get_argument("dataset_name", None)
        username = self.get_argument("username", None)

        self.set_header('Content-Type', 'application/octet-stream')
        gridfs_save_name = generate_dataset_gridfs_save_name(dataset_name, username)

        versions = await gridfs_manager.count_file_chunks(gridfs_save_name)
        version = versions[chunk_number]  # 指定切片
        chunk_id = version['_id']

        download_stream = await gridfs_manager.download_chunk(chunk_id)

        data = await download_stream.read()
        self.write(data)


class DownloadModelHandler(BaseHandler):
    async def get(self):
        # 处理获取数据集管理的逻辑
        chunk_number = int(self.request.headers.get('X-Chunk-Number', default='0'))
        model_name = self.get_argument("model_name", None)
        version = self.get_argument("version", None)
        username = self.get_argument("username", None)

        gridfs_manager = AsyncGridFSManager()

        self.set_header('Content-Type', 'application/octet-stream')
        gridfs_save_name = generate_model_gridfs_save_name(model_name, version, username)

        versions = await gridfs_manager.count_file_chunks(gridfs_save_name)
        version = versions[chunk_number]  # 指定切片
        chunk_id = version['_id']

        download_stream = await gridfs_manager.download_chunk(chunk_id)

        data = await download_stream.read()
        self.write(data)



class DownloadDetectionFileHandler(BaseHandler):
    async def get(self):
        chunk_number = int(self.request.headers.get('X-Chunk-Number', default='0'))
        model_name = self.get_argument("model_name", None)
        version = self.get_argument("version", None)
        username = self.get_argument("username", None)

        gridfs_manager = AsyncGridFSManager()

        self.set_header('Content-Type', 'application/octet-stream')
        gridfs_save_name = generate_model_gridfs_save_name(model_name, version, username)

        versions = await gridfs_manager.count_file_chunks(gridfs_save_name)
        version = versions[chunk_number]  # 指定切片
        chunk_id = version['_id']

        download_stream = await gridfs_manager.download_chunk(chunk_id)

        data = await download_stream.read()
        self.write(data)

