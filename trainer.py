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
        self.epsilon_decay_rate = self.epsilon / self.episodes
        self.states = []
        self.distributions = []
        self.rewards = []
        self.policy = Policy(hex_config["size"] ** 2)

    def train(self):
        policies = {0: self.policy.clone_policy()}
        try:
            for episode_number in range(1, self.episodes + 1):
                print(f"training on episode {episode_number}/{self.episodes}")
                episode = Episode(self.policy, self.epsilon)
                episode_states, episode_distributions, rewards, winner = episode.play()
                self.states += episode_states
                self.distributions += episode_distributions
                self.rewards += rewards
                self.train_policy()
                self.epsilon -= self.epsilon_decay_rate
                if episode_number % (self.episodes // self.amount_of_players) == 0:
                    policy_to_save = self.policy.clone_policy()
                    policies[episode_number] = policy_to_save
        except (KeyboardInterrupt):
            policy_to_save = self.policy.clone_policy()
            policies[episode_number] = policy_to_save
            return policies

        return policies

    def train_policy(self):
        number_in_batch = len(self.states) // 3
        states_batch, distributions_batch, rewards_batch = self.get_batches()
        self.policy.train_from_batch(self.states, self.distributions, rewards_batch)

    def get_batches(self):
        number_in_batch = len(self.states)
        probability_distribution = [
            ((i // 13) + 1) / len(self.states) for i in range(len(self.states))
        ]
        states_batch, distributions_batch, rewards_batch = zip(
            *random.choices(
                population=list(zip(self.states, self.distributions, self.rewards)),
                k=number_in_batch,
                weights=probability_distribution,  # it should favorize later states
            )  # Gives a random sample for training
        )
        return states_batch, distributions_batch, rewards_batch
