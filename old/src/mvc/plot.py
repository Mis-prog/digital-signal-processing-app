import sys
import numpy as np
import pandas as pd

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from mysignal import MySignal



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas,self).__init__(fig)

    def plot_original(self, signal: MySignal):
        _data = signal.get_data_curr()
        _name_column = signal.get_name_column()
        _name_sheet = signal.get_name_sheet()
        self.axes.plot(_data['MD'], _data[_name_column])
        self.axes.set_title(f"{_name_sheet}/{_name_column}")
        self.axes.set_xlabel('MD')
        self.axes.set_ylabel('Value')
        self.draw()

    def plot_filter(self, signal: MySignal):
        _data = signal.get_data_curr()
        _name_column = signal.get_name_column()
        _name_sheet = signal.get_name_sheet()
        self.axes.plot(_data['MD'], _data[_name_column])
        self.axes.plot(_data['MD'], _data[f"{_name_column}_filter"])
        self.axes.set_title(f"{_name_sheet}/{_name_column}")
        self.axes.set_xlabel('MD')
        self.axes.set_ylabel('Value')
        self.draw()

    def clear(self):
        self.axes.clear()
        self.draw()

# plot1 = MplCanvas()
# _signal=MySignal("Набор 1","Data 1","../../../data/data_small.xlsx")
# _signal.set_data()
#
# plot1.plot_original(_signal)
#
# # toolbar1=NavigationToolbar(plot1,self)



