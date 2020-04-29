from board_node import Node
from direction import Direction
from drawer import Drawer
import numpy as np
import math


class Hex:
    board = []
    drawer = Drawer()

    def __init__(self, size, state=None):
        self.board = [[Node(i, j, owner=0) for j in range(size)] for i in range(size)]
        if state:
            count = 0
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    self.board[i][j].owner = state[count]
                    count += 1
        self.size = size
        self.set_all_neighbours(self.board)

    def position_is_on_board(self, r, c):
        return 0 <= r and len(self.board) > r and 0 <= c and len(self.board[r]) > c

    def get_legal_moves(self):
        legalMoves = []
        for row in self.board:
            for node in row:
                if not node.owner:
                    legalMoves.append(node.coordinates)
        return legalMoves

    def set_all_neighbours(self, board):
        for row in board:
            for node in row:
                self.set_neighbours(node)

    def get_action_from_network_output(self, output):
        action = None
        output = output[0][0]
        while not self.is_legal_action(action):
            best_index = np.argmax(output)  # get index with highest value
            action = (
                best_index // self.size,
                best_index % self.size,
            )  # Get coordinates from flat-list
            output[best_index] = -math.inf
        return action

    def is_legal_action(self, action):
        return (
            action
            and self.position_is_on_board(*action)
            and not self.get_node_from_coordinates(action).owner
        )

    def set_neighbours(self, node):
        neighbours = {
            Direction.UP: self.up_neighbour(node),
            Direction.UPRIGHT: self.up_right_neighbour(node),
            Direction.RIGHT: self.right_neighbour(node),
            Direction.DOWN: self.down_neighbour(node),
            Direction.DOWNLEFT: self.down_left_neighbour(node),
            Direction.LEFT: self.left_neighbour(node),
        }
        node.set_neighbours(neighbours)

    def is_end_state(self):
        self.set_nodes_unvisted()
        return self.is_player1_winning() or self.is_player2_winning()

    def set_nodes_unvisted(self):
        for row in self.board:
            for node in row:
                node.visited = False

    def is_player1_winning(self):
        for i in range(self.size):
            start_node = self.board[i][0]

            if not start_node.owner == 1:
                continue

            if self.search_for_other_edge(start_node, start_node, self.is_bottom_right):
                return True

    def is_player2_winning(self):
        for i in range(self.size):
            start_node = self.board[0][i]

            if not start_node.owner == 2:
                continue

            if self.search_for_other_edge(start_node, start_node, self.is_bottom_left):
                return True

    def search_for_other_edge(self, node, initial_node, is_correct_edge):
        node.visited = True

        if is_correct_edge(node):
            return True

        connected_neighbours = node.get_connected_neighbours()
        unvisited_neighbours = filter(
            lambda node: not node.visited, connected_neighbours
        )
        for neighbour in unvisited_neighbours:
            if self.search_for_other_edge(neighbour, initial_node, is_correct_edge):
                return True

    def is_top_right(self, node):
        return node.coordinates[0] == 0

    def is_top_left(self, node):
        return node.coordinates[1] == 0

    def is_bottom_right(self, node):
        return node.coordinates[1] == self.size - 1

    def is_bottom_left(self, node):
        return node.coordinates[0] == self.size - 1

    def get_state(self):
        return [node.owner for row in self.board for node in row]

    def move(self, action, current_player):
        if action:
            node = self.get_node_from_coordinates(action)
            if not node.owner:
                node.owner = current_player
            else:
                raise Exception("Move is not legal")
        return self.is_end_state()

    def reward(self):
        if self.is_end_state():
            return -1
        return

    def draw(self):
        self.drawer.draw(self.board)

    def get_node_from_coordinates(self, coordinates):
        return self.board[coordinates[0]][coordinates[1]]

    def up_neighbour(self, node):
        r = node.coordinates[0]
        c = node.coordinates[1]
        return self.neighbour(r - 1, c)

    def up_right_neighbour(self, node):
        r = node.coordinates[0]
        c = node.coordinates[1]
        return self.neighbour(r - 1, c + 1)

    def right_neighbour(self, node):
        r = node.coordinates[0]
        c = node.coordinates[1]
        return self.neighbour(r, c + 1)

    def down_neighbour(self, node):
        r = node.coordinates[0]
        c = node.coordinates[1]
        return self.neighbour(r + 1, c)

    def down_left_neighbour(self, node):
        r = node.coordinates[0]
        c = node.coordinates[1]
        return self.neighbour(r + 1, c - 1)

    def left_neighbour(self, node):
        r = node.coordinates[0]
        c = node.coordinates[1]
        return self.neighbour(r, c - 1)

    def neighbour(self, r, c):
        if self.position_is_on_board(r, c):
            return self.board[r][c]
