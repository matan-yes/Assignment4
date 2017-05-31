
import pandas as pd

class Classifier:
    def buil_model(self,train):
        raise NotImplementedError

    def classify(self,test):
        raise NotImplementedError

    def write_output_file(salf,path):
        raise NotImplementedError