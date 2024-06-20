import pandas as pd
import numpy as np


class MySignal:
    def __init__(self, name_sheet, name_column, path):
        self.name_sheet = name_sheet
        self.name_column = name_column
        self.path = path
        self.data = None

    def get_name_sheet(self):
        return self.name_sheet

    def get_name_column(self):
        return self.name_column

    def get_data(self):
        current_data_all = pd.read_excel(self.path, sheet_name=self.name_sheet)
        data_ = current_data_all[['MD', self.name_column]]
        return data_

    def get_data_with_frequency(self, frequency):
        if not self.data_:
            return None
        else:
            return self.data_[::frequency]

    def get_data_start_end_work(self):

        if not self.data_:
            return None
        else:
            self.data_start_end = []
            md_values = self.data_['MD'].values

            start_node = None
            end_node = None
            for i, value in enumerate(self.data_[self.name_sheet]):
                if value != -999.25:
                    start_node = md_values[i]
                    break

            for i, value in reversed(list(enumerate(self.data_[self.name_sheet]))):
                if value != -999.25:
                    end_node = md_values[i]
                    break

            self.data_start_end.append((start_node, end_node))

            return self.data_start_end

    def data_to_index(self, start, end):
        init_value = self.data_['MD'].iloc[0]
        h = self.data_['MD'].iloc[1] - init_value

        section_start = int(abs(start - init_value) / h)
        section_end = int(abs(end - init_value) / h)

        index = []
        index.append((section_start, section_end))
        return index

    def get_data_border_work(self):
        data_border_work = []
        md_values = self.data_['MD'].values

        start_node = None
        for i, value in enumerate(self.data_[self.name_column]):
            if value != -999.25 and start_node is None:
                start_node = md_values[i]
            elif value == -999.25 and start_node is not None:
                data_border_work.append((start_node, md_values[i - 1]))
                start_node = None
        if start_node is not None:
            data_border_work.append((start_node, md_values[-1]))
        return data_border_work

    def get_data_border_not_work(self):
        data_border_not_work = []
        md_values = self.data_['MD'].values

        start_node = None
        for i, value in enumerate(self.data_[self.name_column]):
            if value == -999.25 and start_node is None:
                start_node = md_values[i]
            elif value != -999.25 and start_node is not None:
                data_border_not_work.append((start_node, md_values[i - 1]))
                start_node = None
        if start_node is not None:
            data_border_not_work.append((start_node, md_values[-1]))
        return data_border_not_work
