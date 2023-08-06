import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from termcolor import colored


def add_subparser(subparsers):
    subparser_name = "bench"
    function_to_call = main

    subparser = subparsers.add_parser(
        subparser_name, help="Benchmark algorithms/datasets."
    )

    subparser.add_argument(
        "--datasets", nargs="+", required=True, help="Datasets to ingest."
    )

    subparser.add_argument(
        "--datasets-path", required=True, help="Path of datasets to ingest."
    )

    subparser.add_argument(
        "--models", nargs="+", required=True, help="Algorithms to execute."
    )

    subparser.add_argument(
        "--models-path", required=True, help="Path of models to ingest."
    )


    subparser.add_argument(
        "--budget", default=1200, type=int, help="Time budget in seconds."
    )

    subparser.set_defaults(func=function_to_call)


def main(datasets, datasets_path, models, models_path, budget, *args, **kwargs):
    python_exe = sys.executable
    datasets_root = os.path.abspath(datasets_path)
    models_root = os.path.abspath(models_path)
    output_root = os.getcwd()

    max_duration = budget * len(models) * len(datasets)

    print(colored(f"Starting benchmark of {len(datasets)} datasets and {len(models)} models with an individual budget time of {budget} sec. corresponding to a maximum duration of {max_duration/3600:.2f} hours.", "yellow"))

    for M in models:
        for D in datasets:
            print(f"Model ~{colored(M, 'cyan')}~ {colored('VERSUS', 'red')}  Dataset ~{colored(D, 'green')}~")

            datetime = time.strftime("%Y%m%d-%H%M%S")
            output_folder = os.path.join(output_root, f"{M}_{D}_{datetime}")
            Path(output_folder).mkdir(parents=True, exist_ok=True)
            os.chdir(output_folder)

            print(f"  {colored('output_folder', 'magenta')}: {output_folder}")

            command_template = "{} -m autodl.core.run -dataset_dir={} -code_dir={} -time_budget={} >> outputs.log"

            dataset_path = os.path.join(datasets_root, D)
            model_path = os.path.join(models_root, M)

            print(f"  {colored('dataset_folder', 'magenta')}: {dataset_path}")
            print(f"  {colored('model_folder', 'magenta')}: {model_path}")

            command = command_template.format(python_exe, dataset_path, model_path, budget)

            print(f"  {colored('command', 'magenta')}: {command}")

            try:
                subprocess.run(command, shell=True, check=True, start_new_session=True)
                print(colored("√ command succesful √", "green"))
            except subprocess.CalledProcessError:
                print(colored("/!\ command failed /!\\", "red"))

