hex = dict(size=5)

general = dict(
    verbose=True,
    starting_player="one",  # one, two or mix
    episodes=300,
    amount_of_players=10,
    games_in_series=2,
    c=1,
    rollouts=75,  # 300 rollouts
    epsilon=1,
    draw=False,
)
