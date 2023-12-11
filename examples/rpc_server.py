import os
import asyncio
import subprocess as sp
import multiprocessing as mp
from enum import Enum
import psutil
import aio_msgpack_rpc


RPC_SERVER = "127.0.0.1"
RPC_PORT = 4000
pid_list = list()


class TaskTypeEnum(Enum):
    Detect = 1
    Training = 2


def kill_all(pids):
    for pid in pids:
        proc = psutil.Process(pid)
        for p_clild in proc.children(recursive=True):
            p_clild.kill()

        proc.kill()


class MyServicer:
    async def start_worker(self, task_type, task_info):
        # Todo: start task by subprocess

        # task_info = {"command": "python detect.py", "task_id": "123"}
        task_command = task_info.get("command")
        task_id = task_info.get("task_id")

        if task_type == TaskTypeEnum.Detect.value:
            task_command = f"{task_command} --task_id {task_id}"
            cmd = task_command.split()
            pipe = sp.Popen(cmd, stderr=sp.STDOUT, universal_newlines=True, preexec_fn=os.setsid )
            pid = pipe.pid
            global pid_list
            pid_list.append(pid)
            msg = {"data": pid, "error_code": "1000"}

            return msg

        elif task_type == TaskTypeEnum.Training.value:
            # Todo: 参数拼接逻辑
            task_command = f"{task_command} --task_id {task_id}"
            cmd = task_command.split()
            pipe = sp.Popen(cmd, stderr=sp.STDOUT, universal_newlines=True)
            pid = pipe.pid
            msg = {"data": pid, "error_code": "1000"}
            return msg

        else:
            msg = {"error_msg": "Please check the code type.", "error_code": "123"}
            return msg

    async def stop_worker(self, task_type, proc_pid):
        # Todo: Get PID and other task info from Redis

        task_info = {"command": "python detect.py", "task_id": "123", "pid": proc_pid}
        # proc_pid = task_info.get("proc_pid")
        print(f"task_type: {task_type} {type(task_type)} {task_type == TaskTypeEnum.Detect.value} "
              f"{task_type == TaskTypeEnum.Training.value}")

        if task_type == TaskTypeEnum.Detect.value:
            if psutil.pid_exists(proc_pid):
                try:
                    os.killpg(proc_pid, 1)

                except Exception as e:
                    kill_all([proc_pid])

        elif task_type == TaskTypeEnum.Training.value:
            if psutil.pid_exists(proc_pid):
                try:
                    os.killpg(proc_pid, 1)

                except Exception as e:
                    kill_all([proc_pid])

        else:
            msg = {"error_msg": "Please check the code type.", "error_code": "123"}
            return msg


async def rpc_main():
    try:
        server = await asyncio.start_server(aio_msgpack_rpc.Server(MyServicer()), host=RPC_SERVER, port=RPC_PORT)
        while True:
            await asyncio.sleep(0.1)
    finally:
        server.close()


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(rpc_main())
    except KeyboardInterrupt as e:

        kill_all(pid_list)
        print("Rpc server KeyboardInterrupt", e)

