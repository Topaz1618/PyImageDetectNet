"""

用于分布式场景训练,处理图片等任务的控制

"""

import os
import psutil
import json
import asyncio
import subprocess as sp
import aio_msgpack_rpc


local_ip = "192.168.0.65"
rpc_port = 4000
restart_command = "python app.py"
current_pid = None


def kill_all(proc_pid):
    proc = psutil.Process(proc_pid)
    for p_clild in proc.children(recursive=True):
        p_clild.kill()

    proc.kill()


class MyServicer:
    def __init__(self):
        self.child_pid = None
        self.start_process()

    def start_process(self):
        try:
            cmd = restart_command.split()
            pipe = sp.Popen(cmd, stderr=sp.STDOUT, universal_newlines=True)
            pid = pipe.pid
            self.child_pid = pipe.pid
            global current_pid
            current_pid = pid
            return True

        except Exception as e:
            return False

    def kill_process(self, proc_pid=None):
        if proc_pid is None:
            proc_pid = self.child_pid

        if psutil.pid_exists(proc_pid):
            try:
                os.killpg(proc_pid, 1)

            except Exception as e:
                kill_all(proc_pid)
        else:
            return False

    async def restart_proc(self, is_pid, proc_pid=None):
        self.kill_process(proc_pid)
        start_status = self.start_process()

        if start_status:
            data = json.dumps({"msg": "Restart successful", "error_code": "1"})
        else:
            data = json.dumps({"msg": "Restart failed", "error_code": "0"})

        return data


async def rpc_main():
    try:
        server = await asyncio.start_server(aio_msgpack_rpc.Server(MyServicer()), host=local_ip, port=rpc_port)
        while True:
            await asyncio.sleep(0.1)
    finally:
        server.close()


if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(rpc_main())
    except KeyboardInterrupt as e:
        kill_all(current_pid)
        print("Rpc server", e, current_pid)






