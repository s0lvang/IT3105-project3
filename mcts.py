from node import MonteCarloSearchNode
import random, math
from game import Game
from policy import Policy
from config import hex as hex_config
import numpy as np


class MonteCarloSearchTree:
    def __init__(self, M, c, policy):
        self.M = M
        self.c = c
        self.policy = policy

    def suggest_action(self, root):
        for _ in range(0, self.M):
            node_to_visit = self.traverse(root)
            simulation_result = self.rollout(node_to_visit)
            self.backpropagate(node_to_visit, simulation_result)
        suggested_child = self.best_child(root)
        return (suggested_child.move_from_parent, suggested_child)

    def traverse(self, node):
        while node.is_fully_expanded():
            node = self.best_uct(node)

        return self.pick_unvisited_child(node) or node

    def rollout(self, node):
        node.expand()
        node.visited = True
        rollout_game = Game(*node.game_object.get_state())
        result = self.play_game(rollout_game)  # this is our rollout policy
        return result

    def play_game(self, game):
        while not game.is_end_state():
            legal_moves = game.get_legal_moves()
            prediction = self.policy.predict([game.current_player] + game.get_state()[0])
            best_index = np.argmax(prediction[0][: len(legal_moves)])
            best_move = legal_moves[best_index]
            game.move(best_move, False)
        return game.reward()

    def get_distribution(self, node):
        return [child.total_number_of_visits for child in node.children]

    def backpropagate(self, node, result):
        if node:
            self.update_stats(node, result)
            self.backpropagate(node.parent, result)
        return

    def update_stats(self, node, result):
        node.total_number_of_visits += 1
        node.total_simulation_reward += result

    def best_child(self, node):
        return self.child_with_highest_number_of_visits(node)

    def child_with_highest_number_of_visits(self, node):
        return max(node.children, key=lambda child: child.total_number_of_visits)

    def pick_unvisited_child(self, node):
        unvisited_children = list(
            filter(lambda child: child.total_number_of_visits == 0, node.children)
        )
        return random.choice(unvisited_children) if unvisited_children else False

    def best_uct(self, node):
        if node.game_object.current_player == node.game_object.starting_player:
            return max(
                node.children, key=lambda child: self.utc(child, node), default=node
            )
        else:
            return min(
                node.children,
                key=lambda child: self.utc_negative(child, node),
                default=node,
            )

    def utc(self, node, parent):
        return self.exploitation_component(node) + self.exploration_component(
            node, parent
        )

    def utc_negative(self, node, parent):
        return self.exploitation_component(node) - self.exploration_component(
            node, parent
        )

    def exploitation_component(self, node):
        return node.total_simulation_reward / node.total_number_of_visits

    def exploration_component(self, node, parent):
        return self.c * math.sqrt(
            math.log(parent.total_number_of_visits) / node.total_number_of_visits
        )
