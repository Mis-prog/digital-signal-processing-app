import pandas as pd
import numpy as np


class MySignal:
    def __init__(self, name_sheet: str, name_column: str, path: str):
        self.__path = path
        self.__name_sheet = name_sheet
        self.__name_column = name_column
        self.__data = None
        self.__diff_data = None
        self.__curr_data = None

    def get_name_sheet(self):
        return self.__name_sheet

    def get_name_column(self):
        return self.__name_column

    def set_data(self):
        self.__data = pd.read_excel(self.__path, sheet_name=self.__name_sheet)[['MD', self.__name_column]]
        self.__curr_data = self.__data

    def get_data_original(self):
        if self.__data.empty:
            return None
        else:
            return self.__data

    def set_data_curr(self, data: pd.DataFrame):
        self.__curr_data = data

    def get_data_curr(self, frequency: int = 1):
        if self.__curr_data.empty:
            return None
        else:
            return self.__curr_data[::frequency]

    def save_diff(self):
        self.__diff_data = self.__curr_data

    def back_signal(self):
        self.__curr_data = self.__diff_data

    def set_data_start_end_work(self):
        if self.__data.empty:
            return None
        else:
            _start_node = None
            _end_node = None
            for i, value in enumerate(self.__data[self.__name_column]):
                if value != -999.25:
                    _start_node = i
                    break

            for i, value in enumerate(reversed(self.__data[self.__name_column])):
                if value != -999.25:
                    _end_node = len(self.__data) - i
                    break
            self.__curr_data = self.__data.iloc[_start_node:_end_node]

    # Доработать
    # def data_to_index(self, start, end):
    #     init_value = self.data_['MD'].iloc[0]
    #     h = self.data_['MD'].iloc[1] - init_value
    #
    #     section_start = int(abs(start - init_value) / h)
    #     section_end = int(abs(end - init_value) / h)
    #
    #     index = []
    #     index.append((section_start, section_end))
    #     return index
    #
    # def get_data_border_work(self):
    #     data_border_work = []
    #     md_values = self.data_['MD'].values
    #
    #     start_node = None
    #     for i, value in enumerate(self.data_[self.__name_column]):
    #         if value != -999.25 and start_node is None:
    #             start_node = md_values[i]
    #         elif value == -999.25 and start_node is not None:
    #             data_border_work.append((start_node, md_values[i - 1]))
    #             start_node = None
    #     if start_node is not None:
    #         data_border_work.append((start_node, md_values[-1]))
    #     return data_border_work
    #
    # def get_data_border_not_work(self):
    #     data_border_not_work = []
    #     md_values = self.data_['MD'].values
    #
    #     start_node = None
    #     for i, value in enumerate(self.data_[self.__name_column]):
    #         if value == -999.25 and start_node is None:
    #             start_node = md_values[i]
    #         elif value != -999.25 and start_node is not None:
    #             data_border_not_work.append((start_node, md_values[i - 1]))
    #             start_node = None
    #     if start_node is not None:
    #         data_border_not_work.append((start_node, md_values[-1]))
    #     return data_border_not_work
