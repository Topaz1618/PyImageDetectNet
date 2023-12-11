import json
import redis

redis_client = redis.Redis("127.0.0.1", 6379)

USED_TRAINING_NODES = "used_training_nodes"


# Training任务处理节点
training_nodes = {
    "training_node1": {
        "ip": "127.0.0.1",
        "capacity": 1,  # 初始能力数值为1
    },
    "training_node2": {
        "ip": "127.0.0.1",
        "capacity": 2,  # 初始能力数值为1
    },
}


def get_idle_workers(used_capacity, total_nodes):
    used_capacity = used_capacity if used_capacity else {}

    # from ipdb import set_trace; set_trace()

    if not used_capacity:
        for node, capacity_info in total_nodes.items():
            if capacity_info["capacity"] > 0:
                return node

    for node, capacity in total_nodes.items():
        print(node, capacity, used_capacity)
        node_capacity_info = used_capacity.get(node.encode(), {})
        if isinstance(node_capacity_info, bytes):
            node_capacity_info = node_capacity_info.decode()

        if isinstance(node_capacity_info, str):
            node_capacity_info = json.loads(node_capacity_info)

        used_capacity_num = node_capacity_info.get("cap_num", 0)

        available_capacity_num = capacity["capacity"] - used_capacity_num

        if available_capacity_num > 0:
            return node


if __name__ == "__main__":
    # used_training_nodes = redis_client.hgetall(USED_TRAINING_NODES)
    # print(used_training_nodes)
    used_training_nodes = {b'training_node2': b'{"cap_num": 1}'}
    idle_training_node = get_idle_workers(used_training_nodes, training_nodes)
    print( f"Training Node: Used [{used_training_nodes if used_training_nodes else 'None'}] | Idle [{idle_training_node}]")
