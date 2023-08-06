from typing import List
from autodl.data import DataBundle
from autodl.resource import Resource

Resources = List[Resource]

__all__ = ["Task"]


class Task:
    def __init__(self, data_bundle: DataBundle, metric, resources: Resources):
        self.data_bundle: DataBundle = data_bundle
        self.metric = metric
        self.resources: Resources = []

    def get_train_databundle(self) -> DataBundle:
        return self.data_bundle.get_sub_data_bundle("train")

    def get_test_databundle(self) -> DataBundle:
        return self.data_bundle.get_sub_data_bundle("test")
