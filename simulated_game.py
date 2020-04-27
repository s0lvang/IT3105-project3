from game import Game
from config import general as config


class SimulatedGame:
    def __init__(self, player1, player2):
        self.verbose = config["verbose"]
        self.game = Game()
        self.player1 = player1
        self.player2 = player2

    def play(self, draw):
        while not self.game.is_end_state():
            current_player = self.game.current_player
            action = self.get_action(current_player)
            self.game.move(action, self.verbose)
            if draw:
                self.game.draw()
        return current_player

    def get_action(self, current_player):
        if current_player == 0:
            policy = self.player1
        else:
            policy = self.player2
        prediction = policy.predict(*self.game.get_state())
        action = self.game.get_action_from_network_output(prediction)
        return action
