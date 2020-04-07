from node import Node
from direction import Direction
from config import board as config


class Board:
    board = []

    def __init__(self, size, boardType="D", state=""):
        if boardType == "D":
            self.board = [[Node(i, j) for j in range(size)] for i in range(size)]
        elif boardType == "T":
            self.board = [[Node(i, j) for j in range(size - i)] for i in range(size)]
        if state:
            count = 0
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if state[count] == "0":
                        self.board[i][j].empty = True
                    count += 1
        self.set_all_neighbours(self.board)

    def position_is_on_board(self, r, c):
        return 0 <= r and len(self.board) > r and 0 <= c and len(self.board[r]) > c

    def get_legal_moves(self):
        legalMoves = []
        for row in self.board:
            for node in row:
                for legalMove in node.legalMoves():
                    legalMoves.append(legalMove)
        return legalMoves

    def set_all_neighbours(self, board):
        for row in board:
            for node in row:
                self.set_neighbours(node)

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
        node.legal_moves()

    def is_end_state(self):
        return not len(self.get_legal_moves())

    def get_state(self):
        get_bit_from_node = lambda node: str(int(node.empty))
        return [[get_bit_from_node(node) for node in row]for row in self.board]  

    def move(self, action):
        if action:
            node = self.get_node_from_coordinates(action[0])
            node.move(action[1])
        self.updateBitString()
        return self.is_end_state() 

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
