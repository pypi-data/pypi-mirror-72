import argparse
import os
import sys

from termcolor import colored


def add_subparser(subparsers):
    subparser_name = "dataset"
    function_to_call = main

    subparser = subparsers.add_parser(
        subparser_name, help="Manage the public datasets of AutoDL."
    )

    subparser.add_argument(
        "-l", "--list", dest="list", action="store_true", help="List available datasets."
    )
    subparser.add_argument(
        "--name", type=str, required=False, default=None, help="Name of the dataset."
    )
    subparser.add_argument(
        "-d",
        "--download",
        dest="download",
        action="store_true",
        help="Download the dataset.",
    )
    subparser.set_defaults(func=function_to_call)


def main(name, *args, **kwargs):
    if kwargs["list"]:
        import autodl

        repo_path = os.path.dirname(os.path.dirname(os.path.abspath(autodl.__file__)))
        datasets_path = os.path.join(repo_path, "datasets")
        downloaded_datasets = [f.name for f in os.scandir(datasets_path) if f.is_dir()]
        print(
            colored(f"{len(downloaded_datasets)} datasets already downloaded.", "yellow")
        )

        from autodl.data.urls import DATA_URLS

        for i, el in enumerate(DATA_URLS.keys()):
            if el in downloaded_datasets:
                print(colored(f"{i:02} {el}", "green"))
            else:
                print(colored(f"{i:02} {el}", "red"))
    elif kwargs["download"]:
        from autodl.data import DataBundle

        hammer = DataBundle(dataset_name=name, download=True)
