import argparse
from yolo_samples import yolo_train_wrapper


parser = argparse.ArgumentParser()

# 添加需要的参数
parser.add_argument('--task_id', type=str, help='Id of detect task')
parser.add_argument('--epochs', type=int, help='Number of epochs')

# 解析命令行参数
args = parser.parse_args()


def main(task_id, epoch):
    print(task_id, epoch)
    yolo_train_wrapper(task_id, epoch)


if __name__ == "__main__":
    task_id = args.task_id
    epochs = args.epochs
    main(task_id, epochs)