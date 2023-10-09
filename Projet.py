import pandas as pd
from itertools import product

def get_valuation(path: tuple) -> float:
    valuation = 1

    for i in range(len(path) - 1):
        valuation *= df_currency[path[i]][path[i + 1]]

    return valuation

p = 3
paths = {}
df_currency = pd.read_csv('data/currency.csv', sep=',', index_col=0, header=0)
df_currency = df_currency.astype(float)
initial_currency = "EURO"

for i in range(2, p + 1):
    all_paths = product(df_currency.index, repeat=i)

    for path in all_paths:
        if path[0] == initial_currency and path[-1] == initial_currency:
            paths[path] = get_valuation(path)

max_valuation = max(paths, key=paths.get)
print(max_valuation, paths[max_valuation])