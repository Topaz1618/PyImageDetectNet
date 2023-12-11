from base import BaseHandler


class CheckDetectWorkerStatusHandler(BaseHandler):
    def get(self):
        """
        检查检测工作进程是否存活的逻辑

        :return:
            Success:
                {[{"task_id": "", "status": ""}, {"task_id": "", "status": ""}], "error_code": "1000"}
            Failed:
                {"error_message": "", "error_code": ""}
        """

        pass


class CheckTrainingWorkerStatusHandler(BaseHandler):
    def get(self):

        """
        检查训练工作进程是否存活的逻辑

        :return:
            Success:
                {[{"task_id": "", "status": ""}, {"task_id": "", "status": ""}], "error_code": "1000"}
            Failed:
                {"error_message": "", "error_code": ""}
        """

        pass