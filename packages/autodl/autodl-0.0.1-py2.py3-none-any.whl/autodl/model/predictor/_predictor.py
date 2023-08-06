from abc import ABC, abstractclassmethod


__all__ = ["Predictor"]


class Predictor(ABC):
    @abstractclassmethod
    def predict(self, *args, **kwargs):
        pass
