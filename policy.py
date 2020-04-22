import tensorflow as tf
from tensorflow import keras
import numpy as np

tf.logging.set_verbosity(tf.logging.ERROR)
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


class Policy:
    def __init__(self, size):
        model = keras.Sequential()
        model.add(keras.layers.Dense(10, input_shape=(size + 2,)))
        model.add(keras.layers.Dense(30))
        model.add(keras.layers.Dense(size))  # TODO make outputlayer generalized.
        model.compile(optimizer="adam", loss="mse")
        self.model = model

    def predict(self, state, PID):
        input_array = self.prepend_PID(state, PID)
        return self.model.predict(np.array([input_array]))

    def prepend_PID(self, state, PID):
        player = [0, 0]
        player[PID - 1] = 1
        return player + state

    def train_from_batch(self, states, distributions):
        X = [self.prepend_PID(*state) for state in states]
        self.model.fit(np.array(X), np.array(distributions))