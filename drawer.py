import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class Drawer:
    def draw(self, game, board, board_size):
        self.board_size = board_size
        coords = self.coords
        G = nx.Graph()
        labels = {}
        nodes = self.state_in_ints(board)
        labels = [coords(i) for i in range(len(nodes))]
        G.add_nodes_from(labels)
        for i in range(len(nodes)):
            for neighbour in game.get_neighbours(i):
                if neighbour:
                    G.add_edge(coords(i), coords(neighbour))

        empty_nodes = [coords(i) for i in range(len(nodes)) if nodes[i] == 0]
        player1_nodes = [coords(i) for i in range(len(nodes)) if nodes[i] == 1]
        player2_nodes = [coords(i) for i in range(len(nodes)) if nodes[i] == 2]
        board = [coords(i) for i in range(len(nodes))]

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

    def coords(self, index):
        return (index // self.board_size, index % self.board_size)

    def state_in_ints(self, state):
        state_in_ints = []
        for pos in state:
            if pos[0] == 1:
                state_in_ints.append(1)
            elif pos[1] == 1:
                state_in_ints.append(2)
            else:
                state_in_ints.append(0)

        return state_in_ints

    def generate_pos(self, board):
        pos = {}
        for i in range(len(board)):
            node = board[i]
            i = node[0]
            j = node[1]
            pos[node] = [300 + i * -30 + j * 30, 30 * i + 30 * j]
        return pos

    def display_results(self, scores):
        a = np.convolve(scores, np.ones((100,)) / 100, mode="valid")
        plt.ylim(0, max(a) + 2)
        plt.plot(a)
        plt.show()
