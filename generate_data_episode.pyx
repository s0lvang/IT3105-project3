from game import Game
from mcts import MonteCarloSearchTree
from node import MonteCarloSearchNode


class Episode:
    def __init__(self, policy, epsilon):
        self.verbose = False
        self.policy = policy
        self.game = Game()
        self.rollouts = 300
        self.c = 1
        self.mcst = MonteCarloSearchTree(
            self.rollouts, self.rollouts, policy=self.policy, epsilon=epsilon
        )
        self.starting_node = MonteCarloSearchNode(
            is_root=True, game_object=self.game, parent=None, move_from_parent=None
        )
        self.states = []
        self.distributions = []

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

        return self.states, self.distributions, current_player
