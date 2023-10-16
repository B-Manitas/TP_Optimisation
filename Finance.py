import pandas as pd
from itertools import product


class Finance:
    def __init__(self, path_df: str, max_iter: int = 3, initial_currency: str = "EURO") -> None:
        """
            Class to find the optimal profit.

            Args:
                path_df (str): the path of the file containing the currency matrix in the format '.csv'.
                max_iter (int): the maximum number of exchange. Must be greather than 2.
                initial_currency (str): the initial currency.
        """

        # Load the dataframe containing currency data.
        self.df_currency = pd.read_csv(path_df, index_col=0, header=0)
        self.df_currency = self.df_currency.astype(float).T

        # Throw an error if max_iter less than 1.
        if max_iter <= 0:
            raise Exception(
                "The 'max_iter' argument must be greather than 0. Actual :" + max_iter)

        self.max_iter = max_iter

        # Throw an error if initial_currency not a key of the dataframe.
        if initial_currency not in self.df_currency.columns:
            raise Exception(
                "The 'initial_currency' argument must be a key of the dataframe. Actual :" + initial_currency)

        self.initial_currency = initial_currency

    def get_valuation(self, path: tuple) -> float:
        """
            Get the valuation of path.

            Args:
                path (tuple): the tuple containing currency

            Returns:
                float: the valuation of the path
        """
        valuation = 1

        for i in range(len(path) - 1):
            # Remove duplication path
            # Ex: valuation self.df_currency["EURO"]["EURO"]
            if path[i] == path[i+1]:
                valuation = 0

            else:
                valuation *= self.df_currency[path[i]][path[i + 1]]

        return valuation

    def find_optimum_path(self) -> tuple:
        """
            Find the path with the maximum valuation.

            Returns:
                - float: the maximum valuation
                - tuple: the path associate to this maximum valuation
        """
        # Stored all valid paths associating to their value
        paths_values_dict = {}

        for i in range(1, self.max_iter + 1):
            # Generate all possibles combinaisons
            all_paths = product(self.df_currency.index, repeat=i)

            for path in all_paths:
                # Valid path must be start and end with the initial currency
                if path[0] == self.initial_currency and path[-1] == self.initial_currency:
                    paths_values_dict[path] = self.get_valuation(path)

        return max(zip(paths_values_dict.values(), paths_values_dict.keys()))
