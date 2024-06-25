from window import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTreeWidgetItem, QTableWidgetItem, QMenu, QVBoxLayout
from PyQt6.QtWidgets import QFileDialog
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
        self._model = model
        super(View, self).__init__()
        self.setupUi(self)

        self.tablewidget_buffer_signals.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.open_dialog.clicked.connect(self.open_file_dialog)
        self.treewidget_all_signals.itemClicked.connect(self.display_selected_signal)
        self.set_signal.clicked.connect(self.set_current_signal)
        self.tablewidget_buffer_signals.customContextMenuRequested.connect(self.show_context_menu)

    def open_file_dialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")

        if fileName:
            self._model.buffer_signals.clear()
            self.clear_buffer_signals_widget()
            self._model.path_file = fileName
            self.show_success_message()
            self._model.init()
            self.set_treewidget()

    def show_success_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Файл успешно загружен")
        msg.setWindowTitle("Success")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def set_treewidget(self):
        self.treewidget_all_signals.clear()

        for _sheet in self._model.all_signals.keys():
            _parent = QTreeWidgetItem(self.treewidget_all_signals)
            _parent.setText(0, _sheet)
            for _signal in self._model.all_signals[_sheet]:
                _child = QTreeWidgetItem(_parent)
                _child.setText(0, _signal.get_name_column())
                _child.setData(0, 1, _signal)

    def display_selected_signal(self, item):    
        signal = item.data(0, 1)
        if isinstance(signal, MySignal):
            self.signal_name.setText(signal.get_name_sheet() + "/" + signal.get_name_column())
            self._model.signal_current = signal

    def set_current_signal(self):
        if self.signal_name.text() and self._model.add_signal_in_buffer():
            row_position = self.tablewidget_buffer_signals.rowCount()
            self.tablewidget_buffer_signals.insertRow(row_position)
            item = QTableWidgetItem(self.signal_name.text())
            self.tablewidget_buffer_signals.setItem(row_position, 0, item)

    def clear_buffer_signals_widget(self):
        rows = self.tablewidget_buffer_signals.rowCount()

        for row in range(rows - 1, -1, -1):
            self.tablewidget_buffer_signals.removeRow(row)

    def show_context_menu(self, pos):
        index = self.tablewidget_buffer_signals.indexAt(pos)

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

        context_menu.exec(self.tablewidget_buffer_signals.mapToGlobal(pos))

    def delete_signal(self, row):
        _name = self.tablewidget_buffer_signals.item(row, 0).text()
        _signal = self._model.buffer_signals[_name]
        self.tablewidget_buffer_signals.removeRow(row)
        self._model.delete_signal_from_buffer(_name)
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

        _name = self.tablewidget_buffer_signals.item(row, 0).text()
        _signal = self._model.buffer_signals[_name]
        _signal.set_data()
        _signal.set_data_start_end_work()
        self.signal_plot = _signal

        _data = _signal.get_data_curr()

        sc1 = MplCanvas(self, width=5, height=4, dpi=100)
        sc2 = MplCanvas(self, width=5, height=4, dpi=100)
        sc3 = MplCanvas(self, width=5, height=4, dpi=100)
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