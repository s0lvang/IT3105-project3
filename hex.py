from board_node import Node
from direction import Direction
from drawer import Drawer
import numpy as np
import math


class Hex:
    def __init__(self, size, state=None):
        if state:
            self.board = [*state]
        else:
            self.board = self.setup_board(size)

        self.size = size

    def setup_board(self, size):
        slot = (0, 0)  # slot[0]=player1, slot[1]=player2
        return [slot] * (size ** 2)

    def get_legal_moves(self):
        board = self.board
        legal_moves = []
        for i in range(len(board)):
            slot = board[i]
            if slot[0] == 0 and slot[1] == 0:
                legal_moves.append(i)

        return legal_moves

    def get_action_from_network_output(self, output):
        action = None
        if isinstance(output[0][0], np.floating):
            output = output[0]
        else:
            output = output[0][0]

        while not self.is_legal_action(action):
            action = np.argmax(output)  # get index with highest value
            output[action] = -math.inf
        return action

    def is_legal_action(self, action):
        if action is None:
            return False
        board = self.board
        slot = board[action]

        is_on_board = 0 <= action and action < len(board)
        is_filled = slot[0] == 1 or slot[1] == 1

        return is_on_board and not is_filled

    def is_end_state(self):
        visited = [0] * (self.size ** 2)
        return self.is_player1_winning(visited) or self.is_player2_winning(visited)

    def is_player1_winning(self, visited):
        board = self.board
        size = self.size
        search_for_other_edge = self.search_for_other_edge
        is_bottom_right = self.is_bottom_right
        owner = 0

        for i in range(0, size ** 2, size):
            if not board[i][owner] == 1:
                continue

            if search_for_other_edge(i, is_bottom_right, visited, owner, board, size):
                return True
        return False

    def is_player2_winning(self, visited):
        board = self.board
        size = self.size
        search_for_other_edge = self.search_for_other_edge
        is_bottom_left = self.is_bottom_left
        owner = 1

        for i in range(size):
            if not board[i][owner] == 1:
                continue

            if search_for_other_edge(i, is_bottom_left, visited, owner, board, size):
                return True
        return False

    def search_for_other_edge(self, i, is_correct_edge, visited, owner, board, size):
        visited[i] = True
        search_for_other_edge = self.search_for_other_edge

        if is_correct_edge(i, size):
            return True

        neighbours = self.get_neighbours(i)
        connected = [x for x in neighbours if board[x][owner] == 1]
        unvisited = [y for y in connected if visited[y] == 0]

        for neighbour in unvisited:
            if search_for_other_edge(
                neighbour, is_correct_edge, visited, owner, board, size
            ):
                return True

    def get_neighbours(self, i):
        size = self.size
        neighbours = []

        if i - size >= 0:
            neighbours.append(i - size)  # up
        if i % size != 0:
            neighbours.append(i - 1)  # left
        if (i + 1) % size != 0:
            neighbours.append(i + 1)  # right
        if i + size < size ** 2:
            neighbours.append(i + size)  # down
        if (i - size + 1) >= 0 and ((i + 1) % size != 0):
            neighbours.append(i - size + 1)  # up_right
        if (i + size - 1) < size ** 2 and i % size != 0:
            neighbours.append(i + size - 1)  # down_left

        return neighbours

    def is_bottom_right(self, i, size):
        return i in range(size - 1, size ** 2, size)

    def is_bottom_left(self, i, size):
        return i in range((size ** 2) - size, size ** 2)

    def get_state(self):
        return self.board

    def move(self, action, current_player):
        if self.is_legal_action(action):
            if current_player == 1:
                slot = (1, 0)
            else:
                slot = (0, 1)

            self.board[action] = slot
        else:
            raise Exception("Move is not legal")

        return self.is_end_state()

    def reward(self):
        if self.is_end_state():
            return 1
        return

    def draw(self):
        Drawer().draw(self, self.board, self.size)


if __name__ == "__main__":
    state = [
        (0, 1),
        (1, 0),
        (1, 0),
        (0, 1),
        (0, 1),
        (1, 0),
        (1, 0),
        (1, 0),
        (1, 0),
        (1, 0),
        (0, 1),
        (0, 1),
        (1, 0),
        (0, 1),
        (0, 1),
        (0, 1),
    ]
    hex = Hex(4, state)
    print(hex.get_state())
    print(hex.is_end_state())
