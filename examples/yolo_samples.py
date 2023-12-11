import argparse


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, help='total training epochs')
    parser.add_argument('--task_id', type=str, help='total training epochs')
    return parser.parse_args()


def yolo_train_wrapper(task_id, epochs):
    # Checks
    print(task_id, epochs)
    opt = parse_opt()
    opt.task_id = task_id
    opt.epochs = epochs
    print("opt", opt)


if __name__ == "__main__":
    task_id = "123"
    epoch = 2
    yolo_train_wrapper(task_id, epoch)