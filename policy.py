import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.metrics import accuracy_score


class Policy:
    def __init__(self, size):
        self.size = size
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
        states_with_PID = [self.prepend_PID(*state) for state in states]
        self.model.fit(np.array(states_with_PID), np.array(distributions))
    
    def clone_policy(self):
        new_policy = Policy(self.size)
        old_weights = self.model.get_weights()
        new_policy.model.set_weights(old_weights)
        return new_policy

    def check_accuracy(self, states, distributions):
        states_with_PID = [self.prepend_PID(*state) for state in states]
        pred = self.model.predict(np.array(states_with_PID))
        print(pred[0:10])
        print(accuracy_score(distributions, pred))
