import numpy as np
import pandas as pd 

#Метод скользящего среднего
def moving_average_py(data, column_name, window_size):
    filtered_data = data[['MD', column_name]].copy()
    filtered_data[column_name] = data[column_name].rolling(window=window_size, min_periods=1).mean()
    return filtered_data

#Метод скользящего среднего ручной
def moving_average_manual(data, column_name, window_size):
    filtered_data = data[['MD', column_name]].copy()
    for i in range(len(filtered_data[column_name])):
        if (i-abs(i-window_size))<0:
            filtered_data[column_name][i] = sum(filtered_data[column_name][i:i+window_size])//window_size
        else:
            filtered_data[column_name][i] = sum(filtered_data[column_name][i-window_size:i])//window_size
    return filtered_data

# def weighted_moving_average(data, column_name, window_size, weights):
#     filtered_data = data[['MD', column_name]].copy()  
#     for i in range(len(filtered_data[column_name])):  
#         if (i-window_size)<0:  
#             weighted_sum = sum(weights[:i+1] * filtered_data[column_name][:i+1])
#             filtered_data[column_name][i] = weighted_sum / sum(weights[:i+1])
#         else:
#             weighted_sum = sum(weights * filtered_data[column_name][i-window_size+1:i+1])
#             filtered_data[column_name][i] = weighted_sum / sum(weights)
#     return filtered_data


def 