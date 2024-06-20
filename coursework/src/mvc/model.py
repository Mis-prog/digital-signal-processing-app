import pandas as pd
import os
import pickle
from mysignal import MySignal


class Model:
    def __init__(self):
        self.signal_current = None
        self.name_cache_file = None
        self.path_file = None
        self.buffer_signals = {}
        self.all_signals = {}

    def init(self):
        self.set_cache_file()
        self.connect_name_and_signal()

    def add_signal_in_buffer(self):
        _name = self.signal_current.name_sheet + "/" + self.signal_current.name_column
        if (_name) not in self.buffer_signals.keys():
            self.buffer_signals[_name] = self.signal_current
            return True
        return False

    def set_cache_file(self):
        _name_cache_file = f"{self.path_file}.cache"
        if os.path.exists(_name_cache_file):
            with open(_name_cache_file, 'rb') as f:
                self.name_sheets_columns = pickle.load(f)
        else:
            self.name_sheets_columns = self.get_name_sheets_columns()
            with open(_name_cache_file, 'wb') as f:
                pickle.dump(self.name_sheets_columns, f)

    def get_name_sheets(self):
        return pd.ExcelFile(self.path_file).sheet_names

    def get_name_columns(self, sheet):
        _data_current = pd.read_excel(self.path_file, sheet_name=sheet)
        _data_current = _data_current.iloc[:, 1:]
        return _data_current.columns[1:]

    def get_name_sheets_columns(self):
        _name_sheets = self.get_name_sheets()
        _name_sheets_columns = {}
        for _name_sheet in _name_sheets:
            _name_sheets_columns[_name_sheet] = self.get_name_columns(_name_sheet)
        return _name_sheets_columns

    def connect_name_and_signal(self):
        self.all_signals = {}
        for _name_sheet in self.name_sheets_columns.keys():
            _current_signals = []
            for _name_column in self.name_sheets_columns[_name_sheet]:
                _signal = MySignal(_name_sheet, _name_column, self.path_file)
                _current_signals.append(_signal)
            self.all_signals[_name_sheet] = _current_signals

    def write_file(self, signals):
        for signal in signals:
            df = pd.read_excel(self.path_file, sheet_name=signal.name_sheet)
            df[signal.name_column] = signal.data
            with pd.ExcelWriter(self.path_file, mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=signal.name_sheet, index=False)


    def delete_signal_from_buffer(self, name):
        if name in self.buffer_signals.keys():
            del self.buffer_signals[name]

# if __name__ == "__main__":
#     model = Model()
#     model.path_file = "../../../../data/data_big.xlsx"
#     model.init()
