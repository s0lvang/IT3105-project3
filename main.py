from trainer import Trainer
from competition import Competition


def train_policy():
    trainer = Trainer()
    trainer.train()
    return trainer.policy

def play_games(policy1, policy2):
    competition = Competition(policy1, policy2)
    competition.play()
    

policy1 = train_policy()
policy2 = train_policy()

play_games(policy1, policy2)