from __future__ import division
import pandas as pd
from decimal import Decimal


class Classifier:
    def __init__(self, train, structure, bins_amount, dir_path):
        self.train = train
        self.structure = structure.get_structure()
        self.bins_amount = bins_amount;
        self.dir_path = dir_path
        self.progress = 0
        self.row_done = 0

    def set_test_class(self, test_class):
        self.test_class = test_class

    def build_model(self):
        _m = 2
        self.summary = pd.DataFrame(columns=['column', 'column_val', 'classification_val', 'm_esti'])
        data = self.train.get_train()

        self.classes_count = data[data.columns[-1]].value_counts()
        self.classes_probablity = self.classes_count / self.classes_count.sum()
        self.classes = data[data.columns[-1]].unique()  # classes names

        for column in data:
            # column_val_count = data[column].unique().size
            column_val_count = self.structure[self.structure["attribute_name"] == column]
            column_val_count = column_val_count.iloc[0]["attribute_value_count"]
            if (column_val_count == 0):  # this is numeric
                column_val_count = self.bins_amount
            different_column_vals = data[column].unique()
            for column_val in different_column_vals:
                for classification_val in self.classes:
                    col_val_and_class = len(
                        data[(data[column] == column_val) & (data[data.columns[-1]] == classification_val)])
                    m_esti = (col_val_and_class + _m * (1 / column_val_count)) / (
                    self.classes_count[classification_val] + _m)
                    self.summary.loc[len(self.summary)] = [column, column_val, classification_val, m_esti]

    def getMaxValue(self, MyCount):
        max = 0
        ind = "";
        for key, val in MyCount.items():
            val = Decimal(val)
            if (max <= val):
                max = val
                ind = key
        return ind

    def classify(self):
        self.test_data = self.test_class.get_test()
        # remove class column
        self.answer_list = []
        dataWithNoClass = self.test_data.drop(self.test_data.columns[len(self.test_data.columns) - 1], axis=1,
                                              inplace=False)
        dataWithNoClass.apply(lambda row: self.getClassification(row), axis=1)
        self.get_accuracy()
        self.write_output_file(self.dir_path)

    def write_output_file(self, path):
        text_file = open(path + "/output.txt", "w")
        for i in range(0, self.answer_list.__len__() - 1):
            text_file.write(self.answer_list[i] + "\n")
        text_file.close()

    def getClassification(self, row):
        MyCount = {}
        for class_val in self.classes:
            totalMultiply = 1
            for column, column_val in row.iteritems():
                rowFromSummary = self.summary[
                    (self.summary['column'] == column) & (self.summary['column_val'] == column_val) & (
                    self.summary['classification_val'] == class_val)]
                if rowFromSummary.empty == False:
                    m_esti = rowFromSummary['m_esti'].values[0]
                else: # we have tuple that we didn't have in the  train test
                    count_diff_val = self.structure[self.structure["attribute_name"] == column]
                    count_diff_val = count_diff_val.iloc[0]["attribute_value_count"]
                    if (count_diff_val == 0):  # this is numeric
                        count_diff_val = self.bins_amount
                    m_esti = (0 + 2 * (1 / count_diff_val)) / (self.classes_count[class_val] + 2)
                totalMultiply = totalMultiply * m_esti
            MyCount[class_val] = totalMultiply * self.classes_probablity[class_val]
        ans = self.getMaxValue(MyCount)
        self.answer_list.append(ans)
        self.row_done += 1
        if (int((float(self.row_done) / float(self.test_data.__len__())) * 100) != self.progress):
            self.progress = int((float(self.row_done) / float(self.test_data.__len__())) * 100)
            print(str(self.progress) + "% done")

    def get_accuracy(self):
        hits = int(0)
        test_class = self.test_data["class"]
        classifier_class = self.answer_list
        for i in range(0, self.answer_list.__len__() - 1):
            if test_class[i] == classifier_class[i]:
                hits = hits + 1
        accuracy = "%.3f" % ((float(hits) / float(self.answer_list.__len__())) * 100)
        print("accuracy: " + accuracy)
        return accuracy
