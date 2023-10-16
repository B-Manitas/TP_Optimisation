from Graph import Graph
from Finance import Finance

# TP1
print("==========")
print("TP1")
graph = Graph(path="data/adjacency_matrix.csv")
shorter_path = graph.find_shorter_path()
print(f"The shorter path is {shorter_path[1]}.")
print(f"The valuation associates to this shorter path is {shorter_path[0]}.")

# Projet Finance
print("\n==========")
print("PROJET FINANCE")

p, initial_currency = 1, "EURO"

finance = Finance(path_df="data/currency.csv",
                  max_iter=p, 
                  initial_currency=initial_currency)
optimum = finance.find_optimum_path()
print(f"Args: p: {p}, initial currency: {initial_currency}")
print(f"The optimal path is {optimum[1]} with a value of {optimum[0]}.")