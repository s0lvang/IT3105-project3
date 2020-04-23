
class Episode:
    def __init__(self, policy, verbose):
        self.game = Game()
        self.mcst = MonteCarloSearchTree(config["M"], config["c"], policy=policy)
        self.starting_node = MonteCarloSearchNode(
            is_root=True, game_object=self.game, parent=None, move_from_parent=None
        )
        self.policy = policy
        self.states = []
        self.distributions = []
        self.verbose = verbose

    def play(self):
        node = self.starting_node
        while not self.game.is_end_state():
            action, node = self.mcst.suggest_action(node)
            current_player = self.game.current_player

            state = node.game_object.get_state()
            distribution = self.mcst.get_distribution(node)

            self.states.append(state)
            self.distributions.append(distribution)

            self.game.move(action, self.verbose)

        number_in_batch = len(self.states) // 3
        states_batch, distributions_batch = zip(
            *random.sample(
                list(zip(self.states, self.distributions)), number_in_batch
            )  # Gives a random sample for training
        )
        self.policy.train_from_batch(states_batch, distributions_batch)

        return self.states, self.distributions, current_player