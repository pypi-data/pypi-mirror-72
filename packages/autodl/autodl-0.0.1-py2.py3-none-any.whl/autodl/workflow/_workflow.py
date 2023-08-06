from abc import ABC, abstractmethod
from typing import List

from autodl.callback import BaseCallback

__all__ = ["Workflow"]

Callbacks = List[BaseCallback]


class Workflow(ABC):
    """Base class representing a workflow.
    """

    def __init__(self, *args, **kwargs):

        self.callbacks: Callbacks = []

    @abstractmethod
    def run(self, *args, **kwargs) -> None:
        """Method representing the execution of the workflow.
        """

    def add_callback(self, callback: BaseCallback):
        """Method to add a new callback to the workflow.

        Args:
            callback (BaseCallback): callback to add.

        Raises:
            TypeError: raised if the callback argument is not of type BaseCallback.
        """
        if not (isinstance(callback, BaseCallback)):
            raise TypeError(
                f"the callback argument should be of type {BaseCallback} but is {type(callback)}"
            )

        self.callbacks.append(callback)
