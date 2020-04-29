import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.metrics import accuracy_score
from ann_config import ANN as config


class Policy:
    def __init__(self, size):
        self.size = size
        inputs = keras.layers.Input(shape=(size + 2,))
        actor_branch = self.create_actor_branch(inputs)
        critic_branch = self.create_critic_branch(inputs)
        model = keras.Model(
            inputs=inputs, outputs=[actor_branch, critic_branch], name="hex_net"
        )
        print(model.summary())
        losses = {
            "actor_output": "categorical_crossentropy",
            "critic_output": "mse",
        }
        loss_weights = {"actor_output": 1.0, "critic_output": 1.0}
        model.compile(
            optimizer=config["optimizer"].value, loss=losses, loss_weights=loss_weights
        )
        self.model = model

    def create_actor_branch(self, x):
        hidden_layers = config["hidden_layers"]
        for layer in hidden_layers:
            x = keras.layers.Dense(layer[0], activation=layer[1].value)(x)
        x = keras.layers.Dense(self.size)(x)
        x = keras.layers.Activation(activation="softmax", name="actor_output")(x)
        return x

    def create_critic_branch(self, x):
        hidden_layers = config["hidden_layers"]
        for layer in hidden_layers:
            x = keras.layers.Dense(layer[0], activation=layer[1].value)(x)
        x = keras.layers.Dense(1)(x)
        x = keras.layers.Activation(activation="softmax", name="critic_output")(x)
        return x

    def predict(self, state, PID):
        input_array = self.prepend_PID(state, PID)
        return self.model.predict(np.array([input_array]))

    def prepend_PID(self, state, PID):
        player = [0, 0]
        player[PID - 1] = 1
        return player + state

    def train_from_batch(self, states, distributions, values):
        states_with_PID = [self.prepend_PID(*state) for state in states]
        pred = self.model.predict(np.array(states_with_PID[0:5]))
        normalized_distributions = [
            np.array(distribution)
            / (np.array(distribution).sum(axis=0, keepdims=1) or 1)
            for distribution in distributions
        ]
        Y = {
            "actor_output": np.array(normalized_distributions),
            "critic_output": np.array(values),
        }

        self.model.fit(np.array(states_with_PID), Y)

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
