from simulated_game import SimulatedGame
from config import general as config
from itertools import combinations


class Tournament:
    def __init__(self, players):
        self.games_in_series = config["games_in_series"]
        self.episodes = config["episodes"]
        self.wins = dict.fromkeys(players.keys(), 0)
        self.total_games_played = 0
        self.result_as_expected = 0
        self.won_by_player_1 = 0
        self.players = players

    def round_robin(self):
        self.present_the_players()
        pairings = list(combinations(self.players.items(), 2))
        for pair in pairings:
            for i in range(self.games_in_series):
                if i % 2 == 0:
                    self.play_game(pair[0], pair[1])
                else:
                    self.play_game(pair[1], pair[0])
        self.display_result()

    def play_game(self, player1, player2):
        simulated_game = SimulatedGame(player1[1], player2[1])
        winner = simulated_game.play(True)
        winner = self.determine_winner(winner, player1[0], player2[0])

        if winner == max(player1[0], player2[0]):
            evaluation = "Just as expected."
            self.update_result(winner, True)
        else:
            self.update_result(winner, False)
            evaluation = "What an upset!"

        print(
            f"In the game between {player1[0]} and {player2[0]}; The winner is {winner}! {evaluation}"
        )

    def determine_winner(self, winner, player1_name, player2_name):
        if winner == 1:
            self.won_by_player_1 += 1
            return player1_name
        else:
            return player2_name

    def update_result(self, winner, expected_result):
        self.total_games_played += 1
        self.wins[winner] += 1
        if expected_result:
            self.result_as_expected += 1

    def display_result(self):
        total = self.total_games_played
        print(f"In total {total} games were played")
        for player in self.wins:
            percent = round(self.wins[player] / total * 100)
            print(f"{player} won {percent}% of their games")

        print(
            f"{self.result_as_expected / total * 100}% of the games were won by the player with more training."
        )
        print(
            f"{self.won_by_player_1 / total * 100}% of the games were won by the player going first"
        )

    def present_the_players(self):
        player_names = self.players.keys()
        print(
            f"In tonights tournament we are lucky to be joined by {len(player_names)} talented players! And they are:"
        )
        for name in player_names:
            print(f"{name} who has been trained for {name} episodes!")

        print("May the best player win!")
