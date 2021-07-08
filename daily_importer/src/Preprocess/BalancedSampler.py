import numpy as np
from pandas import DataFrame

from src.Preprocess.Sampler import Sampler


class BalancedSampler:

    def __init__(self, sampler: Sampler):
        self.sampler = sampler

    def sample(self, period, df: DataFrame, relevant_fields=None):
        x, y = self.sampler.sample(period=period, df_source=df, relevant_fields=relevant_fields)
        x_final, y_final = [], []

        # Get number of max allowed elements
        distribution = DataFrame(y).value_counts().sort_index()
        index_min_value = np.argmin(distribution.values)
        max_elements = distribution.values[index_min_value]

        # Initialize counter
        counter = {}
        for i in distribution.keys().to_list():
            counter[i[0]] = 0

        # Select sequences
        for row in np.c_[x, y]:
            sequence = row[:-1]
            target = int(row[-1])

            if counter[target] < max_elements:
                x_final.append(sequence)
                y_final.append(target)
                counter[target] += 1

        x_final = np.array(x_final)
        y_final = np.array(y_final)

        return x_final, y_final
