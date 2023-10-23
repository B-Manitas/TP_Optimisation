import pandas as pd
import numpy as np


class Graph:
    """
    Class to represent a graph

    Args:
        path (str): path to the adjacency matrix csv file
        val_node_not_connected (int): value of the adjacency matrix for nodes not connected. Default: -1
    """

    def __init__(self, path: str, val_node_not_connected: int = -1) -> None:
        self.df_adjacency = None
        self.node_not_connected = val_node_not_connected

        if path:
            self.set_df_adjacency(path)

    def set_df_adjacency(self, path: str) -> None:
        """
        Set the adjacency matrix from a csv file

        Args:
            path (str): path to the adjacency matrix csv file
        """
        self.df_adjacency = pd.read_csv(path, header=None, dtype=int)

    def get_previous_nodes_set(self, node: int) -> set:
        """
        Get the set of previous nodes of a node

        Args:
            node (int): node to get the previous nodes

        Returns:
            set: set of previous nodes of the node
        """
        return set(self.df_adjacency[node][self.df_adjacency[node] > self.node_not_connected].index)

    def get_next_nodes_set(self, node: int) -> set:
        """
        Get the set of next nodes of a node

        Args:
            node (int): node to get the next nodes

        Returns:
            set: set of next nodes of the node
        """
        return set(self.df_adjacency[self.df_adjacency[node] > self.node_not_connected].index)

    def is_cyclic(self) -> bool:
        """
        Check if a graph is cyclic (TP1: Question 2)

        Returns:
            bool: True if the graph is cyclic, False otherwise
        """
        # Set of all nodes. (Equivalent to M in the TP).
        set_of_visited_nodes = set()

        # Set of visited nodes. (Equivalent to X in the TP).
        set_of_nodes = set(self.df_adjacency.index)
        df_adjency = self.df_adjacency.copy()

        while set_of_nodes - set_of_visited_nodes != set():
            xi = None

            # Get a node that is not visited
            for node in set_of_nodes - set_of_visited_nodes:
                if self.get_next_nodes_set(node) == set():
                    xi = node
                    break

            # Remove xi everywhere it appears in next nodes of nodes not visited
            for node in set_of_nodes - set_of_visited_nodes:
                self.df_adjacency[node][xi] = self.node_not_connected

            # Add xi to the set of visited nodes
            set_of_visited_nodes.add(xi)

        # Set the adjacency matrix to the original one
        self.df_adjacency = df_adjency

        # If all nodes are visited, the graph is not cyclic
        if set_of_visited_nodes == set_of_nodes:
            return False

        # If not, the graph is cyclic
        else:
            return True

    def find_shorter_path(self):
        """
        Find the shorter path in a graph without cycles (TP1: Question 3)

        Returns:
            dict: dict with the distance of the shorter path
            dict: dict with the previous node of each node in the shorter path
        """
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
