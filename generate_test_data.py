from generate_data_episode import Episode
import random


class Generator:
    def __init__(self):
        self.episodes = 2
        self.states = []
        self.distributions = []
        self.policy = None

    def train(self):
        for episode_number in range(1, self.episodes + 1):
            episode = Episode(self.policy, 1)
            episode_states, episode_distributions, winner = episode.play()
            self.states += episode_states
            self.distributions += episode_distributions
            if episode_number % episode_number == 0:
                with open("states4x4.txt", "a+") as file:
                    for state in self.states:
                        file.write(",".join([str(number) for number in state]) + "\n")
                with open("distributions4x4.txt", "a+") as file:
                    for distribution in self.distributions:
                        file.write(
                            ",".join([str(number) for number in distribution]) + "\n"
                        )


gen = Generator()
gen.train()
