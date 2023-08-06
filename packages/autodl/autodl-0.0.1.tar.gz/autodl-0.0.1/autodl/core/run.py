################################################################################
# Name:         Run Local Test Tool
# Author:       Zhengying Liu
# Created on:   20 Sep 2018
# Update time:  22 Apr 2020
# Usage: 		    python run_local_test.py -dataset_dir=<dataset_dir> -code_dir=<code_dir>

VERISION = "v20200422"
DESCRIPTION = """This script allows participants to run local test of their method within the
downloaded starting kit folder (and avoid using submission quota on CodaLab). To
do this, run:
```
python -m autodl.core.run -dataset_dir=../autodl-benchmark/autodl/data/miniciao/ -code_dir=../autodl-benchmark/workflows/Zero/ -score_dir=$PWD
```
in the starting kit directory. If you want to test the performance of a
different algorithm on a different dataset, please specify them using respective
arguments.
"""

# ALL INFORMATION, SOFTWARE, DOCUMENTATION, AND DATA ARE PROVIDED "AS-IS".
# ISABELLE GUYON, CHALEARN, AND/OR OTHER ORGANIZERS OR CODE AUTHORS DISCLAIM
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ANY PARTICULAR PURPOSE, AND THE
# WARRANTY OF NON-INFRINGEMENT OF ANY THIRD PARTY'S INTELLECTUAL PROPERTY RIGHTS.
# IN NO EVENT SHALL ISABELLE GUYON AND/OR OTHER ORGANIZERS BE LIABLE FOR ANY SPECIAL,
# INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF SOFTWARE, DOCUMENTS, MATERIALS,
# PUBLICATIONS, OR INFORMATION MADE AVAILABLE FOR THE CHALLENGE.
################################################################################

# Verbosity level of logger.
# Can be: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

import os
import tensorflow as tf
import time
import shutil  # for deleting a whole directory
import webbrowser
from multiprocessing import Process

from ..data import DataBundle
from ..core.logging import get_logger

logger = get_logger("INFO")


def _HERE(*args):
    h = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(h, *args)


def remove_dir(output_dir):
    """Remove the directory `output_dir`.

  This aims to clean existing output of last run of local test.
  """
    if os.path.isdir(output_dir):
        logger.info(
            "Cleaning existing output directory of last run: {}".format(output_dir)
        )
        shutil.rmtree(output_dir)


def get_basename(path):
    if len(path) == 0:
        return ""
    if path[-1] == os.sep:
        path = path[:-1]
    return path.split(os.sep)[-1]


