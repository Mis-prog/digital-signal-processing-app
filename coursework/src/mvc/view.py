from window import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTreeWidgetItem, QTableWidgetItem, QMenu, QVBoxLayout
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from mysignal import MySignal
from plot import MplCanvas
from filter import all_filter
from searchanomaly import *

import matplotlib

matplotlib.use('QtAgg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class View(QMainWindow, Ui_MainWindow):
    def __init__(self, model, parent=None):
        self.signal_plot = None
        self._model = model
        super(View, self).__init__()
        self.setupUi(self)

        self.smoothing_param_window.hide()
        self.smoothing_param_value_widget.hide()

        self.tablewidget_buffer_signals.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tablewidget_intervals_anomaly.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.open_dialog.clicked.connect(self.open_file_dialog)
        self.treewidget_all_signals.itemClicked.connect(self.display_selected_signal)
        self.set_signal.clicked.connect(self.set_current_signal)
        self.tablewidget_buffer_signals.customContextMenuRequested.connect(self.show_context_menu)
        self.tablewidget_intervals_anomaly.customContextMenuRequested.connect(
            self.show_context_menu_for_tablewidget_anomaly)
        self.list_filter_smoothing_widget.currentIndexChanged.connect(self.set_filter_widget)
        self.run_smoothing_widget.clicked.connect(self.plot_filter)
        self.append_interval.clicked.connect(self.append_interval_anomaly_widget)
        self.run_analysis_signals.clicked.connect(self.set_analysis_signal)
        # self.cut_intervals_anomaly.clicked.connect(self.)

    def set_analysis_signal(self):
        if self.signal_plot and self.list_method_search_anomaly is not None:
            index = self.list_method_search_anomaly.currentIndex()
            analysis_anomaly(self.signal_plot, index)
            _all_interval = self.signal_plot.get_all_intervals()
            for interval in _all_interval:
                start, end = interval
                print(interval)
                row_position = self.tablewidget_intervals_anomaly.rowCount()
                self.tablewidget_intervals_anomaly.insertRow(row_position)
                self.tablewidget_intervals_anomaly.setItem(row_position, 0, QTableWidgetItem(str(start[0])))
                self.tablewidget_intervals_anomaly.setItem(row_position, 1, QTableWidgetItem(str(end[0])))
    def append_interval_anomaly_widget(self):
        row_position = self.tablewidget_intervals_anomaly.rowCount()
        self.tablewidget_intervals_anomaly.insertRow(row_position)

    def show_context_menu_for_tablewidget_anomaly(self, pos):
        index = self.tablewidget_intervals_anomaly.indexAt(pos)

        if not index.isValid():
            return

        context_menu = QMenu(self)
        # work_action = QAction('Отобразить аномалию', self)
        delete_action = QAction('Удалить', self)

        # work_action.triggered.connect(lambda: self.work_with_signal(index.row()))
        delete_action.triggered.connect(lambda: self.delete_interval(index.row()))
        # context_menu.addAction(work_action)
        context_menu.addAction(delete_action)

        context_menu.exec(self.tablewidget_intervals_anomaly.mapToGlobal(pos))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.run_smoothing_widget.click()

    def plot_filter(self):
        if self.signal_plot:
            layout = self.smoothing_widget.layout()
            if layout is not None:
                self.clearLayout(layout)
            else:
                layout = QVBoxLayout(self.smoothing_widget)
                self.smoothing_widget.setLayout(layout)

            self.set_filter()
            _signal = self.signal_plot
            plot = MplCanvas(self, width=5, height=4, dpi=100)
            plot.plot_filter(_signal)
            toolbar = NavigationToolbar(plot, self)

            layout.addWidget(toolbar)
            layout.addWidget(plot)

    def open_file_dialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")

        if fileName:
            self._model.buffer_signals.clear()
            self.clear_buffer_signals_widget()
            self.clear_interval_anomaly_widget()
            self._model.path_file = fileName
            self.show_success_message()
            self._model.init()
            self.set_treewidget()

    def set_filter_widget(self, index):
        if index != 2 and index != 4:
            self.smoothing_window_widget.show()
            self.smoothing_window_value_widget.show()
            self.smoothing_param_window.hide()
            self.smoothing_param_value_widget.hide()
        elif index == 2:
            self.smoothing_window_widget.hide()
            self.smoothing_window_value_widget.hide()
            self.smoothing_param_window.show()
            self.smoothing_param_value_widget.show()
        elif index == 4:
            self.smoothing_window_widget.show()
            self.smoothing_window_value_widget.show()
            self.smoothing_param_window.show()
            self.smoothing_param_value_widget.show()

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
            self.signal_name.setText(f"{signal.get_name_sheet()}/{signal.get_name_column()}")
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

    def clear_interval_anomaly_widget(self):
        rows = self.tablewidget_intervals_anomaly.rowCount()

        for row in range(rows - 1, -1, -1):
            self.tablewidget_intervals_anomaly.removeRow(row)

    def show_context_menu(self, pos):
        index = self.tablewidget_buffer_signals.indexAt(pos)

        if not index.isValid():
            return

        context_menu = QMenu(self)
        work_action = QAction('Отобразить сигнал', self)
        delete_action = QAction('Удалить', self)

        work_action.triggered.connect(lambda: self.work_with_signal(index.row()))
        delete_action.triggered.connect(lambda: self.delete_signal(index.row()))
        context_menu.addAction(work_action)
        context_menu.addAction(delete_action)

        context_menu.exec(self.tablewidget_buffer_signals.mapToGlobal(pos))

    def work_with_signal(self, row):
        try:
            self.clear_interval_anomaly_widget()
            _name = self.tablewidget_buffer_signals.item(row, 0).text()
            _signal = self._model.buffer_signals[_name]
            _signal.set_data()
            _signal.set_data_start_end_work()
            self.signal_plot = _signal

            widgets = [self.smoothing_widget, self.eliminating_gaps_widget, self.search_anomaly_widget]

            for widget in widgets:
                layout = widget.layout()
                if layout is not None:
                    self.clearLayout(layout)
                else:
                    layout = QVBoxLayout(widget)
                    widget.setLayout(layout)

                plot = MplCanvas(self, width=5, height=4, dpi=100)
                plot.plot_original(_signal)
                toolbar = NavigationToolbar(plot, self)

                layout.addWidget(toolbar)
                layout.addWidget(plot)
        except Exception as e:
            print(f"Error in work_with_signal: {e}")

    def delete_signal(self, row):
        try:
            _name = self.tablewidget_buffer_signals.item(row, 0).text()
            _signal = self._model.buffer_signals[_name]

            self.tablewidget_buffer_signals.removeRow(row)
            self._model.delete_signal_from_buffer(_name)

            if self.signal_plot == _signal:
                for widget in [self.smoothing_widget, self.eliminating_gaps_widget, self.search_anomaly_widget]:
                    layout = widget.layout()
                    if layout is not None:
                        self.clearLayout(layout)
                self.signal_plot = None
        except Exception as e:
            print(f"Error in delete_signal: {e}")

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

    def set_filter(self):
        value = None
        param = None
        index = self.list_filter_smoothing_widget.currentIndex()

        if index != 2 and index != 4:
            if self.smoothing_window_value_widget is not None:
                value = int(self.smoothing_window_value_widget.value())

            if value != 0:
                all_filter[index](self.signal_plot, value)
            else:
                all_filter[index](self.signal_plot, 101)
                self.smoothing_window_value_widget.setValue(101)

        elif index == 2:
            if self.smoothing_param_value_widget is not None:
                param = float(self.smoothing_param_value_widget.value())

            if param != 0 and param <= 1:
                all_filter[2](self.signal_plot, param)
            else:
                all_filter[2](self.signal_plot, 0.5)
                self.smoothing_param_value_widget.setValue(0.5)
        elif index == 4:

            if self.smoothing_window_value_widget is not None and self.smoothing_param_value_widget.value is not None:
                value = int(self.smoothing_window_value_widget.value())
                param = float(self.smoothing_param_value_widget.value())

            if value != 0 and param != 0:
                all_filter[index](self.signal_plot, value, param)
            else:
                all_filter[index](self.signal_plot, 101, 5.0)
                self.smoothing_window_value_widget.setValue(101)
                self.smoothing_param_value_widget.setValue(5.0)

    def delete_interval(self, row):
        self.tablewidget_intervals_anomaly.removeRow(row)
