from base import BaseHandler
from extensions import (DatasetsManager, ModelsManager, TrainingTaskManager, DetectionTaskManager,
                        AsyncGridFSManager)
from account_utils import (get_token_user, get_account_info, admin_login_redirect, async_admin_login_redirect,
                           auth_login_redirect)


class GetDatasetsHandler(BaseHandler):
    @async_admin_login_redirect
    async def get(self):
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        dataset_obj = DatasetsManager()
        datasets_count = dataset_obj.get_datasets_count(username, is_admin)
        dataset_list = dataset_obj.get_datasets(0, datasets_count, username, is_admin)
        print(dataset_list)
        # self.write({"msg":data_list })
        self.render("manage_datasets.html", username=username, account_name=account_name, is_admin=is_admin,
                    dataset_list=dataset_list)


class DeleteDatasetManagerHandler(BaseHandler):
    @async_admin_login_redirect
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


class GetModelsHandler(BaseHandler):
    @async_admin_login_redirect
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
        self.render("manage_models.html", username=username, account_name=account_name, is_admin=is_admin, model_list=model_list)


class DeleteModelManagerHandler(BaseHandler):
    @async_admin_login_redirect
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


class GetDetectionTaskListHandler(BaseHandler):
    @async_admin_login_redirect
    async def get(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        task_obj = DetectionTaskManager()
        task_count = task_obj.get_tasks_count(username, is_admin)
        task_list = task_obj.get_tasks(0, task_count, username, is_admin)

        # self.render("user_models.html", data=data_list)
        self.render("manage_detection_tasks.html", username=username, account_name=account_name, is_admin=is_admin, task_list=task_list)


class GetTrainingTaskListHandler(BaseHandler):
    @async_admin_login_redirect
    async def get(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        task_obj = TrainingTaskManager()
        task_count = task_obj.get_tasks_count(username, is_admin)
        task_list = task_obj.get_tasks(0, task_count, username, is_admin)

        # self.render("user_models.html", data=data_list)
        self.render("manage_training_tasks.html", username=username, account_name=account_name, is_admin=is_admin, task_list=task_list)


class GetSingleDetectionTaskHandler(BaseHandler):
    @async_admin_login_redirect
    async def get(self):
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)
        task_id = self.get_argument("task_id", None)

        task_obj = DetectionTaskManager()

        task_info = task_obj.get_task(task_id)
        result = task_info["res"]
        # self.render("user_models.html", data=data_list)
        self.render("single_detection_task.html", username=username, account_name=account_name, is_admin=is_admin, task_id=task_id, task_result=result)



class GetSingleTrainingTaskHandler(BaseHandler):
    @async_admin_login_redirect
    async def get(self):
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)
        task_id = self.get_argument("task_id", None)

        task_obj = TrainingTaskManager()

        task_info = task_obj.get_task(task_id)
        # result = task_info.get("res")
        # self.render("user_models.html", data=data_list)
        self.render("single_training_task.html", username=username, account_name=account_name, is_admin=is_admin, task_id=task_id, task_result=task_info)


class DeleteDetectionTaskHandler(BaseHandler):
    @async_admin_login_redirect
    async def post(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        detection_task_obj = DetectionTaskManager()
        detection_task_count = detection_task_obj.get_tasks_count(username, is_admin)
        detection_task_list = detection_task_obj.get_tasks(0, detection_task_count, username, is_admin)

        # self.render("user_models.html", data=data_list)
        self.render("user_models.html", username=username, account_name=account_name, is_admin=is_admin, detection_task_list=detection_task_list)


class DeleteTrainingTaskHandler(BaseHandler):
    @async_admin_login_redirect
    async def post(self):
        # 处理获取数据集管理的逻辑
        cookie_token = self.get_secure_cookie("token")
        token = self.get_argument("Authorization", None)
        username, account_name, is_admin = get_account_info(cookie_token, token)

        detection_task_obj = DetectionTaskManager()
        detection_task_count = detection_task_obj.get_tasks_count(username, is_admin)
        detection_task_list = detection_task_obj.get_tasks(0, detection_task_count, username, is_admin)

        # self.render("user_models.html", data=data_list)
        self.render("user_models.html", username=username, account_name=account_name, is_admin=is_admin, detection_task_list=detection_task_list)
