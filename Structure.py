from numpy import genfromtxt
import pandas as pd
import re


class Structure:
    def __init__(self,path):
        #self.structure = genfromtxt(path, delimiter=' ')
        self.structure = pd.read_csv(path, sep=' ', names=["attr", "attribute_name", "attribute_value"])

    def get_structure(self):
        return self.structure[["attribute_name","attribute_value"]]



    def prepere_structure(self):
        self.names = self.structure["attribute_name"]
        optional_values = self.structure["attribute_value"]
        for index in range(len( optional_values)):
            if(optional_values[index] == "NUMERIC"):
                continue
            else:
                line = str(optional_values[index]).replace("{","").replace("}","")
                splited_line = re.split(',',line)
                if("yes" in splited_line and "no" in splited_line and len(splited_line)==2):
                    optional_values[index] = "binary".upper()
                else:
                    if(len(splited_line)>=2):
                        optional_values[index] = "discrete".upper()
        self.structure["attribute_value"] = optional_values







