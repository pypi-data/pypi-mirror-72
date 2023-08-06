import tensorflow as tf
import numpy as np

from ._predictor import Predictor


class ConstantPredictor(Predictor):
    def __init__(self, output_shape, value=0):
        super().__init__()
        self.output_shape = (output_shape,) if type(output_shape) is int else output_shape
        self.value = value

    def predict(self, x):
        if isinstance(x, np.ndarray):
            sample_count = np.shape(x)[0]
        elif isinstance(x, tf.data.Dataset):
            sample_count = len(list(x))
        else:
            sample_count = len(x)

        return self._predict(x, sample_count)

    def _predict(self, x, sample_count):
        return np.ones((sample_count, *self.output_shape)) * self.value
