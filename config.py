nim = dict(pieces=50, max_take=10)

ledge = dict(initial_board="0101010100200111")

general = dict(
    verbose=True,
    game="ledge",
    starting_player="one",  # one, two or mix
    episodes=10,
    M=10,
    c=1,
)
