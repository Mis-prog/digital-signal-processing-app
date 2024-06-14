import sys
from window import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QTreeWidgetItem
from data import Data
from signal_ import Signal


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        self.signal = None
        self.buffer = {}
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.open_dialog.clicked.connect(self.open_file_dialog)
        self.list_signals.itemClicked.connect(self.display_selected_signal)
        self.set_signal.clicked.connect(self.set_current_signal)
        self.save_file.clicked.connect(self.save_different)

    def open_file_dialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "",
                                                  "Excel Files (*.xlsx; *.xls);;All Files (*)")
        if fileName:
            self.data = Data(fileName)
            self.set_tree_widget()

    def set_tree_widget(self):
        self.list_signals.clear()

        for sheet in self.data.signals.keys():
            parent = QTreeWidgetItem(self.list_signals)
            parent.setText(0, sheet)
            for signal in self.data.signals[sheet]:
                child = QTreeWidgetItem(parent)
                child.setText(0, signal.name_column)
                child.setData(0, 1, signal)

    def display_selected_signal(self, item):
        signal = item.data(0, 1)
        if isinstance(signal, Signal):
            self.signal_name.setText(signal.name_sheet + "/" + signal.name_column)
            self.current_signal = signal

    def set_current_signal(self):
        if self.signal_name.text():
            self.name_signal = self.signal_name.text().split('/')[1]
            self.signal = self.current_signal
            self.get_index_data()

    def get_index_data(self):
        if len(self.buffer[self.signal.name_sheet]) == 0:
            self.buffer[self.signal.name_sheet]=[]
            self.buffer[self.signal.name_sheet].append(self.signal)
        else:
            self.buffer[self.signal.name_sheet].append(self.signal)
        return None

    def save_different(self):
        if len(self.buffer) != 0:
            self.data.write_file(self.buffer)
