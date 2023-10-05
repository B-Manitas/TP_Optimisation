import pandas as pd
import numpy as np


class Graph:
    def __init__(self, path: str, val_node_not_connected: int = -1) -> None:
        self.df_adjacency = None
        self.node_not_connected = val_node_not_connected

        if path:
            self.set_df_adjacency(path)

    def set_df_adjacency(self, path: str) -> None:
        self.df_adjacency = pd.read_csv(path, header=None, dtype=int)

    def get_previous_nodes_set(self, node: int) -> list:
        return set(self.df_adjacency[node][self.df_adjacency[node] > self.node_not_connected].index)

    def get_next_nodes_set(self, node: int) -> list:
        return set(self.df_adjacency[self.df_adjacency[node] > self.node_not_connected].index)

    def find_shorter_path(self) -> dict:
        first_node = self.df_adjacency.index[0]
        delta = {first_node: 0}
        shorter_path = {first_node: first_node}

        # Set of all nodes. (Equivalent to M in the TP).
        set_of_nodes = set(self.df_adjacency.index)

        # Set of visited nodes. (Equivalent to X in the TP).
        set_of_visited_nodes = {first_node}

        while set_of_visited_nodes != set_of_nodes:
            node_j = None

            # For each node in node_not_visited, check if all previous nodes are in set_of_visited_nodes
            for node in set_of_nodes - set_of_visited_nodes:
                if self.get_previous_nodes_set(node) - set_of_visited_nodes == set():
                    node_j = node
                    break

            # Find the minimum delta[node_j] and the node_i that minimize the distance
            delta[node_j] = np.inf
            min_node = None

            for node_i in self.get_previous_nodes_set(node_j):

                # delta[node_i] exist because node_i is a previous node of j
                min_delta = delta[node_i] + self.df_adjacency[node_j][node_i]

                # Find the minimum distance
                if delta[node_j] > min_delta:
                    delta[node_j] = min_delta
                    min_node = node_i

            set_of_visited_nodes.add(node_j)
            shorter_path[node_j] = min_node

        return delta, shorter_path
