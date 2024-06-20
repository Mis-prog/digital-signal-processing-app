import pandas as pd
import pickle
import os
from signal_ import Signal


class Data:
    def __init__(self, path):
        self.buffer = {}
        self.signals = {}
        self.path = path
        self.cache_file = f"{path}.cache"
        self.set_cache_file()
        self.connect_name_and_signal()

    def set_cache_file(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                self.name_sheets_columns = pickle.load(f)
        else:
            self.name_sheets_columns = self.get_name_sheets_columns()
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.name_sheets_columns, f)

    def get_name_sheets(self):
        return pd.ExcelFile(self.path).sheet_names

    def get_name_columns(self, sheet):
        data_current = pd.read_excel(self.path, sheet_name=sheet)
        data_current = data_current.iloc[:, 1:]
        return data_current.columns[1:]

    def get_name_sheets_columns(self):
        name_sheets = self.get_name_sheets()
        name_sheets_columns = {}
        for name_sheet in name_sheets:
            name_sheets_columns[name_sheet] = self.get_name_columns(name_sheet)
        return name_sheets_columns

    def connect_name_and_signal(self):
        for name_sheet in self.name_sheets_columns.keys():
            current_signals = []
            for name_column in self.name_sheets_columns[name_sheet]:
                signal = Signal(name_sheet, name_column, self.path)
                current_signals.append(signal)
            self.signals[name_sheet] = current_signals

    def write_file(self, signals):
        for signal in signals:
            df = pd.read_excel(self.path, sheet_name=signal.name_sheet)
            df[signal.name_column] = signal.data
        df.to_excel(self.path, sheet_name=signal.name_sheet, index=False)

    def add_signal_in_buffer(self, name, signal):
        if name not in self.buffer.keys():
            self.buffer[name] = signal
            return True
        return False

    def delete_signal_from_buffer(self, name):
        if name in self.buffer.keys():
            self.buffer[name].remove(name)
