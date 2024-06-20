from window import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTreeWidgetItem, QTableWidgetItem, QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from mysignal import MySignal


class View(QMainWindow, Ui_MainWindow):
    def __init__(self, model, parent=None):
        super(View, self).__init__()
        self.setupUi(self)

        self._model = model

        self.buffer_signals.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    def show_success_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Файл успешно загружен")
        msg.setWindowTitle("Success")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def set_treewidget(self):
        self.list_signals.clear()
        for _sheet in self._model.all_signals.keys():
            _parent = QTreeWidgetItem(self.list_signals)
            _parent.setText(0, _sheet)
            for _signal in self._model.all_signals[_sheet]:
                child = QTreeWidgetItem(_parent)
                child.setText(0, _signal.name_column)
                child.setData(0, 1, _signal)

    def display_selected_signal(self, item):
        signal = item.data(0, 1)
        if isinstance(signal, MySignal):
            self.signal_name.setText(signal.name_sheet + "/" + signal.name_column)
            self._model.signal_current = signal

    def set_current_signal(self):
        if self.signal_name.text() and self._model.add_signal_in_buffer():
            row_position = self.buffer_signals.rowCount()
            self.buffer_signals.insertRow(row_position)
            item = QTableWidgetItem(self.signal_name.text())
            self.buffer_signals.setItem(row_position, 0, item)

    def clear_buffer_signals_widget(self):
        rows = self.buffer_signals.rowCount()

        for row in range(rows - 1, -1, -1):
            self.buffer_signals.removeRow(row)

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
