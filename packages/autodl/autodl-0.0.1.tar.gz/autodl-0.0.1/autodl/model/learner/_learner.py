from abc import ABC, abstractclassmethod

from ..predictor import Predictor

__all__ = ["Learner"]


class Learner(ABC):
    @abstractclassmethod
    def fit(self, *args, **kwargs) -> Predictor:
        pass
