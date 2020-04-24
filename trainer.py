from config import general as config
from episode import Episode
from policy import Policy
from config import hex as hex_config
import random


class Trainer:
    def __init__(self):
        self.episodes = config["episodes"]
        self.stats = {1: 0, 2: 0}
        self.states = []
        self.distributions = []
        self.policy = Policy(hex_config["size"] ** 2)

    def train(self):
        for _ in range(1, self.episodes + 1):
            print(_)
            episode = Episode(self.policy)
            episode_states, episode_distributions, winner = episode.play()
            self.states += episode_states
            self.distributions += episode_distributions
            self.train_policy()

    def train_policy(self):
        number_in_batch = len(self.states) // 3
        states_batch, distributions_batch = zip(
            *random.sample(
                list(zip(self.states, self.distributions)), number_in_batch
            )  # Gives a random sample for training
        )
        self.policy.train_from_batch(states_batch, distributions_batch)
