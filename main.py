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
        self.dir = os.scandir("C:/DSSAT47/Cassava/")

        try:
            self.file = next(file for file in self.dir if file.name == filename)
            self.filename = self.file.name
        except:
            self.filename = self._check_filename(filename)
            self.file = self._create_file()

        self.vars = {}
        self._read_file(self.file)
        #print(self.vars)
        #variables = ['L#SD',  'LAID',  'HWAD',  'LWAD',  'SWAD',  'TWAD']

    def _check_filename(self, filename):

        if re.search("(CST)$", filename.split(".")[1]):
            if len(filename.split(".")[0]) == 8:
                return filename
            else:
                raise ValueError("file name must have 8 characters")
        else:
            raise ValueError("file extension must be '.CST'")

    def _create_file(self):
        raise NotImplementedError

    def _read_file(self, file):

        with open(file.path) as f:
            for i, l in enumerate(f.readlines()):

                if l[0] == '!':  # skip comments
                    continue

                if l[0] == '@':  # start of section

                    self._read_header(l[1:])
                    continue

                if self.vars:
                    if l.strip() == "":
                        continue

                    self._read_values(l)


    def _read_header(self, line):
        new_vars = {var: self._get_specs(var, line) for var in line.split()
                          if var not in self.vars}

        self.vars.update(new_vars)

    def _get_specs(self, var, line):
        start = re.search(var, line).start()
        end = re.search(var, line).end()

        if var == "TRNO":
            return (start, end + 1)
        else:
            return (start - 1, end)

    #def _read_values(self, line):
    #    for k, v in self.vars.items():

