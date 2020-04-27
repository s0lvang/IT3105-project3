import random
from config import hex as hex_config
from config import general as general_config
from hex import Hex


class Game:
    def __init__(self, initial_state=None, current_player=0):
        self.starting_player = self.initialize_starting_player()
        self.current_player = current_player if current_player else self.starting_player
        self.game = self.setup_hex(initial_state)

    def setup_hex(self, initial_state):
        return Hex(state=initial_state, size=hex_config["size"])

    def initialize_starting_player(self):
        player = general_config["starting_player"]
        if player == "one":
            return 1
        elif player == "two":
            return 2
        elif player == "mix":
            return 1 if random.random() > 0.5 else 2

    def switch_current_player(self):
        if self.current_player == 1:
            self.current_player = 2
        else:
            self.current_player = 1

    def move(self, action, verbose):
        is_end_state = self.game.move(action, self.current_player)
        # if verbose:
        #     if is_end_state:
        #         print(f"Player {self.current_player} wins!")
        self.switch_current_player()
        return self

    def is_end_state(self):
        return self.game.is_end_state()

    def generate_child_states(self):
        return [
            (action, Game(*self.get_state()).move(action, False))
            for action in self.get_legal_moves()
        ]

    def get_legal_moves(self):
        return self.game.get_legal_moves()

    def get_state(self):
        return self.game.get_state(), self.current_player

    def reward(self):
        if self.current_player == self.starting_player:
            return self.game.reward()
        else:
            return self.game.reward() * -1

    def play_randomly(self):
        while not self.is_end_state():
            legal_moves = self.get_legal_moves()
            self.move(random.choice(legal_moves), False)
        return self.reward()

    def get_random_action(self):
        return random.choice(self.get_legal_moves())

    def get_action_from_network_output(self, output):
        return self.game.get_action_from_network_output(output)

    def __str__(self):
        return f"GAME: player: {self.current_player}, state: {self.game.get_state()}"

    def __repr__(self):
        return self.__str__()
