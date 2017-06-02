import pandas as pd



class Test:
    def __init__(self,path):
        self.test = pd.read_csv(path, sep=",")

    def get_test(self):
        return self.test



    #not sure if needed
    def clean_test(self):
        raise NotImplementedError


    def classify_test(self):
        raise NotImplementedError

    def get_alon(self):
        print("alon")

    def get_alonn(self):
        print("alon")
