import pandas as pd
from scipy.stats import mode
import numpy as np

class Train:

    def __init__(self,path, structure, bins_amount):
        self.train = pd.read_csv(path, sep=",")
        self.structure = structure
        self.bins_amount = bins_amount

    def get_train(self):
        return self.train

    def clean_train(self):
        # Fill missing values
        for column in self.train:
            if self.structure.loc[self.structure['attribute_name'] == column]['attribute_value'].values == 'NUMERIC':
                self.train[column].fillna((self.train[column].mean()), inplace=True)
            if self.structure.loc[self.structure['attribute_name'] == column]['attribute_value'].values == 'DISCRETE':
                self.train[column].fillna(mode(self.train[column]).mode[0], inplace=True)
        # Discretization
        for column in self.train:
            # We discretizate only numeric columns
            if self.structure.loc[self.structure['attribute_name'] == column]['attribute_value'].values == 'NUMERIC':
                self.train[column] = self.discretization(self.train[column], self.bins_amount)

    def check_bin_max(self):
        return len(self.train.index)-1

    def discretization(self, col, bins_amount):
        minval = col.min()
        maxval = col.max()
        # the distance beween each bin
        cut_point_step = (maxval - minval) / bins_amount
        bins = list(np.arange(minval + cut_point_step, maxval - 0.1, cut_point_step))
        # create list by adding min and max to cut_points
        break_points = [minval] + bins + [maxval]
        labels = range(len(bins) + 1)
        # Binning using cut function of pandas
        col = pd.cut(col, bins=break_points, labels=labels, include_lowest=True)
        return col