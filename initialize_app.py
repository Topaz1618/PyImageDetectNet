import argparse
import hashlib
import hmac
from datetime import datetime

from extensions import ModelsManager, DatasetsManager, GPUServerManager, UserManager
from enums import TrainModelType, ModelDescription, UploadStatus, DatasetSource, ModelSource
from config import SECRET


class DBInitializer:
    def __init__(self, username):
        self.gpu_obj = GPUServerManager()
        self.model_obj = ModelsManager()
        self.username = username

    def initialize_admin(self, username, phone_number, password):
        user_manager = UserManager()
        if not user_manager.is_exists(phone_number):
            password = hmac.new(SECRET, password.encode(), hashlib.md5).hexdigest()
            create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user_manager.create_user(username, phone_number, password, is_admin=True, created_time=create_date)

    def initialize_gpu_servers(self):

        if not self.gpu_obj.is_exists("NVIDIA GeForce RTX 3090", "16G"):
            self.gpu_obj.create_gpu_server("NVIDIA GeForce RTX 3090", "16G")

        if not self.gpu_obj.is_exists("NVIDIA GeForce RTX 3090", "24G"):
            self.gpu_obj.create_gpu_server("NVIDIA GeForce RTX 3090", "24G")

        if not self.gpu_obj.is_exists("NVIDIA Tesla K80", "12G"):
            self.gpu_obj.create_gpu_server("NVIDIA Tesla K80", "12G")

        gpu_server_count = self.gpu_obj.get_gpu_server_count(self.username, is_admin=True)
        gpu_list = self.gpu_obj.get_gpu_servers(0, gpu_server_count, self.username, is_admin=True)
        for gpu in gpu_list:
            print(f"GPU Device【{gpu.get('gpu_name')} {gpu.get('gpu_memory')}】类型已增加")

    def _initialize_single_model(self, model_name, verison, desc, created_time, device, filename):
        if not self.model_obj.\
                is_exists(model_name, verison, filename):
            self.model_obj.create_model(model_name, verison, desc, created_time, self.username, filename=filename, device=device, model_source=ModelSource.BUILT_IN.value)
            self.model_obj.update_model(model_name, verison, "upload_status",  UploadStatus.COMPLETED.value)

    def initialize_models(self):
        created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yolo_gpu_info = self.gpu_obj.get_gpu("NVIDIA GeForce RTX 3090", "16G")
        resnet_gpu_info = self.gpu_obj.get_gpu("NVIDIA Tesla K80", "12G")
        maskrcnn_gpu_info = self.gpu_obj.get_gpu("NVIDIA GeForce RTX 3090", "16G")
        paddle_gpu_info = self.gpu_obj.get_gpu("NVIDIA GeForce RTX 3090", "24G")

        self._initialize_single_model(TrainModelType.RESNET.value, "Default", ModelDescription.RESNET.value, created_time, yolo_gpu_info, "resnet50.pth")
        self._initialize_single_model(TrainModelType.YOLO.value, "Default", ModelDescription.YOLO.value, created_time, resnet_gpu_info, "yolov5.pt")
        self._initialize_single_model(TrainModelType.MaskRCNN.value, "Default", ModelDescription.MaskRCNN.value, created_time, maskrcnn_gpu_info, "maskrcnn_results.pth")
        self._initialize_single_model(TrainModelType.PADDLEOCR.value, "Default", ModelDescription.PADDLEOCR.value, created_time, paddle_gpu_info, "best_accuracy.pdopt")

        models_count = self.model_obj.get_models_count(self.username, is_admin=True)

        model_list = self.model_obj.get_models(0, models_count, self.username, is_admin=True)
        for model in model_list:
            print(f"模型【{model.get('model_name')}】已增加 | 推荐运行设备:【{model.get('device').get('gpu_name')} {model.get('device').get('gpu_memory')}】")

    def _initialize_single_dataset(self, dataset_name, model_name, created_time):
        if not self.dataset_obj.is_exists(dataset_name):
            self.dataset_obj.create_dataset(dataset_name, model_name, DatasetSource.BUILT_IN.value, self.username, created_time)
            self.dataset_obj.update_dataset(dataset_name, "upload_status",  UploadStatus.COMPLETED.value)

    def initialize_datasets(self):
        self.dataset_obj = DatasetsManager()
        created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self._initialize_single_dataset("coco_mini", TrainModelType.MaskRCNN.value, created_time)
        self._initialize_single_dataset("default", TrainModelType.PADDLEOCR.value, created_time)
        self._initialize_single_dataset("imagenet_mini_subset", TrainModelType.RESNET.value, created_time)
        self._initialize_single_dataset("coco128", TrainModelType.YOLO.value,  created_time)

        dataset_count = self.dataset_obj.get_datasets_count(self.username, is_admin=True)

        dataset_list = self.dataset_obj.get_datasets(0, dataset_count, self.username, is_admin=True)
        for dataset in dataset_list:
            print(f"数据集【{dataset.get('dataset_name')}】已增加 | 适用模型:【{dataset.get('model_name')}】")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="命令行输入用户名和密码")
    parser.add_argument("username", type=str, help="用户名")
    parser.add_argument("phone", type=str, help="手机号")
    parser.add_argument("password", type=str, help="密码")

    args = parser.parse_args()

    username = args.username
    phone_number = args.phone
    password = args.password

    db_initializer = DBInitializer(username)
    db_initializer.initialize_admin(username, phone_number, password)
    db_initializer.initialize_gpu_servers()
    db_initializer.initialize_models()
    db_initializer.initialize_datasets()