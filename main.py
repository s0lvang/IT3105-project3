from config import general as config
from episode import Episode


class Agent:
    def __init__(self):
        self.episodes = config["episodes"]
        self.stats = {1: 0, 2: 0}
        self.states = []
        self.distributions = []

    def play(self):
        for _ in range(1, self.episodes + 1):
            episode = Episode()
            episode_states, episode_distributions, winner = episode.play()
            self.states.append(episode_states)
            self.distributions.append(episode_distributions)
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


agent = Agent()
agent.play()
