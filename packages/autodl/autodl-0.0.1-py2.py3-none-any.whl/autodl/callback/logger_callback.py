from autodl.callback import BaseCallback
from autodl.core.logging import get_logger

__all__ = ["Logger"]

logger = get_logger("INFO")


class Logger(BaseCallback):
    def begin_train(self, remaining_time_budget: float):
        logger.info(
            f"Begin training the model (time_budget = {remaining_time_budget:.3f})..."
        )

    def end_train(self, remaining_time_budget: float):
        logger.info(
            f"Finished training the model (time_budget = {remaining_time_budget:.3f})."
        )

    def begin_test(self, remaining_time_budget: float):
        logger.info(
            f"Begin testing the model by making predictions on test set (time_budget = {remaining_time_budget:.3f})..."
        )

    def end_test(self, remaining_time_budget: float):
        logger.info(
            f"Finished testing the model (time_budget = {remaining_time_budget:.3f})."
        )
