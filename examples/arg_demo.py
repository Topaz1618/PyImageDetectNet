import argparse

# from model_demo import handler
from model_demo2 import handler


def main():
    # parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Description of your script')
    parser.add_argument('task_info', help='Path to the file')

    # 添加需要的参数
    parser.add_argument('--task_id', type=str, help='ID of the detect task')
    parser.add_argument('--model', type=str, default='YOLO', choices=['YOLO', 'Mask_RCNN', 'PaddleOCR', 'Resnet'],
                        help='Detection algorithm (default: Tesseract)')
    parser.add_argument('--node', type=str, help='Name of the node')
    parser.add_argument('--dataset', type=str, help='Name of the dataset')
    parser.add_argument('--epoch', type=int, default=100, help='Number of epochs (default: 100)')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size (default: 32)')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Learning rate value (default: 0.001)')

    args = parser.parse_args()

    task_info = args.task_info
    for i in range(10):
        print("main: ", task_info)

    handler()


if __name__ == '__main__':
    main()