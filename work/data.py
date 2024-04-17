import pandas as pd 

# Частота данных
def get_data_with_frequency(data,frequency):
    return data[::frequency]

# Выборка данных по границе
def get_data_by_border(data,start,end,name):
    init_value = data['MD'].iloc[0]
    h = data['MD'].iloc[1] - init_value

    section_start = int(abs(start - init_value) / h)
    section_end = int(abs(end - init_value) / h)

    return data[['MD',name]][section_start:section_end]

# Выборка данных от начало до конца в момент работы
def get_index_start_end_work(data,name):  
    data_index=[]
    md_values = data['MD'].values 

    start_node=None
    end_node=None
    for i,value  in enumerate(data[name]):
        if value!=-999.25:
            start_node=md_values[i]
            break
    for i, value in reversed(list(enumerate(data[name]))):
        if value != -999.25:
            end_node = md_values[i]
            break

    data_index.append((start_node,end_node))
    
    return data_index


# Выборка данных по границе в момент замера параметров
def get_index_work(data,name):  
    data_index=[]
    md_values = data['MD'].values 

    start_node=None
    for i, value in enumerate(data[name]):
        if value!=-999.25 and start_node is None:
            start_node=md_values[i]
            # start_node=i
        elif value==-999.25 and start_node is not None:
            data_index.append((start_node,md_values[i-1]))
            # data_index.append((start_node,i))
            start_node=None
    if start_node is not None:
            data_index.append((start_node, md_values[-1]))
            # data_index.append((start_node,i))
    return data_index

# Выборка данных по границе в момент отсуствия работы прибора
def get_index_not_work(data,name):
    data_index=[]
    md_values = data['MD'].values

    start_node=None
    for i, value in enumerate(data[name]):
        if value==-999.25 and start_node is None:
            start_node=md_values[i]
            # start_node=i
        elif value!=-999.25 and start_node is not None:
            data_index.append((start_node,md_values[i-1]))
            # data_index.append((start_node,i-1))
            start_node=None
    if start_node is not None:
            data_index.append((start_node, md_values[-1]))
            # data_index.append((start_node,i-1))
    return data_index

# Полная разметка данных
def get_index_data(data):
    data_index ={}
    
    data_index_start_end_work={}
    data_index_work={}
    data_index_not_work={}
    
    for name in data.columns[1:]:
        data_index_work[name] = get_index_work(data,name)
        data_index_not_work[name] = get_index_not_work(data,name)
        data_index_start_end_work[name] = get_index_start_end_work(data,name)

    data_index['work']=data_index_work
    data_index['start_end']=data_index_start_end_work
    data_index['not_work']=data_index_not_work
    return data_index
