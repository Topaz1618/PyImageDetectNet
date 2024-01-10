import argparse


def handler():
    parser = argparse.ArgumentParser()
    parser.add_argument('epoch', help='Path to the file')

    args = parser.parse_args()

    epoch = args.epoch
    print("[Resnet] epoch:", epoch)


if __name__ == '__main__':
    handler()

