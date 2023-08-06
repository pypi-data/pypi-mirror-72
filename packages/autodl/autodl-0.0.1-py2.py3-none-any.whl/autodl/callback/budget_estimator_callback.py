import time

import numpy as np
from sklearn.linear_model import LinearRegression

from autodl.callback import BaseCallback
from autodl.core.logging import get_logger

__all__ = ["BudgetEstimator"]

logger = get_logger("INFO")


class BudgetEstimator(BaseCallback):
    def __init__(self):
        self.birthday = time.time()
        self.train_begin_times = []
        self.test_begin_times = []
        self.train_durations = []
        self.test_durations = []
        self.cycle_durations = []
        self.num_steps_trained = []

        self.time_estimator = LinearRegression()

    def begin_train(self, remaining_time_budget: float):
        self.train_begin_times.append(time.time())

    def end_train(self, remaining_time_budget: float):
        self.train_durations.append(time.time() - self.train_begin_times[-1])
        logger.info(
            f"Successfully made one training. {self.train_durations[-1]:.2f} sec used."
        )

    def begin_test(self, remaining_time_budget: float):
        self.test_begin_times.append(time.time())

    def end_test(self, remaining_time_budget: float):
        self.test_durations.append(time.time() - self.test_begin_times[-1])
        self.cycle_durations.append(self.train_durations[-1] + self.test_durations[-1])
        logger.info(
            f"[+] Successfully made one prediction. {self.test_durations[-1]:.2f} sec used. Total time used for training + test: {sum(self.cycle_durations):.2f} sec."
        )
        logger.info(self.cycle_durations)
        logger.info(self.num_steps_trained)

    def add_trained_steps(self, num_steps_trained: int):
        self.num_steps_trained.append(num_steps_trained)

    def predict_duration_cycle(self, num_steps_to_train: int) -> float:
        if len(self.num_steps_trained) > 0 and len(self.cycle_durations) > 0:
            X_train = np.array(self.num_steps_trained).reshape(-1, 1)
            y_train = np.array(self.cycle_durations)
            self.time_estimator.fit(X_train, y_train)
            X = np.array([num_steps_to_train]).reshape(-1, 1)
            y_pred = self.time_estimator.predict(X)[0]
            return y_pred
        else:
            return None

    def predict_max_steps_for_train(self, remaining_time_budget: float) -> int:
        if len(self.num_steps_trained) > 0 and remaining_time_budget is not None:
            X_train = np.array(self.num_steps_trained).reshape(-1, 1)
            y_train = np.array(self.cycle_durations)
            self.time_estimator.fit(X_train, y_train)

            steps_to_train = self.num_steps_trained[-1]

            x0 = np.array([steps_to_train]).reshape(-1, 1)
            y0 = self.time_estimator.predict(x0)[0]

            yn = y0
            if y0 > remaining_time_budget:
                while yn > remaining_time_budget:
                    steps_to_train -= 1
                    xn = np.array([steps_to_train]).reshape(-1, 1)
                    yn = self.time_estimator.predict(xn)[0]
            else:  # y_pred < remaining_time_budget:
                while yn < remaining_time_budget:
                    steps_to_train += 1
                    xn = np.array([steps_to_train]).reshape(-1, 1)
                    yn = self.time_estimator.predict(xn)[0]
                xn = xn - 1
            return xn
        else:
            return None

    def age(self):
        return time.time() - self.birthday
