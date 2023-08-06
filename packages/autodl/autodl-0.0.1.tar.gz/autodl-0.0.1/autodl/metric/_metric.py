from abc import ABC, abstractclassmethod

__all__ = ["Metric"]


class Metric(ABC):
    def __call__(self, y_pred, y_true) -> float:
        return self.call(y_pred, y_true)

    @abstractclassmethod
    def call(self, y_pred, y_true) -> float:
        pass
