from game import Game
from mcts import MonteCarloSearchTree
from node import MonteCarloSearchNode
from config import general as config
from config import hex as hex_config
from policy import Policy
import random


class Agent:
    def __init__(self):
        self.episodes = config["episodes"]
        self.M = config["M"]
        self.c = config["c"]
        self.verbose = config["verbose"]
        self.policy = Policy(hex_config["size"] ** 2)
        self.stats = {1: 0, 2: 0}
        self.states = []
        self.distributions = []

    def play(self):
        for _ in range(1, self.episodes + 1):
            episode = Episode(self.policy, self.verbose)
            episode_states, episode_distributions, winner = episode.play()
            self.states.append(episode_states)
            self.distributions.append(episode_distributions)
            self.update_result(winner)

        self.display_result()

    def update_result(self, winner):
        self.stats[winner] += 1

    def display_result(self):
        print(
            f"Player 1 won {self.stats[1]}/{self.episodes} ({round(100 * self.stats[1]/self.episodes, 1)}%)"
        )
        print(
            f"Player 2 won {self.stats[2]}/{self.episodes} ({round(100 * self.stats[2]/self.episodes, 1)}%)"
        )


class Episode:
    def __init__(self, policy, verbose):
        self.game = Game()
        self.mcst = MonteCarloSearchTree(config["M"], config["c"], policy=policy)
        self.starting_node = MonteCarloSearchNode(
            is_root=True, game_object=self.game, parent=None, move_from_parent=None
        )
        self.policy = policy
        self.states = []
        self.distributions = []
        self.verbose = verbose

    def play(self):
        node = self.starting_node
        while not self.game.is_end_state():
            action, node = self.mcst.suggest_action(node)
            current_player = self.game.current_player

            state = node.game_object.get_state()
            distribution = self.mcst.get_distribution(node)

            self.states.append(state)
            self.distributions.append(distribution)

            self.game.move(action, self.verbose)

        number_in_batch = len(self.states) // 3
        states_batch, distributions_batch = zip(
            *random.sample(
                list(zip(self.states, self.distributions)), number_in_batch
            )  # Gives a random sample for training
        )
        self.policy.train_from_batch(states_batch, distributions_batch)

    def display_result(self):
        print(
            f"Player 1 won {self.stats[1]}/{self.episodes} ({round(100 * self.stats[1]/self.episodes, 1)}%)"
        )
        print(
            f"Player 2 won {self.stats[2]}/{self.episodes} ({round(100 * self.stats[2]/self.episodes, 1)}%)"
        )


agent = Agent()
agent.play()
