from game import Game
from config import general as config


class SimulatedGame:
    def __init__(self, policy_player1, policy_player2):
        self.verbose = config["verbose"]
        self.game = Game()
        self.policies = [policy_player1, policy_player2]

    def play(self):
        while not self.game.is_end_state():
            current_player = self.game.current_player
            action = self.get_action(current_player)
            self.game.move(action, self.verbose)
        return current_player

    def get_action(self, current_player):
        policy = self.policies[current_player - 1]
        prediction = policy.predict(*self.game.get_state())
        action = self.game.get_action_from_network_output(prediction)
        return action
