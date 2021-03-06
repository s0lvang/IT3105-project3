from game import Game
from mcts import MonteCarloSearchTree
from node import MonteCarloSearchNode
from policy import Policy
from config import general as config


class Episode:
    def __init__(self, policy, epsilon):
        self.verbose = config["verbose"]
        self.policy = policy
        self.game = Game()
        self.mcst = MonteCarloSearchTree(
            config["rollouts"], config["c"], policy=self.policy, epsilon=epsilon
        )
        self.starting_node = MonteCarloSearchNode(
            is_root=True, game_object=self.game, parent=None, move_from_parent=None
        )
        self.states = []
        self.distributions = []
        self.rewards = []

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

        x = lambda number: -1 if number%2==0 else 1  
        rewards = [x(i) for i in range(len(self.states))]
        return self.states, self.distributions, rewards, current_player
