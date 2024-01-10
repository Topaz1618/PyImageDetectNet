import os
import subprocess as sp

command = "python arg_demo.py task1"
cmd = command.split()

pipe = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT,
                universal_newlines=True)


while True:
    if pipe.poll() is not None:  # 检查进程是否已经结束
        break

    data = pipe.stdout.readline()
    if data and len(data):
        print(data)