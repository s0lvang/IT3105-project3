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
            self.play_episode()

        self.display_result()

    def play_episode(self):
        game = Game()
        mcst = MonteCarloSearchTree(config["M"], config["c"], policy=self.policy)
        node = MonteCarloSearchNode(
            is_root=True, game_object=game, parent=None, move_from_parent=None
        )
        while not game.is_end_state():
            action, node = mcst.suggest_action(node)
            current_player = game.current_player
            self.states.append(node.game_object.get_state())
            distribution = mcst.get_distribution(node)
            self.distributions.append(distribution)
            game.move(action, self.verbose)
        self.stats[current_player] += 1
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