def run(
    dataset_dir,
    code_dir,
    score_dir=None,
    time_budget=1200,
    mark_datetime=False,
    open_browser=False,
):
    logger.info("#" * 50)
    logger.info("Begin running local test using")
    workflow_name = get_basename(code_dir)
    dataset_name = get_basename(dataset_dir)
    logger.info("code_dir = {}".format(workflow_name))
    logger.info("dataset_dir = {}".format(get_basename(dataset_dir)))
    logger.info("#" * 50)

    # Current directory containing this script
    core_dir = os.path.dirname(os.path.realpath(__file__))

    if not mark_datetime:
        ingestion_output_basename = "sample_result_submission"
        scoring_output_basename = "scoring_output"
    else:
        datetime = time.strftime("%Y%m%d-%H%M%S")
        # ingestion_output_basename = 'sample_result_submission_{}'.format(datetime)
        # As the predictions made by ingestion will be copied to scoring output
        # we won't duplicate the results.
        ingestion_output_basename = f"sample_result_submission_{datetime}"
        scoring_output_basename = f"scoring_output_{datetime}"

    suffix = f"_{workflow_name}_{dataset_name}"
    ingestion_output_dir = os.path.join(
        os.getcwd(), f"{ingestion_output_basename}{suffix}"
    )
    score_dir = (
        os.path.join(os.getcwd(), f"{scoring_output_basename}{suffix}")
        if score_dir is None
        else os.path.join(score_dir, f"{scoring_output_basename}{suffix}")
    )

    # Run ingestion and scoring at the same time
    command_ingestion = "python -m autodl.core.ingestion.ingestion --dataset_dir={} --code_dir={} --time_budget={} --output_dir={} --score_dir={}".format(
        dataset_dir, code_dir, time_budget, ingestion_output_dir, score_dir
    )
    command_scoring = "python -m autodl.core.scoring.score --solution_dir={} --workflow_name={} --score_dir={} --prediction_dir={}".format(
        dataset_dir, workflow_name, score_dir, ingestion_output_dir
    )

    logger.info(f"Command Ingestion: {command_ingestion}")
    logger.info(f"Command Scoring: {command_scoring}")

    def run_ingestion():
        exit_code = os.system(command_ingestion)
        assert exit_code == 0

    def run_scoring():
        exit_code = os.system(command_scoring)
        assert exit_code == 0

    ingestion_process = Process(name="ingestion", target=run_ingestion)
    scoring_process = Process(name="scoring", target=run_scoring)

    # Clean the output of previous runs if exists
    remove_dir(ingestion_output_dir)
    remove_dir(score_dir)
    ingestion_process.start()
    scoring_process.start()
    detailed_results_page = os.path.join(score_dir, "detailed_results.html")
    detailed_results_page = os.path.abspath(detailed_results_page)

    if open_browser:
        # Open detailed results page in a browser
        time.sleep(2)
        for i in range(30):
            if os.path.isfile(detailed_results_page):
                webbrowser.open("file://" + detailed_results_page, new=2)
                break
                time.sleep(1)

    ingestion_process.join()
    scoring_process.join()
    if not ingestion_process.exitcode == 0:
        logger.info("Some error occurred in ingestion program.")
    if not scoring_process.exitcode == 0:
        raise Exception("Some error occurred in scoring program.")


if __name__ == "__main__":
    default_core_dir = _HERE()
    # The default dataset is 'miniciao' under the folder AutoDL_sample_data/
    default_dataset_dir = os.path.join(default_core_dir, "../dataset", "miniciao")
    default_code_dir = os.path.join(
        default_core_dir, "../../models/AutoDL_sample_code_submission/"
    )
    default_time_budget = 1200

    tf.compat.v1.flags.DEFINE_string(
        "dataset_dir",
        default_dataset_dir,
        "Directory containing the content (e.g. adult.data/ + "
        "adult.solution) of an AutoDL dataset. Specify this "
        "argument if you want to test on a different dataset.",
    )

    tf.compat.v1.flags.DEFINE_string(
        "dataset_name",
        None,
        "Name of an AutoDL dataset. If `None`, will use " + "`dataset_dir` instead.",
    )

    tf.compat.v1.flags.DEFINE_string(
        "code_dir",
        default_code_dir,
        "Directory containing a `model.py` file. Specify this "
        "argument if you want to test on a different algorithm.",
    )

    tf.compat.v1.flags.DEFINE_string(
        "score_dir", None, "Directory where the scoring will be output."
    )

    tf.compat.v1.flags.DEFINE_float(
        "time_budget",
        default_time_budget,
        "Time budget for running ingestion " + "(training + prediction).",
    )

    tf.compat.v1.flags.DEFINE_bool(
        "mark_datetime",
        False,
        "Whether mark datetime in the ouput directories. If "
        "True, results from previous runs will not be removed.",
    )

    tf.compat.v1.flags.DEFINE_bool(
        "open_browser", True, "Whether open the detailed results page in a browser."
    )

    FLAGS = tf.compat.v1.flags.FLAGS
    dataset_dir = FLAGS.dataset_dir
    dataset_name = FLAGS.dataset_name
    if not dataset_name is None:
        if dataset_dir != default_dataset_dir:
            logger.warn(
                "Both `dataset_dir` and `dataset_name` are provided. "
                + "Using `dataset_name`."
            )
        dataset_dir = DataBundle(dataset_name=dataset_name).get_dataset_dir()
    code_dir = FLAGS.code_dir
    score_dir = FLAGS.score_dir
    time_budget = FLAGS.time_budget
    mark_datetime = FLAGS.mark_datetime
    open_browser = FLAGS.open_browser

    run(
        dataset_dir,
        code_dir,
        score_dir,
        time_budget,
        mark_datetime=mark_datetime,
        open_browser=open_browser,
    )
