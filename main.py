import os
import re

import pandas as pd


class File(object):

    def __init__(self, directory):
        self.dir = directory


class sourceFile(File):

    def __init__(self, directory):
        super().__init__(directory)

        self.data = self._read_data()
        self.vars = self._getAvailableVariables()
        self.cultivars = self.data["VARIEDADE"].unique()
        self.trats = self.data["TRATAMENTO"].unique()

    def _read_data(self):
        try:
            data = pd.read_csv(self.dir)
        except:
            data = pd.read_excel(self.dir)

        return self._drop_na_columns(data)

    def _drop_na_columns(self, data):
        to_drop = [to_drop[0] for to_drop in enumerate(data.columns)
                   if str(to_drop[1]).startswith("Unnamed")]

        return data.drop(data.columns[to_drop], axis=1)

    def _getAvailableVariables(self):
        return [var for var in self.data.columns]

    def get_var(self, var, cultivar, trat):
        avg = self.data.loc[(self.data["VARIEDADE"] == cultivar) &
                            (self.data["TRATAMENTO"] == trat)].groupby("DAP").mean()

        var_index = next(index[0] for index in enumerate(avg)
                         if var == index[1])

        return avg.iloc[:, var_index]


class targetFile(File):

    def __init__(self, filename):
        self.dir = os.scandir("C:/DSSAT47/Cassava")

        try:
            next(file.name for file in self.dir if file.name == filename)
            self.filename = filename
        except:
            self.filename = self._check_filename(filename)

    def _check_filename(self, filename):

        if re.search("(CST)$", filename.split(".")[1]):
            if len(filename.split(".")[0]) == 8:
                return filename
            else:
                raise ValueError("file name must have 8 characters")
        else:
            raise ValueError("file extension must be '.CST'")

    # def _read_file(self):
    #     file = os.scandir(self.dir.split("/")[:-1])
    #     print(file)
    #     with open(file.path) as f:
    #         print(f)
