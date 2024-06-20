import sys
from window import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QTreeWidgetItem, QMessageBox, QTableWidgetItem, QMenu,QVBoxLayout
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
from data import Data
from signal_ import Signal
from plot import MplCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self ,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.open_dialog.clicked.connect(self.open_file_dialog)
        self.list_signals.itemClicked.connect(self.display_selected_signal)
        self.set_signal.clicked.connect(self.set_current_signal)
        self.buffer_signals.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.buffer_signals.customContextMenuRequested.connect(self.show_context_menu)
        self.plot_smoothing()
        # self.save_file.clicked.connect(self.save_different)

    def open_file_dialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "",
                                                  "Excel Files (*.xlsx; *.xls);;All Files (*)")
        if fileName:
            self.data = Data(fileName)
            self.set_tree_widget()
            self.show_success_message()

    def show_success_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Файл успешно загружен")
        msg.setWindowTitle("Success")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

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
            self.signal_сurrent = signal

    def set_current_signal(self):
        if self.signal_name.text() and self.data.add_signal_in_buffer(self.signal_name.text(), self.signal_сurrent):
            row_position = self.buffer_signals.rowCount()
            self.buffer_signals.insertRow(row_position)
            item = QTableWidgetItem(self.signal_name.text())
            self.buffer_signals.setItem(row_position, 0, item)

    def show_context_menu(self, pos):
        index = self.buffer_signals.indexAt(pos)
        if not index.isValid():
            return

        context_menu = QMenu(self)
        work_action = QAction('Отобразить сигнал', self)
        delete_action = QAction('Удалить', self)

        # # Подключаем действия к слотам
        # work_action.triggered.connect(lambda: self.work_with_signal(index.row()))
        # delete_action.triggered.connect(lambda: self.delete_signal(index.row()))
        #
        context_menu.addAction(work_action)
        context_menu.addAction(delete_action)

        context_menu.exec(self.buffer_signals.mapToGlobal(pos))

    def plot_smoothing(self):
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

        toolbar = NavigationToolbar(sc, self)
        smoothing_layout = QVBoxLayout()
        smoothing_layout.addWidget(toolbar)
        smoothing_layout.addWidget(sc)

        self.smoothing_widget.setLayout(smoothing_layout)
        self.e

# def get_index_data(self):
#     if len(self.buffer[self.signal.name_sheet]) == 0:
#         self.buffer[self.signal.name_sheet]=[]
#         self.buffer[self.signal.name_sheet].append(self.signal)
#     else:
#         self.buffer[self.signal.name_sheet].append(self.signal)
#     return None
#
# def save_different(self):
#     if len(self.buffer) != 0:
#         self.data.write_file(self.buffer)
