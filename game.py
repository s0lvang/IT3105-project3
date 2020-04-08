import random
from config import nim as nim_config
from config import ledge as ledge_config
from config import general as general_config
from ledge import Ledge
from hex import Hex


class Game:
    def __init__(self, initial_state=None, current_player=0):
        self.starting_player = self.initialize_starting_player()
        self.current_player = current_player if current_player else self.starting_player
        self.game = self.setup_hex(initial_state)

    def setup_hex(self, initial_state):
        state = None  # initial_state if initial_state != None else nim_config["pieces"]
        return Hex(state=state, size=4)

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
        if verbose:
            print(self.game.get_verbose(self.current_player, action))
            if is_end_state:
                print(f"Player {self.current_player} wins!")
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

    def __str__(self):
        return f"GAME: player: {self.current_player}, state: {self.game.get_state()}"

    def __repr__(self):
        return self.__str__()


game = Game()
game.play_randomly()
