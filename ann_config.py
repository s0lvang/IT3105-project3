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


ANN = dict(
    actor_hidden_layers=[(69, Activation.RELU), (69, Activation.RELU),(42, Activation.RELU)],
    critic_hidden_layers=[(32, Activation.RELU), (60, Activation.RELU)],
    shared_hidden_layers=[(64, Activation.RELU)],
    use_critic=True,
    learning_rate=lr,
    optimizer=Optmizers.Adam,
)
