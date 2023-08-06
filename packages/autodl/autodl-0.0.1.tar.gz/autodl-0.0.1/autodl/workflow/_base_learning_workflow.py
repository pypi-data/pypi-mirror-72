import os
import time

import numpy as np

from ..data import data_io
from ..core.logging import get_logger
from ..callback import Logger
from ..model.predictor import Predictor
from ..workflow import Workflow


__all__ = ["BaseLearningWorkflow"]


verbosity_level = "INFO"

logger = get_logger(verbosity_level)


def write_timestamp(output_dir, predict_idx, timestamp):
    start_filename = "start.txt"
    start_filepath = os.path.join(output_dir, start_filename)
    with open(start_filepath, "a") as f:
        f.write("{}: {}\n".format(predict_idx, timestamp))
    logger.debug(
        "Wrote timestamp {} to 'start.txt' for predition {}.".format(
            timestamp, predict_idx
        )
    )


class BadPredictionShapeError(Exception):
    pass


def run_callbacks(workflow: Workflow, method: str, *args, **kwargs):
    """Run callbacks of workflow.

  Args:
      model (autodl.workflow.Workflow): workflow on witch to run callbacks.
      method (callable): method of callbacks to run.
  """
    for cb in workflow.callbacks:
        if hasattr(cb, method):
            func = getattr(cb, method)
            func(*args, **kwargs)


class BaseLearningWorkflow(Workflow):
    def __init__(self, metadata):
        super().__init__()
        self.done_training = False
        self.metadata = metadata
        self.add_callback(Logger())

    def train(self, data_bundle, remaining_time_budget: float) -> Predictor:
        raise NotImplementedError

    def test(self, data_bundle, remaining_time_budget: float) -> np.array:
        raise NotImplementedError

    def run(self, task, start_time, output_dir, basename, use_done_training_api=True):
        ## Get correct prediction shape
        num_examples_test = task.get_test_databundle().get_metadata().size()
        output_dim = task.get_test_databundle().get_metadata().get_output_size()
        correct_prediction_shape = (num_examples_test, output_dim)

        time_budget = 1200
        start = start_time  # TODO: replace by ressource Time

        # Keeping track of how many predictions are made
        prediction_order_number = 0

        # Start the CORE PART: train/predict process
        while not (use_done_training_api and self.done_training):
            remaining_time_budget = start + time_budget - time.time()
            # Train the model

            run_callbacks(
                self, "begin_train", remaining_time_budget=remaining_time_budget
            )

            self.train(
                task.get_train_databundle(), remaining_time_budget=remaining_time_budget
            )

            remaining_time_budget = start + time_budget - time.time()

            run_callbacks(self, "end_train", remaining_time_budget=remaining_time_budget)

            # Make predictions using the trained model
            run_callbacks(self, "begin_test", remaining_time_budget=remaining_time_budget)

            Y_pred = self.test(
                task.get_test_databundle(), remaining_time_budget=remaining_time_budget
            )

            remaining_time_budget = start + time_budget - time.time()

            run_callbacks(self, "end_test", remaining_time_budget=remaining_time_budget)

            if Y_pred is None:  # Stop train/predict process if Y_pred is None
                logger.info(
                    "The method model.test returned `None`. "
                    + "Stop train/predict process."
                )
                break
            else:  # Check if the prediction has good shape
                prediction_shape = tuple(Y_pred.shape)
                if prediction_shape != correct_prediction_shape:
                    raise BadPredictionShapeError(
                        "Bad prediction shape! Expected {} but got {}.".format(
                            correct_prediction_shape, prediction_shape
                        )
                    )
            # Write timestamp to 'start.txt'
            write_timestamp(
                output_dir, predict_idx=prediction_order_number, timestamp=time.time()
            )
            # Prediction files: adult.predict_0, adult.predict_1, ...
            filename_test = basename[:-5] + ".predict_" + str(prediction_order_number)
            # Write predictions to output_dir
            data_io.write(os.path.join(output_dir, filename_test), Y_pred)
            prediction_order_number += 1
            logger.info(
                "[+] {0:d} predictions made, time spent so far {1:.2f} sec".format(
                    prediction_order_number, time.time() - start
                )
            )
            remaining_time_budget = start + time_budget - time.time()
            logger.info("[+] Time left {0:.2f} sec".format(remaining_time_budget))
            if remaining_time_budget <= 0:
                break
