import pandas as pd


class Train:

    def __init__(self,path):
        self.train = pd.read_csv(path, sep=",")

    def get_train(self):
        return self.train

    def clean_train(self):
        # Clean date
        # Discretization
        raise NotImplementedError

    def check_bin_max(self):
        return  len(self.train.index)-1





