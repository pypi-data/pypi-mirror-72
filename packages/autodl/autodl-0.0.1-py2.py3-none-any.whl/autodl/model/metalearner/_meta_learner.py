from abc import ABC, abstractclassmethod

from ..learner import Learner

__all__ = ["MetaLearner"]


class MetaLearner(ABC):
    @abstractclassmethod
    def meta_fit(self, *args, **kwargs) -> Learner:
        pass
