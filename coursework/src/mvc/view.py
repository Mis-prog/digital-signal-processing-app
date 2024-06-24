from window import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTreeWidgetItem, QTableWidgetItem, QMenu, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from mysignal import MySignal

import matplotlib

matplotlib.use('QtAgg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class View(QMainWindow, Ui_MainWindow):
    def __init__(self, model, parent=None):
        self.signal_plot = None

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
                child.setText(0, _signal.__name_column)
                child.setData(0, 1, _signal)

    def display_selected_signal(self, item):
        signal = item.__data(0, 1)
        if isinstance(signal, MySignal):
            self.signal_name.setText(signal.__name_sheet + "/" + signal.__name_column)
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
        work_action.triggered.connect(lambda: self.work_with_signal(index.row()))
        delete_action.triggered.connect(lambda: self.delete_signal(index.row()))
        context_menu.addAction(work_action)
        context_menu.addAction(delete_action)

        context_menu.exec(self.buffer_signals.mapToGlobal(pos))

    def delete_signal(self, row):
        _name = self.buffer_signals.item(row, 0).text()
        _signal = self._model.buffer_signals[_name]
        self.buffer_signals.removeRow(row)
        self._model.delete_signal_from_buffer(row)
        if self.smoothing_widget.layout() is not None and self.signal_plot == _signal:
            self.clearLayout(self.smoothing_widget.layout())
            self.clearLayout(self.eliminating_gaps_widget.layout())
            self.clearLayout(self.anomaly_search_widget.layout())

    def work_with_signal(self, row):
        if self.smoothing_widget.layout() is not None:
            self.clearLayout(self.smoothing_widget.layout())
        else:
            self.smoothing_widget.setLayout(QVBoxLayout())

        if self.eliminating_gaps_widget.layout() is not None:
            self.clearLayout(self.eliminating_gaps_widget.layout())
        else:
            self.eliminating_gaps_widget.setLayout(QVBoxLayout())

        if self.anomaly_search_widget.layout() is not None:
            self.clearLayout(self.anomaly_search_widget.layout())
        else:
            self.anomaly_search_widget.setLayout(QVBoxLayout())

        _name = self.buffer_signals.item(row, 0).text()
        _signal = self._model.buffer_signals[_name]
        self.signal_plot = _signal

        sc1 = MplCanvas(self, width=5, height=4, dpi=100)
        sc2 = MplCanvas(self, width=5, height=4, dpi=100)
        sc3 = MplCanvas(self, width=5, height=4, dpi=100)

        _data = _signal.get_data()

        sc1.axes.plot(_data['MD'], _data[_signal.get_name_column()])
        sc2.axes.plot(_data['MD'], _data[_signal.get_name_column()])
        sc3.axes.plot(_data['MD'], _data[_signal.get_name_column()])

        toolbar1 = NavigationToolbar(sc1, self)
        toolbar2 = NavigationToolbar(sc2, self)
        toolbar3 = NavigationToolbar(sc3, self)

        layout_1 = self.smoothing_widget.layout()
        layout_1.addWidget(toolbar1)
        layout_1.addWidget(sc1)

        layout_2 = self.eliminating_gaps_widget.layout()
        layout_2.addWidget(toolbar2)
        layout_2.addWidget(sc2)

        layout_3 = self.anomaly_search_widget.layout()
        layout_3.addWidget(toolbar3)
        layout_3.addWidget(sc3)




    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().setParent(None)

    def set_widget(self, widget):
        pass