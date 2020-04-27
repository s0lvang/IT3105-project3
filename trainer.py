from config import general as config
from episode import Episode
from policy import Policy
from config import hex as hex_config
import random


class Trainer:
    def __init__(self):
        self.episodes = config["episodes"]
        self.amount_of_players = config["amount_of_players"]
        self.epsilon = config["epsilon"]
        self.epsilon_decay_rate = config["epsilon_decay_rate"]
        self.stats = {1: 0, 2: 0}
        self.states = []
        self.distributions = []
        self.policy = Policy(hex_config["size"] ** 2)

    def train(self):
        policies = {0: self.policy.clone_policy()}
        for episode_number in range(1, self.episodes + 1):
            episode = Episode(self.policy, self.epsilon)
            episode_states, episode_distributions, winner = episode.play()
            self.states += episode_states
            self.distributions += episode_distributions
            self.train_policy()
            self.epsilon *= 1 - self.epsilon_decay_rate
            if episode_number % (self.episodes // self.amount_of_players) == 0:
                policy_to_save = self.policy.clone_policy()
                policies[episode_number] = policy_to_save
        return policies

    def train_policy(self):
        number_in_batch = len(self.states) // 3
        states_batch, distributions_batch = zip(
            *random.sample(
                list(zip(self.states, self.distributions)),
                number_in_batch,  # it should favorize later states
            )  # Gives a random sample for training
        )
        self.policy.train_from_batch(self.states, self.distributions)
