from trainer import Trainer
from tournament import Tournament


def train_policy():
    trainer = Trainer()
    policies = trainer.train()
    return policies


def play_games(policies):
    print(policies)
    topp = Tournament(policies)
    topp.round_robin()


print("initiate training")
policies = train_policy()
print("training complete")

print("start playing")
play_games(policies)
print("done playing")
