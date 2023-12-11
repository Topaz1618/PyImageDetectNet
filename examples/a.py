import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model')
args = parser.parse_args()


def main(model):
    print(model)
    # 使用 model 参数，而不是从命令行参数中获取

if __name__ == "__main__":
    main(args.model)