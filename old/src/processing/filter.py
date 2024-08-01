import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor


# Метод скользящего среднего
def moving_average_py(data, column_name, window_size):
    filtered_data = data[['MD', column_name]].copy()
    filtered_data[column_name] = data[column_name].rolling(window=window_size, min_periods=1).mean()
    return filtered_data


# Метод скользящего среднего ручной
def moving_average_manual(data, column_name, window_size):
    filtered_data = data[['MD', column_name]].copy()

    start = data[column_name].index[0]
    end = data[column_name].index[-1]

    for i in range(start, end):
        if (i - abs(i - window_size)) < 0:
            filtered_data[column_name][i] = sum(filtered_data[column_name][i:i + window_size]) // window_size
        else:
            filtered_data[column_name][i] = sum(filtered_data[column_name][i - window_size:i]) // window_size
    return filtered_data


# Метод скользящего среднего с обработкой краевых условий
def moving_average_manual_mean(data, column_name, radius):
    input_data = data[['MD', column_name]].copy()
    output_data = data[['MD', column_name]].copy()

    start = data[column_name].index[0]
    end = data[column_name].index[-1]

    for i in range():
        if i >= radius and i <= (end - radius):
            output_data[column_name][i] = sum(input_data[column_name][i - radius:i + radius + 1]) // (2 * radius + 1)
        elif i < radius:
            output_data[column_name][i] = sum(input_data[column_name][0:i + radius + 1]) // (i + radius + 1)
        else:
            output_data[column_name][i] = sum(input_data[column_name][i - radius:end]) // (end - i + radius + 1)

    return output_data


def moving_average_weight_manual(data, column_name, window_size):
    return None


# Метод Калмана
def kalman_filter(data, column_name, Q, R):
    signal = data[column_name].values

    x_hat = signal[0]
    P = 1

    filtered_signal = []

    for z in signal:
        x_hat_minus = x_hat
        P_minus = P + Q

        K = P_minus / (P_minus + R)
        x_hat = x_hat_minus + K * (z - x_hat_minus)
        P = (1 - K) * P_minus

        filtered_signal.append(x_hat)

    filtered_data = data.copy()
    filtered_data[column_name] = filtered_signal

    return filtered_data
