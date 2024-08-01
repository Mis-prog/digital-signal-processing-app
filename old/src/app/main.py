from PyQt6 import QtWidgets
from control import MainWindow
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())


# import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMenu, QMessageBox
# from PyQt6.QtGui import QAction
# from PyQt6.QtCore import Qt
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle('Signal Buffer with Context Menu')
#
#         layout = QVBoxLayout()
#
#         # Создаем QTableWidget с 1 столбцом
#         self.table_widget = QTableWidget()
#         self.table_widget.setColumnCount(1)
#         self.table_widget.setHorizontalHeaderLabels(['Signals'])
#         self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
#         self.table_widget.customContextMenuRequested.connect(self.show_context_menu)
#
#         # Добавляем несколько начальных сигналов для примера
#         for i in range(5):
#             self.add_signal(f'Signal {i + 1}')
#
#         layout.addWidget(self.table_widget)
#         self.setLayout(layout)
#
#     def add_signal(self, signal_name):
#         row_position = self.table_widget.rowCount()
#         self.table_widget.insertRow(row_position)
#         item = QTableWidgetItem(signal_name)
#         self.table_widget.setItem(row_position, 0, item)
#
#     def show_context_menu(self, pos):
#         # Получаем индекс строки, где была нажата правая кнопка мыши
#         index = self.table_widget.indexAt(pos)
#         if not index.isValid():
#             return
#
#         # Создаем контекстное меню
#         context_menu = QMenu(self)
#         work_action = QAction('Work with Signal', self)
#         delete_action = QAction('Delete', self)
#
#         # Подключаем действия к слотам
#         work_action.triggered.connect(lambda: self.work_with_signal(index.row()))
#         delete_action.triggered.connect(lambda: self.delete_signal(index.row()))
#
#         context_menu.addAction(work_action)
#         context_menu.addAction(delete_action)
#
#         # Отображаем контекстное меню
#         context_menu.exec(self.table_widget.mapToGlobal(pos))
#
#     def work_with_signal(self, row):
#         signal_name = self.table_widget.item(row, 0).text()
#         QMessageBox.information(self, 'Work with Signal', f'Working with {signal_name}')
#
#     def delete_signal(self, row):
#         self.table_widget.removeRow(row)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
