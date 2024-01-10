# Configure of MongoDB server addresses
# HOST = "82.157.31.231"
HOST = '10.211.55.8'

MONGODB_SERVERS = [
    f'{HOST}:30001',
    f'{HOST}:30002',
    f'{HOST}:30003',
]


replicaSet = 'rs0'
FileSystem = 'filesystem'
GRIDFS_COLLECTION_NAME = "dfs"

# Configure of Redis
# REDIS_HOST = "82.157.31.231"
REDIS_HOST = '10.211.55.8'
REDIS_PORT = 6379

RPC_PORT = 4000


TRAINING_TASK_LIST_KEY = "training_task_list"
DETECT_TASK_LIST_KEY = "detect_task_list"
DETECT_DATA_PATH = "detect_data"

# Detect任务处理节点
detect_nodes = {
    "detect_node1": {
        # "ip": "127.0.0.1",
        "ip": '10.211.55.8',
        # "ip": "81.71.15.27",
        "capacity": 2,  # 初始能力数值为1
    },
}

# Training任务处理节点
training_nodes = {
    "training_node1": {
        "ip": "81.71.15.27",
        "capacity": 2,  # 初始能力数值为1
    },
    "training_node2": {
        "ip": "127.0.0.1",
        "capacity": 0,  # 初始能力数值为1
    },
}


USED_DETECT_NODES = "used_detect_nodes"
USED_TRAINING_NODES = "used_training_nodes"
DETECT_TASK_QUEUE = "detect_task_queue"
TRAINING_TASK_QUEUE = "training_task_queue"
TASK_DICT = "task_dict"


SECRET = b'kt+rL$lL2rO*:hwL'
SECRET_KEY = 'gkT@&dL9$Z^Wxu5y#hFqV4R7bNcJmz!8'
TOKEN_TIMEOUT = 3600 * 1000 * 24

if __name__ == "__main__":
   print(training_nodes)

