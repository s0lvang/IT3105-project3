from simulated_game import SimulatedGame
from config import general as config
from itertools import combinations


class Tournament:
    def __init__(self, players):
        self.episodes = config["episodes"]
        self.wins = dict.fromkeys(players.keys(), 0)
        self.players = players

    def round_robin(self):
        self.present_the_players()
        pairings = list(combinations(self.players.items(), 2))
        for pair in pairings:
            self.play_game(pair[0], pair[1])

    def play_game(self, player1, player2):
        simulated_game = SimulatedGame(player1[1], player2[1])
        winner = simulated_game.play()
        winner = self.determine_winner(winner, player1[0], player2[0])

        self.update_result(winner)
        print(
            f"In the game between {player1[0]} and {player2[0]}; The winner is {winner}!"
        )

    def determine_winner(self, winner, player1_name, player2_name):
        if winner == 0:
            return player1_name
        else:
            return player2_name

    def update_result(self, winner):
        self.wins[winner] += 1

    def display_result(self, player1, player2):
        for player in self.wins:
            print(player, self.wins[player])

    def present_the_players(self):
        player_names = self.players.keys()
        print(
            f"In tonights tournament we are lucky to be joined by {len(player_names)} talented players! And they are:"
        )
        for name in player_names:
            print(f"{name} who has been trained for {name} episodes!")

        print("May the best player win!")
