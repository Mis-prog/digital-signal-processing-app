import pandas as pd
import os
import pickle
from mysignal import MySignal


class Model:
    def __init__(self):
        self.names_of_sheets_and_columns = None
        self.signal_current = None
        self.path_file = None
        self.buffer_signals = {}
        self.all_signals = {}

    def init(self):
        self.set_cache_file()
        self.connect_name_and_signal()

    def add_signal_in_buffer(self):
        _name = self.signal_current.__name_sheet + "/" + self.signal_current.__name_column
        if (_name) not in self.buffer_signals.keys():
            self.buffer_signals[_name] = self.signal_current
            return True
        return False

    def delete_signal_from_buffer(self, _name):
        if _name in self.buffer_signals.keys():
            del self.buffer_signals[_name]

    def set_cache_file(self):
        _name_cache_file = f"{self.path_file}.cache"
        if os.path.exists(_name_cache_file):
            with open(_name_cache_file, 'rb') as f:
                self.names_of_sheets_and_columns = pickle.load(f)
        else:
            self.names_of_sheets_and_columns = self.get_file_info()
            with open(_name_cache_file, 'wb') as f:
                pickle.dump(self.names_of_sheets_and_columns, f)

    def get_file_info(self):
        _all_data_from_files = pd.read_excel(self.path_file, sheet_name=None)
        _name_sheets_columns = {}
        for _name_sheet in _all_data_from_files.keys():
            _name_sheets_columns[_name_sheet] = _all_data_from_files[_name_sheet].keys()
        return _name_sheets_columns

    def connect_name_and_signal(self):
        for _name_sheet in self.names_of_sheets_and_columns.keys():
            _signals_for_sheet = []
            for _name_column in self.names_of_sheets_and_columns[_name_sheet]:
                _signal = MySignal(_name_sheet, _name_column, self.path_file)
                _signals_for_sheet.append(_signal)
            self.all_signals[_name_sheet] = _signals_for_sheet

    # доработать
    # def write_file(self, signals):
    #     for signal in signals:
    #         df = pd.read_excel(self.path_file, sheet_name=signal.__name_sheet)
    #         df[signal.__name_column] = signal.__data
    #         with pd.ExcelWriter(self.path_file, mode='a', if_sheet_exists='replace') as writer:
    #             df.to_excel(writer, sheet_name=signal.__name_sheet, index=False)
    #


# if __name__ == "__main__":
#     model = Model()
#     model.path_file = "../../../../data/data_big.xlsx"
#     model.init()
