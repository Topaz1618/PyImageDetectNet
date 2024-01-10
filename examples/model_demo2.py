import argparse


def handler():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epoch', help='Path to the file')
    parser.add_argument("--use-cuda", action="store_true")
    #
    # parser.add_argument("--dataset", default="coco")
    # parser.add_argument("--data-dir", default="moudules/Mask_RCNN/coco_mini")
    # parser.add_argument("--ckpt-path")
    # parser.add_argument("--results")
    # parser.add_argument("--task_id")
    #
    # parser.add_argument("--seed", type=int, default=3)
    # parser.add_argument('--lr-steps', nargs="+", type=int, default=[6, 7])
    # parser.add_argument("--lr", type=float)
    # parser.add_argument("--momentum", type=float, default=0.9)
    # parser.add_argument("--weight-decay", type=float, default=0.0001)
    #
    # parser.add_argument("--epochs", type=int, default=3)
    # parser.add_argument("--iters", type=int, default=10, help="max iters per epoch, -1 denotes auto")
    # parser.add_argument("--print-freq", type=int, default=100, help="frequency of printing losses")
    args = parser.parse_args()

    epoch = args.epoch
    print("[Resnet] epoch:", epoch)


if __name__ == '__main__':
    handler()

