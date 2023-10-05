from Graph import Graph

graph = Graph(path="data/adjacency_matrix.csv")
shorter_path = graph.find_shorter_path()
print(shorter_path)
