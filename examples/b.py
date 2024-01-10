import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--task_id", help="store_true")
parser.add_argument('--epochs', help='Path to the file')
parser.add_argument("--use-cuda", help="store_true")
parser.add_argument("--batch_size", help="store_true")
parser.add_argument("--cos_lr", help="store_true")
parser.add_argument("--sss", help="store_true")

args = parser.parse_args()


def yolo_train_wrapper(task_id, epochs, batch_size, learning_rate):
    print("handler: epoch =", epochs)
    print("handler: use_cuda =", batch_size)


if __name__ == "__main__":
    task_id = args.task_id
    epochs = args.epochs
    batch_size = args.batch_size
    learning_rate = args.cos_lr

    yolo_train_wrapper(task_id, epochs, batch_size, learning_rate)