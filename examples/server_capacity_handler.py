import json
import redis
from enum import Enum 


# 原始的服务器处理能力信息
server_capacity = {
    "worker1": {
        "ip": "192.168.0.1",
        "detect_capacity": 5,
        "train_capacity": 3
    },
    "worker2": {
        "ip": "192.168.0.2",
        "detect_capacity": 10,
        "train_capacity": 2
    },
    "worker3": {
        "ip": "192.168.0.3",
        "detect_capacity": 8,
        "train_capacity": 5
    }
}


class TaskTypeEnum(Enum):
    Detect = 1
    Training = 2


redis_client = redis.Redis(host='127.0.0.1', port=6379)

# 从 Redis 中获取已使用的机器能力列表
used_capacity_json = redis_client.get('used_capacity')
used_capacity = json.loads(used_capacity_json) if used_capacity_json else {}


# 计算剩余的机器能力
def calculate_remaining_capacity():
    remaining_capacity = {}
    for machine, capacity in server_capacity.items():
        used_detect_capacity = used_capacity.get(machine, {}).get("detect_capacity", 0)
        used_train_capacity = used_capacity.get(machine, {}).get("train_capacity", 0)

        remaining_detect_capacity = capacity["detect_capacity"] - used_detect_capacity
        remaining_train_capacity = capacity["train_capacity"] - used_train_capacity

        remaining_capacity[machine] = {
            "ip": capacity["ip"],
            "detect_capacity": remaining_detect_capacity,
            "train_capacity": remaining_train_capacity
        }

        return remaining_capacity


def allocate_capacity(new_task_machine, new_task_required_detect_capacity=0, new_task_required_train_capacity=0):
    # 更新已使用的机器能力列表
    used_capacity.setdefault(new_task_machine, {}).setdefault("detect_capacity", 0)
    used_capacity.setdefault(new_task_machine, {}).setdefault("train_capacity", 0)
    used_capacity[new_task_machine]["detect_capacity"] += new_task_required_detect_capacity
    used_capacity[new_task_machine]["train_capacity"] += new_task_required_train_capacity

    # 将更新后的已使用的机器能力列表存回 Redis
    used_capacity_json = json.dumps(used_capacity)
    redis_client.set('used_capacity', used_capacity_json)

    print(f"分配任务给机器: {new_task_machine}")


def release_capacity(completed_task_machine,  completed_detect_capacity, completed_task_type):
    completed_task_machine = "machine1"

    # 检查任务所占用的机器是否在已使用的机器能力列表中
    if completed_task_machine in used_capacity:
        # 获取任务所占用的能力值
        if completed_task_type == TaskTypeEnum.Detect.value:
            released_detect_capacity = used_capacity[completed_task_machine]["detect_capacity"]
            used_capacity[completed_task_machine]["detect_capacity"] -= released_detect_capacity
            
        if completed_task_type == TaskTypeEnum.Training.value:
            released_train_capacity = used_capacity[completed_task_machine]["train_capacity"]
            used_capacity[completed_task_machine]["train_capacity"] -= released_train_capacity

        # 检查任务所占用的机器能力是否已释放完毕
        if used_capacity[completed_task_machine]["detect_capacity"] <= 0 and used_capacity[completed_task_machine][
            "train_capacity"] <= 0:
            # 从已使用的机器能力列表中移除该机器
            del used_capacity[completed_task_machine]

        # 将更新后的已使用的机器能力列表存回 Redis
        used_capacity_json = json.dumps(used_capacity)
        redis_client.set('used_capacity', used_capacity_json)

        print(f"已更新 Redis 中的 used_capacity，释放任务 {completed_task_machine} 所占用的能力")
    else:
        print(f"任务 {completed_task_machine} 不存在于 used_capacity 中")


def assign_task():
    # 假设有一个新任务需要处理
    new_task_machine = None
    new_task_required_detect_capacity = 1
    new_task_required_train_capacity = 0

    remaining_capacity = calculate_remaining_capacity()
    # 打印剩余的机器能力
    for machine, capacity in remaining_capacity.items():
        print(f"机器: {machine}")
        print(f"IP 地址: {capacity['ip']}")
        print(f"剩余任务处理能力: {capacity['detect_capacity']}个任务")
        print(f"剩余模型训练能力: {capacity['train_capacity']}个模型")
        print()

    # 查找适合的机器来处理新任务
    for machine, capacity in remaining_capacity.items():
        if (
                capacity["detect_capacity"] >= new_task_required_detect_capacity and
                capacity["train_capacity"] >= new_task_required_train_capacity
        ):
            new_task_machine = machine
            break

    if new_task_machine:
        allocate_capacity(new_task_machine, new_task_required_detect_capacity)
    else:
        print("没有足够的机器能力来处理新任务")


if __name__ == "__main__":
    pass
