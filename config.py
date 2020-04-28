from enum import Enum
from tensorflow import keras


class Activation(Enum):
    SIGMOID = "sigmoid"
    LINEAR = "linear"
    TANH = "tanh"
    RELU = "relu"
    SOFTMAX = "softmax"


lr = 0.01


class Optmizers(Enum):
    RMSProp = keras.optimizers.RMSprop(
        learning_rate=lr,
        rho=0.9,
        momentum=0.0,
        epsilon=1e-07,
        centered=False,
        name="RMSprop",
    )
    Adam = keras.optimizers.Adam(
        learning_rate=lr,
        beta_1=0.9,
        beta_2=0.999,
        epsilon=1e-07,
        amsgrad=False,
        name="Adam",
    )
    Adagrad = keras.optimizers.Adagrad(
        learning_rate=lr, epsilon=1e-07, initial_accumulator_value=0.1, name="Adagrad"
    )
    SGD = keras.optimizers.SGD(
        learning_rate=lr, momentum=0.0, nesterov=False, name="SGD"
    )


hex = dict(size=4)

general = dict(
    verbose=True,
    starting_player="one",  # one, two or mix
    episodes=20,
    amount_of_players=3,
    games_in_series=2,
    c=1,
    rollouts=200,  # 300 rollouts
    epsilon=1,
    epsilon_decay_rate=0.05,
)

ANN = dict(
    hidden_layers=[(30, Activation.SOFTMAX), (20, Activation.SOFTMAX)],
    learning_rate=lr,
    optimizer=Optmizers.Adagrad,
)
