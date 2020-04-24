from simulated_game import SimulatedGame
from config import general as config

class Competition:
    def __init__(self, policy_player1, policy_player2):
        self.episodes = config["episodes"]
        self.stats = {1: 0, 2: 0}
        self.policy_player1 = policy_player1 
        self.policy_player2 = policy_player2

    def play(self):
        for _ in range(1, self.episodes + 1):
            print(_)
            simulated_game = SimulatedGame(self.policy_player1, self.policy_player2)
            winner = simulated_game.play()
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