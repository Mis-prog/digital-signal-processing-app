import pandas as pd
import numpy as np
from mysignal import MySignal
import matplotlib.pyplot as plt
from scipy.signal.windows import gaussian


def search_median(data):
    data = sorted(data)
    mid = len(data) // 2
    return (data[mid] + data[~mid]) / 2.0 if len(data) % 2 == 0 else data[mid]


def median_filter(signal: MySignal, width: int, frequency: int = 1):
    if width % 2 == 0:
        return
    else:
        _data = signal.get_data_curr(frequency)
        _name_column = signal.get_name_column()

        values = _data[_name_column].to_numpy()
        n = len(values)
        filtered_values = np.zeros(n)

        half_width = width // 2

        for i in range(n):
            start = max(0, i - half_width)
            end = min(n, i + half_width + 1)
            _curr_window = values[start:end]
            filtered_values[i] = search_median(_curr_window)

        _data.loc[:, [f"{_name_column}_filter"]] = filtered_values

        signal.set_data_curr(_data)


def moving_average_filter(signal: MySignal, radius: int, frequency: int = 1):
    _data = signal.get_data_curr(frequency)
    _name_column = signal.get_name_column()

    values = _data[_name_column].to_numpy()
    n = len(values)
    filtered_values = np.zeros(n)

    for i in range(len(_data)):
        if i < radius:
            filtered_values[i] = sum(values[0:i + radius]) / (radius + i)
        elif i >= len(_data) - radius:
            filtered_values[i] = sum(values[i - radius:n]) / (radius + n - i)
        else:
            filtered_values[i] = sum(values[i - radius:i + radius + 1]) / (2 * radius + 1)

    _data.loc[:, [f"{_name_column}_filter"]] = filtered_values

    signal.set_data_curr(_data)


# https://help.fsight.ru/ru/mergedProjects/lib/02_time_series_analysis/uimodelling_expsmooth.htm
def exponential_filter(signal: MySignal, alfa: float):
    _data = signal.get_data_curr()
    _name_column = signal.get_name_column()

    values = _data[_name_column].to_numpy()
    n = len(values)
    filtered_values = np.zeros(n)

    for i in range(n):
        if i == 0:
            filtered_values[i] = values[i]
        else:
            filtered_values[i] = alfa * values[i] + (1 - alfa) * filtered_values[i - 1]

    _data.loc[:, [f"{_name_column}_filter"]] = filtered_values

    signal.set_data_curr(_data)


def window_hamping_filter(signal: MySignal, radius: int):
    _data = signal.get_data_curr()
    _name_column = signal.get_name_column()

    values = _data[_name_column].to_numpy()
    n = len(values)
    filtered_values = np.zeros(n)

    for i in range(n):
        if i < radius:
            window = np.hamming(radius + i + 1)
            filtered_values[i] = np.dot(values[0:i + radius + 1], window) / window.sum()
        elif i >= n - radius:
            window = np.hamming(radius + n - i)
            filtered_values[i] = np.dot(values[i - radius:n], window) / window.sum()
        else:
            window = np.hamming(2 * radius + 1)
            filtered_values[i] = np.dot(values[i - radius:i + radius + 1], window) / window.sum()

    _data.loc[:, [f"{_name_column}_filter"]] = filtered_values

    signal.set_data_curr(_data)


def window_gauss_filter(signal: MySignal, radius: int, std: float):
    _data = signal.get_data_curr()
    _name_column = signal.get_name_column()

    values = _data[_name_column].to_numpy()
    n = len(values)
    filtered_values = np.zeros(n)

    for i in range(n):
        if i < radius:
            window = gaussian(i + radius + 1, std)
            filtered_values[i] = np.dot(values[0:i + radius + 1], window) / window.sum()
        elif i >= n - radius:
            window = gaussian(radius + n - i, std)
            filtered_values[i] = np.dot(values[i - radius:n], window) / window.sum()
        else:
            window = gaussian(2 * radius + 1, std)
            filtered_values[i] = np.dot(values[i - radius:i + radius + 1], window) / window.sum()

    _data.loc[:, [f"{_name_column}_filter"]] = filtered_values

    signal.set_data_curr(_data)


def kalman_filter(signal: MySignal):
    pass


all_filter = {
    0: moving_average_filter,
    1: median_filter,
    2: exponential_filter,
    3: window_hamping_filter,
    4: window_gauss_filter
}
