from abc import ABC, abstractclassmethod


class Resource(ABC):
    @abstractclassmethod
    def kill(self):
        pass
