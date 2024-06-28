from mysignal import MySignal
from filter import moving_average_filter, window_hamping_filter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def _value_into_index(data, value_start, value_end):
    init_value = data['MD'].iloc[0]
    h = data['MD'].iloc[1] - init_value

    index_start = int(abs(value_start - init_value) / h)
    index_end = int(abs(value_end - init_value) / h)

    marking_border = [index_start, index_end]
    return marking_border


def analysis_anomaly(signal: MySignal, index_method: int):
    _data = signal.get_data_curr()
    _intervals = []
    _name = signal.get_name_column()

    if index_method == 0:
        moving_average_filter(signal, 100)
    elif index_method == 1:
        window_hamping_filter(signal, 100)

    filtered_data = signal.get_data_curr()[_name + "_filter"]
    original_data = signal.get_data_curr()[_name]
    diff_data = abs(original_data - filtered_data)

    threshold = 1000
    start_index = None
    for i, value in enumerate(diff_data):
        if value > threshold and start_index is None:
            start_index = i
        elif value < threshold and start_index is not None:
            end_index = i - 1
            _intervals.append(([_data['MD'][start_index], start_index], [_data['MD'][end_index], end_index]))
            start_index = None
    if start_index is not None:
        end_index = len(diff_data) - 1
        _intervals.append(([_data['MD'][start_index], start_index], [_data['MD'][end_index], end_index]))
    signal.set_intervals(_intervals)


def cut_anomaly(signal: MySignal):
    _data = signal.get_data_curr()
    _intervals = signal.get_index_interval()
    if _intervals:
        for (index_start, index_end) in _intervals:
            _data.loc[index_start:index_end, signal.get_name_column()] = None
        signal.set_data_curr(_data)


def append_anomaly(signal: MySignal, start: float, end: float):
    _intervals = signal.get_all_intervals()
    _data = signal.get_data_curr()
    _marking_border = _value_into_index(_data, start, end)
    _intervals.append(([start, _marking_border[0]], [end, _marking_border[1]]))
    signal.set_intervals(_intervals)


def delete_anomaly(signal: MySignal, index: int):
    _intervals = signal.get_all_intervals()
    del _intervals[index]
    signal.set_intervals(_intervals)


# signal = MySignal("Набор 1", "Data 12", "../../../data/data_small.xlsx")
# signal.set_data()
#
# signal.set_data_start_end_work()
# analysis_anomaly(signal, 1)
# append_anomaly(signal,1200,1300)
# cut_anomaly(signal)
# plt.plot(signal.get_data_curr()['MD'], signal.get_data_curr()[signal.get_name_column()])
# plt.show()
