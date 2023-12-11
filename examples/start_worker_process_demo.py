import subprocess


def start_worker_process():
    # 启动子进程

    command = "python detect.py --task_id 1"
    cmd = command.split()
    process = subprocess.Popen(cmd)
    print(process.pid)


if __name__ == "__main__":
    # 启动子进程
    start_worker_process()

    # 继续执行其他操作
    print("Main process started")
    # 其他代码...

    # 不等待子进程，直接退出
    print("Main process finished")