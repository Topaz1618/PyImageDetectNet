"""
Usage:

    loop = asyncio.get_event_loop()
    client = loop.create_task(rpc_c(worker_ip, rpc_port))
    client = await client

    if proc_pid is not None:
        res = await client.call("restart_proc", PidCode.is_exists.value, proc_pid)

    else:
        res = await client.call("restart_proc", PidCode.not_exists.value)

"""


import asyncio
import aio_msgpack_rpc


from code import RpcClientError


async def rpc_client_conn(worker_ip, worker_port=4000):
    try:
        client = aio_msgpack_rpc.Client(*await asyncio.open_connection(worker_ip, worker_port))
        return client
    except:
        raise RpcClientError("1000")




