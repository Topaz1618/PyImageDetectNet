import argparse
import subprocess as sp
from b import yolo_train_wrapper


def main():
    parser = argparse.ArgumentParser(description='Description of your script')

    # 添加需要的参数
    parser.add_argument('--task_id', type=str, help='ID of the detect task')
    parser.add_argument('--model', type=str, default='YOLO', choices=['YOLO', 'Mask_RCNN', 'PaddleOCR', 'Resnet'],
                        help='Detection algorithm (default: Tesseract)')
    parser.add_argument('--node', type=str, help='Name of the node')
    parser.add_argument('--dataset', type=str, help='Name of the dataset')
    parser.add_argument('--epoch', type=int, default=100, help='Number of epochs (default: 100)')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size (default: 32)')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Learning rate value (default: 0.001)')

    # args, unknown_args = parser.parse_known_args()
    args = parser.parse_known_args()[0]
    task_id = args.task_id
    epoch = args.epoch
    batch_size = args.batch_size
    learning_rate = args.learning_rate

    # learning_rate = 1
    # command = f'python b.py --task_id 123 --epochs 1 --batch_size 2 --cos_lr {learning_rate}'
    #
    # b_args = command.split()
    #
    # pipe = sp.Popen(b_args, stdout=sp.PIPE, stderr=sp.STDOUT,
    #                 universal_newlines=True)
    #
    # while True:
    #     if pipe.poll() is not None:  # 检查进程是否已经结束
    #         break
    #
    #     data = pipe.stdout.readline()
    #     if data and len(data):
    #         print(data)

    yolo_train_wrapper(task_id, epoch, batch_size, learning_rate)


if __name__ == '__main__':
    main()
