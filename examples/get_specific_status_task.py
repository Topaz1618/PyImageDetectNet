import json
import redis
from enum import Enum

redis_client = redis.Redis("127.0.0.1", 6379)
USED_DETECT_NODES = "used_detect_nodes"
USED_TRAINING_NODES = "used_training_nodes"
DETECT_TASK_QUEUE = "detect_task_queue"
TRAINING_TASK_QUEUE = "training_task_queue"

# Detect任务处理节点
detect_nodes = {
    "detect_node1": {
        "ip": "127.0.0.1",
        "capacity": 2,  # 初始能力数值为1
    },
}

# Training任务处理节点
training_nodes = {
    "training_node1": {
        "ip": "127.0.0.1",
        "capacity": 2,  # 初始能力数值为1
    },
    "training_node2": {
        "ip": "127.0.0.1",
        "capacity": 1,  # 初始能力数值为1
    },
}


class TaskStatus(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    FAILED = 4
    CANCELLED = 5
    RETRYING = 6
    TIMEOUT = 7
    TERMINATED = 8


class TaskType(Enum):
    DETECT = 1
    TRAINING = 2

    def get_text_format(self):
        return self.name


def get_available_nodes(task_type):
    if task_type == TaskType.DETECT.value:
        used_capacity = redis_client.hgetall(USED_DETECT_NODES)
        total_nodes = detect_nodes

    elif task_type == TaskType.TRAINING.value:
        used_capacity = redis_client.hgetall(USED_TRAINING_NODES)
        total_nodes = training_nodes

    else:
        raise ValueError("check task type")

    available_nodes = list()
    used_capacity = used_capacity if used_capacity else {}

    for node, capacity in total_nodes.items():
        # print(node, capacity, used_capacity)
        node_capacity_info = used_capacity.get(node.encode(), {})
        if isinstance(node_capacity_info, bytes):
            node_capacity_info = node_capacity_info.decode()

        if isinstance(node_capacity_info, str):
            node_capacity_info = json.loads(node_capacity_info)

        used_capacity_num = node_capacity_info.get("cap_num", 0)

        available_capacity_num = capacity["capacity"] - used_capacity_num

        if available_capacity_num > 0:
            available_nodes.append({"node": node, "capacity_num": available_capacity_num})


    print(available_nodes)
    return available_nodes


def get_task_status_lists():
    task_dict_data = redis_client.hgetall("task_dict")

    # Check if the task status is 1
    complete_task_list = list()
    pending_task_list = list()
    processing_task_list = list()

    # Iterate over the task data
    for task_id, task_data in task_dict_data.items():
        # Convert the task data from bytes to a string
        task_data_str = task_data.decode("utf-8")

        # Parse the task data as a JSON object
        task = json.loads(task_data_str)

        if isinstance(task_id, bytes):
            task_id = task_id.decode()

        if task["status"] == TaskStatus.COMPLETED.value:
            # Perform actions on the task with status 1
            complete_task_list.append({"task_id": task_id, "status": task["status"], "task_type": task.get("task_type"), "create_time": task.get("create_time")})

        elif task["status"] == TaskStatus.PENDING.value:
            # Perform actions on the task with status 1
            pending_task_list.append({"task_id": task_id, "status": task["status"], "task_type": task.get("task_type"), "create_time": task.get("create_time")})

        elif task["status"] == TaskStatus.IN_PROGRESS.value:
            # Perform actions on the task with status 1
            processing_task_list.append({"task_id": task_id, "status": task["status"], "task_type": task.get("task_type"), "create_time": task.get("create_time")})

        else:
            continue

    return complete_task_list, pending_task_list, processing_task_list


if __name__ == "__main__":
    complete_task_list, pending_task_list, processing_task_list = get_task_status_lists()
    nodes = get_available_nodes(TaskType.TRAINING.value)

    data = {
        "nodes": nodes,
        "complete_task_list": complete_task_list,
        "pending_task_list": pending_task_list,
        "processing_task_list": processing_task_list,
    }

    print(data)
    print(json.dumps(data))