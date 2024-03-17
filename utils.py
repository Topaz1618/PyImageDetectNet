import sys
import pdb
import redis
import zipfile
import tarfile
import json
from enum import Enum


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


def string_to_dict(data):
    if isinstance(data, dict):
        return data


class MaterialType(Enum):
    ID_CARD = "身份证"
    LAND_MAP = "宗地图"
    HOUSEHOLD_REGISTER = "户口本"
    HOUSE_FLOOR_PLAN = "房屋平面图"
    REAL_ESTATE_APPLICATION = "不动产申请表"


def handle_material(file_data):
    material_type = file_data.get("material_type")
    if material_type in [m.value for m in MaterialType]:
        return material_type


def res_dict(data):
    print("input data: ", data)
    if data and isinstance(data, dict):
        output_data = dict()

        # data = {'17 房屋平面图.pdf': {'file_type': 'PDF', 'material_type': '房屋平面图'},
        #  '15 不动产调查登记申请表.pdf': {'file_type': 'PDF', 'material_type': '不动产申请表'},
        #  '05 户口薄.pdf': {'file_type': 'PDF', 'material_type': 'Unknown'},
        #  '16 宗地图.pdf': {'file_type': 'PDF', 'material_type': 'Unknown'},
        #  '03 权利人身份证.pdf': {'file_type': 'PDF', 'material_type': 'Unknown'}
        #  }

        for filename, file_data in data.items():
            if not isinstance(file_data, dict):
                continue

            material_type = handle_material(file_data)
            if material_type:
                output_data[material_type] = filename
        print(output_data)
        return output_data

