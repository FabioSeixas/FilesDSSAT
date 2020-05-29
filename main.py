import os
import re
import time

import pandas as pd
from datetime import datetime



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

    def _round_numbers(self, values, var):
        if max(values) > 10:
            return [int(value) for value in values]
        elif max(values) < 10 and var == "GSTD":
            return [int(value) for value in values]
        else:
            return [round(value, 2) for value in values]

    def choose_variables(self, var_list, cultivar):
        self.choosed_vars = [var for var in var_list if var in self.vars]

        self.process_vars(cultivar)

    def get_var_values(self, var, cultivar, trat):
        avg = self.data.loc[(self.data["VARIEDADE"] == cultivar) &
                            (self.data["TRATAMENTO"] == trat)].groupby(["DATA DA AVALIAÇÃO", "DAP"]).mean()

        var_index = next(index[0] for index in enumerate(avg)
                         if var == index[1])

        return self.process_values(avg.iloc[:, var_index], var)

    def process_values(self, serie, var):
        values = self._round_numbers(serie.values, var)
        index = [(i.date().strftime("%y%j"), dap) for i, dap in serie.index]

        return [i + (v, ) for i, v in zip(index, values)]

    def process_vars(self, cultivar):
        self.values = {i: {var: self.get_var_values(var, cultivar, trat)
                          for var in self.choosed_vars}
                      for i, trat in enumerate(self.trats, start = 1)}

    def write_file(self, target):

        trat_sizes = self._size_table()

        with open(f"C:/DSSAT47/Cassava/{target.filename}", mode = "w") as f:
            f.write("*EXP. DATA (T): \n \n")

            self._write_header(f, target)
            f.write("\n")

            for i, trat in enumerate(self.trats, start = 1):
                self._write_table(f, target, i, trat_sizes[i - 1])

    def _write_header(self, file, target):
        file.write("@TRNO ")
        for n in target.variables:
            file.write(self._handle_header_spaces(n))

    def _handle_header_spaces(self, var):
        while len(var) < 6:
            var = " " + var
        return var

    def _write_table(self, file, target, trat, size):
        print(self.values)
        for l in range(size):
            file.write("     ")
            file.write(f'{trat}')
            values = self.get_line_values(trat, l)
            for var_value in values:

                try:
                    if var_value[0] == date:
                        if var_value[1] == dap:
                            pass
                        else:
                            raise ValueError("valores de dap entre variaveis não correspondem")
                    else:
                        raise ValueError("valores de date entre variaveis não correspondem")
                except:
                    date, dap, val = [*var_value]
                    file.write(self._handle_header_spaces(str(date)))
                    file.write(self._handle_header_spaces(str(dap)))

                date, dap, val = [*var_value]
                file.write(self._handle_header_spaces(str(val)))

            file.write("\n")


    def _size_table(self):
        size = []
        for values in self.values.values():
            lengths = [len(v) for v in values.values()]
            size.append(max(lengths))
        return size

    def get_line_values(self, trat, line):
        return [v[line] for v in self.values[trat].values()]





class targetFile(File):

    def __init__(self, filename):
        self.dir = os.scandir("C:/DSSAT47/Cassava/")

        try:
            # if file already exist
            self.file = next(file for file in self.dir if file.name == filename)
            self.filename = self.file.name
        except:
            # if file do not exist
            self.filename = self._check_filename(filename)
            self.file = self._create_file()

        self.variables = ['DATE', 'DAP']

    def _check_filename(self, filename):

        if re.search("(CST)$", filename.split(".")[1]):
            if len(filename.split(".")[0]) == 8:
                return filename
            else:
                raise ValueError("file name must have 8 characters")
        else:
            raise ValueError("file extension must be '.CST'")

    def _create_file(self):

        with open(f'C:/DSSAT47/Cassava/{self.filename}', mode = "w"):
            print(f' \n {self.filename} created on "C:/DSSAT47/Cassava/"')

        self.dir = os.scandir("C:/DSSAT47/Cassava/")

        return next(file for file in self.dir if file.name == self.filename)

    def _read_file(self, file):

        self.vars = {}
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

    def _read_values(self, line):
        raise NotImplementedError

    def set_variables(self, var_list):
        self.variables.extend([var for var in var_list
                               if var not in self.variables])




