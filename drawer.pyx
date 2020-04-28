import networkx as nx
import matplotlib.pyplot as plt
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
            map(
                lambda node: node.coordinates,
                filter(lambda node: not node.owner, nodes),
            )
        )
        player1_nodes = list(
            map(
                lambda node: node.coordinates,
                filter(lambda node: not node.owner == 1, nodes),
            )
        )
        player2_nodes = list(
            map(
                lambda node: node.coordinates,
                filter(lambda node: not node.owner == 2, nodes),
            )
        )

        pos = self.generate_pos(board)
        fig, ax = plt.subplots()
        nx.draw_networkx_nodes(
            G, ax=ax, pos=pos, nodelist=player1_nodes, node_color="r"
        )
        nx.draw_networkx_nodes(
            G, ax=ax, pos=pos, nodelist=player2_nodes, node_color="black"
        )
        nx.draw_networkx_nodes(
            G, ax=ax, pos=pos, nodelist=empty_nodes, node_color="white"
        )
        nx.draw_networkx_edges(G, ax=ax, pos=pos)
        nx.draw_networkx_labels(G, ax=ax, pos=pos, font_color="black")
        ax.invert_yaxis()
        plt.axis("off")
        plt.show(block=True)

    def generate_pos(self, board):
        pos = {}
        for i in range(len(board)):
            for j in range(len(board[i])):
                pos[board[i][j].coordinates] = [300 + i * -30 + j * 30, 30 * i + 30 * j]
        return pos

