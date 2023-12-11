import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--node', required=True)
args = parser.parse_args()

import a


def main(node):
    # 传递参数给 a.main，而不是通过命令行参数
    a.main("123")


if __name__ == "__main__":
    main(args.node)