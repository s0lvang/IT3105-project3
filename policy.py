import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.metrics import accuracy_score
from ann_config import ANN as config
from scipy.special import softmax


class Policy:
    def __init__(self, size):
        self.size = size
        shared_layers = config["shared_hidden_layers"]
        input_layer = keras.layers.Input(shape=(size + 2,))
        x = input_layer
        for layer in shared_layers:
            x = keras.layers.Dense(layer[0], activation=layer[1].value)(x)
        actor_branch = self.create_actor_branch(x)
        critic_branch = self.create_critic_branch(x)
        model = keras.Model(
            inputs=input_layer, outputs=[actor_branch, critic_branch], name="hex_net"
        )
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
        hidden_layers = config["actor_hidden_layers"]
        for layer in hidden_layers:
            x = keras.layers.Dense(layer[0], activation=layer[1].value)(x)
        x = keras.layers.Dense(self.size)(x)
        x = keras.layers.Activation(activation="softmax", name="actor_output")(x)
        return x

    def create_critic_branch(self, x):
        hidden_layers = config["critic_hidden_layers"]
        for layer in hidden_layers:
            x = keras.layers.Dense(layer[0], activation=layer[1].value)(x)
        x = keras.layers.Dense(1)(x)
        x = keras.layers.Activation(activation="softmax", name="critic_output")(x)
        return x

    def predict(self, state, PID):
        input_array = self.prepend_PID(state, PID)
        return self.model.predict(np.array([input_array]))

    def prepend_PID(self, state, PID):
        state_in_ints = []
        for pos in state:
            if pos[0] == 1:
                state_in_ints.append(1)
            elif pos[1] == 1:
                state_in_ints.append(2)
            else:
                state_in_ints.append(0)
        player = [0, 0]
        player[PID - 1] = 1
        return player + state_in_ints

    def train_from_batch(self, states, distributions, values):
        states_with_PID = [self.prepend_PID(*state) for state in states]
        # pred = self.model.predict(np.array(states_with_PID[0:5]))
        normalized_distributions = [
            softmax(distribution) for distribution in distributions
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
