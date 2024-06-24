import pandas as pd
import numpy as np
from mysignal import MySignal
import matplotlib.pyplot as plt
import scipy.ndimage


def search_median(data):
    data = sorted(data)
    mid = len(data) // 2
    return (data[mid] + data[~mid]) / 2.0 if len(data) % 2 == 0 else data[mid]


def median_filter(signal: MySignal, width: int, frequency: int = 1):
    if width % 2 == 0:
        raise ValueError("Размер окна width должен быть нечётным числом.")

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
            filtered_values[i] = sum(values[0:i + radius]) // (radius + i)
        elif i >= len(_data) - radius:
            filtered_values[i] = sum(values[i - radius:n]) // (radius + n - i)
        else:
            filtered_values[i] = sum(values[i - radius:i + radius + 1]) // (2 * radius + 1)

    _data.loc[:, [f"{_name_column}_filter"]] = filtered_values

    signal.set_data_curr(_data)


# https://ru.wikipedia.org/wiki/LULU-%D1%81%D0%B3%D0%BB%D0%B0%D0%B6%D0%B8%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5
def L(signal: MySignal, window: int):
    _data = signal.get_data_curr()
    _name_column = signal.get_name_column()

    values = _data[_name_column].to_numpy()
    n = len(values)
    filtered_values = np.zeros(n)

    for i in range(n):
        if i < window:
            min_vals = [np.min(values[:i + 1])]
            for j in range(1, window + 1):
                start = max(0, i - j)
                end = i + 1
                min_vals.append(np.min(values[start:end]))
            filtered_values[i] = np.max(min_vals)
        elif i >= n - window:
            min_vals = [np.min(values[i:])]
            for j in range(1, window + 1):
                start = i - j
                end = min(n, i + 1)
                min_vals.append(np.min(values[start:end]))
            filtered_values[i] = np.max(min_vals)
        else:
            min_vals = []
            for j in range(window + 1):
                start = i - j
                end = i + 1
                min_vals.append(np.min(values[start:end]))
            filtered_values[i] = np.max(min_vals)

    _data.loc[:, [f"{_name_column}_filter"]] = filtered_values

    signal.set_data_curr(_data)


def U(signal: MySignal, window: int):
    _data = signal.get_data_curr()
    _name_column = signal.get_name_column()

    values = _data[f"{_name_column}_filter"].to_numpy()
    n = len(values)
    filtered_values = np.zeros(n)

    for i in range(n):
        if i < window:
            min_vals = [np.max(values[:i + 1])]
            for j in range(1, window + 1):
                start = max(0, i - j)
                end = i + 1
                min_vals.append(np.max(values[start:end]))
            filtered_values[i] = np.min(min_vals)
        elif i >= n - window:
            min_vals = [np.max(values[i:])]
            for j in range(1, window + 1):
                start = i - j
                end = min(n, i + 1)
                min_vals.append(np.max(values[start:end]))
            filtered_values[i] = np.min(min_vals)
        else:
            min_vals = []
            for j in range(window + 1):
                start = i - j
                end = i + 1
                min_vals.append(np.max(values[start:end]))
            filtered_values[i] = np.min(min_vals)

    _data.loc[:, [f"{_name_column}_filter"]] = filtered_values

    signal.set_data_curr(_data)


def Lulu_filter(signal: MySignal, window: int):
    _data = signal.get_data_curr()
    _name_column = signal.get_name_column()

    values = _data[_name_column].to_numpy()
    n = len(values)
    filtered_values = np.zeros(n)

    pass

#https://help.fsight.ru/ru/mergedProjects/lib/02_time_series_analysis/uimodelling_expsmooth.htm
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

def weight_moving_filter(signal: MySignal):
    pass


def kalman_filter(signal: MySignal):
    pass


signal = MySignal("Набор 1", "Data 6", "../../../data/data_small.xlsx")
signal.set_data()
signal.set_data_start_end_work()
# moving_average_filter(signal, 100,10)
# median_filter(signal, 11)
# Требуют доработки
# L(signal, 100)
# U(signal, 100)

exponential_filter(signal,0.1)

data = signal.get_data_curr()
plt.plot(data['MD'], data['Data 6'])
plt.plot(data['MD'], data['Data 6_filter'], linestyle='--')
plt.show()
