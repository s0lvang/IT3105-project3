import networkx as nx
import matplotlib.pyplot as plt
from board import Board
from config import agent as game
import numpy as np


class Drawer:
    def draw(self, board):
        G = nx.Graph()
        labels = {}
        nodes = [node for sublist in board for node in sublist]
        labels = [node.coordinates for node in nodes]
        G.add_nodes_from(labels)
        for node in nodes:
            for neighbour in node.neighbours.values():
                if neighbour:
                    G.add_edge(node.coordinates, neighbour.coordinates)
        empty_nodes = list(
            map(lambda node: node.coordinates, filter(lambda node: node.empty, nodes))
        )
        full_nodes = list(
            map(
                lambda node: node.coordinates,
                filter(lambda node: not node.empty, nodes),
            )
        )

        pos = self.generate_pos(board, full_nodes)
        fig, ax = plt.subplots()
        nx.draw_networkx_nodes(G, ax=ax, pos=pos, nodelist=full_nodes, node_color="r")
        nx.draw_networkx_nodes(
            G, ax=ax, pos=pos, nodelist=empty_nodes, node_color="blue"
        )
        nx.draw_networkx_edges(G, ax=ax, pos=pos)
        nx.draw_networkx_labels(G, ax=ax, pos=pos, font_color="black")
        ax.invert_yaxis()
        plt.axis("off")
        plt.show(block=False)

    def generate_pos(self, board, full_nodes):
        pos = {}
        for i in range(len(board)):
            for j in range(len(board[i])):
                pos[board[i][j].coordinates] = [300 + i * -30 + j * 30, 30 * i + 30 * j]
        return pos

    def visualize_game(self, history):
        for s, a in history:
            board = Board(game["size"], game["boardType"], state=s)
            plt.pause(game["timeBetweenFrames"])
            plt.close("all")
            self.draw(board.board)
        plt.clf()

    def display_results(self, scores):
        a = np.convolve(scores, np.ones((100,)) / 100, mode="valid")
        plt.ylim(0, max(a) + 2)
        plt.plot(a)
        plt.show()
