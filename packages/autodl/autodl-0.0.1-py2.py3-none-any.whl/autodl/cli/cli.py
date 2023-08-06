
import argparse
import os
import sys

from autodl.cli import bench
from autodl.cli import dataset


def create_parser():
    parser = argparse.ArgumentParser(
        description='AutoDL command line.')

    subparsers = parser.add_subparsers()

    # bench
    bench.add_subparser(subparsers)

    # datasets
    dataset.add_subparser(subparsers)

    return parser


def main():
    parser = create_parser()

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(**vars(args))
    else:
        parser.print_help()
