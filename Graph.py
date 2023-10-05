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
        set_of_nodes = set(self.df_adjacency.index)
        set_of_visited_nodes = {first_node}

        while set_of_visited_nodes != set_of_nodes:
            node_not_visited = set_of_nodes - set_of_visited_nodes
            j = None

            for node in node_not_visited:
                if self.get_previous_nodes_set(node) - set_of_visited_nodes == set():
                    j = node
                    break

            delta[j] = np.inf
            for i in self.get_previous_nodes_set(j):
                # delta[i] exist because i is a previous node of j
                a = delta[i] + self.df_adjacency[j][i]

                if delta[j] > a:
                    delta[j] = a
                    set_of_visited_nodes.add(j)
                    break

        return delta
