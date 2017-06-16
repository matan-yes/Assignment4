import pandas as pd
import numpy as np


class Test:
    def __init__(self,path, structure,classifier, bins_amount):
        self.test = pd.read_csv(path, sep=",")
        self.structure = structure
        self.classifier = classifier
        self.bins_amount = bins_amount;

    def get_test(self):
        return self.test

    def clean_test(self):
        # Discretization
        for column in self.test:
            # We discretizate only numeric columns
            if self.structure.loc[self.structure['attribute_name'] == column]['attribute_value'].values == 'NUMERIC':
                self.test[column] = self.discretization(self.test[column], self.bins_amount)

    def classify_test(self):
        self.classifier.set_test_class(self)
        self.classifier.classify()

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