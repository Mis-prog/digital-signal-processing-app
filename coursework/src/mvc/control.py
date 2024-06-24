import sys
from PyQt6.QtWidgets import QMainWindow, QFileDialog




class Controller():
    def __init__(self, model, view):
        self._model = model
        self._view = view

        self._view.open_dialog.clicked.connect(self.open_file_dialog)
        self._view.list_signals.itemClicked.connect(self._view.display_selected_signal)
        self._view.set_signal.clicked.connect(self._view.set_current_signal)
        self._view.buffer_signals.customContextMenuRequested.connect(self._view.show_context_menu)


    def open_file_dialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self._view, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")

        if fileName:
            self._model.buffer_signals.clear()
            self._view.clear_buffer_signals_widget()
            self._model.path_file = fileName
            self._view.show_success_message()
            self._model.init()
            self._view.set_treewidget()

