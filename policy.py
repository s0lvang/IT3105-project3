import tensorflow as tf
from tensorflow import keras
import numpy as np
tf.logging.set_verbosity(tf.logging.ERROR)
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


class Policy:
    def __init__(self, size):
        model = keras.Sequential()
        model.add(keras.layers.Dense(10, input_shape=(size+1,)))
        model.add(keras.layers.Dense(30))
        model.add(keras.layers.Dense(size))  # TODO make outputlayer generalized.
        model.compile(optimizer="adam", loss="mse")
        self.model = model

    def predict(self, state):
        return self.model.predict(np.array([state]))

    def train_from_batch(self, states, distributions):
        self.model.fit(np.array(states), np.array(distributions))
