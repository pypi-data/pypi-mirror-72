from typing import List

from autodl.task import Task

Tasks = List[Task]


class MetaTask:
    def __init__(self):
        self.tasks: Tasks = []

    def get_meta_train_task(self) -> Tasks:
        pass

    def get_meta_test_task(self) -> Tasks:
        pass
