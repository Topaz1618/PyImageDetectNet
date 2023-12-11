import sys
import pdb
import redis
import zipfile
import tarfile


from config import REDIS_HOST, REDIS_PORT


def redis_conn():
    pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
    redis_cli = redis.Redis(connection_pool=pool, max_connections=100)
    return redis_cli



class ForkedPdb(pdb.Pdb):
    """ ForkedPdb().set_trace() """
    def interaction(self, *args, **kwargs):
        _stdin = sys.stdin
        try:
            sys.stdin = open('/dev/stdin')
            pdb.Pdb.interaction(self, *args, **kwargs)
        finally:
            sys.stdin = _stdin


def get_running_tasks(all_tasks):
    running_tasks = []
    for task_data in all_tasks:
        task = eval(task_data)  # Assuming task_data is stored as a string
        if task["status"] == "1":  # Adjust the condition according to your status representation
            running_tasks.append(task)

    return running_tasks


