from trainer import Trainer
from tournament import Tournament
from policy import Policy
import datetime
from config import general as config
from config import hex as hex_config
import pickle
import os
import tensorflow as tf


def train_policy():
    trainer = Trainer()
    policies = trainer.train()
    return policies


def play_games(policies):
    print(policies)
    topp = Tournament(policies)
    topp.round_robin()


def save_policies(policies):
    rollouts = config["rollouts"]
    episodes = config["episodes"]
    time = datetime.datetime.now().strftime("%dT%H_%M")
    filename = f"{rollouts}r{episodes}e-{time}"
    if not os.path.exists("saved_models"):
        os.mkdir("saved_models")
    os.mkdir(f"saved_models/{filename}")
    for episode_number, policy in policies.items():
        policy.model.save(f"saved_models/{filename}/{episode_number}")
    return filename


def load_policies(directory):
    directory = f"saved_models/{directory}"
    policies = {}
    for file in os.listdir(directory):
        model = tf.keras.models.load_model(f"{directory}/{file}")
        pol = Policy(hex_config["size"])
        pol.model = model
        policies[file] = pol
    return policies


def main():
    print("initiate training")
    policies = train_policy()
    print("training complete")
    print("saving policies")
    filename = save_policies(policies)
    print("start playing")
    play_games(policies)
    print("done playing")


if __name__ == "__main__":
    main()
