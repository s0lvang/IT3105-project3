from trainer import Trainer
from competition import Competition


def train_policy():
    trainer = Trainer()
    policies = trainer.train()
    return policies


def play_games(policies):
    print("1")
    competition = Competition(
        policies[0], policies[30]
    )  # temporary until i bother implementing round robin
    print("2")
    competition = Competition(
        policies[10], policies[30]
    )  # temporary until i bother implementing round robin
    print("3")
    competition = Competition(
        policies[20], policies[30]
    )  # temporary until i bother implementing round robin
    competition.play()


policies = train_policy()
play_games(policies)
