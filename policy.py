import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.metrics import accuracy_score
from ann_config import ANN as config


class Policy:
    def __init__(self, size):
        hidden_layers = config["hidden_layers"]
        self.size = size
        model = keras.Sequential()
        model.add(keras.layers.Dense(10, input_shape=(size + 2,)))
        for layer in hidden_layers:
            model.add(keras.layers.Dense(layer[0], activation=layer[1].value))
        model.add(
            keras.layers.Dense(size, activation="softmax")
        )  # TODO make outputlayer generalized.
        model.compile(
            optimizer=config["optimizer"].value, loss="categorical_crossentropy"
        )
        self.model = model

    def predict(self, state, PID):
        input_array = self.prepend_PID(state, PID)
        return self.model.predict(np.array([input_array]))

    def prepend_PID(self, state, PID):
        state_in_ints = []
        for pos in state:
            if pos[0] == 1:
                state_in_ints.append(1)
            elif pos[1] == 1:
                state_in_ints.append(1)
            else:
                state_in_ints.append(0)
        player = [0, 0]
        player[PID - 1] = 1
        return player + state_in_ints

    def train_from_batch(self, states, distributions):
        states_with_PID = [self.prepend_PID(*state) for state in states]
        normalized_distributions = [
            np.array(distribution)
            / (np.array(distribution).sum(axis=0, keepdims=1) or 1)
            for distribution in distributions
        ]
        self.model.fit(np.array(states_with_PID), np.array(normalized_distributions))

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
