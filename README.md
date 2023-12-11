# 项目目录结构
    .PyImageDetectNet
    ├── apps.py                   # 入口文件
    ├── backend.py                # 管理后台 APIs
    ├── base.py
    ├── code.py                   # 错误码定义
    ├── compression_utils.py      # 用于压缩，解压缩的实用函数的文件
    ├── config.py                 # 项目配置文件
    ├── dataset                   # 数据集目录
    ├── detect_demo.py            # 测试用文件识别的代码文件
    ├── detect_management.py      # 文件识别 APIs
    ├── enums.py                  # 包含枚举定义
    ├── file_management.py        # 文件管理相关 APIs
    ├── models.py                 # 表结构的文件
    ├── rcp_client.py             # 与 RCP (远程过程调用) 客户端交互的文件
    ├── result_management.py      # 处理结果 APIs
    ├── rpc_server.py             # RPC Server 代码 (所有 Worker 节点需要运行)
    ├── scripts                   # 包含脚本的目录，
    │   └── BingExtendImageFetcher.py # 数据集爬取的 BingExtendImageFetcher.py 脚本
    ├── task_handler.py           # 项目任务管理 APIs
    ├── task_management.py        # 任务管理的文件 APIs
    ├── task_monitor.py           # 任务监听
    ├── training_management.py    # 训练任务管理 APIs
    ├── utils.py                  # 项目中使用的实用函数
    ├── worker_monitor.py         # 监控工作进程的文件
    ├── 接口文档.md
    └── 表结构设计.md



# 环境要求
python3.9+


